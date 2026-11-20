# Independent setup for Fano scheme of F=0 (eps=sqrt2 via variable s, s^2=2). Own seed, own T, homogeneous lam/mu extraction.
import random, itertools, sympy as sp
random.seed(20261119)
while True:
    T = sp.Matrix(4,4,lambda i,j: random.randint(-4,4))
    if T.det()!=0: break
print("T =", T.tolist(), "det", T.det())
z = sp.symbols('z0:4'); s,lam,mu = sp.symbols('s lam mu')
a,b,c,d = sp.symbols('a b c d')
z0,z1,z2,z3 = z
F = 3*s*z0**2*z1*z2+3*s*z1*z2*z3**2-s*z1**3*z2-s*z1*z2**3+4*z0**3*z3-4*z0*z3**3
def chart(i,j):
    k,l = [x for x in range(4) if x not in (i,j)]
    p=[0]*4; q=[0]*4
    p[i]=1; q[j]=1; p[k]=a; p[l]=b; q[k]=c; q[l]=d
    return p,q
def system(i,j):
    p,q = chart(i,j)
    w = [lam*p[t]+mu*q[t] for t in range(4)]
    zz = T*sp.Matrix(w)
    G = sp.expand(F.subs(dict(zip(z,zz)),simultaneous=True))
    P = sp.Poly(G, lam, mu)
    coeffs = [sp.expand(P.coeff_monomial(lam**e*mu**(4-e))) for e in range(5)]
    assert all(sp.Poly(cf,lam,mu).total_degree()==0 for cf in coeffs)
    p01 = sp.expand(p[0]*q[1]-p[1]*q[0])
    return coeffs, p01, (a,b,c,d)
def write(fn, polys, vars_):
    with open(fn,'w') as f:
        f.write(",".join(map(str,vars_))+"\n0\n")
        f.write(",\n".join(str(sp.expand(pp)).replace('**','^') for pp in polys)+"\n")
for (i,j) in itertools.combinations(range(4),2):
    co,p01,vs = system(i,j)
    V = list(vs)+[s]
    base = co+[s**2-2]
    write(f"fano_{i}{j}.ms", base, V)
    if (i,j)!=(0,1):
        write(f"fano_{i}{j}_p01.ms", base+[p01], V)
print("done")
