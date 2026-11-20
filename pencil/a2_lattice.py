# EXACT: lattice of the 40 first-order-unobstructed lines vs full 56-line lattice of Y56
import json, sympy as sp
from sympy.matrices.normalforms import smith_normal_form
edges=json.load(open('../core/data/edges.json')); d=json.load(open('a1_firstorder.json'))
ob=d['obstructed']; keep=[i for i in range(56) if i not in ob]
n=56; G=sp.zeros(n,n)
for i in range(n): G[i,i]=-2
for i,j in edges: G[i,j]=G[j,i]=1
def zbasis(rows):
    # Hermite normal form basis of integer row lattice
    M=sp.Matrix(rows); 
    from sympy.matrices.normalforms import hermite_normal_form
    H=hermite_normal_form(M.T).T
    return H
def lat(idx,name):
    # lattice = Z-span of lines idx modulo radical of the 56-form; realise via pairing vectors against all 56 lines
    rows=[list(G[i,:]) for i in idx]
    Mr=sp.Matrix(rows); rk=Mr.rank()
    # Z-basis: integer row reduce
    R=[[int(t) for t in r] for r in rows]; basis=[]; comb=[[int(k==t) for k in range(len(idx))] for t in range(len(idx))]
    R=[r+c for r,c in zip(R,comb)]
    m=n
    for col in range(m):
        while True:
            nz=[r for r in R if r[col]!=0]
            if len(nz)<=1: break
            nz.sort(key=lambda r:abs(r[col])); p=nz[0]
            for r in nz[1:]:
                q=r[col]//p[col]
                for k in range(len(r)): r[k]-=q*p[k]
        nz=[r for r in R if r[col]!=0]
        if nz: basis.append(nz[0]); R.remove(nz[0])
    C=sp.Matrix([b[m:] for b in basis])  # coefficients on idx lines
    Gi=G.extract(idx,idx); Gram=C*Gi*C.T
    print(name,': rank',rk,' basis size',len(basis),' det',Gram.det(),' smith',[t for t in smith_normal_form(Gram,domain=sp.ZZ).diagonal() if abs(t)!=1])
    ev=Gram.eigenvals(); 
    return C,Gram,basis
C56,G56,B56=lat(list(range(56)),'56 lines')
C40,G40,B40=lat(keep,'40 persistent lines')
C16,G16,B16=lat(ob,'16 special lines')
for k,o in enumerate(d['orbits']):
    lat(o,'orbit %d (size %d)'%(k,len(o)))
lat(d['orbits'][2]+d['orbits'][1],'8+orbit1'); lat(d['orbits'][2]+d['orbits'][3],'8+orbit3')
# signature of G40
import numpy as np
ev=np.linalg.eigvalsh(np.array(G40.tolist(),float)); print('G40 signature +',int((ev>1e-9).sum()),'-',int((ev<-1e-9).sum()))
# h = sum of 4 coplanar lines (complete graph K4 among mutually meeting lines in a plane): pairing vector all ones
ones=sp.ones(1,56)
# is h (pairing vector all ones) in Z-span of 40-line pairing vectors?
P40=sp.Matrix([b[:56] for b in B40]); 
sol=sp.linsolve((P40.T,ones.T)); print('h in 40-lattice coords:',sol)
# primitive closure index of 40-lattice in 56-lattice: pairing-vector lattices
P56=sp.Matrix([b[:56] for b in B56])
# express P40 rows in P56 basis
X=(P56.T).gauss_jordan_solve(P40.T)[0].T  # 19 x 20 integer
assert all(sp.denom(t)==1 for t in X)
sn=smith_normal_form(X,domain=sp.ZZ); print('Smith of inclusion 40-lattice -> 56-lattice:',[sn[i,i] for i in range(min(sn.shape))])
# orthogonal complement of 40-lattice in 56-lattice: v in Z^20 coords with X*G56*v=0
K=(X*G56).nullspace(); v=K[0]; v=v*sp.ilcm(*[sp.denom(t) for t in v]); g=sp.igcd(*[int(t) for t in v]); v=v/g
print('complement dim',len(K),' v.v =',(v.T*G56*v)[0])
# v as combination of lines: coordinates in 56-line pairing: pairing vector of v with all lines
pv=(v.T*P56); print('v . L_i for i=0..55:',list(pv))
print('v.h =', sum(pv[i] for i in [2,14,22,24] )," (sum over 4 lines; see planes)")
# v in terms of lines: v = sum c_i L_i ; C56 gives basis in line coords
vl=(v.T*C56); print('v as line combination (nonzero):',{i:vl[i] for i in range(56) if vl[i]!=0})
json.dump(dict(v_pair=[int(t) for t in pv],vv=int((v.T*G56*v)[0])),open('a2_lattice.json','w'))
