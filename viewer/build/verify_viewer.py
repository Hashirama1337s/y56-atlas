"""Accuracy check of everything the viewer draws.

usage: python verify_viewer.py <three@0.160.0 package dir>
  1. runs node_check.mjs (the viewer's own maths core, core.js, headless) and reads its output;
  2. decodes data/y56-data.js and checks, in floating point, that every exported curve point lies on the surface,
     ties every point back to the exact release data, and checks the counts against the exact tables.
Writes build/verify_report.json.
"""
import sys, os, json, base64, subprocess, tempfile, re
import numpy as np
from common import *

three = sys.argv[1]
tmp = os.path.join(tempfile.gettempdir(), 'y56_node_check.json')
subprocess.run(['node', os.path.join(HERE, 'node_check.mjs'), three, tmp], check=True, stdout=subprocess.DEVNULL)
NODE = json.load(open(tmp))
txt = open(os.path.join(OUT, 'y56-data.js'), encoding='ascii').read()
D = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
dec = lambda s, sh: np.frombuffer(base64.b64decode(s), '<f4').astype(float).reshape(sh)
R = {}; FAIL = []
def check(name, ok, val):
    R[name] = dict(ok=bool(ok), value=val); print(('PASS ' if ok else 'FAIL ') + name + ': ' + str(val))
    if not ok: FAIL.append(name)
TOL = 2e-6     # float32 storage of unit vectors: |F| on a degree-4 form with coefficients <= 4 stays far below this
SS = D['s_star']
check('s_star = 3/2^(1/4)', abs(SS - 3 / 2 ** 0.25) < 1e-15, SS)

# ---- exact data, parsed afresh ----
L = load_lines(); SY = load_syms(); P2, P4 = load_planes(); CPP = load_cpp()
DINV = 1 / DIAG
def proj(B): Q = orth_rows(B); return Q.T @ Q

# ---- A. the 56 lines ----
LP = dec(D['line_pts'], (56, D['nline'], 4))
check('A1 56 lines x %d points: max |G_s*(y)|' % D['nline'], np.abs(G(LP, SS)).max() < TOL, float(np.abs(G(LP, SS)).max()))
check('A2 same points in release coordinates: max |F(z)|, z = (y0, m y1, m y2, y3)', np.abs(F(LP * DIAG)).max() < 4 * TOL, float(np.abs(F(LP * DIAG)).max()))
res = 0.0
for i in range(56):
    Pz = proj(L[i]['B'])                       # exact line (release coordinates)
    Z = LP[i] * DIAG; Z /= np.linalg.norm(Z, axis=1)[:, None]
    res = max(res, float(np.abs(Z - Z @ Pz).max()))
check('A3 every line point lies on the exact line of lines_exact.txt with the same index', res < 1e-6, res)
orb = {}
for i, m in enumerate(D['lines']): orb.setdefault(m['orbit'], []).append(i)
check('A4 orbit sizes 8 + 16 + 16 + 16', sorted(len(v) for v in orb.values()) == [8, 16, 16, 16], [len(orb[k]) for k in sorted(orb)])
ok = True
for g in SY:
    for i, j in enumerate(g['sigma']): ok &= D['lines'][i]['orbit'] == D['lines'][j]['orbit']
check('A5 orbit labels are invariant under all 32 symmetries', ok, ok)
check('A6 each line meets exactly 16 others (incidence lists)', all(len(m['meets']) == 16 for m in D['lines']), 16)

# ---- B. conics ----
CP = dec(D['conic_pts'], (188, D['nconic'], 4))
check('B1 188 conics x %d points: max |G_s*(y)|' % D['nconic'], np.abs(G(CP, SS)).max() < TOL, float(np.abs(G(CP, SS)).max()))
fam = np.array([m['fam'] for m in D['conics']])
check('B2 148 + 40 conics', (int((fam == 0).sum()), int((fam == 1).sum())) == (148, 40), [int((fam == 0).sum()), int((fam == 1).sum())])
pl = 0.0
for k, m in enumerate(D['conics']):
    n = np.array([num(t) for t in m['plane']]); n /= np.linalg.norm(n)
    Z = CP[k] * DIAG
    pl = max(pl, float(np.abs(Z @ n).max() / np.linalg.norm(Z, axis=1).max()))
