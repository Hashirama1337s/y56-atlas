# EXPLORATORY: Y56 -> wall -> Fermat-type morph, stereographic S^3 sphere model, fixed camera. Family F(1,b,-1), b=sqrt|kappa|.
import numpy as np, pyvista as pv, sys, os
from skimage.measure import marching_cubes, find_contours
from PIL import Image, ImageDraw, ImageFont
from track import Ffun, orth
D=''
BG="#0b0d12"; L=3.0
Bs=np.load('lines56_basis.npy'); mu=2**0.25
B0=Bs.copy(); B0[:,:,1:3]/=mu; B0=orth(B0)
def rot_to(v):
    v=v/np.linalg.norm(v); M=np.linalg.qr(np.column_stack([v,np.random.default_rng(0).normal(size=(4,3))]))[0]
    if M[:,0]@v<0: M[:,0]*=-1
    return M
rng=np.random.default_rng(3); cand=rng.normal(size=(20000,4)); cand/=np.linalg.norm(cand,axis=1)[:,None]
d=np.min([1-np.sum((cand@B.T)**2,axis=1) for B in B0],axis=0); M=rot_to(cand[np.argmax(d)])
def stereo(z):  # z (...,4) unit -> R^3
    u=z@M; return u[...,1:]/(1-u[...,0:1]+1e-300)
def mesh_for(b,N):
    g=np.linspace(-L,L,N); X,Y,Z=np.meshgrid(g,g,g,indexing='ij'); s=X**2+Y**2+Z**2
    zz=np.stack([(s-1)/(s+1),2*X/(s+1),2*Y/(s+1),2*Z/(s+1)],axis=-1)
    G=Ffun(zz@M.T,b)
    v,f,_,_=marching_cubes(G,0.0,spacing=(g[1]-g[0],)*3); v+=g[0]
    ok=(np.linalg.norm(v,axis=1)<L*0.98)[f].all(axis=1); f=f[ok]
    return pv.PolyData(v,np.hstack([np.full((len(f),1),3),f]).ravel())
def add_curve(pl,x,col,rad,glow=False):
    m=np.linalg.norm(x,axis=1)<L*0.97; idx=np.where(m)[0]
    for rn in np.split(idx,np.where(np.diff(idx)>1)[0]+1):
        if len(rn)<2: continue
        pl.add_mesh(pv.lines_from_points(x[rn]).tube(radius=L*rad,n_sides=6),color=col,smooth_shading=True,ambient=0.8,diffuse=0.5)
t=np.linspace(0,2*np.pi,3000)
def line_curve(B): return stereo(np.outer(np.cos(t),B[0])+np.outer(np.sin(t),B[1]))
def in_coord_plane(B):  # persistent lines: contained in z1=0 or z2=0
    return any(np.abs(B[:,k]).max()<1e-4 for k in (1,2))
# wall nodes (exact closed forms, floats)
tt=2*np.cos(np.pi/8); s=np.sqrt(2); tp=2*np.sin(np.pi/8)
NODES=np.array([(1+s,-tt,tt,1),(1+s,tt,-tt,1),(1-s,tp,-tp,1),(1-s,-tp,tp,1),(-1+s,tp,tp,1),(-1+s,-tp,-tp,1),(-1-s,tt,tt,1),(-1-s,-tt,-tt,1)])
NODES=NODES/np.linalg.norm(NODES,axis=1)[:,None]
def add_nodes(pl):
    for n in NODES:
        for sg in (1,-1):
            p=stereo(sg*n)
            if np.linalg.norm(p)<L*0.95:
                pl.add_mesh(pv.Sphere(radius=L*0.035,center=p),color="#ffe66b",ambient=1.0,diffuse=0.0)
                pl.add_mesh(pv.Sphere(radius=L*0.07,center=p),color="#ffb300",opacity=0.22,ambient=1.0,diffuse=0.0)
