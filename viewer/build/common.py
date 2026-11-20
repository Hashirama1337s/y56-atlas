"""Shared loaders and maths for the Y56 atlas viewer build (reads only the exact release data files)."""
import os, re, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'core', 'data'))
OUT = os.path.normpath(os.path.join(HERE, '..', 'data'))
R2 = math.sqrt(2.0)
M8 = 2.0 ** 0.125                      # z1, z2 of the release equation = M8 * (family coordinates)
S_STAR = 3.0 / 2.0 ** 0.25             # Y56 in the family: s^4 = 81/2
DIAG = np.array([1.0, M8, M8, 1.0])    # z = DIAG * y

def num(t):
    """exact string over Q(sqrt2) -> float (via sympy, 30 digits)"""
    return float(sp.N(sp.sympify(t), 30))

def F(z):
    """release equation, z[...,4]"""
    z0, z1, z2, z3 = z[..., 0], z[..., 1], z[..., 2], z[..., 3]
    return (3*R2*z0**2*z1*z2 + 3*R2*z1*z2*z3**2 - R2*z1**3*z2 - R2*z1*z2**3
            + 4*z0**3*z3 - 4*z0*z3**3)

def G(y, s):
    """family G_s = Im(w^4) + Im(p^2)(s|w|^2 - |p|^2), w = y0 + i y3, p = y1 + i y2"""
    y0, y1, y2, y3 = y[..., 0], y[..., 1], y[..., 2], y[..., 3]
    return 4*y0**3*y3 - 4*y0*y3**3 + 2*y1*y2*(s*(y0**2 + y3**2) - (y1**2 + y2**2))

def load_lines():
    out = []
    for ln in open(os.path.join(DATA, 'lines_exact.txt')):
        if not ln.startswith('L'): continue
        name, rest = ln.split(':', 1)
        a, b = rest.split('|')
        ea, eb = eval(a.strip()), eval(b.strip())
        out.append(dict(name=name.strip(), exact=[ea, eb],
                        B=np.array([[num(t) for t in ea], [num(t) for t in eb]])))
    assert len(out) == 56
    return out

def load_syms():
    out = []
    for ln in open(os.path.join(DATA, 'symmetry_exact.txt')):
        if not ln.startswith('g'): continue
        name = ln.split()[0]
        c = num(re.search(r'c=(\S+)', ln).group(1))
        Ms = re.search(r'M=(\[\[.*?\]\])', ln).group(1)
        M = np.array([[float(sp.N(t, 30)) for t in row] for row in sp.sympify(Ms)])
        sig = eval(re.search(r'sigma=(\[.*\])', ln).group(1))
        out.append(dict(name=name, c=c, M=M, sigma=sig))
    assert len(out) == 32
    return out

def load_planes():
    P2, P4 = [], []
    for ln in open(os.path.join(DATA, 'planes_exact.txt')):
        m = re.match(r"P([24]) (\[.*?\]) lines (\[.*\])", ln)
        if m:
            ex = eval(m.group(2))
            rec = dict(exact=ex, n=np.array([num(t) for t in ex]), lines=eval(m.group(3)))
            (P2 if m.group(1) == '2' else P4).append(rec)
    assert len(P2) == 148 and len(P4) == 50
    return P2, P4

def load_cpp():
    out = []; cur = None
    for ln in open(os.path.join(DATA, 'conic_pair_planes_exact.txt')):
        m = re.match(r"([ABC]) (\[.*?\]) verified", ln)
        if m:
            ex = eval(m.group(2))
            cur = dict(label=m.group(1), exact=ex, n=np.array([num(t) for t in ex]), Q=[None, None]); out.append(cur); continue
        m = re.match(r"\s+Q1=(.*)", ln)
        if m: cur['Q'][0] = m.group(1).strip(); continue
        m = re.match(r"\s+Q2=(.*)", ln)
        if m: cur['Q'][1] = m.group(1).strip()
    assert len(out) == 20
    return out

def plane_param(n):
    """the release convention: first nonzero index i of n is solved for; the other coordinates, in order, are (x, y, w).
    Returns P (4x3) with z = P (x, y, w)."""
    i = [j for j in range(4) if abs(n[j]) > 1e-12][0]
    oth = [j for j in range(4) if j != i]
    P = np.zeros((4, 3))
    for k, o in enumerate(oth):
        P[o, k] = 1.0
        P[i, k] = -n[o] / n[i]
    return P

def orth_rows(B):
    q, _ = np.linalg.qr(np.asarray(B, float).T)
    return q.T

def conic_points(P, S, n_out=360, n_fine=6000):
    """real points of the nondegenerate indefinite conic u^T S u = 0 in the plane z = P u, as unit vectors in R^4,
    one closed lift on S^3, resampled to equal chord length. Returns None if the conic has no real points."""
    S = (S + S.T) / 2
    w, V = np.linalg.eigh(S)
    npos = int((w > 0).sum())
    if npos in (0, 3): return None
    if npos == 1: w = -w
    o = np.argsort(-w); w = w[o]; V = V[:, o]
    t = np.linspace(0, 2*np.pi, n_fine, endpoint=False)
    u = np.stack([np.cos(t)/np.sqrt(w[0]), np.sin(t)/np.sqrt(w[1]), np.full_like(t, 1/np.sqrt(-w[2]))])
    p = (P @ (V @ u)).T
    p /= np.linalg.norm(p, axis=1)[:, None]
    return resample_closed(p, n_out)

def resample_closed(p, n_out):
    q = np.vstack([p, p[:1]])
    d = np.linalg.norm(np.diff(q, axis=0), axis=1)
    c = np.concatenate([[0], np.cumsum(d)])
    tt = np.linspace(0, c[-1], n_out, endpoint=False)
    out = np.stack([np.interp(tt, c, q[:, k]) for k in range(q.shape[1])], axis=1)
    return out / np.linalg.norm(out, axis=1)[:, None]

def line_points(B, n=200):
    """one copy of a projective line: half a great circle, t in [0, pi), endpoints antipodal (closed in RP^3)"""
    Q = orth_rows(B)
    t = np.linspace(0, np.pi, n, endpoint=False)
    return np.outer(np.cos(t), Q[0]) + np.outer(np.sin(t), Q[1])

# monomials of degree 4 in 4 variables (35), fixed order shared with the viewer
MONOS = [(a, b, c, 4-a-b-c) for a in range(4, -1, -1) for b in range(4-a, -1, -1) for c in range(4-a-b, -1, -1)]
assert len(MONOS) == 35

def fit_quartic(fun, rng, npts=400):
    X = rng.normal(size=(npts, 4))
    A = np.stack([np.prod(X**np.array(e), axis=1) for e in MONOS], axis=1)
    v = fun(X)
    coef, *_ = np.linalg.lstsq(A, v, rcond=None)
    return coef, float(np.abs(A @ coef - v).max() / np.abs(v).max())

def eval_quartic(coef, X):
    return sum(c * np.prod(X**np.array(e), axis=-1) for c, e in zip(coef, MONOS))
