"""Build data/y56-data.js for the Y56 atlas viewer from the exact release data files.

Everything numeric in the viewer comes from here (or from formulas in core.js that verify_viewer.py re-checks):
  - the 56 lines (core/data/lines_exact.txt), orbits from symmetry_exact.txt,
  - the 148 conics of the two-line planes (planes_exact.txt; conic = section / (line x line), solved by least squares, residual checked),
  - the 40 conics of the 20 line-free planes (conic_pair_planes_exact.txt, exact Q1, Q2),
  - the six real faces (real structures sigma_g = g o conj for the six class representatives of SISTERS.md),
  - the family G_s quartic coefficients and the 8 node points of the wall s = 2.

Picture coordinates: the family frame y with z = (y0, m y1, m y2, y3), m = 2^(1/8), in which Y56 is G_s at s^4 = 81/2.
Ball model: real projective space = unit 3-sphere modulo sign; each point is flipped into the hemisphere x.c >= 0 around the
centre c and projected stereographically, Y = E x / (1 + c.x), so RP^3 becomes the unit ball with opposite boundary points glued.
"""
import json, base64, sys
import numpy as np, sympy as sp
from common import *

rng = np.random.default_rng(20261120)
REPORT = {}
DINV = 1.0 / DIAG

def b64(a):
    return base64.b64encode(np.ascontiguousarray(a, dtype='<f4').tobytes()).decode('ascii')

# ---------------- lines and orbits ----------------
L = load_lines(); SY = load_syms()
By = [orth_rows(l['B'] * DINV) for l in L]          # rows of B are points z; y = z / DIAG
par = list(range(56))
def root(i):
    while par[i] != i: i = par[i]
    return i
for g in SY:
    for i, j in enumerate(g['sigma']): par[root(i)] = root(j)
groups = {}
for i in range(56): groups.setdefault(root(i), []).append(i)
FIXED8 = [2, 14, 22, 24, 27, 30, 43, 53]                         # lines in y1 = 0 or y2 = 0 (on every G_s)
SPECIAL16 = [0, 6, 10, 11, 12, 19, 29, 33, 35, 36, 42, 44, 48, 50, 54, 55]   # pencil/RESULT.md item 7: the Y56-only lines (orbit S)
orbits = sorted(groups.values(), key=lambda v: (len(v), v[0]))
orbit_of = [None]*56
# name the orbits by their role in the family
names = {}
for v in orbits:
    if sorted(v) == FIXED8: names['anchor'] = v
    elif sorted(v) == SPECIAL16: names['y56only'] = v
assert 'anchor' in names and 'y56only' in names, 'orbit/role mismatch'
rest = [v for v in orbits if v is not names['anchor'] and v is not names['y56only']]
rest.sort(key=lambda v: v[0])
names['wallA'], names['wallB'] = rest
ORB_KEYS = ['anchor', 'wallA', 'wallB', 'y56only']
for k, key in enumerate(ORB_KEYS):
    for i in names[key]: orbit_of[i] = k
REPORT['orbit_sizes'] = {k: len(names[k]) for k in ORB_KEYS}

# incidence (meeting pairs) and incidence type, for the hover card
def meets(A, B):
    return abs(np.linalg.det(np.vstack([A, B]))) < 1e-9
deg = [sum(meets(By[i], By[j]) for j in range(56) if j != i) for i in range(56)]
assert set(deg) == {16}, deg
REPORT['each_line_meets'] = 16

# line samples (one copy of each projective line = half a great circle)
NL = 160
line_pts = np.stack([line_points(b, NL) for b in By])                # 56 x NL x 4
lines_meta = [dict(name=L[i]['name'], orbit=orbit_of[i], exact=L[i]['exact'],
                   meets=[j for j in range(56) if j != i and meets(By[i], By[j])]) for i in range(56)]

# ---------------- conics ----------------
NC = 240
P2, P4 = load_planes(); CPP = load_cpp()
conic_pts, conic_meta = [], []
worst_fit = 0.0
for k, pl in enumerate(P2):
    P = plane_param(pl['n'])                                         # z = P u
    lam = []
    for li in pl['lines']:
        U = np.linalg.lstsq(P, L[li]['B'].T, rcond=None)[0]          # 3x2, plane coords of the line
        assert np.abs(P @ U - L[li]['B'].T).max() < 1e-9, 'line not in plane'
        lam.append(np.cross(U[:, 0], U[:, 1]))
    X = rng.normal(size=(300, 3))
    f = F(X @ P.T)
    l12 = (X @ lam[0]) * (X @ lam[1])
    idx = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    A = np.stack([l12 * X[:, i] * X[:, j] * (1 if i == j else 2) for i, j in idx], axis=1)
    sol, *_ = np.linalg.lstsq(A, f, rcond=None)
    worst_fit = max(worst_fit, float(np.abs(A @ sol - f).max() / np.abs(f).max()))
    Sm = np.zeros((3, 3))
    for (i, j), v in zip(idx, sol): Sm[i, j] = Sm[j, i] = v
    pts = conic_points(DINV[:, None] * P, Sm, NC)
    assert pts is not None
    conic_pts.append(pts)
    conic_meta.append(dict(fam=0, plane=pl['exact'], lines=[L[i]['name'] for i in pl['lines']]))