def conic_curves():
    # planes z1=-z2 (v=(z0,-z2,z2,z3)) and z1=z2; factor quadrics in (z0,z2,z3)
    out=[]
    facs={-1:[lambda a,c,d:c*c-a*a+a*d, lambda a,c,d:c*c-d*d-a*d], 1:[lambda a,c,d:c*c-a*a-a*d, lambda a,c,d:c*c-d*d+a*d]}
    nu,nv=900,1800; th=np.linspace(0,np.pi,nu); ph=np.linspace(0,2*np.pi,nv)
    TH,PH=np.meshgrid(th,ph,indexing='ij'); A=np.sin(TH)*np.cos(PH); C=np.sin(TH)*np.sin(PH); Dd=np.cos(TH)
    for sg,fl in facs.items():
        for q,f in enumerate(fl):
            for c in find_contours(f(A,C,Dd),0.0):
                th_=np.interp(c[:,0],np.arange(nu),th); ph_=np.interp(c[:,1],np.arange(nv),ph)
                a=np.sin(th_)*np.cos(ph_); cc=np.sin(th_)*np.sin(ph_); dd=np.cos(th_)
                z=np.stack([a,-sg*cc,cc,dd],axis=1) if sg==-1 else np.stack([a,cc,cc,dd],axis=1)
                z/=np.linalg.norm(z,axis=1)[:,None]
                out.append((stereo(z),sg,q))
    return out
def scene(b,lines,tags,size,N,nodes=False,conics=False,title=None,sub=None,lcol=None):
    pl=pv.Plotter(off_screen=True,window_size=(size,size)); pl.set_background(BG)
    pl.add_mesh(mesh_for(b,N),color="#2b9ac9",opacity=0.30,smooth_shading=True,specular=0.4,specular_power=20)
    for i,B in enumerate(lines):
        add_curve(pl,line_curve(B),lcol[i],0.0032)
    if conics:
        for x,sg,q in conic_curves():
            add_curve(pl,x,"#ffd23d" if sg==-1 else "#b36bff",0.0042)
    if nodes: add_nodes(pl)
    R=L*3.0; pl.camera_position=[(R,R*0.6,R*0.5),(0,0,0),(0,0,1)]
    if title: pl.add_text(title,position="upper_left",font_size=int(size/75),color="#e6f1ff")
    if sub: pl.add_text(sub,position="lower_left",font_size=int(size/110),color="#9fb4c8")
    img=pl.screenshot(None,return_img=True); pl.close(); return img
def colors(lines,prev=None,first=False):
    cols=[]
    for i,B in enumerate(lines):
        if in_coord_plane(B): cols.append("#39d6ff")
        elif first and prev is not None:
            P=B.T@B; dist=min(np.linalg.norm(P-C.T@C) for C in prev); cols.append("#ffd23d" if dist>0.05 else "#ff3da8")
        else: cols.append("#ff3da8")
    return cols
if __name__=="__main__":
    mode=sys.argv[1]; T=np.load(D+'lines_track.npz'); kap=T['kappa']
    if mode=="frames":
        os.makedirs(D+'frames',exist_ok=True); done={}
        for fi,k in enumerate(kap):
            key=round(float(k),6)
            if key in done: Image.fromarray(done[key]).save(D+f'frames/f{fi:02d}.png'); continue
            b=np.sqrt(k); lines=T[f'L{fi}']; n=len(lines)
            wall=abs(k-4)<1e-9; y56=fi==0; fer=k<1e-9
            name="Y56 (56 lines)" if y56 else "wall: 8 pinch points" if wall else "Fermat quartic (b = 0 member)" if fer else ("between Y56 and the wall" if k>4 else "between the wall and Fermat")
            cols=colors(lines,T['L1'] if y56 else None,y56)
            title=f"{name}\n|kappa| = {k:.3f}   real lines found: {n}"
            sub="EXPLORATORY  |  line counts NUMERICAL (Newton + fresh search)  |  cyan = 8 lines in z1=0 / z2=0 on every member"+("  |  amber = 16 lines that vanish the moment kappa moves" if y56 else "")
            img=scene(b,lines,None,900,150,nodes=wall,title=title,sub=sub,lcol=cols)
            done[key]=img; Image.fromarray(img).save(D+f'frames/f{fi:02d}.png'); print(fi,n,flush=True)
    if mode=="wall":
        fi=14; lines=T[f'L{fi}']; cols=colors(lines)
        img=scene(2.0,[],None,1800,210,nodes=True,conics=True,lcol=[],
          title="Y56 wall: quartic with 8 ordinary nodes (gold)\n4 conics through the nodes: 2 in plane z1=-z2 (amber), 2 in z1=z2 (violet)",
          sub="EXPLORATORY  |  stereographic S^3 model  |  wall member (a,b,c)=(1,2,-1), |kappa|=4   |  each node shows twice (the sphere model double-covers)")
        Image.fromarray(img).save(D+'y56_wall.png')
