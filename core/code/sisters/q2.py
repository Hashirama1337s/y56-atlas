# Exact arithmetic in Q(sqrt2): x = a + b*sqrt2, a,b Fractions. Plus parsing of the Y56 exact data files.
from fractions import Fraction as Fr
import re, os, sympy as sp

class Q2:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0):
        s.a = Fr(a); s.b = Fr(b)
    @staticmethod
    def c(x):
        return x if isinstance(x, Q2) else Q2(x)
    def __add__(s, o): o = Q2.c(o); return Q2(s.a+o.a, s.b+o.b)
    __radd__ = __add__
    def __neg__(s): return Q2(-s.a, -s.b)
    def __sub__(s, o): o = Q2.c(o); return Q2(s.a-o.a, s.b-o.b)
    def __rsub__(s, o): return Q2.c(o) - s
    def __mul__(s, o): o = Q2.c(o); return Q2(s.a*o.a + 2*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def conj(s): return Q2(s.a, -s.b)          # Galois conjugate sqrt2 -> -sqrt2
    def norm(s): return s.a*s.a - 2*s.b*s.b
    def inv(s):
        n = s.norm(); assert n != 0, 'division by zero in Q(sqrt2)'
        return Q2(s.a/n, -s.b/n)
    def __truediv__(s, o): return s*Q2.c(o).inv()
    def __rtruediv__(s, o): return Q2.c(o)*s.inv()
    def __eq__(s, o): o = Q2.c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def iszero(s): return s.a == 0 and s.b == 0
    def sign(s):
        """exact sign of a + b sqrt2"""
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        d = a*a - 2*b*b
        assert d != 0
        return ((a > 0) - (a < 0)) if d > 0 else ((b > 0) - (b < 0))
    def __float__(s): return float(s.a) + float(s.b)*2**0.5
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f'({s.a}{"+" if s.b >= 0 else "-"}{abs(s.b)}*r2)'
    def sym(s): return sp.Rational(s.a.numerator, s.a.denominator) + sp.Rational(s.b.numerator, s.b.denominator)*sp.sqrt(2)

R2 = sp.sqrt(2)
def parse(t):
    e = sp.expand(sp.sympify(t) if isinstance(t, str) else t)
    b = sp.Rational(e.coeff(R2)); a = sp.Rational(sp.expand(e - b*R2))
    return Q2(Fr(int(a.p), int(a.q)), Fr(int(b.p), int(b.q)))

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'  # repository root
def load_lines():
    L = []
    for ln in open(D+'data/lines_exact.txt'):
        if not ln.startswith('L'): continue
        a_, b_ = ln.split(':', 1)[1].split('|')
        L.append([[parse(t) for t in eval(a_.strip())], [parse(t) for t in eval(b_.strip())]])
    return L
def load_syms():
    out = []
    for ln in open(D+'data/symmetry_exact.txt'):
        if not ln.startswith('g'): continue
        name = ln.split()[0]; c = parse(re.search(r'c=(\S+)', ln).group(1))
        M = [[parse(str(t)) for t in row] for row in sp.sympify(re.search(r'M=(\[\[.*?\]\])', ln).group(1))]
        sig = eval(re.search(r'sigma=(\[.*\])', ln).group(1))
        out.append((name, c, M, sig))
    return out
def load_planes():
    P2, P4 = [], []
    for ln in open(D+'data/planes_exact.txt'):
        m = re.match(r"P([24]) (\[.*?\]) lines (\[.*\])", ln)
        if m:
            rec = ([parse(t) for t in eval(m.group(2))], eval(m.group(3)))
            (P2 if m.group(1) == '2' else P4).append(rec)
    return P2, P4
def load_cpp():
    """20 conic-pair planes: (label, normal, Q1 str, Q2 str) in plane coords (x,y,w) with z = Bm (x,y,w)"""
    out = []; cur = None
    for ln in open(D+'data/conic_pair_planes_exact.txt'):
        m = re.match(r"([ABC]) (\[.*?\]) verified", ln)
        if m: cur = [m.group(1), [parse(t) for t in eval(m.group(2))], None, None]; out.append(cur); continue
        m = re.match(r"\s+Q1=(.*)", ln)
        if m: cur[2] = m.group(1).strip(); continue
        m = re.match(r"\s+Q2=(.*)", ln)
        if m: cur[3] = m.group(1).strip()
    return out

# ---------- linear algebra over Q(sqrt2) ----------
def matmul(A, B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))), Q2()) for j in range(len(B[0]))] for i in range(len(A))]
def matvec(A, v): return [sum((A[i][k]*v[k] for k in range(len(v))), Q2()) for i in range(len(A))]
def dot(u, v): return sum((a*b for a, b in zip(u, v)), Q2())
def rref(M):
    M = [row[:] for row in M]; piv = []; r = 0
    rows, cols = len(M), len(M[0]) if M else 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if not M[i][c].iszero()), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        iv = M[r][c].inv(); M[r] = [x*iv for x in M[r]]
        for i in range(rows):
            if i != r and not M[i][c].iszero():
                f = M[i][c]; M[i] = [x - f*y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    return M[:r], piv
def nullspace(M, n):
    if not M: return [[Q2(1) if i == j else Q2() for i in range(n)] for j in range(n)]
    R, piv = rref(M); free = [c for c in range(n) if c not in piv]; out = []
    for f in free:
        v = [Q2() for _ in range(n)]; v[f] = Q2(1)
        for i, p in enumerate(piv): v[p] = -R[i][f]
        out.append(v)
    return out
def rank(M): return len(rref(M)[1]) if M else 0
def det(M):
    n = len(M); M = [row[:] for row in M]; d = Q2(1)
    for c in range(n):
        p = next((i for i in range(c, n) if not M[i][c].iszero()), None)
        if p is None: return Q2()
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d = d*M[c][c]; iv = M[c][c].inv()
        for i in range(c+1, n):
            if not M[i][c].iszero():
                f = M[i][c]*iv; M[i] = [x - f*y for x, y in zip(M[i], M[c])]
    return d
