import json, itertools, math, sys
from fractions import Fraction as F
import numpy as np
from flint import fmpz_mat, fmpq_mat, fmpq, fmpz
edges=json.load(open('../../core/data/edges.json'))
SPECIAL=[0,6,10,11,12,19,29,33,35,36,42,44,48,50,54,55]
keep=[i for i in range(56) if i not in SPECIAL]; assert len(keep)==40
G56=[[0]*56 for _ in range(56)]
for i in range(56): G56[i][i]=-2
for i,j in edges: G56[i][j]=G56[j][i]=1
G40=[[G56[i][j] for j in keep] for i in keep]
def hnf_basis(Gm, n):
    # rows [Gm | I]; HNF; rows with nonzero left part give basis of Z^n/ker
    A=fmpz_mat([[Gm[i][j] for j in range(n)]+[1 if k==i else 0 for k in range(n)] for i in range(n)])
    H=A.hnf()
    rows=[[int(H[i,j]) for j in range(2*n)] for i in range(n)]
    B=[r[n:] for r in rows if any(r[:n])]
    return B
C=hnf_basis(G40,40); r=len(C); print('rank',r)
def gram(Cc,Gm):
    n=len(Gm); out=[[0]*len(Cc) for _ in Cc]
    for a in range(len(Cc)):
        v=[sum(Cc[a][k]*Gm[k][j] for k in range(n)) for j in range(n)]
        for b in range(len(Cc)): out[a][b]=sum(v[j]*Cc[b][j] for j in range(n))
    return out
Gn=gram(C,G40)
M=fmpz_mat(Gn); print('det',M.det(),'snf',[int(x) for x in M.snf().entries() if abs(int(x))!=1])
ev=np.linalg.eigvalsh(np.array(Gn,float)); print('sig',(ev>1e-9).sum(),(ev<-1e-9).sum())
# h coordinates: h.b_i = sum of coeffs
dvec=[sum(row) for row in C]
Gq=fmpq_mat(M); x=Gq.solve(fmpq_mat(r,1,[fmpq(d) for d in dvec]))
hco=[x[i,0] for i in range(r)]; print('h integral in N:',all(t.q==1 for t in hco)); hco=[int(t.p) for t in hco]
print('h.h',sum(hco[i]*Gn[i][j]*hco[j] for i in range(r) for j in range(r)))
# primitivity in 56-line lattice
C56=hnf_basis(G56,56); print('56 lattice rank',len(C56))
# inclusion: express N basis in 56-lattice basis via pairing vectors vs 56 lines
P56=fmpz_mat([[sum(c[k]*G56[k][j] for k in range(56)) for j in range(56)] for c in C56])
# N basis pairing vectors with 56 lines
PN=fmpz_mat([[sum(sum(Cr[a]*(1 if k==keep[a] else 0) for a in range(40)) *0 for k in range(1)) for j in range(1)] for Cr in C]) if False else None
PN=[]
for Cr in C:
    vec56=[0]*56
    for a in range(40): vec56[keep[a]]=Cr[a]
    PN.append([sum(vec56[k]*G56[k][j] for k in range(56)) for j in range(56)])
# solve X*P56 = PN
P56q=fmpq_mat(P56); 
# least squares via pivot: use Smith of stacked check: lattice of PN rows inside lattice of P56 rows; primitive iff same saturation
from sympy import Matrix
X=Matrix(PN).T.gauss_jordan_solve(Matrix(P56.tolist()).T)  if False else None
# simpler: saturation test. rowspace(PN) primitive in rowspace(P56) iff gcd of 19x19 minors ratio... use snf of coordinates
Pm=Matrix(P56.tolist()); Qm=Matrix(PN)
# coordinates: solve Pm^T y = Q^T columns
sol,params=Pm.T.gauss_jordan_solve(Qm.T); X=sol.T  # 19x20
assert all(t.q==1 for t in X)
Xf=fmpz_mat([[int(t) for t in X.row(i)] for i in range(X.rows)])
print('inclusion N->NS56 snf (nonunit):',[int(t) for t in Xf.snf().entries() if abs(int(t))!=1], 'rank',Xf.rank())
json.dump({'Gn':Gn,'h':hco,'C':C},open('N19.json','w'))
