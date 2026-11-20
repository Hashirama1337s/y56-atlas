# Task B step 2 (NUMERICAL search, then handed to msolve for an exact certificate):
# mesh X_R (lift to S^3), label components (antipodes merged), and find by LP a quadratic form q(x) = x^T Q x / |x|^2
# whose values on the three components lie in three disjoint ranges.  Output Q (small integers) and two
# rational thresholds t1 < t2, then write msolve inputs that certify  {G = 0} cap {q = t_i} has NO real point.
import sys, pickle, itertools, numpy as np, sympy as sp
from fractions import Fraction
sys.path.insert(0, '../../core/code/sisters')
import s5_portraits as S5
from s4_mesh import F
from skimage.measure import marching_cubes
import scipy.sparse as sps
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from scipy.optimize import linprog
gen = pickle.load(open('b_gen_g12_g13.pkl', 'rb'))
x = sp.symbols('x0:4'); s = sp.Symbol('s'); r = sp.sqrt(2)
def comps_samples(rep, N=150):
    A = S5.mesh[rep]['A']; ph = S5.mesh[rep]['ph']; Gs = lambda Xt: (F(A @ Xt)/ph).real
    rng = np.random.default_rng(1)
    X = rng.normal(size=(200000, 4)); X /= np.linalg.norm(X, axis=1)[:, None]
    v_ = Gs(X.T); pole = X[np.argmax(abs(v_))]
    near = X[abs(v_) < 0.01*abs(v_).max()]
    th0 = np.arccos(np.clip(near @ pole, -1, 1)).min(); Lb = 1.25/np.tan(th0/2)
    Q = S5.frame_of(pole, rng)
    g = np.linspace(-Lb, Lb, N); Gv = np.empty((N, N, N)); Y1, Y2 = np.meshgrid(g, g, indexing='ij')
    for i in range(N):
        Y0 = np.full((N, N), g[i]); s_ = Y0**2 + Y1**2 + Y2**2
        Gv[i] = Gs(Q @ np.stack([(s_-1)/(s_+1), 2*Y0/(s_+1), 2*Y1/(s_+1), 2*Y2/(s_+1)]).reshape(4, -1)).reshape(N, N)
    v, f, _, _ = marching_cubes(Gv, 0.0, spacing=(g[1]-g[0],)*3); v += g[0]
    Am = sps.coo_matrix((np.ones(3*len(f)), (np.r_[f[:, 0], f[:, 1], f[:, 2]], np.r_[f[:, 1], f[:, 2], f[:, 0]])), shape=(len(v), len(v)))
    nc, lab = connected_components(Am, directed=False); tree = cKDTree(v)
    rep_of = {}
    for c in set(lab[f[:, 0]]):
        y = v[lab == c][0]; _, j = tree.query(-y/(y @ y)); rep_of[c] = min(c, lab[j])
    comps = sorted(set(rep_of.values()))
    ss = np.sum(v**2, axis=1)
    Xf = Q @ np.vstack([(ss-1)/(ss+1), 2*v.T/(ss+1)])          # 4 x V on S^3 (float real coords)
    Ae = np.array(gen[rep]['A'].evalf(30).tolist(), dtype=complex)
    T = np.linalg.solve(Ae, A); assert abs(T.imag).max() < 1e-12
    Xe = T.real @ Xf; Xe /= np.linalg.norm(Xe, axis=0)
    out = []
    for c in comps:
        idx = np.where(np.isin(lab, [k for k, rr in rep_of.items() if rr == c]))[0]
        out.append(Xe[:, idx[::max(1, len(idx)//1500)]].T)
    return out, T.real
def quadfeat(X):   # X: n x 4 unit -> 10 features x_i x_j
    return np.column_stack([X[:, i]*X[:, j]*(1 if i == j else 2) for i in range(4) for j in range(i, 4)])
def lp_sep(groups):
    best = None
    for order in itertools.permutations(range(len(groups))):
        # variables: Q (10), t1, t2, margin m ; maximise m ; |Q entries| <= 1
        nv = 10 + 2 + 1; Aub = []; bub = []
        for pos, gi in enumerate(order):
            Fm = quadfeat(groups[gi])
            if pos > 0:   # q >= t_pos + m  ->  -q + t + m <= 0
                for row in Fm: a = np.zeros(nv); a[:10] = -row; a[10 + pos - 1] = 1; a[12] = 1; Aub.append(a); bub.append(0)
            if pos < len(order) - 1:   # q <= t_{pos+1} - m
                for row in Fm: a = np.zeros(nv); a[:10] = row; a[10 + pos] = -1; a[12] = 1; Aub.append(a); bub.append(0)
        c = np.zeros(nv); c[12] = -1
        bnd = [(-1, 1)]*10 + [(None, None)]*2 + [(None, 1)]
        res = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), bounds=bnd, method='highs')
        if res.status == 0 and (best is None or res.x[12] > best[1]): best = (order, res.x[12], res.x)
    return best
def to_Q(vec):
    Q = np.zeros((4, 4)); k = 0
    for i in range(4):
        for j in range(i, 4): Q[i, j] = Q[j, i] = vec[k]; k += 1
    return Q
report = {}
for rep in sys.argv[1:]:
    groups, T = comps_samples(rep)
    print(rep, 'mesh components (RP^3):', len(groups), ' samples:', [len(gp) for gp in groups])
    order, m, sol = lp_sep(groups)
    print('   best LP order', order, 'margin %.4f' % m)
    if m <= 0: report[rep] = None; continue
    # integerise: scale so max |Q| = 20, round; thresholds: midpoints of the gaps, rounded to rationals
    Qr = np.round(to_Q(sol[:10])/np.abs(sol[:10]).max()*20).astype(int)
    qv = [np.einsum('ni,ij,nj->n', gp, Qr, gp) for gp in groups]
    rng_ = [(q.min(), q.max()) for q in qv]
    o = order; ts = []
    for a, b in zip(o, o[1:]):
        lo, hi = rng_[a][1], rng_[b][0]
        assert lo < hi, ('integerised Q loses separation', rep)
        ts.append(Fraction((lo+hi)/2).limit_denominator(8))
    print('   integer Q =', Qr.tolist(), ' ranges by component:', [(round(a, 3), round(b, 3)) for a, b in rng_], ' thresholds', [str(t) for t in ts])
    report[rep] = dict(order=order, Q=Qr, ts=ts, ranges=rng_, T=T)
    # msolve certificates: G = 0, q - t|x|^2 = 0, |x|^2 = 1, det[grad h2; x; grad G; grad q] = 0, s^2 = 2
    G = gen[rep]['G']; Gs = sp.expand(G.subs(r, s))
    den = sp.lcm([sp.fraction(sp.together(tm))[1] for tm in sp.Add.make_args(Gs)]); Gs = sp.expand(Gs*den)
    Qs = sp.Matrix(Qr.tolist()); H2 = sp.Matrix([[3, -1, 2, 0], [-1, 1, 1, 2], [2, 1, -4, 1], [0, 2, 1, 5]])
    X = sp.Matrix(x)
    for k, t in enumerate(ts):
        t = sp.Rational(t.numerator, t.denominator)
        qe = sp.expand((X.T*Qs*X)[0] - t*sum(v**2 for v in x)); qe = sp.expand(qe*sp.denom(t))
        Mm = sp.Matrix([list(H2*X), list(X), [sp.diff(Gs, v) for v in x], [sp.diff(qe, v) for v in x]])
        eqs = [Gs, qe, sp.expand(sum(v**2 for v in x) - 1), sp.expand(Mm.det()), s**2 - 2]
        with open('b_%s_sep%d.ms' % (rep, k), 'w') as f:
            f.write('x0,x1,x2,x3,s\n0\n' + ',\n'.join(str(e).replace('**', '^') for e in eqs) + '\n')
pickle.dump(report, open('b_sep_%s.pkl' % '_'.join(sys.argv[1:]), 'wb'))
