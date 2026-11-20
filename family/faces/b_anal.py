# Task B analysis: parse msolve real critical points of h = x^T Q x on X_R (lift to S^3), keep s > 0 (s = +sqrt2),
# Morse index from the constrained Hessian, sorted pattern, then place every real conic oval in an h-interval.
import sys, re, pickle, numpy as np, sympy as sp
from fractions import Fraction
sys.path.insert(0, '../../core/code/sisters')
import s5_portraits as S5
x = sp.symbols('x0:4')
gen = {}
for k in ('g12_g13', 'g01_g02_g24_g00'):
    gen.update(pickle.load(open('b_gen_%s.pkl' % k, 'rb')))
def parse(fn):
    txt = open(fn).read().strip().rstrip(':')
    t2 = re.sub(r'(-?\d+)\s*/\s*2\^(\d+)', lambda m: f'Fraction({m.group(1)},2**{m.group(2)})', txt)
    data = eval(t2)
    assert data[0] == 0, 'not zero-dimensional'
    return data[1][1]
report = {}
for rep in sys.argv[1:]:
    d = gen[rep]; G = d['G']; QH = np.array(d['QH'].tolist(), dtype=float)
    Gf = sp.lambdify([x], G, 'numpy'); gr = sp.lambdify([x], [sp.diff(G, v) for v in x], 'numpy')
    He = sp.lambdify([x], sp.hessian(G, x).tolist(), 'numpy')
    sols = parse('b_%s.out' % rep)
    pts = []
    for sl in sols:
        lo = [float(b[0]) for b in sl]; hi = [float(b[1]) for b in sl]
        mid = np.array([(a+b)/2 for a, b in zip(lo, hi)]); width = max(b-a for a, b in zip(lo, hi))
        if mid[4] < 0: continue
        pts.append((mid[:4], width))
    print(f'{rep}: msolve real solutions {len(sols)}, with s = +sqrt2: {len(pts)}; max box width {max(w for _, w in pts):.1e}')
    crit = []
    for p, w in pts:
        g = np.array(gr(p), dtype=float)
        # 2Qx = mu g + 2 nu x
        co, *_ = np.linalg.lstsq(np.column_stack([g, 2*p]), 2*QH @ p, rcond=None); mu, nu = co
        resid = np.linalg.norm(np.column_stack([g, 2*p]) @ co - 2*QH @ p)
        T = np.linalg.svd(np.vstack([p, g]))[2][2:].T
        H = T.T @ (2*QH - mu*np.array(He(p), dtype=float) - 2*nu*np.eye(4)) @ T
        ev = np.linalg.eigvalsh(H)
        idx = int((ev < 0).sum())
        crit.append(dict(x=p, h=float(p @ QH @ p), idx=idx, ev=ev, G=float(Gf(p)), res=resid))
    crit.sort(key=lambda c: c['h'])
    # antipodal pairs share h (h even): collapse to RP^3 points
    rp = []
    for c in crit:
        if rp and abs(rp[-1]['h'] - c['h']) < 1e-9 and np.allclose(rp[-1]['x'], -c['x'], atol=1e-8): rp[-1]['pair'] = True; continue
        rp.append(dict(c, pair=False))
    print(f'   RP^3 critical points: {len(rp)} (all antipodally paired: {all(c["pair"] for c in rp)})')
    for c in rp:
        print(f'   h = {c["h"]: .9f}  index {c["idx"]}  Hessian eigs {c["ev"][0]: .3e},{c["ev"][1]: .3e}  |G| {abs(c["G"]):.1e}')
    pattern = ''.join('m' if c['idx'] == 0 else ('M' if c['idx'] == 2 else 's') for c in rp)
    print('   sorted index pattern:', pattern)
    # intervals (only valid if pattern alternates mMmM...)
    ivs = [(rp[2*k]['h'], rp[2*k+1]['h']) for k in range(len(rp)//2)] if pattern == 'mM'*(len(rp)//2) else None
    print('   component h-intervals:', ivs)
    if ivs is None: report[rep] = dict(pattern=pattern); continue
    # ovals: x_float (z = A_f x_f) -> x_exact = A_e^{-1} z
    Af = S5.mesh[rep]['A']; Ae = np.array(d['A'].evalf(30).tolist(), dtype=complex)
    T = np.linalg.solve(Ae, Af); Tr = T.real; assert abs(T.imag).max() < 1e-12
    lines, conics = S5.real_curves(rep)
    tally = {}; gapmin = np.inf
    for k, (C, kind) in enumerate(conics):
        X = (Tr @ C.T); X /= np.linalg.norm(X, axis=0)
        hv = np.einsum('in,ij,jn->n', X, QH, X); gres = np.abs(Gf(X)).max()
        lo, hi = hv.min(), hv.max()
        comp = [j for j, (a, b) in enumerate(ivs) if a - 1e-9 <= lo and hi <= b + 1e-9]
        assert len(comp) == 1, (rep, k, lo, hi, ivs)
        j = comp[0]; tally.setdefault(j, []).append(kind)
        gapmin = min(gapmin, lo - ivs[j][0], ivs[j][1] - hi)
    for j in range(len(ivs)):
        ks = tally.get(j, [])
        print(f'   component {j} (h in [{ivs[j][0]:.6f}, {ivs[j][1]:.6f}]): {len(ks)} ovals ({ks.count("res")} two-line-plane, {ks.count("cpp")} pair-plane)')
    gaps = [ivs[j+1][0] - ivs[j][1] for j in range(len(ivs)-1)]
    print(f'   gaps between component intervals: {gaps};  min margin oval-range to own interval end: {gapmin:.3e}; lines: {len(lines)}')
    report[rep] = dict(pattern=pattern, ivs=ivs, tally={j: tally.get(j, []) for j in range(len(ivs))}, crit=rp)
pickle.dump(report, open('b_anal_%s.pkl' % '_'.join(sys.argv[1:]), 'wb'))
