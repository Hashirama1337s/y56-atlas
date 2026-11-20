import ast, os, sympy as sp
r2=sp.sqrt(2)
L=[]
for ln in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","core","data","lines_exact.txt")):
    if ln.startswith("L"):
        a,b=ln.split(":",1)[1].split("|")
        L.append([[sp.sympify(x) for x in ast.literal_eval(a.strip())],[sp.sympify(x) for x in ast.literal_eval(b.strip())]])
def same(P,Q): return sp.Matrix(P+Q).rank(simplify=True)==2
R=lambda v:[v[0],-v[2],v[1],v[3]]
gal=lambda v:[sp.expand(x).subs(r2,-r2) for x in v]
tau=[]
for P in L:
    img=[R(gal(P[0])),R(gal(P[1]))]
    m=[j for j,Q in enumerate(L) if same(img,Q)]; assert len(m)==1; tau.append(m[0])
t2=[tau[tau[i]] for i in range(56)]
print("tau is identity?",tau==list(range(56)),"| tau^2 identity?",t2==list(range(56)),"| tau^4 identity?",[t2[t2[i]] for i in range(56)]==list(range(56)))
