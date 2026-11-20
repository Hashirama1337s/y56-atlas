# Task C, family part.  Pencil P(a,b,c) = a Im(w^4) + Im(p^2)(b|w|^2 + c|p|^2) (all 32 maps act on every member with the
# same characters, so every sister real structure sigma_g = g o conj lives on every real member).  Singular members
# (Singular, c_fam.log): c = 0 or kappa = b^2/(ac) = +-4; kappa -> -kappa is a real projective equivalence (w -> e^{i pi/4} w).
# Y56: kappa = -9/sqrt2 ~ -6.364.  Fermat-type member: b = 0 (kappa = 0).
# (1) the 8 nodes of the wall member (a,b,c) = (1,2,-1): coordinates (Newton), which are sigma_g-real (g fixes the node);
# (2) NUMERICAL mesh topology of each sister real structure on members on both sides of the wall.
import sys, pickle, numpy as np
sys.path.insert(0, '../../core/code/sisters')
import s4_mesh as S4
res = pickle.load(open('../../core/code/sisters/s1_group.pkl', 'rb'))['res']
def Ffam(a, b, c):
    def F(z):
        z0, z1, z2, z3 = z
        return a*(4*z0**3*z3 - 4*z0*z3**3) + 2*z1*z2*(b*(z0**2 + z3**2) + c*(z1**2 + z2**2))
    return F
def grad(F, z, h=1e-7):
    return np.array([(F(z + h*e) - F(z - h*e))/(2*h) for e in np.eye(4)])
# --- (1) nodes of the wall member: Newton on grad F = 0 with |z| = 1 from many real starts
F = Ffam(1, 2, -1)
def J(z):
    import numpy as _np
    H = _np.empty((4, 4))
    for k, e in enumerate(_np.eye(4)): H[:, k] = (grad(F, z + 1e-5*e) - grad(F, z - 1e-5*e))/2e-5
    return H
rng = np.random.default_rng(0); nodes = []
for _ in range(4000):
    z = rng.normal(size=4); z /= np.linalg.norm(z)
    for it in range(60):
        g = grad(F, z); Aug = np.vstack([J(z), 2*z]); rhs = -np.r_[g, z @ z - 1]
        dz = np.linalg.lstsq(Aug, rhs, rcond=None)[0]; z = z + dz
        if np.linalg.norm(dz) < 1e-13: break
    if np.linalg.norm(grad(F, z)) < 1e-9 and abs(np.linalg.norm(z) - 1) < 1e-9:
        zz = z if z[np.argmax(abs(z))] > 0 else -z
        if not any(np.allclose(zz, n, atol=1e-7) for n in nodes): nodes.append(zz)
print('wall member (1,2,-1): real singular points found by Newton (standard real structure):', len(nodes), '(Singular: 8 singular points in all)')
for n in nodes: print('   ', np.round(n, 6), ' |w|^2 =', round(n[0]**2 + n[3]**2, 6))
# Hessian signature of each node (restricted to the tangent space of S^3)
for n in nodes:
    H = J(n); T = np.linalg.svd(n[None, :])[2][1:].T; ev = np.linalg.eigvalsh(T.T @ H @ T)
    print('    node Hessian signature (on S^3 tangent):', (ev > 0).sum(), '+', (ev < 0).sum(), '-')
for d in res:
    M = np.array([[float(x) for x in row] for row in d['M']])
    fixed = sum(1 for n in nodes if np.linalg.matrix_rank(np.column_stack([M @ n, n]), tol=1e-8) == 1)
    print(f"{d['rep']}: nodes of the wall member fixed by g (= sigma_g-real nodes, all 8 nodes being conj-real): {fixed}")
# --- (2) mesh topology on both sides
if len(sys.argv) > 1:
    N = int(sys.argv[1])
    members = [('kappa=-9 (Y56 chamber)', (1, 3, -1)), ('Y56 itself', (1, 3/np.sqrt(2), -1/np.sqrt(2))),
               ('kappa=-1 (Fermat chamber)', (1, 1, -1)), ('kappa=0 Fermat-type', (1, 0, -1))]
    for name, (a, b, c) in members:
        Fm = Ffam(a, b, c); out = []
        for d in res:
            A, ph, resid, npos = S4.realframe(d)
            Xs = np.random.default_rng(0).normal(size=(4, 20000)); Xs /= np.linalg.norm(Xs, axis=0)
            Fv = Fm(A @ Xs); k = np.argmax(abs(Fv)); ph = Fv[k]/abs(Fv[k])
            assert abs((Fv/ph).imag).max() < 1e-9*abs(Fv).max()
            st = S4.mesh_stats(lambda Xt, A=A, ph=ph: (Fm(A @ Xt)/ph).real, N)
            out.append(f"{d['rep']}: chi(X_R) {st['chi_lift']//2:+d}, lift comps {st['ncomp']}, bad edges {st['bad_edges']}, box-sign ok {st['boundary_sign_constant']}")
        print(f'{name} (a,b,c)=({a:.4g},{b:.4g},{c:.4g}) N={N}:'); [print('   ', o) for o in out]; sys.stdout.flush()
