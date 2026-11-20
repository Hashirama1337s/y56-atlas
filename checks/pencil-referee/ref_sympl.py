# Referee: which of the 32 block maps act symplectically, on EVERY member G_s; group structure of that subgroup.
import sympy as sp
from sympy import sqrt, Matrix
D0='../../core/data/'
s,z0,z1,z2,z3=sp.symbols('s z0 z1 z2 z3'); Z=Matrix([z0,z1,z2,z3])
Gs=4*z0**3*z3-4*z0*z3**3+2*z1*z2*(s*(z0**2+z3**2)-(z1**2+z2**2))
Ms=[]
for l in open(D0+'symmetry_exact.txt'):
    if not l.startswith('g'): continue
    nm=l.split()[0]; c=sp.sympify(l.split('c=')[1].split()[0]); M=Matrix(sp.sympify(l.split('M=')[1].split(' sigma')[0]))
    # Y56 coords y1,y2 = 2^(1/8) z1,z2: conjugation by a scalar on the (1,2) block leaves block-diagonal M unchanged; assert block form
    blk=all(M[i,j]==0 for i in (0,3) for j in (1,2)) and all(M[i,j]==0 for i in (1,2) for j in (0,3))
    lhs=sp.expand(Gs.subs(dict(zip([z0,z1,z2,z3],list(M*Z))),simultaneous=True)); ok=sp.expand(lhs-c*Gs)==0
    Ms.append((nm,M,c,blk,ok,sp.simplify(M.det()/c)))
print('all block-diagonal:',all(m[3] for m in Ms),' all preserve G_s for every s (with same c):',all(m[4] for m in Ms))
sy=[m for m in Ms if m[5]==1]; print('det(M)/c values:',sorted(set(str(m[5]) for m in Ms)),' symplectic count',len(sy),[m[0] for m in sy])
def porder(M):
    P=M
    for k in range(1,33):
        if all(P[i,j]==0 for i in range(4) for j in range(4) if i!=j) and len(set(P[i,i] for i in range(4)))==1: return k
        P=sp.simplify(P*M)
    return None
from collections import Counter
print('projective element orders, symplectic subgroup:',sorted(Counter(porder(m[1]) for m in sy).items()))
print('projective element orders, all 32:',sorted(Counter(porder(m[1]) for m in Ms).items()))
# abelian?
def eqp(A,B):
    r=[(i,j) for i in range(4) for j in range(4) if B[i,j]!=0][0]; lam=A[r]/B[r]; return sp.simplify(A-lam*B)==sp.zeros(4,4)
ab=all(eqp(a[1]*b[1],b[1]*a[1]) for a in sy for b in sy); print('symplectic subgroup abelian:',ab)