REPORT['conic148_fit_rel_residual'] = worst_fit
x_, y_, w_ = sp.symbols('x y w')
pair_planes = []
for k, cp in enumerate(CPP):
    P = plane_param(cp['n'])
    for q in (0, 1):
        expr = sp.sympify(cp['Q'][q], locals={'x': x_, 'y': y_, 'w': w_})
        H = sp.hessian(expr, (x_, y_, w_)) / 2
        Sm = np.array([[float(sp.N(H[i, j], 30)) for j in range(3)] for i in range(3)])
        pts = conic_points(DINV[:, None] * P, Sm, NC)
        assert pts is not None
        conic_pts.append(pts)
        conic_meta.append(dict(fam=1, plane=cp['exact'], label=cp['label'], plane_index=k))
    ny = cp['n'] * DIAG; ny /= np.linalg.norm(ny)                     # n.z = (DIAG n).y
    pair_planes.append(dict(n=ny.tolist(), label=cp['label'], exact=cp['exact']))
conic_pts = np.stack(conic_pts)                                        # 188 x NC x 4
REPORT['conics'] = dict(total=len(conic_pts), fam0=148, fam1=40)

# ---------------- view frame (centre with a 16-element stabiliser) ----------------
C0 = np.array([0, 1, 1, 0]) / np.sqrt(2)
E0 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], np.array([0, 1, -1, 0]) / np.sqrt(2)])
stab = 0
for g in SY:
    Mo = g['M'] / np.sqrt((g['M'] @ g['M'].T)[0, 0])
    if abs(abs(Mo @ C0 @ C0) - 1) < 1e-9: stab += 1
REPORT['centre_stabiliser'] = stab

# ---------------- family coefficients ----------------
K0, r0 = fit_quartic(lambda X: G(X, 0.0), rng)
K1, r1 = fit_quartic(lambda X: G(X, 1.0) - G(X, 0.0), rng)
K0[np.abs(K0) < 1e-10] = 0; K1[np.abs(K1) < 1e-10] = 0
REPORT['family_fit_residual'] = max(r0, r1)
# wall nodes, s = 2 (8 points of RP^3); closed forms from the morph study, checked here
tt = 2*np.cos(np.pi/8); tp = 2*np.sin(np.pi/8); s2 = np.sqrt(2)
NODES = np.array([(1+s2, -tt, tt, 1), (1+s2, tt, -tt, 1), (1-s2, tp, -tp, 1), (1-s2, -tp, tp, 1),
                  (-1+s2, tp, tp, 1), (-1+s2, -tp, -tp, 1), (-1-s2, tt, tt, 1), (-1-s2, -tt, -tt, 1)])
NODES = NODES / np.linalg.norm(NODES, axis=1)[:, None]
h = 1e-6
grad = np.stack([(G(NODES + h*np.eye(4)[k], 2.0) - G(NODES - h*np.eye(4)[k], 2.0))/(2*h) for k in range(4)], 1)
REPORT['wall_nodes'] = dict(max_G=float(np.abs(G(NODES, 2.0)).max()), max_grad=float(np.abs(grad).max()))
assert REPORT['wall_nodes']['max_G'] < 1e-12 and REPORT['wall_nodes']['max_grad'] < 1e-6

# ---------------- six real faces ----------------
FACE_REPS = ['g00', 'g02', 'g24', 'g01', 'g12', 'g13']
FACE_EXPECT = dict(g00=(56, 188, 188), g02=(12, 14, 10), g24=(8, 12, 8), g01=(4, 12, 8), g12=(0, 28, 22), g13=(0, 28, 20))
FACE_TOPO = dict(g00='one connected surface of genus 10', g02='one surface of genus 2', g24='one surface of genus 2',
                 g01='one surface of genus 2', g12='three separate spheres', g13='three separate spheres')
symd = {g['name']: g for g in SY}
G56 = lambda Z: G(Z, S_STAR)
# conic data in y coordinates for the face computation: plane basis P_y (4x3) and Gram S
conic_planes = []
for pl in P2:
    conic_planes.append(DINV[:, None] * plane_param(pl['n']))
for cp in CPP:
    Py = DINV[:, None] * plane_param(cp['n'])
    conic_planes += [Py, Py]
