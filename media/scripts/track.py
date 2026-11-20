# EXPLORATORY: track real lines of F(1,b,-1), b=sqrt(kappa), from Y56 (kappa 6.364) to b=0; NUMERICAL
import numpy as np, sys

def Ffun(z,b):
    z0,z1,z2,z3=z[...,0],z[...,1],z[...,2],z[...,3]
    return 4*z0**3*z3-4*z0*z3**3+2*z1*z2*(b*(z0**2+z3**2)-(z1**2+z2**2))
TH=np.arange(8)*np.pi/8
def resid(B,b):  # B (n,2,4)
    c=np.cos(TH)[None,:,None]; s=np.sin(TH)[None,:,None]
    pts=c*B[:,None,0,:]+s*B[:,None,1,:]
    return Ffun(pts,b)
def orth(B):
    q=np.linalg.qr(np.transpose(B,(0,2,1)))[0]; return np.transpose(q,(0,2,1))
def refine(B,b,iters=80):
    B=orth(B); lam=np.full(len(B),1e-3)
    r=resid(B,b); f=(r**2).sum(1)
    for it in range(iters):
        J=np.zeros((len(B),8,8)); h=1e-7
        for k in range(8):
            d=np.zeros(8); d[k]=h; Bp=B+d.reshape(2,4)[None]
            J[:,:,k]=(resid(Bp,b)-r)/h
        A=np.einsum('nri,nrj->nij',J,J); g=np.einsum('nri,nr->ni',J,r)
        A=A+lam[:,None,None]*np.eye(8)[None]*(1+np.einsum('nii->n',A)[:,None,None]/8)
        dl=-np.linalg.solve(A,g[:,:,None])[:,:,0]
        Bn=orth(B+dl.reshape(-1,2,4)); rn=resid(Bn,b); fn=(rn**2).sum(1)
        ok=fn<f
        B=np.where(ok[:,None,None],Bn,B); r=np.where(ok[:,None],rn,r); f=np.where(ok,fn,f)
        lam=np.where(ok,lam*0.3,lam*5); lam=np.clip(lam,1e-14,1e8)
    return B,np.sqrt(f)
def proj(B): return np.einsum('nia,nib->nab',B,B)
def dedupe(B,res,tol=2e-3):
    keep=[]; P=proj(B)
    for i in np.argsort(res):
        if all(np.linalg.norm(P[i]-P[j])>tol for j in keep): keep.append(i)
    return np.array(keep,int)
if __name__=="__main__":
    Bs=np.load('lines56_basis.npy'); mu=2**0.25
    B0=Bs.copy(); B0[:,:,1:3]/=mu; B0=orth(B0)
    kap=np.concatenate([np.linspace(2**-0.5*0+9/2**0.5,4,15)[:-1],np.full(6,4.0),np.linspace(4,0,29)[1:]])
    print(len(kap))
    rng=np.random.default_rng(1); cur=B0.copy(); alive=np.ones(56,bool)
    out=dict(kappa=kap); counts=[]; tr=[];fr=[]
    P0=None
    for fi,k in enumerate(kap):
        b=np.sqrt(k)
        cur,res=refine(cur,b,60)
        tol=1e-6 if abs(k-4)>1e-9 else 1e-5
        good=res<tol
        # fresh search
        S=orth(rng.normal(size=(500,2,4))); S,rs=refine(S,b,70)
        gs=rs<tol; S=S[gs]; rs=rs[gs]
        allB=np.concatenate([cur[good],S]); allr=np.concatenate([res[good],rs])
        tag=np.concatenate([np.ones(good.sum()),np.zeros(len(S))])
        keep=dedupe(allB,allr-1e-3*tag)  # prefer tracked
        n=len(keep); ntr=int(tag[keep].sum())
        print(fi,round(k,3),"distinct real lines",n,"tracked-from-Y56",ntr,"fresh-only",n-ntr,"tracked alive",int(good.sum()),flush=True)
        counts.append(n); tr.append(ntr)
        out[f'L{fi}']=allB[keep]; out[f'T{fi}']=tag[keep]
    out['counts']=np.array(counts); np.savez('lines_track.npz',**out)
