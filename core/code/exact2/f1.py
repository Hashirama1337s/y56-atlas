# (1) exact real-point check of the 40 conics  (4) orbit sizes of 148 + 50 planes. Run e1.py first (it writes e1_out.pkl).
import pickle, re, numpy as np, sympy as sp
x, y, w = sp.symbols('x y w'); r = sp.sqrt(2)
out = pickle.load(open('e1_out.pkl', 'rb'))

def sgn(e):
    """exact sign of a + b*sqrt2 (a,b rational)"""
    e = sp.radsimp(sp.expand(e)); a, b = sp.Rational(0), sp.Rational(0)
    e = sp.expand(e); a = e.subs(r, 0) if False else None
    c = sp.Poly(e, sp.sqrt(2)) if e.has(sp.sqrt(2)) else None
    if c is None: return int(sp.sign(e))
    co = c.all_coeffs()[::-1]; a = co[0]; b = co[1] if len(co) > 1 else 0
    a = sp.Rational(a); b = sp.Rational(b)
    if b == 0: return int(sp.sign(a))
    if a == 0: return int(sp.sign(b))
    if a > 0 and b > 0: return 1
    if a < 0 and b < 0: return -1
    # opposite signs: compare a^2 with 2 b^2
    d = a*a - 2*b*b
    assert d != 0
    return int(sp.sign(a)) if d > 0 else int(sp.sign(b))

rows = []; Pms = []; Ss = []; allreal = True
for name, n, ok, facs, dets in out:
    n = [sp.sympify(t) for t in n]
    i = [j for j in range(4) if n[j] != 0][0]; oth = [j for j in range(4) if j != i]
    Bm = np.zeros((4, 3))
    for k, o in enumerate(oth): Bm[o, k] = 1
    for k, o in enumerate(oth): Bm[i, k] = float(sp.N(-n[o]/n[i], 30))
    for f in facs:
        f = sp.sympify(f); H = (sp.hessian(f, (x, y, w))/2).applyfunc(sp.radsimp)
        m1 = H[0, 0]; m2 = H[:2, :2].det(); m3 = H.det()
        s = [sgn(m1), sgn(m2), sgn(m3)]
        pd = s == [1, 1, 1]; nd = s == [-1, 1, -1]
        # leading-minor test is valid for definiteness only if the minors are nonzero; if a minor is 0 the form is not definite
        definite = (pd or nd)
        if 0 in s:
            definite = False  # a zero leading minor forbids definiteness (strict)
        real = not definite
        allreal &= real
        rows.append((name, [str(t) for t in n], s, real))
print('conics checked', len(rows), 'all have real points (indefinite):', allreal)
for rw in rows: print(rw[0], 'leading minor signs', rw[2], 'indefinite' if rw[3] else 'DEFINITE')
pickle.dump(rows, open('f1_real.pkl', 'wb'))
# (4) orbits of the 148 / 50 planes via the exact induced line permutations
sig = [eval(re.search(r'sigma=(\[.*\])', ln).group(1)) for ln in open('../../data/symmetry_exact.txt') if ln.startswith('g')]
P2 = []; P4 = []
for ln in open('../../data/planes_exact.txt'):
    mm = re.match(r"P([24]) .* lines (\[.*\])", ln)
    if mm: (P2 if mm.group(1) == '2' else P4).append(frozenset(eval(mm.group(2))))
print('counts', len(P2), len(P4))
def orbits(P):
    S = set(P); seen = set(); sizes = []
    for p in P:
        if p in seen: continue
        o = {frozenset(s[i] for i in p) for s in sig}
        assert o <= S, 'orbit leaves the plane list'
        seen |= o; sizes.append(len(o))
    return sorted(sizes, reverse=True)
print('orbit sizes 148 two-line planes:', orbits(P2), sum(orbits(P2)))
print('orbit sizes 50 four-line planes:', orbits(P4), sum(orbits(P4)))
