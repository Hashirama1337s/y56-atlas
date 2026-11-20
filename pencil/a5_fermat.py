# NUMERICAL incidence (40 digits) + EXACT integer lattice algebra: at s=0 (Fermat-type member), the class orthogonal to the 40-line lattice
import mpmath as mp, sympy as sp, itertools
from sympy.matrices.normalforms import smith_normal_form
mp.mp.dps=40
L=[]
for d in mp.polyroots([4,0,0,0,0,0,0,0,1],maxsteps=500,extraprec=200):
    e=-(2*d**5); L.append(('G',[[1,e,-d,0],[0,e,d,1]])); L.append(('G',[[1,e,d,0],[0,-e,d,1]]))
for d in mp.polyroots([1,0,0,0,0,0,0,0,4],maxsteps=500,extraprec=200):
    h=d**5/2; L.append(('G',[[1,0,d,0],[0,-h,0,1]])); L.append(('G',[[1,h,0,0],[0,0,d,1]]))
for a,b in [(1,0),(0,1),(1,1),(1,-1)]:
    L.append(('G',[[a,0,0,b],[0,0,1,0]])); L.append(('G',[[a,0,0,b],[0,1,0,0]]))
    for e in [1j,-1j]: L.append(('F',[[a,0,0,b],[0,1,e,0]]))
def det4(M):
    tot=mp.mpf(0)
    for perm in itertools.permutations(range(4)):
        sg=1
        for a in range(4):
            for b in range(a+1,4):
                if perm[a]>perm[b]: sg=-sg
        tot+=sg*M[0][perm[0]]*M[1][perm[1]]*M[2][perm[2]]*M[3][perm[3]]
    return tot
n=len(L); G=sp.zeros(n,n)
for i in range(n):
    G[i,i]=-2
    for j in range(i+1,n):
        if abs(det4(L[i][1]+L[j][1]))<mp.mpf(10)**-25: G[i,j]=G[j,i]=1
gen=[i for i in range(n) if L[i][0]=='G']; ext=[i for i in range(n) if L[i][0]=='F']
# rational vector x on lines with G x pairing zero against the 40: work in Q-span modulo radical. Solve for c (48) with (G c)[gen]=0, modulo kernel of G
K=G.extract(gen,list(range(n))).nullspace(); R=G.nullspace()
# pick a null vector not in radical of G
cand=[k for k in K if (G*k)!=sp.zeros(n,1)]
k=cand[0]; pv=G*k; den=sp.ilcm(*[sp.denom(t) for t in pv]); pv=pv*den; g=sp.igcd(*[int(t) for t in pv]); pv=pv/g; k=k*den/g
print('pairing of orthogonal class with the 8 extra lines:',[pv[i] for i in ext],' with the 40:',set(pv[i] for i in gen))
print('self-intersection of this (line-pairing-primitive) class:',(k.T*G*k)[0])
print('extra-line incidence among the 8:',[[G[i,j] for j in ext] for i in ext])