check('B3 every conic point lies in its exact plane (planes_exact / conic_pair_planes_exact)', pl < 1e-6, pl)
lines_in_planes = all(sorted(m['lines']) == sorted(L[i]['name'] for i in P2[k]['lines']) for k, m in enumerate(D['conics'][:148]))
check('B4 the 148 conics are listed with the two lines of their plane', lines_in_planes, lines_in_planes)
# a conic is not a line: points span a 3-space (not 2)
sv = min(np.linalg.svd(CP[k], compute_uv=False)[2] for k in range(188))
check('B5 each conic spans a plane, not a line (3rd singular value)', sv > 1e-3, float(sv))
pp = 0.0
for p in D['pair_planes']:
    n = np.array(p['n'])
    ks = [k for k, m in enumerate(D['conics']) if m['fam'] == 1 and m['plane'] == p['exact']]
    for k in ks: pp = max(pp, float(np.abs(CP[k] @ n).max()))
check('B6 the 20 drawn planes (picture coordinates) contain their 40 conics', pp < 1e-6 and len(D['pair_planes']) == 20, pp)

# ---- C. six faces ----
EXPECT = dict(g00=(56, 188, 188), g02=(12, 14, 10), g24=(8, 12, 8), g01=(4, 12, 8), g12=(0, 28, 22), g13=(0, 28, 20))
symd = {g['name']: g for g in SY}
rng = np.random.default_rng(7)
for f in D['faces']:
    rep = f['rep']; g = symd[rep]
    Mo = g['M'] / np.sqrt((g['M'] @ g['M'].T)[0, 0])
    A = np.array(f['A_re']) + 1j * np.array(f['A_im']); ph = f['phase'][0] + 1j * f['phase'][1]
    check(f'C0 {rep}: frame A is unitary and maps real x to sigma-real points (M conj(A) = A)',
          np.abs(A.conj().T @ A - np.eye(4)).max() < 1e-12 and np.abs(Mo @ A.conj() - A).max() < 1e-12, float(np.abs(Mo @ A.conj() - A).max()))
    X = rng.normal(size=(500, 4))
    q = eval_quartic(np.array(f['coef']), X); t = (G(X @ A.T, SS) / ph)
    check(f'C1 {rep}: drawn quartic = G_s*(A x)/phase, real', np.abs(q - t.real).max() / np.abs(t).max() < 1e-12 and np.abs(t.imag).max() / np.abs(t).max() < 1e-12,
          float(np.abs(q - t.real).max() / np.abs(t).max()))
    nl, no = f['lines'], f['ovals']
    check(f'C2 {rep}: real lines / sigma-real conics / ovals = {EXPECT[rep]}', (nl, f['real_conics'], no) == EXPECT[rep], (nl, f['real_conics'], no))
    fixed = [i for i in range(56) if g['sigma'][i] == i]
    check(f'C3 {rep}: the drawn lines are exactly the lines fixed by {rep}', sorted(f['line_ids']) == fixed, len(fixed))
    if rep == 'g00': continue            # the standard face reuses the main data (A = identity, phase 1, checked in C0/C1)
    worst = 0.0; worst_line = 0.0; worst_real = 0.0
    if nl:
        P = dec(f['line_pts'], (nl, D['nline'], 4))
        for j, i in enumerate(f['line_ids']):
            Y = P[j] @ A.T
            worst = max(worst, float(np.abs(G(Y, SS)).max()))
            Yz = Y * DIAG; Yz /= np.linalg.norm(Yz, axis=1)[:, None]
            worst_line = max(worst_line, float(np.abs(Yz - Yz @ proj(L[i]['B'])).max()))
            worst_real = max(worst_real, float(np.abs(Y @ Mo.T - Y.conj()).max()))   # sigma-real: M conj(y) = y  <=>  M y = conj(y) for real M
    if no:
        P = dec(f['oval_pts'], (no, D['nconic'], 4))
        for j, m in enumerate(f['oval_meta']):
            Y = P[j] @ A.T
            worst = max(worst, float(np.abs(G(Y, SS)).max()))
            n = np.array([num(t) for t in D['conics'][m['conic']]['plane']])
            worst_line = max(worst_line, float(np.abs((Y * DIAG) @ n).max() / np.abs(n).max()))
            worst_real = max(worst_real, float(np.abs(Y @ Mo.T - Y.conj()).max()))
    check(f'C4 {rep}: every drawn point y = A x satisfies |G_s*(y)| ~ 0, is sigma-real, and lies on its exact line / in its exact plane',
          worst < TOL and worst_line < 1e-5 and worst_real < 1e-6, dict(G=worst, on_exact=worst_line, sigma_real=worst_real))

