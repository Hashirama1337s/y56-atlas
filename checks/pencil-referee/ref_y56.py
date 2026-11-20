# Referee checks (iii),(iv),(vi),(vii) from Y56 exact data. Own code.
import sympy as sp, json, itertools, mpmath as mp
from sympy.matrices.normalforms import smith_normal_form
D0='../../core/data/'
r2=sp.sqrt(2)
lines=[]
for ln in open(D0+'lines_exact.txt'):
    if not ln.startswith('L'): continue
    a,b=ln.split(':',1)[1].split('|')
    lines.append(sp.Matrix([[sp.nsimplify(sp.sympify(t)) for t in eval(a)],[sp.sympify(t) for t in eval(b)]]))
print('n lines',len(lines))
z0,y1,y2,z3,lam,mu=sp.symbols('z0 y1 y2 z3 lam mu')
s0=3/sp.root(2,4); c=sp.root(2,8)
# family in Y56 coords with z_i = y_i / c (i=1,2)
Fy=sp.expand(4*z0**3*z3-4*z0*z3**3+2*(y1/c)*(y2/c)*(s0*(z0**2+z3**2)-((y1/c)**2+(y2/c)**2)))
Fy=sp.expand(sp.simplify(Fy)); print('Y56 eq (z1,z2 -> y/2^(1/8)):',Fy)
bad=0
for i,N in enumerate(lines):
    P=lam*N.row(0)+mu*N.row(1)
    val=sp.expand(Fy.subs({z0:P[0],y1:P[1],y2:P[2],z3:P[3]},simultaneous=True))
    if sp.simplify(val)!=0: bad+=1
print('lines not on Y56 equation:',bad)
# incidence recomputed from coordinates
inc=set()
for i,j in itertools.combinations(range(56),2):
    if sp.simplify(sp.Matrix.vstack(lines[i],lines[j]).det())==0: inc.add((i,j))
E=set(tuple(sorted(e)) for e in json.load(open(D0+'edges.json')))
print('incidences recomputed',len(inc),' edges.json',len(E),' equal:',inc==E)
G=lambda i,j: -2 if i==j else (1 if (min(i,j),max(i,j)) in inc else 0)
SP=[0,6,10,11,12,19,29,33,35,36,42,44,48,50,54,55]
P40=[i for i in range(56) if i not in SP]
def lat(idx):
    M=sp.Matrix(len(idx),len(idx),lambda a,b:G(idx[a],idx[b]))
    # integral basis of span via HNF of the Gram rows is not valid; use the lattice spanned by classes:
    # rank = rank of Gram (NS nondegenerate); det of span via Gram of a Z-basis found by LLL-free method below
    return M
def zbasis_gram(idx):
    # lattice spanned by classes e_i in Z^n modulo kernel of Gram; quotient by radical
    M=sp.Matrix(len(idx),len(idx),lambda a,b:G(idx[a],idx[b]))
    r=M.rank()
    # image of Z^n under M (as map to dual) : integral lattice L = Z^n / ker. Gram on L: choose Z-basis of Z^n/ker
    # Z^n/ker is torsion-free of rank r; Z-basis = rows of a unimodular complement. Use Smith: M = U S V
    S=smith_normal_form(M,domain=sp.ZZ)
    return M,r
M56,r56=zbasis_gram(list(range(56)))
print('rank 56-line Gram',r56)
# Robust lattice invariants: L = span of classes = Z^n/ker(M). Disc group of L ~ coker of M restricted. Use: if K=ker basis (integral saturated),
# then pick B = Z-basis of Z^n / K via HNF of K-complement. Simplest: integer row-reduce to find r independent combos that generate.
from sympy import Matrix
def lattice_invariants(idx, extra_h=False):
    n=len(idx)
    M=Matrix(n,n,lambda a,b:G(idx[a],idx[b]))
    ker=M.nullspace()
    # saturated integer kernel basis
    if ker:
        K=Matrix.hstack(*[ (k*sp.ilcm(*[sp.fraction(x)[1] for x in k])) for k in ker]).T
        # saturate: Hermite/Smith on K
        from sympy.matrices.normalforms import hermite_normal_form
    # Gram of generators M; invariants of lattice: nonzero Smith factors of M give disc group of the image lattice L in its dual?
    # For L = Z^n/ker with Gram M: Smith(M) nonzero part = invariants of L^*/L  (since Z^n -> L is surjective, M = B^T G B with B surjective)
    S=smith_normal_form(M,domain=sp.ZZ)
    d=[abs(S[k,k]) for k in range(n) if S[k,k]!=0]
    return M.rank(), d
for nm,idx in [('56',list(range(56))),('40',P40),('16',SP)]:
    r,d=lattice_invariants(idx)
    det=sp.prod(d)
    print(nm,'lines: rank',r,' |det|',det,' nontrivial Smith',[x for x in d if x!=1])
# signature of 40-lattice: eigenvalues of Gram on a basis
M40=Matrix(40,40,lambda a,b:G(P40[a],P40[b]))
ev=[complex(e).real for e in mp.eig(mp.matrix(M40.tolist()))[0]]
print('40 Gram: #pos',sum(e>1e-9 for e in ev),'#neg',sum(e<-1e-9 for e in ev),'#zero',sum(abs(e)<=1e-9 for e in ev))
# h: is h in the span of 40? check via h.L=1 functional: find x with M40 x restricted... h = sum of lines in a plane section with 4 lines among P40
json.dump({'inc':sorted(inc)},open('ref_inc.json','w'))
# complement v: vector in Q-span of 56 classes orthogonal to the 40 (and to h). Work in coordinates of 56 generators.
M56=Matrix(56,56,lambda a,b:G(a,b))
A=M56.extract(P40,list(range(56)))  # pairings of 40 lines with generator combos
ns=A.nullspace()   # combos x with L_i . (sum x_k L_k) = 0 for all i in 40
# remove kernel of M56
vs=[n for n in ns if (M56*n)!=sp.zeros(56,1)]
print('dim orth-complement combos (mod kernel):', Matrix.hstack(*[M56*n for n in ns]).rank())
x=vs[0]; x=x*sp.ilcm(*[sp.fraction(t)[1] for t in x]); w=M56*x  # w_k = L_k . v_x
g=sp.igcd(*[int(t) for t in w if t!=0]); 
# the primitive class in NS: v such that pairings are w/g * (something); compute v.v for x scaled
vv=(x.T*M56*x)[0]
print('raw v pairings with lines (nonzero set):',sorted(set(int(t) for t in w)),' v.v raw',vv,' gcd of pairings',g)
