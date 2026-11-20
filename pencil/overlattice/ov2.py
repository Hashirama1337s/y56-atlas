import json, itertools, math
from fractions import Fraction as F
import numpy as np
from flint import fmpz_mat, fmpq_mat, fmpq
d=json.load(open('N19.json')); Gn=d['Gn']; h=d['h']; C=d['C']; r=19
Gq=fmpq_mat(fmpz_mat(Gn)); Gi=Gq.inv()
def fr(t): return F(int(t.p),int(t.q))
Ginv=[[fr(Gi[i,j]) for j in range(r)] for i in range(r)]
def form(x,y,Gm): return sum(x[i]*Gm[i][j]*y[j] for i in range(len(x)) for j in range(len(y)) if x[i] and y[j])
def red(x): return tuple(t-(t.numerator//t.denominator) for t in x)
# discriminant group by closure of columns of Ginv
gens=[red(tuple(Ginv[i][j] for i in range(r))) for j in range(r)]
zero=tuple(F(0) for _ in range(r))
def add(a,b): return red(tuple(x+y for x,y in zip(a,b)))
A={zero}; frontier=[zero]
while frontier:
    nf=[]
    for a in frontier:
        for g in gens:
            c=add(a,g)
            if c not in A: A.add(c); nf.append(c)
    frontier=nf
print('|A|',len(A))
def q(x): return form(x,x,Gn)%2
def b(x,y): return form(x,y,Gn)%1
def order(x):
    k=1; y=x
    while y!=zero: y=add(y,x); k+=1
    return k
from collections import Counter
print('orders',sorted(Counter(order(a) for a in A).items()))
print('q values on A (value: count)',sorted(Counter(q(a) for a in A).items()))
iso=[a for a in A if a!=zero and q(a)==0]
print('isotropic nonzero elements',len(iso))
def gen_sub(gs):
    S={zero}; fr_=[zero]
    while fr_:
        nf=[]
        for a in fr_:
            for g in gs:
                c=add(a,g)
                if c not in S: S.add(c); nf.append(c)
        fr_=nf
    return frozenset(S)
def is_iso(S): return all(q(a)==0 for a in S)
subs={frozenset([zero])}
cur={gen_sub([a]) for a in iso}; cur={S for S in cur if is_iso(S)}
allsubs=set(cur)|subs
while cur:
    new=set()
    for S in cur:
        for a in iso:
            if a in S: continue
            T=gen_sub(list(S)+[a])
            if T not in allsubs and is_iso(T): new.add(T)
    allsubs|=new; cur=new
allsubs=sorted(allsubs,key=len)
print('isotropic subgroups (incl trivial):',len(allsubs),Counter(len(S) for S in allsubs))
# overlattice machinery
def basis_of(S):
    gl=[a for a in S if a!=zero]
    D=1
    for a in gl:
        for t in a: D=D*t.denominator//math.gcd(D,t.denominator)
    rows=[[D if i==j else 0 for j in range(r)] for i in range(r)]+[[int(t*D) for t in a] for a in gl]
    H=fmpz_mat(rows).hnf()
    B=[[F(int(H[i,j]),D) for j in range(r)] for i in range(H.nrows()) if any(int(H[i,j]) for j in range(r))]
    assert len(B)==r
    return B
def enum(B, bound):
    # vectors v=sum n_i B_i in M with Qp(v) = -v^2 + (v.h)^2/2 <= bound ; return list of (coords in N-basis (Fractions), v2, deg)
    Gm=[[form(B[i],B[j],Gn) for j in range(r)] for i in range(r)]
    hd=[form(B[i],h,Gn) for i in range(r)]
    Qp=[[-Gm[i][j]+hd[i]*hd[j]/2 for j in range(r)] for i in range(r)]
    den=1
    for row in Qp:
        for t in row: den=den*t.denominator//math.gcd(den,t.denominator)
    Qi=fmpz_mat([[int(t*den) for t in row] for row in Qp])
    Qred,T=Qi.lll(rep='gram',transform=True) if False else (None,None)
    try:
        Qred,T=Qi.lll(rep='gram',transform=True)
    except TypeError:
        raise
    T=[[int(T[i,j]) for j in range(r)] for i in range(r)]
    Qf=np.array([[float(Qred[i,j])/den for j in range(r)] for i in range(r)])
    L=np.linalg.cholesky(Qf)  # Qf = L L^T
    # Fincke-Pohst: x^T Q x with upper-tri R = L^T
    R=L.T; res=[]
    x=[0]*r; bnd=bound+1e-6
    def rec(k,rem):
        if k<0:
            res.append(tuple(x)); return
        s=sum(R[k][j]*x[j] for j in range(k+1,r))
        rad=math.sqrt(max(rem,0))/R[k][k]
        c=-s/R[k][k]
        lo=math.ceil(c-rad-1e-9); hi=math.floor(c+rad+1e-9)
        for v in range(lo,hi+1):
            x[k]=v
            t=(R[k][k]*v+s)**2
            if t<=rem+1e-9: rec(k-1,rem-t)
        x[k]=0
    rec(r-1,bnd)
    out=[]
    for xv in res:
        if not any(xv): continue
        n=[sum(xv[i]*T[i][j] for i in range(r)) for j in range(r)]  # coefficients wrt B (T rows = new basis in old)
        co=[sum(n[i]*B[i][j] for i in range(r)) for j in range(r)]
        v2=form(co,co,Gn); dg=form(co,h,Gn)
        if -v2+dg*dg/2<=bound: out.append((tuple(co),v2,dg))
    return out
def inN(co): return all(t.denominator==1 for t in co)
results=[]
for S in allsubs:
    B=basis_of(S); 
    vs=enum(B,F(5,2))
    # classify
    roots0=[(c,v2,dg) for c,v2,dg in vs if v2==-2 and dg==0]
    e1=[(c,v2,dg) for c,v2,dg in vs if v2==0 and dg in (1,-1)]
    e2=[(c,v2,dg) for c,v2,dg in vs if v2==0 and dg in (2,-2)]
    l1=[(c,v2,dg) for c,v2,dg in vs if v2==-2 and dg==1]
    c2=[(c,v2,dg) for c,v2,dg in vs if v2==-2 and dg==2]
    newl1=[x for x in l1 if not inN(x[0])]
    # discriminant length of M: |disc|=128/|S|^2 ; compute via Gram of B
    Gm=fmpz_mat([[int(form(B[i],B[j],Gn)) if form(B[i],B[j],Gn).denominator==1 else 0 for j in range(r)] for i in range(r)])
    even=all(form(B[i],B[i],Gn).denominator==1 and form(B[i],B[i],Gn)%2==0 for i in range(r)) and all(form(B[i],B[j],Gn).denominator==1 for i in range(r) for j in range(r))
    snf=[int(t) for t in Gm.snf().entries() if int(t) not in (0,1,-1)] if even else None
    rec=dict(order=len(S),even=even,det=int(Gm.det()) if even else None,snf=snf,
      roots_h0=len(roots0),roots_h0_new=len([x for x in roots0 if not inN(x[0])]),
      e_deg1=len(e1),e_deg2=len(e2),deg1_m2=len(l1),deg1_m2_new=len(newl1),deg2_m2=len(c2),
      witness_root=[str(t) for t in roots0[0][0]] if roots0 else None,
      witness_e=[str(t) for t in (e1+e2)[0][0]] if (e1 or e2) else None, witness_e_data=((e1+e2)[0][1:] if (e1 or e2) else None),
      witness_newline=[str(t) for t in newl1[0][0]] if newl1 else None,
      glue=[[str(t) for t in a] for a in sorted(S) if a!=zero][:8])
    print({k:v for k,v in rec.items() if not k.startswith('witness') and k!='glue'},flush=True)
    results.append(rec)
json.dump(results,open('overlattice_results.json','w'),indent=1,default=str)