# recover each conic's Gram in its own plane coordinates (again, from the same construction)
def gram_of(k):
    pts = conic_pts[k]
    P = conic_planes[k]
    U = np.linalg.lstsq(P, pts.T, rcond=None)[0].T                     # NC x 3
    A = np.stack([U[:, 0]**2, U[:, 1]**2, U[:, 2]**2, 2*U[:, 0]*U[:, 1], 2*U[:, 0]*U[:, 2], 2*U[:, 1]*U[:, 2]], 1)
    _, _, Vt = np.linalg.svd(A); a = Vt[-1]
    return np.array([[a[0], a[3], a[4]], [a[3], a[1], a[5]], [a[4], a[5], a[2]]])
GRAMS = [gram_of(k) for k in range(len(conic_pts))]

def real_subspace(V):
    """V: 4xk complex basis of a subspace of C^4 (in x coordinates). Return a real orthonormal basis (rows) of its real points."""
    Vr, Vi = V.real, V.imag
    M = np.hstack([Vi, Vr])                       # Im(V (a + i b)) = Vi a + Vr b = 0
    _, s, Vt = np.linalg.svd(M)
    k = V.shape[1]
    null = Vt[(s > 1e-9).sum():] if len(s) == 2*k else Vt[(np.concatenate([s, np.zeros(2*k-len(s))]) > 1e-9).sum():]
    X = np.array([Vr @ v[:k] - Vi @ v[k:] for v in null])
    if len(X) == 0: return X
    q, r = np.linalg.qr(X.T)
    rank = (np.abs(np.diag(r)) > 1e-9).sum()
    return q[:, :rank].T

faces = []
for rep in FACE_REPS:
    g = symd[rep]
    Mo = g['M'] / np.sqrt((g['M'] @ g['M'].T)[0, 0])
    assert np.allclose(Mo, Mo.T) and np.allclose(Mo @ Mo, np.eye(4))
    w, V = np.linalg.eigh(Mo)
    A = np.hstack([V[:, w > 0], 1j * V[:, w < 0]])                   # y = A x, x real  <=>  y is sigma_g-real
    if rep == "g00": A = np.eye(4, dtype=complex)                   # standard face: x = y, same picture as the main view
    Xs = rng.normal(size=(4000, 4)); Fv = G56(Xs @ A.T)
    k = np.argmax(np.abs(Fv)); ph = 1.0 if rep == "g00" else Fv[k] / abs(Fv[k])
    reality = float(np.abs((Fv/ph).imag).max() / np.abs(Fv).max())
    assert reality < 1e-12
    coef, fitres = fit_quartic(lambda X: (G56(X @ A.T) / ph).real, rng)
    coef[np.abs(coef) < 1e-12] = 0
    AH = A.conj().T
    # real lines: lines fixed by g
    flines, fline_ids = [], []
    for i in range(56):
        if g['sigma'][i] != i: continue
        R = real_subspace(AH @ By[i].T)
        assert R.shape[0] == 2, (rep, i, R.shape)
        flines.append(line_points(R, NL)); fline_ids.append(i)
    # real conics: plane fixed and conic fixed, then real points if indefinite
    fovals, foval_meta, nreal = [], [], 0
    for k in range(len(conic_pts)):
        P = conic_planes[k]
        W = real_subspace(AH @ P)
        if W.shape[0] != 3: continue                                  # plane not fixed by sigma
        T = np.linalg.lstsq(P.astype(complex), A @ W.T, rcond=None)[0]  # P T = A W^T
        assert np.abs(P @ T - A @ W.T).max() < 1e-9
        K = T.T @ GRAMS[k] @ T
        j = np.unravel_index(np.argmax(np.abs(K)), K.shape); K = K / (K[j] / abs(K[j]))
        if np.abs(K.imag).max() > 1e-7 * np.abs(K).max(): continue    # conic swapped with its partner
        nreal += 1
        pts = conic_points(W.T, K.real, NC)
        if pts is None: continue                                      # sigma-real conic without real points
        fovals.append(pts); foval_meta.append(dict(fam=conic_meta[k]['fam'], conic=k))
    exp = FACE_EXPECT[rep]
    got = (len(flines), nreal, len(fovals))
    assert got == exp, (rep, got, exp)
    # ball centre: g00 uses the symmetric centre; others: maximise how far the cutting sphere stays from the surface
    if rep == 'g00':
        c, E = C0, E0
    else:
        best = None
        cand = rng.normal(size=(1500, 4)); cand /= np.linalg.norm(cand, axis=1)[:, None]
        probe = rng.normal(size=(1200, 4))
        mx = np.abs(eval_quartic(coef, cand)).max()
        for cc in cand:
            Pp = probe - np.outer(probe @ cc, cc); Pp /= np.linalg.norm(Pp, axis=1)[:, None]
            sc = np.quantile(np.abs(eval_quartic(coef, Pp)), 0.03) / mx
            if best is None or sc > best[0]: best = (sc, cc)
        c = best[1]
        q, _ = np.linalg.qr(np.column_stack([c, np.eye(4)[:, np.argsort(np.abs(c))[:3]]]))
        E = q[:, 1:].T
        if q[:, 0] @ c < 0: pass
    faces.append(dict(rep=rep, lines=len(flines), real_conics=nreal, ovals=len(fovals), topology=FACE_TOPO[rep],
                      coef=coef.tolist(), centre=list(map(float, c)), frame=E.tolist(), line_ids=fline_ids,
                      line_pts='' if rep == 'g00' or not flines else b64(np.stack(flines)), oval_pts='' if rep == 'g00' or not fovals else b64(np.stack(fovals)),
                      oval_meta=foval_meta, fitres=fitres, reality=reality, reuse_main=(rep == 'g00'),
                      A_re=A.real.tolist(), A_im=A.imag.tolist(), phase=[float(np.real(ph)), float(np.imag(ph))]))
    print(rep, 'lines', len(flines), 'sigma-real conics', nreal, 'ovals', len(fovals), 'fit', fitres, flush=True)
