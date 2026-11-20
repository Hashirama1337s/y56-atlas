# EXPLORATORY renders: the six real forms of Y56 (S^3 double-cover model, stereographic), real lines + real conics;
# 2x3 contact sheet; screw-symmetry animation of the standard form.  Not a proof of anything.
import sys, pickle, numpy as np, pyvista as pv
from skimage.measure import marching_cubes
sys.path.insert(0, '../../core/code/sisters')
from q2 import load_lines
OUT = '../../core/code/sisters/'
BG = "#0b0d12"; SURF = "#2b9ac9"; LINE = "#39ff9c"; RES = "#ffd23d"; PAIR = "#b36bff"; TXT = "#9fb4c8"
r2 = np.sqrt(2)
def F(z):
    z0, z1, z2, z3 = z
    return 3*r2*z0**2*z1*z2 + 3*r2*z1*z2*z3**2 - r2*z1**3*z2 - r2*z1*z2**3 + 4*z0**3*z3 - 4*z0*z3**3
g1 = pickle.load(open(OUT+'s1_group.pkl', 'rb')); res = {d['rep']: d for d in g1['res']}
lat = pickle.load(open(OUT+'s2_lattice.pkl', 'rb')); con = pickle.load(open(OUT+'s3_conics.pkl', 'rb'))
mesh = pickle.load(open(OUT+'s4_mesh.pkl', 'rb'))
Lx = [(np.array([float(x) for x in l[0]]), np.array([float(x) for x in l[1]])) for l in load_lines()]
ORDER = ['g00', 'g02', 'g24', 'g01', 'g12', 'g13']
TOPO = {'g00': 'one surface of genus 10', 'g02': 'one surface of genus 2', 'g24': 'one surface of genus 2',
        'g01': 'one surface of genus 2', 'g12': 'three spheres', 'g13': 'three spheres'}
def real_curves(rep, nt=1500):
    """real lines and real conic ovals of structure rep, as point arrays on S^3 in real coords x (z = A x)."""
    A = mesh[rep]['A']; Ah = A.conj().T; d = res[rep]
    M = np.array([[float(x) for x in row] for row in d['M']]); Mp = M/np.sqrt((M @ M)[0, 0])
    lines = []
    t = np.linspace(0, 2*np.pi, nt)
    for i in d['fixed']:
        U = np.column_stack(Lx[i]).astype(complex)        # z = U c
        Mb = np.hstack([A, -U, -1j*U]); Rr = np.vstack([Mb.real, Mb.imag])
        _, s, Vt = np.linalg.svd(Rr); X = Vt[-2:, :4].T    # real x-directions (2-dim)
        assert s[-2] < 1e-9 and s[-3] > 1e-6
        X = np.linalg.qr(X)[0]
        lines.append((np.outer(X[:, 0], np.cos(t)) + np.outer(X[:, 1], np.sin(t))).T)
    conics = []
    for (ci, kind, has_real) in con['summary'][rep]['details']:
        if not has_real: continue
        _, P, Q = con['conics'][ci]; P = np.array(P); Q = np.array(Q)
        G = np.linalg.lstsq(P, Mp @ P, rcond=None)[0]
        nsp = lambda K: np.linalg.svd(K)[2][np.linalg.svd(K)[1] < 1e-9].T
        Ep, Em = nsp(G - np.eye(3)), nsp(G + np.eye(3)); assert Ep.shape[1] + Em.shape[1] == 3, (rep, ci)
        B = np.hstack([Ep, 1j*Em])
        Rc = B.T @ Q @ B; k = np.unravel_index(np.argmax(abs(Rc)), Rc.shape); Rc = (Rc/(Rc[k]/abs(Rc[k]))).real
        Rc = (Rc + Rc.T)/2; ev, W = np.linalg.eigh(Rc)
        if (ev > 0).sum() == 1: ev = -ev
        o = np.argsort(-ev); ev = ev[o]; W = W[:, o]
        y = W @ np.stack([np.cos(t)/np.sqrt(ev[0]), np.sin(t)/np.sqrt(ev[1]), np.ones_like(t)/np.sqrt(-ev[2])])
        z = P @ (B @ y); x = Ah @ z
        ph = x[:, 0]/abs(x[:, 0]) if False else None
        # x is real up to a common complex phase per point; remove it
        j = np.argmax(abs(x), axis=0); phs = x[j, np.arange(x.shape[1])]/abs(x[j, np.arange(x.shape[1])])
        xr = (x/phs).real; assert np.abs((x/phs).imag).max() < 1e-8*np.abs(x).max()
        xr /= np.linalg.norm(xr, axis=0)
        conics.append((xr.T, kind))
    return lines, conics