# ---- D. family dial (from the viewer's own code) ----
bad = []; maxG = 0.0; table = {}
for rec in NODE['family']:
    s = rec['s']
    for pts in rec['lines']:
        P = np.array(pts).reshape(-1, 4)
        maxG = max(maxG, float(np.abs(G(P, s)).max()))
    isstar = abs(s - SS) < 1e-12
    shown = rec['count'] + (16 if isstar else 0)
    exp = 8 if s < 2 else 24 if s == 2 else 56 if isstar else 40
    if shown != exp: bad.append((s, shown, exp))
    key = 's<2' if s < 2 else 's=2' if s == 2 else 's*' if isstar else 's>2'
    table.setdefault(key, set()).add(shown)
check('D1 family lines drawn by core.js (float32 samples) lie on G_s (all s on the dial, 307 values)', maxG < TOL, maxG)
check('D2 real line count per s matches the exact table (8 below the wall, 24 at s = 2, 40 past it, 56 at s^4 = 81/2)', not bad, {k: sorted(v) for k, v in table.items()})
star = [r for r in NODE['family'] if abs(r['s'] - SS) < 1e-12][0]
PY = [proj(orth_rows(l['B'] * DINV)) for l in L]
got = set()
for pts in star['lines']:
    P = np.array(pts).reshape(-1, 4)
    Pm = proj(P[[0, 7]])
    d = [np.linalg.norm(Pm - p) for p in PY]; i = int(np.argmin(d))
    if d[i] < 1e-6: got.add(i)
special = set(D['special16'])
check('D3 at s^4 = 81/2 the 40 formula lines are exactly the 40 non-special Y56 lines; with the 16 they give all 56',
      got == set(range(56)) - special and len(special) == 16, len(got))
check('D4 the 16 special lines are one orbit (orbit S)', len({D['lines'][i]['orbit'] for i in special}) == 1, sorted(special))

# ---- E. viewer geometry (headless) ----
mc = NODE['mc']
check('E1 marching cubes (browser code): max |f| at mesh vertices relative to field scale (grid interpolation)',
      all(v['worst_rel_f_at_vertices'] < 2e-3 for k, v in mc.items() if isinstance(v, dict)), {k: round(v['worst_rel_f_at_vertices'], 6) for k, v in mc.items() if isinstance(v, dict)})
check('E2 family coefficients at s* equal the standard-face quartic', mc['family_at_sstar_vs_face_g00_coef_diff'] < 1e-12, mc['family_at_sstar_vs_face_g00_coef_diff'])
sg = NODE['segments']
check('E3 curve pieces stay in the ball and end on the glass', all(v['maxR'] <= 1 + 1e-9 and v['maxEndpointOffGlass'] < 1e-9 for v in sg.values()), sg)
nodes = np.array(D['wall_nodes'])
h = 1e-6; gr = np.stack([(G(nodes + h * np.eye(4)[k], 2.0) - G(nodes - h * np.eye(4)[k], 2.0)) / (2 * h) for k in range(4)], 1)
check('E4 the 8 gold points at the wall are singular points of G_2 (G = 0, gradient = 0)', np.abs(G(nodes, 2.0)).max() < 1e-12 and np.abs(gr).max() < 1e-6,
      dict(G=float(np.abs(G(nodes, 2.0)).max()), grad=float(np.abs(gr).max())))

# ---- F. shipped files ----
VIEW = os.path.normpath(os.path.join(HERE, '..'))
shipped = ['index.html', 'core.js', os.path.join('data', 'y56-data.js')]
sizes = {p: os.path.getsize(os.path.join(VIEW, p)) for p in shipped}
check('F1 total size under 15 MB', sum(sizes.values()) < 15e6, sizes)
pat = re.compile(r'((?<![A-Za-z])[A-Za-z]:[\\/](?!/)|/Users/|App[D]ata)', re.I)
hits = []
for p in shipped:
    t = re.sub(r'[A-Za-z0-9+/=]{40,}', ' ', open(os.path.join(VIEW, p), encoding='utf-8').read())
    for m in pat.finditer(t): hits.append((p, m.group(0), t[max(0, m.start() - 30):m.end() + 30]))
check('F2 no local paths, personal names or AI product names in shipped files', not hits, hits[:5])
libs = re.findall(r'https://[^"\' ]+', open(os.path.join(VIEW, 'index.html'), encoding='utf-8').read())
check('F3 external libraries only from cdn.jsdelivr.net/npm with an exact version', all(u.startswith('https://cdn.jsdelivr.net/npm/three@0.160.0/') for u in libs), libs)

json.dump(dict(results=R, failed=FAIL), open(os.path.join(HERE, 'verify_report.json'), 'w'), indent=1, default=str)
print('\n%d checks, %d failed' % (len(R), len(FAIL)))
sys.exit(1 if FAIL else 0)
