# Round 2, task 3 (EXACT lattice arithmetic): polarized invariants of the real structures sigma_g on (H^2(X,Z), h).
# Reuses the exact construction of core/code/sisters/s2_lattice.py (N = line lattice, NS = N by DIS, H = even unimodular
# overlattice of N (+) T glued by each of the 4 anti-isometries).  h = class of a plane section = sum of the 4 lines in a 4-line plane.
# Invariants of the triple (H, sigma*, h) computed for each sister (all must be gluing-independent):
#   L+ = ker(sigma - 1), L- = ker(sigma + 1) (h in L-), S = h^perp in L-;
#   div(h in L-), Smith invariants and discriminant-form fingerprint of L+ and of S,
#   whether h in (1 - sigma) H  (h is a "coboundary"), whether h in L+ + 2H  (mod-2 image).
import sys, itertools, math
from fractions import Fraction as Fr
from collections import Counter
src = open('../../core/code/sisters/s2_lattice.py', encoding='utf-8').read().split('out = {}')[0]
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(src)
from q2 import load_planes
P2, P4 = load_planes()
print('4-line planes:', len(P4))
def lineZ(j):      # Z-coords (row) of line j in the Z-basis of N
    v = flint.fmpq_mat([[C[r, j] for r in range(20)]])  # B-coords row
    z = v*Zinv
    return [z[0, k] for k in range(20)]
hs = []
for nrm, L in P4:
    assert len(L) == 4
    v = [sum(lineZ(j)[k] for j in L) for k in range(20)]
    hs.append(tuple(v))
print('distinct h vectors from the 4-line planes:', len(set(hs)), '(must be 1: all plane sections are linearly equivalent)')
assert len(set(hs)) == 1
hN = list(hs[0]); assert all(x.q == 1 for x in hN)
print('h.h =', bil(hN, hN))
def smith(Mint):
    D_, s_, t_ = smith_normal_decomp(Matrix(Mint.tolist()), domain=ZZ)
    return D_, s_, t_
def disc_fingerprint(Bm, GH):
    """Bm: list of integer row vectors (basis of a sublattice K of H, coords in H basis). Returns (Smith invariants, Counter of q mod 2 over A_K)."""
    Km = flint.fmpz_mat(Bm); GK = Km*GH*Km.transpose(); r = len(Bm)
    D_, s_, t_ = smith(GK)
    dk = [abs(int(D_[i, i])) for i in range(r)]
    tq = flint.fmpq_mat([[int(x) for x in row] for row in t_.tolist()]); GKq = flint.fmpq_mat(GK)
    gens = [[tq[k, i]/dk[i] for k in range(r)] for i in range(r) if dk[i] != 1]
    ords = [dk[i] for i in range(r) if dk[i] != 1]
    def qf(v): return sum(v[x]*GKq[x, y]*v[y] for x in range(r) for y in range(r))
    # Gram of generators (mod 1 off-diagonal, mod 2 diagonal) -> enumerate group
    gq = [[qf([a + b for a, b in zip(gens[i], gens[j])]) for j in range(len(gens))] for i in range(len(gens))]
    qq = [qf(g) for g in gens]
    bb = [[(gq[i][j] - qq[i] - qq[j])/2 for j in range(len(gens))] for i in range(len(gens))]
    cnt = Counter()
    total = 1
    for o in ords: total *= o
    if total <= 1 << 16:
        for e in itertools.product(*[range(o) for o in ords]):
            val = sum(e[i]*e[i]*qq[i] for i in range(len(e))) + 2*sum(e[i]*e[j]*bb[i][j] for i in range(len(e)) for j in range(i+1, len(e)))
            v = Fr(int(val.p), int(val.q)) % 2
            cnt[v] += 1
    return tuple(sorted(Counter(ords).items())), tuple(sorted(cnt.items()))
def solve_Z(Mrows, target):
    """is target (row) in the Z-row-span of Mrows?"""
    Hh = flint.fmpz_mat(Mrows).hnf()
    rows = [[int(Hh[i, j]) for j in range(Hh.ncols())] for i in range(Hh.nrows()) if any(Hh[i, j] != 0 for j in range(Hh.ncols()))]
    # reduce target by HNF rows
    t = list(target); n = len(t)
    for row in rows:
        piv = next(j for j in range(n) if row[j] != 0)
        if t[piv] % row[piv] != 0: return False
        f = t[piv] // row[piv]; t = [a - f*b for a, b in zip(t, row)]
    return all(x == 0 for x in t)
