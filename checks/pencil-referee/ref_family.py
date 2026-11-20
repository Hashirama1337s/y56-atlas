# Referee: (iii) identify family lines at s0=3*2^(-1/4) with lines_exact indices; (vi) conic norm; (vii) real counts.
import sympy as sp, mpmath as mp, itertools
mp.mp.dps=50
D0='../../core/data/'
lines=[]
for ln in open(D0+'lines_exact.txt'):
    if not ln.startswith('L'): continue
    a,b=ln.split(':',1)[1].split('|')
    lines.append([[mp.mpf(sp.N(sp.sympify(t),60)) for t in eval(a)],[mp.mpf(sp.N(sp.sympify(t),60)) for t in eval(b)]])
def pl(P,Q):
    v=[P[i]*Q[j]-P[j]*Q[i] for i,j in itertools.combinations(range(4),2)]
    k=max(range(6),key=lambda t:abs(v[t])); return [x/v[k] for x in v]
PL=[pl(*L) for L in lines]
def pdist(p,q):  # projective distance: all 2x2 minors of [p;q] (tie-safe)
    return max(abs(p[i]*q[j]-p[j]*q[i]) for i in range(6) for j in range(6))
s0=3*mp.mpf(2)**(-0.25); c=mp.mpf(2)**(mp.mpf(1)/8)
def ident(A,B,C,D):
    # family line z1=A z0+B z3, z2=C z0+D z3 ; Y56 coords y=c*z for indices 1,2
    P=[1,c*A,c*C,0]; Q=[0,c*B,c*D,1]; p=pl(P,Q)
    best=min(range(56),key=lambda k: pdist(p,PL[k]))
    return best,pdist(p,PL[best])
s=s0
fam=[]
# generic components (from report; verified below to lie on G_s)
f1=lambda D:4*D**8-8*s*D**6+5*s**2*D**4-s**3*D**2+1
f2=lambda D:D**8-4*s*D**6+5*s**2*D**4-2*s**3*D**2+4
r1=mp.polyroots([4,0,-8*s,0,5*s**2,0,-s**3,0,1],maxsteps=200,extraprec=200)
r2=mp.polyroots([1,0,-4*s,0,5*s**2,0,-2*s**3,0,4],maxsteps=200,extraprec=200)
for D in r1:
    A=-(2*D**5-3*s*D**3+s**2*D); fam.append(('C1',A,A,-D,D)); fam.append(('C2',A,-A,D,D))
for C in r2: fam.append(('C3',0,-(C**5-3*s*C**3+2*s**2*C)/2,C,0))
for D in r2: fam.append(('C4',(D**5-3*s*D**3+2*s**2*D)/2,0,0,D))
# residual (special) components at s0: from own solution of the mixed shapes: s=3/2(C^2+D^2)
for C in mp.polyroots([1,0,0,0,0,0,0,0,-8],extraprec=100):
    if abs(1.5*C**2-s)<1e-30:
        for sg in (1,-1): fam.append(('R1/2',sg*C**5/4,C**5/4,C,0))
        for sg in (1,-1): fam.append(('R7/8',None,None,None,None))
for D in mp.polyroots([2,0,0,0,0,0,0,0,-1],extraprec=100):
    if abs(3*D**2-s)<1e-30:
        fam += [('R3',2*D**5,0,D,D),('R4',0,-2*D**5,D,D),('R5',2*D**5,0,-D,D),('R6',0,2*D**5,-D,D)]
fam=[f for f in fam if f[1] is not None]
# residual comps 7/8 (C=0, D^8=8): A=-D^5/4,B=D^5/4 and A=B=-D^5/4
for D in mp.polyroots([1,0,0,0,0,0,0,0,-8],extraprec=100):
    if abs(1.5*D**2-s)<1e-30: fam += [('R7',-D**5/4,D**5/4,0,D),('R8',-D**5/4,-D**5/4,0,D)]
# check each on G_s numerically
x,y=sp.symbols('x y')
def onG(A,B,C,D):
    z0,z3=mp.mpf(0.3),mp.mpf(-0.7); vals=[]
    for (u,w) in [(1,0),(0,1),(0.3,-0.7),(1.1,0.4),(-0.6,2.2)]:
        z0,z3=mp.mpf(u),mp.mpf(w); z1=A*z0+B*z3; z2=C*z0+D*z3
        vals.append(abs(4*z0**3*z3-4*z0*z3**3+2*z1*z2*(s*(z0**2+z3**2)-(z1**2+z2**2))))
    return max(vals)