REPORT['faces'] = {f['rep']: (f['lines'], f['real_conics'], f['ovals']) for f in faces}

# ---------------- family branches -> Y56 lines (for colours and hover) ----------------
def family_branches(s):
    """the 32 graph lines by branch label (comp, k, sign); identical ordering to core.js"""
    out = []
    if s < 2: return out
    r = np.sqrt(max(s**4 - 16, 0.0))
    d1, d2 = np.sqrt((s*s + r)/2), np.sqrt((s*s - r)/2)
    vs = [s + d1, s - d1, s + d2, s - d2]
    for comp in (1, 2, 3, 4):
        for k, v in enumerate(vs):
            for sg in (1, -1):
                if comp in (1, 2):
                    D = sg*np.sqrt(v/2); a = -(2*D**5 - 3*s*D**3 + s*s*D)
                    Cc, A_, B_ = (-D, a, a) if comp == 1 else (D, a, -a)
                    B = np.array([[1, A_, Cc, 0], [0, B_, D, 1]])
                elif comp == 3:
                    Cc = sg*np.sqrt(v); B_ = -(Cc**5 - 3*s*Cc**3 + 2*s*s*Cc)/2
                    B = np.array([[1, 0, Cc, 0], [0, B_, 0, 1]])
                else:
                    D = sg*np.sqrt(v); A_ = (D**5 - 3*s*D**3 + 2*s*s*D)/2
                    B = np.array([[1, A_, 0, 0], [0, 0, D, 1]])
                out.append(((comp, k, sg), B))
    return out
def projm(B): Q = orth_rows(B); return Q.T @ Q
PY = [projm(b) for b in By]
branch_to_line = []
for lab, B in family_branches(S_STAR):
    d = [np.linalg.norm(projm(B) - p) for p in PY]; i = int(np.argmin(d))
    assert d[i] < 1e-8 and i not in FIXED8 and i not in SPECIAL16
    branch_to_line.append(i)
assert len(set(branch_to_line)) == 32
REPORT['family_branches_match_y56'] = True

DATA = dict(
    version='1.0', s_star=S_STAR, m8=M8,
    orbit_keys=ORB_KEYS, orbit_sizes=[len(names[k]) for k in ORB_KEYS],
    centre=C0.tolist(), frame=E0.tolist(),
    lines=lines_meta, nline=NL, line_pts=b64(line_pts),
    conics=conic_meta, nconic=NC, conic_pts=b64(conic_pts),
    pair_planes=pair_planes,
    fixed8=FIXED8, special16=SPECIAL16, branch_to_line=branch_to_line,
    family=dict(K0=K0.tolist(), K1=K1.tolist()),
    monos=[list(e) for e in MONOS],
    wall_nodes=NODES.tolist(),
    faces=faces,
)
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'y56-data.js'), 'w', encoding='ascii') as fh:
    fh.write('/* Y56 atlas viewer data, generated by build/build_data.py from the exact release data. Do not edit. */\n')
    fh.write('window.Y56DATA = ' + json.dumps(DATA, separators=(',', ':')) + ';\n')
with open(os.path.join(HERE, 'build_report.json'), 'w') as fh:
    json.dump(REPORT, fh, indent=1, default=float)
print(json.dumps(REPORT, indent=1, default=float))
print('wrote', os.path.join('data', 'y56-data.js'), os.path.getsize(os.path.join(OUT, 'y56-data.js')), 'bytes')