out = {}
for d in res:
    name = d['rep']; gm = gmats[name]
    eps = 1 if all(act_AN(gm, e) == e for e in elems[:3]) else -1
    sT = [1, -1] if eps == 1 else [-1, 1]
    results = set()
    for gam in gammas:
        lifts = []
        for e in [tuple(1 if k == j else 0 for k in range(2)) for j in range(2)]:
            a, b = gam[e]
            lifts.append(combo(e) + [flint.fmpq(a, 2), flint.fmpq(b, 32)])
        vecs = [[flint.fmpq(1 if i == j else 0) for j in range(22)] for i in range(22)] + lifts
        Hint = flint.fmpz_mat([[int(v*64) for v in row] for row in vecs]).hnf()
        Hb = flint.fmpq_mat([[flint.fmpq(int(Hint[i, j]), 64) for j in range(22)] for i in range(22)])
        Gfull = flint.fmpq_mat(22, 22)
        for i in range(20):
            for j in range(20): Gfull[i, j] = GZq[i, j]
        Gfull[20, 20] = 2; Gfull[21, 21] = 32
        GH = Hb*Gfull*Hb.transpose(); GHi = flint.fmpz_mat([[int(GH[i, j]) for j in range(22)] for i in range(22)])
        Sig = flint.fmpq_mat(22, 22)
        for i in range(20):
            for j in range(20): Sig[i, j] = -gm[i, j]
        Sig[20, 20] = sT[0]; Sig[21, 21] = sT[1]
        SH = Hb*Sig*Hb.inv(); SHi = flint.fmpz_mat([[int(SH[i, j]) for j in range(22)] for i in range(22)])
        I22 = flint.fmpz_mat([[1 if i == j else 0 for j in range(22)] for i in range(22)])
        # h in H coordinates
        h22 = flint.fmpq_mat([hN + [flint.fmpq(0), flint.fmpq(0)]])*Hb.inv()
        assert all(h22[0, k].q == 1 for k in range(22))
        h = [int(h22[0, k]) for k in range(22)]
        hm = flint.fmpz_mat([h])
        assert hm*SHi == flint.fmpz_mat([[-x for x in h]]), 'sigma h != -h'
        assert (hm*GHi*hm.transpose())[0, 0] == 4
        divH = math.gcd(*[int((hm*GHi)[0, k]) for k in range(22)])
        Lp = kernel_Z(SHi - I22); Lm = kernel_Z(SHi + I22)
        # S = h^perp in L-
        Lmm = flint.fmpz_mat(Lm)
        hv = Lmm*GHi*hm.transpose()          # column: h . (basis of L-)
        divLm = math.gcd(*[int(hv[i, 0]) for i in range(len(Lm))])
        Sk = kernel_Z(hv)                     # coefficient vectors x with x . hv = 0
        Sb = [[sum(x[i]*int(Lmm[i, k]) for i in range(len(Lm))) for k in range(22)] for x in Sk]
        fpLp = disc_fingerprint(Lp, GHi); fpS = disc_fingerprint(Sb, GHi); fpLm = disc_fingerprint(Lm, GHi)
        cob = solve_Z([[int((I22 - SHi)[i, j]) for j in range(22)] for i in range(22)], h)       # h in (1 - sigma)H ?
        mod2 = solve_Z([list(map(int, row)) for row in Lp] + [[2 if i == j else 0 for j in range(22)] for i in range(22)], h)  # h in L+ + 2H ?
        # h^perp in H: involution restricted; its invariant part is L+ (h in L-) and anti-invariant part S
        results.add((len(Lp), len(Lm), len(Sb), divH, divLm, fpLp, fpLm, fpS, cob, mod2))
    assert len(results) == 1, ('gluing-dependent', name, results)
    rL, rM, rS, divH, divLm, fpLp, fpLm, fpS, cob, mod2 = results.pop()
    out[name] = (rL, rM, rS, divH, divLm, fpLp, fpLm, fpS, cob, mod2)
    print(f'{name}: rank L+ {rL}, L- {rM}, S=h^perp in L- {rS}; div(h) in H {divH}, in L- {divLm}; h in (1-sigma)H: {cob}; h in L+ + 2H: {mod2}')
    print(f'      A(L+) {fpLp[0]} q-fingerprint {fpLp[1]}')
    print(f'      A(L-) {fpLm[0]} q-fingerprint {fpLm[1]}')
    print(f'      A(S)  {fpS[0]} q-fingerprint {fpS[1]}')
print()
for a, b in [('g01', 'g02'), ('g01', 'g24'), ('g02', 'g24'), ('g12', 'g13')]:
    same = out[a] == out[b]
    diff = [k for k, (x, y) in enumerate(zip(out[a], out[b])) if x != y]
    print(f'{a} vs {b}: all invariants equal: {same}; differing fields: {diff}')
