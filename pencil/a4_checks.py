# Checks on the explicit generic lines. Parts: (a) EXACT identities; (b) EXACT Sturm real-root counts; (c) EXACT conic degeneration; (d) NUMERICAL (40-digit) incidence Gram at sample s
import sympy as sp, mpmath as mp, itertools
from sympy.matrices.normalforms import smith_normal_form
s,D,y,dl=sp.symbols('s D y delta'); z0,z1,z2,z3=sp.symbols('z0:4')
G=4*z0**3*z3-4*z0*z3**3+2*z1*z2*(s*(z0**2+z3**2)-(z1**2+z2**2))
f1=4*D**8-8*s*D**6+5*s**2*D**4-s**3*D**2+1; f2=D**8-4*s*D**6+5*s**2*D**4-2*s**3*D**2+4
q=y**4-4*s*y**3+5*s**2*y**2-2*s**3*y+4
print('(a) f2(D)=q(D^2):',sp.expand(f2-q.subs(y,D**2))==0,'; 4 f1(D)=q(2D^2):',sp.expand(4*f1-q.subs(y,2*D**2))==0,'; q(s-delta)=',sp.factor(sp.expand(q.subs(y,s-dl))))
E=-(2*D**5-3*s*D**3+s**2*D); H=(D**5-3*s*D**3+2*s**2*D)/2
comps={'C1':(E,E,-D,D,f1),'C2':(E,-E,D,D,f1),'C4':(H,0,0,D,f2)}
for nm,(A,B,C,Dv,f) in comps.items():
    r=sp.expand(G.subs({z1:A*z0+B*z3,z2:C*z0+Dv*z3}))
    ok=all(sp.rem(sp.Poly(c,D),sp.Poly(f,D)).is_zero for c in sp.Poly(r,z0,z3).coeffs())
    print('(a) component',nm,'lies on G_s for all s (remainder mod f = 0):',ok)
A=-H.subs(D,sp.Symbol('C'))  # C3: B = -(C^5-3sC^3+2s^2C)/2, A=D=0
Cs=sp.Symbol('C'); r=sp.expand(G.subs({z1:(-(Cs**5-3*s*Cs**3+2*s**2*Cs)/2)*z3,z2:Cs*z0}))
print('(a) component C3 lies on G_s:',all(sp.rem(sp.Poly(c,Cs),sp.Poly(f2.subs(D,Cs),Cs)).is_zero for c in sp.Poly(r,z0,z3).coeffs()))
print('(b) real roots of f1,f2 (each gives 2 components x that many real lines):')
for sv in [sp.Rational(-7),-3,sp.Rational(-5,2),-1,0,1,sp.Rational(19,10),sp.Rational(201,100),sp.Rational(9,4),sp.Rational(5,2),sp.Rational(25227,10000),sp.Rational(25228,10000),sp.Rational(13,5),3,7]:
    n1=sp.Poly(f1.subs(s,sv),D).count_roots(); n2=sp.Poly(f2.subs(s,sv),D).count_roots()
    print('   s =',sv,' kappa=-s^2=',float(-sv**2),' real roots f1,f2:',n1,n2,' => real lines 8 +',2*n1+2*n2,'=',8+2*n1+2*n2)
# (c) plane z2 = D (z3 - z0) through the C1 line z1 = E (z0+z3) and the persistent line z0=z3,z2=0
K=sp.expand(G.subs(z2,D*(z3-z0))/(z3-z0)) if False else sp.cancel(sp.expand(G.subs(z2,D*(z3-z0)))/(z3-z0))
K=sp.expand(K); Q,R=sp.div(sp.Poly(K,z1),sp.Poly(z1-E*(z0+z3),z1))
print('(c) cubic = (z1 - E(z0+z3)) * conic, remainder mod f1 zero:',all(sp.rem(sp.Poly(c,D),sp.Poly(f1,D)).is_zero for c in sp.Poly(R.as_expr(),z0,z3).coeffs()))
Qe=Q.as_expr(); X=[z0,z3,z1]; Mq=sp.Matrix(3,3,lambda i,j: sp.diff(Qe,X[i],X[j])/2)
det=sp.rem(sp.Poly(sp.expand(Mq.det()),D),sp.Poly(f1,D))
res=sp.factor(sp.resultant(det.as_expr(),f1,D)); print('(c) Norm over D of det(conic) =',res)
# (d) numeric Gram
mp.mp.dps=40
def lines_at(sv, extra=None):
    L=[]
    r1=mp.polyroots([4,0,-8*sv,0,5*sv**2,0,-sv**3,0,1],maxsteps=500,extraprec=200); r2=mp.polyroots([1,0,-4*sv,0,5*sv**2,0,-2*sv**3,0,4],maxsteps=500,extraprec=200)
    for d in r1:
        e=-(2*d**5-3*sv*d**3+sv**2*d); L.append(('C1',[[1,e,-d,0],[0,e,d,1]])); L.append(('C2',[[1,e,d,0],[0,-e,d,1]]))
    for d in r2:
        h=(d**5-3*sv*d**3+2*sv**2*d)/2; L.append(('C3',[[1,0,d,0],[0,-h,0,1]])); L.append(('C4',[[1,h,0,0],[0,0,d,1]]))
    for a,b in [(1,0),(0,1),(1,1),(1,-1)]:
        L.append(('P',[[a,0,0,b],[0,0,1,0]])); L.append(('P',[[a,0,0,b],[0,1,0,0]]))
    if extra=='fermat':
        for a,b in [(1,0),(0,1),(1,1),(1,-1)]:
            for e in [1j,-1j]: L.append(('F',[[a,0,0,b],[0,1,e,0]]))
    return L
