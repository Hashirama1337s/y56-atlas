/* Y56 atlas viewer: maths core (no graphics). Classic script: defines Y56Core on the global object.
   Ball model: a point x of real projective space is a unit vector of R^4 up to sign; it is flipped into the
   hemisphere x.c >= 0 around the centre c and sent to Y = E x / (1 + c.x), a point of the unit ball.
   Opposite points of the ball's boundary are the same point of projective space. */
(function (root) {
  'use strict';

  function decodeF32(b64) {
    if (!b64) return new Float32Array(0);
    let bin;
    if (typeof atob === 'function') bin = atob(b64);
    else bin = Buffer.from(b64, 'base64').toString('binary');
    const buf = new ArrayBuffer(bin.length), u8 = new Uint8Array(buf);
    for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    return new Float32Array(buf);
  }

  /* quartic in 4 variables from 35 coefficients (monomial exponents given), compiled to a fast function f(x0,x1,x2,x3) */
  function compileQuartic(coef, monos) {
    const terms = [];
    for (let i = 0; i < coef.length; i++) {
      const c = coef[i];
      if (!c || Math.abs(c) < 1e-13) continue;
      const f = [];
      for (let v = 0; v < 4; v++) for (let k = 0; k < monos[i][v]; k++) f.push('x' + v);
      terms.push('(' + c.toPrecision(17) + ')*' + f.join('*'));
    }
    if (!terms.length) terms.push('0');
    return new Function('x0', 'x1', 'x2', 'x3', 'return ' + terms.join('+') + ';');
  }

  function familyCoef(K0, K1, s) {
    const out = new Array(K0.length);
    for (let i = 0; i < K0.length; i++) out[i] = K0[i] + s * K1[i];
    return out;
  }

  /* unnormalised inverse ball map: y in R^3 -> X in R^4 (a positive multiple of the unit vector) */
  function ballToR4(y0, y1, y2, c, E, out) {
    const r2 = y0 * y0 + y1 * y1 + y2 * y2, a = 1 - r2;
    for (let k = 0; k < 4; k++) out[k] = a * c[k] + 2 * (y0 * E[0][k] + y1 * E[1][k] + y2 * E[2][k]);
    return out;
  }

  function project(x0, x1, x2, x3, c, E, out, o) {
    let d = x0 * c[0] + x1 * c[1] + x2 * c[2] + x3 * c[3];
    let sg = 1;
    if (d < 0) { sg = -1; d = -d; }
    const den = 1 + d;
    for (let r = 0; r < 3; r++) out[o + r] = sg * (x0 * E[r][0] + x1 * E[r][1] + x2 * E[r][2] + x3 * E[r][3]) / den;
    return sg;
  }

  /* sample the field f(ballToR4(y)) on an N^3 grid over [-B, B]^3 */
  function sampleField(f, c, E, N, B) {
    const field = new Float32Array(N * N * N), X = [0, 0, 0, 0], h = 2 * B / (N - 1);
    let q = 0;
    for (let k = 0; k < N; k++) {
      const z = -B + k * h;
      for (let j = 0; j < N; j++) {
        const y = -B + j * h;
        for (let i = 0; i < N; i++) {
          const x = -B + i * h;
          ballToR4(x, y, z, c, E, X);
          field[q++] = f(X[0], X[1], X[2], X[3]);
        }
      }
    }
    return { field, N, B, h };
  }

  /* marching cubes (Bourke corner/edge order; tables from three.js MarchingCubes). Returns indexed mesh with
     normals from the gradient of the true function (central differences on the analytic field), pointing to f > 0. */
  const EDGE = [ // [dx,dy,dz, axis] of the lower corner of each cube edge
    [0, 0, 0, 0], [1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 1, 1],
    [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 2], [1, 0, 0, 2], [1, 1, 0, 2], [0, 1, 0, 2]];
  const CORNER = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]];

  function marchingCubes(grid, f, c, E, edgeTable, triTable, keepR) {
    const { field, N, B, h } = grid;
    const NN = N * N;
    const cache = new Map();
    let pos = [], idx = [];
    const vid = new Int32Array(12);
    const X = [0, 0, 0, 0];
    const keepR2 = keepR ? keepR * keepR : Infinity;
    function vertexOn(i, j, k, e) {
      const ed = EDGE[e];
      const a0 = i + ed[0], a1 = j + ed[1], a2 = k + ed[2], ax = ed[3];
      const key = ((a0 + N * (a1 + N * a2)) * 3 + ax);
      let v = cache.get(key);
      if (v !== undefined) return v;
      const qa = a0 + N * a1 + NN * a2;
      const qb = qa + (ax === 0 ? 1 : ax === 1 ? N : NN);
      const fa = field[qa], fb = field[qb];
      let t = fa / (fa - fb);
      if (!isFinite(t)) t = 0.5;
      const p = [-B + a0 * h, -B + a1 * h, -B + a2 * h];
      p[ax] += t * h;
      v = pos.length / 3;
      pos.push(p[0], p[1], p[2]);
      cache.set(key, v);
      return v;
    }
    for (let k = 0; k < N - 1; k++) for (let j = 0; j < N - 1; j++) {
      for (let i = 0; i < N - 1; i++) {
        const q = i + N * j + NN * k;
        let ci = 0;
        if (field[q] < 0) ci |= 1;
        if (field[q + 1] < 0) ci |= 2;
        if (field[q + 1 + N] < 0) ci |= 4;
        if (field[q + N] < 0) ci |= 8;
        if (field[q + NN] < 0) ci |= 16;
        if (field[q + 1 + NN] < 0) ci |= 32;
        if (field[q + 1 + N + NN] < 0) ci |= 64;
        if (field[q + N + NN] < 0) ci |= 128;
        const bits = edgeTable[ci];
        if (!bits) continue;
        if (keepR) { // skip cells wholly outside the kept radius
          const cx = -B + (i + 0.5) * h, cy = -B + (j + 0.5) * h, cz = -B + (k + 0.5) * h;
          const rr = Math.sqrt(cx * cx + cy * cy + cz * cz) - 0.9 * h;
          if (rr > 0 && rr * rr > keepR2) continue;
        }
        for (let e = 0; e < 12; e++) if (bits & (1 << e)) vid[e] = vertexOn(i, j, k, e);
        const o = ci * 16;
        for (let t = 0; triTable[o + t] !== -1; t += 3) idx.push(vid[triTable[o + t]], vid[triTable[o + t + 1]], vid[triTable[o + t + 2]]);
      }
    }
    const P = new Float32Array(pos), nv = P.length / 3, Nm = new Float32Array(P.length);
    const d = 1e-4;
    for (let v = 0; v < nv; v++) {
      const x = P[3 * v], y = P[3 * v + 1], z = P[3 * v + 2];
      let g = [0, 0, 0];
      for (let a = 0; a < 3; a++) {
        const p1 = [x, y, z], p2 = [x, y, z]; p1[a] += d; p2[a] -= d;
        ballToR4(p1[0], p1[1], p1[2], c, E, X); const f1 = f(X[0], X[1], X[2], X[3]);
        ballToR4(p2[0], p2[1], p2[2], c, E, X); const f2 = f(X[0], X[1], X[2], X[3]);
        g[a] = f1 - f2;
      }
      let L = Math.hypot(g[0], g[1], g[2]) || 1;
      Nm[3 * v] = g[0] / L; Nm[3 * v + 1] = g[1] / L; Nm[3 * v + 2] = g[2] / L;
    }
    return { positions: P, normals: Nm, index: nv > 65535 ? new Uint32Array(idx) : new Uint16Array(idx), nv, nt: idx.length / 3 };
  }

  /* a closed projective curve (n points on S^3, x[i*4..]) -> segments of 3-D points inside the ball.
     Crossing the boundary sphere is located exactly (in R^4) and both ends are put on the glass. */
  function curveSegments(pts, n, c, E) {
    const flip = new Int8Array(n), P = new Float32Array(3 * n);
    for (let i = 0; i < n; i++) flip[i] = project(pts[4 * i], pts[4 * i + 1], pts[4 * i + 2], pts[4 * i + 3], c, E, P, 3 * i);
    // closed projective curve: point n wraps to point 0 up to sign. Find hemisphere switches of the signed lift.
    const dot = (i) => pts[4 * i] * c[0] + pts[4 * i + 1] * c[1] + pts[4 * i + 2] * c[2] + pts[4 * i + 3] * c[3];
    // lift is a closed curve on S^3 or closes up to sign (lines: half great circle). Determine closing sign.
    const closeSign = (pts[0] * pts[4 * (n - 1)] + pts[1] * pts[4 * (n - 1) + 1] + pts[2] * pts[4 * (n - 1) + 2] + pts[3] * pts[4 * (n - 1) + 3]) >= 0 ? 1 : -1;
    const cuts = []; // index i: crossing between i and i+1 (i+1 mod n, with closeSign)
    for (let i = 0; i < n; i++) {
      const a = dot(i), b = (i + 1 < n) ? dot(i + 1) : closeSign * dot(0);
      if ((a >= 0) !== (b >= 0)) cuts.push(i);
    }
    function boundaryPoint(i) { // crossing between i and i+1: point with x.c = 0, as 3-D unit vector, sign of side i
      const j = (i + 1) % n, sj = (i + 1 < n) ? 1 : closeSign;
      const a = dot(i), b = sj * dot(j);
      const t = a / (a - b);
      const x = [0, 0, 0, 0];
      for (let k = 0; k < 4; k++) x[k] = (1 - t) * pts[4 * i + k] + t * sj * pts[4 * j + k];
      const L = Math.hypot(x[0], x[1], x[2], x[3]);
      const sg = a >= 0 ? 1 : -1; // side of point i
      const out = [0, 0, 0];
      for (let r = 0; r < 3; r++) out[r] = sg * (x[0] * E[r][0] + x[1] * E[r][1] + x[2] * E[r][2] + x[3] * E[r][3]) / L;
      const R = Math.hypot(out[0], out[1], out[2]) || 1;
      return [out[0] / R, out[1] / R, out[2] / R];
    }
    const pt = (i) => [P[3 * i], P[3 * i + 1], P[3 * i + 2]];
    if (!cuts.length) {
      const seg = [];
      for (let i = 0; i < n; i++) seg.push(pt(i));
      return [{ pts: seg, closed: true }];
    }
    const segs = [];
    for (let m = 0; m < cuts.length; m++) {
      const i0 = cuts[m], i1 = cuts[(m + 1) % cuts.length];
      const start = boundaryPoint(i0); // computed with sign of i0's side; segment lies on the side of i0+1
      const seg = [[-start[0], -start[1], -start[2]]];
      let i = (i0 + 1) % n;
      let guard = 0;
      while (true) {
        seg.push(pt(i));
        if (i === i1) break;
        i = (i + 1) % n;
        if (++guard > n + 2) break;
      }
      seg.push(boundaryPoint(i1));
      segs.push({ pts: seg, closed: false });
    }
    return segs;
  }

  function orthRows(B) { // 2x4 -> orthonormal rows
    const a = B[0].slice(), b = B[1].slice();
    const na = Math.hypot(...a); for (let k = 0; k < 4; k++) a[k] /= na;
    const d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];
    for (let k = 0; k < 4; k++) b[k] -= d * a[k];
    const nb = Math.hypot(...b); for (let k = 0; k < 4; k++) b[k] /= nb;
    return [a, b];
  }

  function linePoints(B, n) { // half great circle: one copy of the projective line
    const Q = orthRows(B), out = new Float32Array(4 * n);
    for (let i = 0; i < n; i++) {
      const t = Math.PI * i / n, ct = Math.cos(t), st = Math.sin(t);
      for (let k = 0; k < 4; k++) out[4 * i + k] = ct * Q[0][k] + st * Q[1][k];
    }
    return out;
  }

  /* real lines of G_s = Im(w^4) + Im(p^2)(s|w|^2 - |p|^2), w = y0 + i y3, p = y1 + i y2.
     8 anchor lines (in y1 = 0 or y2 = 0) for every s; the 32 graph lines of components C1..C4 are real exactly when s >= 2:
     with delta^4 - s^2 delta^2 + 4 = 0 and v = s + delta, C3/C4 use C^2 = v (resp. D^2 = v), C1/C2 use D^2 = v/2.
     Returns {lines:[{B, kind, branch}], count} with coincident lines (the wall) merged. */
  function familyLines(s) {
    const lines = [];
    const e = (k) => { const v = [0, 0, 0, 0]; v[k] = 1; return v; };
    const add = (a, b) => a.map((x, k) => x + b[k]), sub = (a, b) => a.map((x, k) => x - b[k]);
    for (const zk of [1, 2]) { // plane y_zk = 0; G restricted = 4 y0 y3 (y0 - y3)(y0 + y3)
      const o = zk === 1 ? 2 : 1; // the remaining p-coordinate
      lines.push({ B: [e(o), e(3)], kind: 'anchor' });          // y0 = 0
      lines.push({ B: [e(0), e(o)], kind: 'anchor' });          // y3 = 0
      lines.push({ B: [add(e(0), e(3)), e(o)], kind: 'anchor' }); // y0 = y3
      lines.push({ B: [sub(e(0), e(3)), e(o)], kind: 'anchor' }); // y0 = -y3
    }
    if (s >= 2) {
      const r = Math.sqrt(Math.max(s ** 4 - 16, 0));
      const d1 = Math.sqrt((s * s + r) / 2), d2 = Math.sqrt((s * s - r) / 2);
      const vs = [s + d1, s - d1, s + d2, s - d2];
      let br = 0;
      for (const comp of [1, 2, 3, 4]) for (let k = 0; k < 4; k++) for (const sg of [1, -1]) {
        const v = vs[k];
        let B;
        if (comp <= 2) {
          const D = sg * Math.sqrt(v / 2), a = -(2 * D ** 5 - 3 * s * D ** 3 + s * s * D);
          B = comp === 1 ? [[1, a, -D, 0], [0, a, D, 1]] : [[1, a, D, 0], [0, -a, D, 1]];
        } else if (comp === 3) {
          const C = sg * Math.sqrt(v), b = -(C ** 5 - 3 * s * C ** 3 + 2 * s * s * C) / 2;
          B = [[1, 0, C, 0], [0, b, 0, 1]];
        } else {
          const D = sg * Math.sqrt(v), a = (D ** 5 - 3 * s * D ** 3 + 2 * s * s * D) / 2;
          B = [[1, a, 0, 0], [0, 0, D, 1]];
        }
        lines.push({ B, kind: 'wall', branch: br++ });
      }
    }
    // merge coincident lines (projector distance)
    const projs = lines.map((l) => { const Q = orthRows(l.B); const M = []; for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) M.push(Q[0][a] * Q[0][b] + Q[1][a] * Q[1][b]); return M; });
    const keep = [];
    for (let i = 0; i < lines.length; i++) {
      let dup = false;
      for (const j of keep) {
        let d = 0; for (let t = 0; t < 16; t++) d += (projs[i][t] - projs[j][t]) ** 2;
        if (d < 1e-10) { dup = true; lines[j].double = true; break; }
      }
      if (!dup) keep.push(i);
    }
    const out = keep.map((i) => lines[i]);
    return { lines: out, count: out.length };
  }

  const api = { decodeF32, compileQuartic, familyCoef, ballToR4, project, sampleField, marchingCubes, curveSegments, orthRows, linePoints, familyLines };
  root.Y56Core = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
