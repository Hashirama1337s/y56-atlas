# EXPLORATORY numerical check (method b): mesh the real locus of sigma_g = g o conj, lifted to S^3, and count
# Euler characteristic, components, antipodal pairing.  Real coordinates: z = A x, A = [Q+ | i Q-] (Q+- orthonormal
# eigenbases of M/sqrt(lambda), which is symmetric orthogonal), x in S^3 real.  F(Ax) = phase * real quartic.
import sys, pickle, numpy as np
from skimage.measure import marching_cubes
import scipy.sparse as sps
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
sys.path.insert(0, '.')
res = pickle.load(open('s1_group.pkl', 'rb'))['res']
r2 = np.sqrt(2)
def F(z):
    z0, z1, z2, z3 = z
    return 3*r2*z0**2*z1*z2 + 3*r2*z1*z2*z3**2 - r2*z1**3*z2 - r2*z1*z2**3 + 4*z0**3*z3 - 4*z0*z3**3
def realframe(d):
    M = np.array([[float(x) for x in row] for row in d['M']]); lam = (M @ M)[0, 0]; Mp = M/np.sqrt(lam)
    assert np.allclose(Mp, Mp.T) and np.allclose(Mp @ Mp, np.eye(4))
    w, V = np.linalg.eigh(Mp)
    Qp = V[:, w > 0]; Qm = V[:, w < 0]
    A = np.hstack([Qp, 1j*Qm]).astype(complex)
    rng = np.random.default_rng(0); X = rng.normal(size=(4, 20000)); X /= np.linalg.norm(X, axis=0)
    Fv = F(A @ X); k = np.argmax(abs(Fv)); ph = Fv[k]/abs(Fv[k])
    resid = abs((Fv/ph).imag).max()/abs(Fv).max()
    return A, ph, resid, Qp.shape[1]
def mesh_stats(Gs, N, seed=1):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(200000, 4)); X /= np.linalg.norm(X, axis=1)[:, None]
    v_ = Gs(X.T); pole = X[np.argmax(abs(v_))]
    near = X[abs(v_) < 0.01*abs(v_).max()]
    th0 = np.arccos(np.clip(near @ pole, -1, 1)).min(); Lbox = 1.25/np.tan(th0/2)
    Q = np.linalg.qr(np.column_stack([pole, rng.normal(size=(4, 3))]))[0]
    if Q[:, 0] @ pole < 0: Q[:, 0] *= -1
    g = np.linspace(-Lbox, Lbox, N); Gv = np.empty((N, N, N))
    for i in range(N):   # slab by slab (memory)
        Y0 = np.full((N, N), g[i]); Y1, Y2 = np.meshgrid(g, g, indexing='ij'); s = Y0**2 + Y1**2 + Y2**2
        U = np.stack([(s-1)/(s+1), 2*Y0/(s+1), 2*Y1/(s+1), 2*Y2/(s+1)]).reshape(4, -1)
        Gv[i] = Gs(Q @ U).reshape(N, N)
    bd = np.concatenate([Gv[0].ravel(), Gv[-1].ravel(), Gv[:, 0].ravel(), Gv[:, -1].ravel(), Gv[:, :, 0].ravel(), Gv[:, :, -1].ravel()])
    bdok = bool((np.sign(bd) == np.sign(bd[0])).all())
    v, f, _, _ = marching_cubes(Gv, 0.0, spacing=(g[1]-g[0],)*3); v += g[0]
    from collections import Counter
    ec = Counter()
    for a, b in ((0, 1), (1, 2), (0, 2)):
        for e in map(tuple, np.sort(f[:, [a, b]], axis=1)): ec[e] += 1
    bad = sum(1 for e, n in ec.items() if n != 2)
    chi = len(v) - len(ec) + len(f)
    Am = sps.coo_matrix((np.ones(3*len(f)), (np.r_[f[:, 0], f[:, 1], f[:, 2]], np.r_[f[:, 1], f[:, 2], f[:, 0]])), shape=(len(v), len(v)))
    ncomp, lab = connected_components(Am, directed=False)
    used = np.unique(f);
    comps = []
    tree = cKDTree(v)
    for c in sorted(set(lab[used])):
        fc = f[lab[f[:, 0]] == c]; Ec = set()
        for a, b in ((0, 1), (1, 2), (0, 2)): Ec.update(map(tuple, np.sort(fc[:, [a, b]], axis=1)))
        vc = np.unique(fc); chic = len(vc) - len(Ec) + len(fc)
        # antipode of a sample of vertices: stereographic y -> -y/|y|^2
        ys = v[vc[::max(1, len(vc)//50)]]; ya = -ys/np.sum(ys**2, axis=1)[:, None]
        dd, jj = tree.query(ya); partners = Counter(lab[jj])
        comps.append(dict(chi=chic, nv=len(vc), antipode=partners.most_common(1)[0][0], antidist=float(np.median(dd))))
    return dict(N=N, box=float(Lbox), boundary_sign_constant=bdok, V=len(v), E=len(ec), F=len(f), bad_edges=bad, chi_lift=chi,
                ncomp=len(comps), comps=comps, labels=sorted(set(lab[used])))
if __name__ == '__main__':
    Ns = [int(a) for a in sys.argv[1:]] or [160, 240]
    out = {}
    for d in res:
        A, ph, resid, npos = realframe(d)
        Gs = lambda Xt, A=A, ph=ph: (F(A @ Xt)/ph).real
        out[d['rep']] = dict(A=A, ph=ph, resid=resid, npos=npos, runs=[])
        print(f"{d['rep']}: eigen signs +{npos} -{4-npos}; reality residual of F(Ax)/phase: {resid:.2e}", flush=True)
        for N in Ns:
            st = mesh_stats(Gs, N); out[d['rep']]['runs'].append(st)
            # components of X_R in RP^3: pair antipodal lift components
            labs = st['labels']; pc = {lb: c for lb, c in zip(labs, st['comps'])}
            seen = set(); real_comps = []
            for lb in labs:
                if lb in seen: continue
                c = pc[lb]; partner = c['antipode']
                if partner == lb: real_comps.append(('self-antipodal', c['chi']//2))
                else: real_comps.append(('pair', c['chi'])); seen.add(partner)
                seen.add(lb)
            st['real_components'] = real_comps
            print(f"   N={N} box={st['box']:.2f} boundary-sign-ok={st['boundary_sign_constant']} V,E,F={st['V']},{st['E']},{st['F']} "
                  f"non-manifold edges={st['bad_edges']} chi(lift)={st['chi_lift']} lift comps={st['ncomp']} -> X_R components "
                  f"{[(k, ch, 'genus %d' % ((2-ch)//2)) for k, ch in real_comps]}", flush=True)
    pickle.dump(out, open('s4_mesh.pkl', 'wb'))