def det4(M):
    import itertools as it
    tot=mp.mpf(0)
    for perm in it.permutations(range(4)):
        sg=1
        for a in range(4):
            for b in range(a+1,4):
                if perm[a]>perm[b]: sg=-sg
        tot+=sg*M[0][perm[0]]*M[1][perm[1]]*M[2][perm[2]]*M[3][perm[3]]
    return tot
def gram(L):
    n=len(L); Gm=sp.zeros(n,n); mind=mp.mpf(1); maxz=mp.mpf(0)
    for i in range(n):
        Gm[i,i]=-2
        for j in range(i+1,n):
            dt=abs(det4(L[i][1]+L[j][1]))/ (mp.norm(mp.matrix(L[i][1]))*mp.norm(mp.matrix(L[j][1])))**2
            if dt<mp.mpf(10)**-25: Gm[i,j]=Gm[j,i]=1; maxz=max(maxz,dt)
            else: mind=min(mind,dt)
    return Gm,mind,maxz
def inv(Gm):
    rk=Gm.rank(); 
    # Z-basis via integer row reduction, Gram on it
    n=Gm.rows; R=[[int(t) for t in Gm.row(i)]+[int(i==k) for k in range(n)] for i in range(n)]; basis=[]
    for col in range(n):
        while True:
            nz=[r for r in R if r[col]!=0]
            if len(nz)<=1: break
            nz.sort(key=lambda r:abs(r[col])); p=nz[0]
            for r in nz[1:]:
                qq=r[col]//p[col]
                for k in range(len(r)): r[k]-=qq*p[k]
        nz=[r for r in R if r[col]!=0]
        if nz: basis.append(nz[0]); R.remove(nz[0])
    C=sp.Matrix([b[n:] for b in basis]); Gr=C*Gm*C.T
    return rk,Gr.det(),[t for t in smith_normal_form(Gr,domain=sp.ZZ).diagonal() if abs(t)!=1],sorted(sum(1 for j in range(n) if Gm[i,j]==1) for i in range(n))
for sv,ex in [(mp.mpf(5)/2,None),(mp.mpf(13)/5,None),(mp.mpf(3),None),(mp.mpf(1),None),(mp.mpc(0,1)*mp.mpf(7)/3,None),(mp.mpf(0),'fermat')]:
    L=lines_at(sv,ex); Gm,mind,maxz=gram(L); rk,dt,sm,deg=inv(Gm)
    print('(d) s =',mp.nstr(sv,8),' lines',len(L),' rank',rk,' det',dt,' smith',sm,' min nonzero |det|',mp.nstr(mind,3),' max zero',mp.nstr(maxz,3)); print('     valencies',deg)
    if ex=='fermat':
        idx=[i for i in range(len(L)) if L[i][0]!='F']; rk,dt,sm,deg=inv(Gm.extract(idx,idx)); print('     40-sublattice at s=0: rank',rk,'det',dt,'smith',sm)
        fi=[i for i in range(len(L)) if L[i][0]=='F']; print('     the 8 extra lines: mutual incidences',sum(Gm[i,j]==1 for i,j in itertools.combinations(fi,2)),' each meets persistent:',[sum(Gm[i,j]==1 for j in idx) for i in fi])
