// Headless check of the viewer's maths core (core.js) with the shipped data.
// usage: node node_check.mjs <path to three@0.160.0 package dir> <out.json>
// Writes the family lines the viewer would draw at many s values (for verify_viewer.py to check in Python),
// plus marching-cubes and curve-segment statistics.
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { pathToFileURL, fileURLToPath } from 'url';
const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const Core = require(path.join(HERE, '..', 'core.js'));
globalThis.window = globalThis;
eval(fs.readFileSync(path.join(HERE, '..', 'data', 'y56-data.js'), 'utf8'));
const D = globalThis.Y56DATA;
const threeDir = process.argv[2];
const { edgeTable, triTable } = await import(pathToFileURL(path.join(threeDir, 'examples', 'jsm', 'objects', 'MarchingCubes.js')).href);
const out = { family: [], mc: {}, segments: {} };

// family lines on a grid of s (plus the special values)
const S = [];
for (let i = 0; i <= 300; i++) S.push(i / 100);
S.push(2, D.s_star, 1.9999, 2.0001, D.s_star - 1e-3, D.s_star + 1e-3);
for (const s of S) {
  const fl = Core.familyLines(s);
  const rec = { s, count: fl.count, anchors: fl.lines.filter(l => l.kind === 'anchor').length, wall: fl.lines.filter(l => l.kind === 'wall').length, lines: [] };
  for (const l of fl.lines) rec.lines.push(Array.from(Core.linePoints(l.B, 24)));
  out.family.push(rec);
}

// marching cubes on Y56 (family at s*) and on each face; check |f| at vertices relative to the field scale
const monos = D.monos;
function mcStats(coef, c, E, N) {
  const f = Core.compileQuartic(coef, monos);
  const t0 = Date.now();
  const grid = Core.sampleField(f, c, E, N, 1.03);
  const t1 = Date.now();
  const m = Core.marchingCubes(grid, f, c, E, edgeTable, triTable, 1.0);
  const t2 = Date.now();
  // residual: evaluate f on the normalised R^4 point of each vertex
  let worst = 0, inside = 0; const X = [0, 0, 0, 0];
  let scale = 0; for (let i = 0; i < grid.field.length; i += 97) scale = Math.max(scale, Math.abs(grid.field[i]));
  for (let v = 0; v < m.nv; v++) {
    const y = [m.positions[3 * v], m.positions[3 * v + 1], m.positions[3 * v + 2]];
    if (Math.hypot(...y) > 1) continue;
    inside++;
    Core.ballToR4(y[0], y[1], y[2], c, E, X);
    worst = Math.max(worst, Math.abs(f(X[0], X[1], X[2], X[3])) / scale);
  }
  return { N, nv: m.nv, nt: m.nt, inside, worst_rel_f_at_vertices: worst, ms_field: t1 - t0, ms_mc: t2 - t1 };
}
const K = Core.familyCoef(D.family.K0, D.family.K1, D.s_star);
out.mc.y56_N96 = mcStats(K, D.centre, D.frame, 96);
out.mc.wall_N64 = mcStats(Core.familyCoef(D.family.K0, D.family.K1, 2), D.centre, D.frame, 64);
out.mc.fermat_N64 = mcStats(Core.familyCoef(D.family.K0, D.family.K1, 0), D.centre, D.frame, 64);
for (const fc of D.faces) out.mc['face_' + fc.rep] = mcStats(fc.coef, fc.reuse_main ? D.centre : fc.centre, fc.reuse_main ? D.frame : fc.frame, 80);
// Y56 coefficients through the family formula must equal face g00's fitted coefficients
let dmax = 0; for (let i = 0; i < 35; i++) dmax = Math.max(dmax, Math.abs(K[i] - D.faces[0].coef[i]));
out.mc.family_at_sstar_vs_face_g00_coef_diff = dmax;

// curve segments: every 3-D point inside the closed unit ball, endpoints on the glass, no big jumps inside a segment
function segStats(pts, ncurve, n) {
  let maxR = 0, maxStep = 0, nseg = 0, endOff = 0;
  for (let i = 0; i < ncurve; i++) {
    const segs = Core.curveSegments(pts.subarray(4 * n * i, 4 * n * (i + 1)), n, D.centre, D.frame);
    for (const s of segs) {
      nseg++;
      for (let j = 0; j < s.pts.length; j++) {
        maxR = Math.max(maxR, Math.hypot(...s.pts[j]));
        if (j) maxStep = Math.max(maxStep, Math.hypot(s.pts[j][0] - s.pts[j - 1][0], s.pts[j][1] - s.pts[j - 1][1], s.pts[j][2] - s.pts[j - 1][2]));
      }
      if (!s.closed) endOff = Math.max(endOff, Math.abs(Math.hypot(...s.pts[0]) - 1), Math.abs(Math.hypot(...s.pts[s.pts.length - 1]) - 1));
    }
  }
  return { nseg, maxR, maxStep, maxEndpointOffGlass: endOff };
}
out.segments.lines = segStats(Core.decodeF32(D.line_pts), 56, D.nline);
out.segments.conics = segStats(Core.decodeF32(D.conic_pts), 188, D.nconic);
fs.writeFileSync(process.argv[3], JSON.stringify(out));
console.log(JSON.stringify({ mc: out.mc, segments: out.segments }, null, 1));