def choose_pole(Gs, curves, rng):
    X = rng.normal(size=(60000, 4)); X /= np.linalg.norm(X, axis=1)[:, None]
    v = np.abs(Gs(X.T)); v /= v.max()
    pts = np.vstack(curves) if curves else np.zeros((0, 4))
    if len(pts):
        pts = pts[::max(1, len(pts)//2500)]; dd = np.min(1 - (X @ pts.T)**2, axis=1)   # sin^2 distance to curves (and antipodes)
        score = np.minimum(v, 3*dd)
    else: score = v
    return X[np.argmax(score)]
def frame_of(pole, rng):
    Q = np.linalg.qr(np.column_stack([pole, rng.normal(size=(4, 3))]))[0]
    if Q[:, 0] @ pole < 0: Q[:, 0] *= -1
    return Q
def stereo(Q, x):   # x: n x 4 on S^3
    u = x @ Q; return u[:, 1:]/(1 - u[:, [0]])
def surface_mesh(Gs, Q, Lb, N):
    g = np.linspace(-Lb, Lb, N); Gv = np.empty((N, N, N))
    Y1, Y2 = np.meshgrid(g, g, indexing='ij')
    for i in range(N):
        Y0 = np.full((N, N), g[i]); s = Y0**2 + Y1**2 + Y2**2
        U = np.stack([(s-1)/(s+1), 2*Y0/(s+1), 2*Y1/(s+1), 2*Y2/(s+1)]).reshape(4, -1)
        Gv[i] = Gs(Q @ U).reshape(N, N)
    v, f, _, _ = marching_cubes(Gv, 0.0, spacing=(g[1]-g[0],)*3); v += g[0]
    return v, f
def add_curve(pl, xyz, col, rad, lim):
    m = np.linalg.norm(xyz, axis=1) < lim; idx = np.where(m)[0]
    if len(idx) < 2: return
    for rn in np.split(idx, np.where(np.diff(idx) > 1)[0]+1):
        if len(rn) < 2: continue
        pl.add_mesh(pv.lines_from_points(xyz[rn]).tube(radius=rad, n_sides=6), color=col, smooth_shading=True, ambient=0.7, diffuse=0.5)
def portrait(rep, N=200, size=1400, fname=None):
    A = mesh[rep]['A']; ph = mesh[rep]['ph']
    Gs = lambda Xt: (F(A @ Xt)/ph).real
    lines, conics = real_curves(rep)
    rng = np.random.default_rng(5)
    pole = choose_pole(Gs, [l for l in lines] + [c for c, _ in conics], rng); Q = frame_of(pole, rng)
    X = rng.normal(size=(100000, 4)); X /= np.linalg.norm(X, axis=1)[:, None]
    gv = Gs(X.T); near = X[np.abs(gv) < 0.01*np.abs(gv).max()]
    rad = np.linalg.norm(stereo(Q, near), axis=1); Rmax = np.quantile(rad, 0.999); Lb = 1.08*Rmax
    v, f = surface_mesh(Gs, Q, Lb, N)
    sc = 1.0/Rmax                                # consistent framing: surface scaled to unit radius
    pm = pv.PolyData(v*sc, np.hstack([np.full((len(f), 1), 3), f]).ravel())
    pl = pv.Plotter(off_screen=True, window_size=(size, size)); pl.set_background(BG)
    pl.add_mesh(pm, color=SURF, opacity=0.33, smooth_shading=True, specular=0.4, specular_power=20)
    lim = Lb*sc*0.995
    for l in lines:
        add_curve(pl, np.vstack([stereo(Q, l)])*sc, LINE, 0.006, lim)
    for c, kind in conics:
        add_curve(pl, stereo(Q, c)*sc, RES if kind == 'res' else PAIR, 0.0030, lim)
        add_curve(pl, stereo(Q, -c)*sc, RES if kind == 'res' else PAIR, 0.0030, lim)
    R_ = 3.4; pl.camera_position = [(R_, R_*0.6, R_*0.5), (0, 0, 0), (0, 0, 1)]
    s = con['summary'][rep]; nreal_con = s['real_res'] + s['real_cpp']
    lab = f"Y56 real form {rep}{' (standard)' if rep == 'g00' else ''}: {len(lines)} real lines, {nreal_con} real conic ovals, {TOPO[rep]}"
    pl.add_text(lab, position="upper_left", font_size=12, color=TXT)
    pl.add_text("EXPLORATORY render | S^3 double-cover model, stereographic | green lines, amber/violet conics", position="lower_left", font_size=9, color=TXT)
    fn = fname or OUT + f'y56_face_{rep}.png'
    pl.screenshot(fn); pl.close(); print('wrote', fn, 'lines', len(lines), 'conic ovals', len(conics), flush=True)
    return fn
def contact():
    from PIL import Image, ImageDraw
    ims = [Image.open(OUT + f'y56_face_{r}.png').convert('RGB').resize((900, 900)) for r in ORDER]
    sheet = Image.new('RGB', (2700, 1860), BG); dr = ImageDraw.Draw(sheet)
    for k, im in enumerate(ims): sheet.paste(im, ((k % 3)*900, 60 + (k//3)*900))
    try:
        from PIL import ImageFont; fnt = ImageFont.truetype('arial.ttf', 30)
    except Exception: fnt = None
    dr.text((20, 15), "Y56: one complex surface, six real faces (lines 56 / 12 / 8 / 4 / 0 / 0)  |  EXPLORATORY renders", fill=TXT, font=fnt)
    sheet.save(OUT + 'y56_six_faces.png'); print('wrote contact sheet')
def anim(nf=40, N=150, size=760):
    import imageio.v2 as imageio
    A = np.eye(4, dtype=complex)
    def Rt(t):   # screw: w = z0 + i z3 -> e^{it} w ; p = z1 + i z2 -> e^{2it} p   (real 4x4 rotation)
        c, s, c2, s2 = np.cos(t), np.sin(t), np.cos(2*t), np.sin(2*t)
        R = np.zeros((4, 4)); R[0, 0] = c; R[0, 3] = -s; R[3, 0] = s; R[3, 3] = c
        R[1, 1] = c2; R[1, 2] = -s2; R[2, 1] = s2; R[2, 2] = c2
        return R
    T = np.linspace(0, np.pi/4, nf, endpoint=False)
    # check: at t = pi/4 F o R^-1 = -F (exact symmetry g04 up to sign)
    X = np.random.default_rng(0).normal(size=(4, 1000))
    print('F(R_{pi/4}^-1 x) + F(x) max:', np.abs(F(Rt(np.pi/4).T @ X) + F(X)).max())
    rng = np.random.default_rng(11)
    C = rng.normal(size=(30000, 4)); C /= np.linalg.norm(C, axis=1)[:, None]
    sc = np.min([np.abs(F(Rt(t).T @ C.T)) for t in np.linspace(0, np.pi/4, 12)], axis=0)
    lines0 = []
    tt = np.linspace(0, 2*np.pi, 1500)
    for a, b in Lx:
        Qb = np.linalg.qr(np.column_stack([a, b]))[0]; lines0.append((np.outer(Qb[:, 0], np.cos(tt)) + np.outer(Qb[:, 1], np.sin(tt))).T)
    allp = np.vstack(lines0)[::60]
    dl = np.min([np.min(1 - ((C @ Rt(t)) @ allp.T)**2, axis=1) for t in np.linspace(0, np.pi/4, 6)], axis=0)
    pole = C[np.argmax(np.minimum(sc/sc.max(), 3*dl))]; Q = frame_of(pole, rng)
    Lb = 3.2; frames = []
    for k, t in enumerate(T):
        R = Rt(t); Gs = lambda Xt, R=R: F(R.T @ Xt)
        v, f = surface_mesh(Gs, Q, Lb, N)
        keep = (np.linalg.norm(v, axis=1) < Lb*0.97)[f].all(axis=1); f = f[keep]
        pl = pv.Plotter(off_screen=True, window_size=(size, size)); pl.set_background(BG)
        pl.add_mesh(pv.PolyData(v, np.hstack([np.full((len(f), 1), 3), f]).ravel()), color=SURF, opacity=0.33, smooth_shading=True, specular=0.4, specular_power=20)
        for l in lines0: add_curve(pl, stereo(Q, l @ R.T), LINE, 0.012, Lb*0.97)
        R_ = Lb*3.0; pl.camera_position = [(R_, R_*0.6, R_*0.5), (0, 0, 0), (0, 0, 1)]
        pl.add_text("Y56 (standard real form) along its screw symmetry (w,p) -> (e^{it} w, e^{2it} p), t = %.1f of 45 deg | EXPLORATORY" % np.degrees(t), position="upper_left", font_size=9, color=TXT)
        pl.screenshot(OUT + '_frame.png'); pl.close(); frames.append(imageio.imread(OUT + '_frame.png')); print('frame', k, flush=True)
    imageio.mimsave(OUT + 'y56_screw.gif', frames, duration=0.09, loop=0)
    try: imageio.mimsave(OUT + 'y56_screw.mp4', frames, fps=12)
    except Exception as e: print('mp4 skipped', e)
    print('anim ok')
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'six':
        for r in (sys.argv[2:] or ORDER): portrait(r)
    elif mode == 'contact': contact()
    elif mode == 'anim': anim(int(sys.argv[2]), int(sys.argv[3]))