gen=[f for f in fam if f[0].startswith('C')]; res=[f for f in fam if f[0].startswith('R')]
print('generic graph lines',len(gen),' residual',len(res))
print('max |G| on generic',mp.nstr(max(onG(*f[1:]) for f in gen),3),' on residual',mp.nstr(max(onG(*f[1:]) for f in res),3))
ig=[ident(*f[1:]) for f in gen]; ir=[ident(*f[1:]) for f in res]
print('generic -> indices distinct',len(set(i for i,_ in ig)),' max err',mp.nstr(max(e for _,e in ig),3))
print('residual -> indices',sorted(set(i for i,_ in ir)),' max err',mp.nstr(max(e for _,e in ir),3))
# meet lines: z2=0 & z3 in {0,z0,-z0} etc. -> Plucker in Y56 coords (scaling irrelevant for coordinate planes)
meetL=[([0,1,0,0],[1,0,0,t]) for t in (0,1,-1)]+[([0,0,1,0],[1,0,0,t]) for t in (0,1,-1)]+[([0,1,0,0],[0,0,0,1]),([0,0,1,0],[0,0,0,1])]
im=[]
for P,Q in meetL:
    p=pl([mp.mpf(t) for t in P],[mp.mpf(t) for t in Q]); k=min(range(56),key=lambda k:pdist(p,PL[k])); im.append((k,pdist(p,PL[k])))
print('meet lines -> ',[k for k,_ in im],' max err',mp.nstr(max(e for _,e in im),3))
SP=[0,6,10,11,12,19,29,33,35,36,42,44,48,50,54,55]
allp=set(i for i,_ in ig)|set(k for k,_ in im)
print('persistent 40 == complement of listed 16:', sorted(allp)==[i for i in range(56) if i not in SP], len(allp))
print('residual set == listed 16:', sorted(set(i for i,_ in ir))==SP)
# (vi) conic norm, own derivation
S,D,z0,z1,z3=sp.symbols('s D z0 z1 z3')
z2=D*(z3-z0)
Gp=sp.expand(4*z0**3*z3-4*z0*z3**3+2*z1*z2*(S*(z0**2+z3**2)-(z1**2+z2**2)))
cub=sp.cancel(Gp/(z3-z0)); A=-(2*D**5-3*S*D**3+S**2*D)
F1=4*D**8-8*S*D**6+5*S**2*D**4-S**3*D**2+1
q,rm=sp.div(sp.Poly(cub,z1), sp.Poly(z1-A*(z0+z3),z1))
rm=sp.rem(sp.expand(rm.as_expr()),F1,D)
print('remainder of cubic / (z1-A(z0+z3)) mod f1 (should be 0):',sp.simplify(rm)==0)
con=sp.expand(q.as_expr())
H=sp.hessian(con,(z0,z1,z3))/2
det=sp.expand(H.det()); det=sp.rem(det,F1,D)
N=sp.factor(sp.resultant(F1,det,D)/sp.LC(sp.Poly(F1,D))**sp.degree(det,D))
print('Norm_{f1}(det conic) =',N)
# (vii) Sturm real-root counts (exact)
def nreal(p): return len(sp.real_roots(sp.Poly(p,D)))
for sv in [sp.Rational(-9,4),-2,sp.Rational(-1,2),0,sp.Rational(3,2),2,sp.Rational(21,10),sp.Rational(11,4),5]:
    a=nreal(F1.subs(S,sv)); b=nreal((D**8-4*S*D**6+5*S**2*D**4-2*S**3*D**2+4).subs(S,sv))
    da=len(set(sp.real_roots(sp.Poly(F1.subs(S,sv),D)))); db=len(set(sp.real_roots(sp.Poly((D**8-4*S*D**6+5*S**2*D**4-2*S**3*D**2+4).subs(S,sv),D))))
    print('s=',sv,' real roots f1,f2 (with mult)',a,b,' distinct',da,db,' => real lines',8+2*da+2*db)
dl=sp.symbols('delta')
q4=lambda X: X**4-4*S*X**3+5*S**2*X**2-2*S**3*X+4
print('q(s-delta) =',sp.expand(q4(S-dl)))
