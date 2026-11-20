# EXACT: which Y56 lines deform to first order along the pencil (direction dF/db = Im(p^2)|w|^2)?
import sympy as sp, re, json
s2=sp.sqrt(2)
z=sp.symbols('z0:4')
F=4*z[0]**3*z[3]-4*z[0]*z[3]**3+2*z[1]*z[2]*(3*(z[0]**2+z[3]**2)-(z[1]**2+z[2]**2))/s2
Gd=2*z[1]*z[2]*(z[0]**2+z[3]**2)
lines=[]
for ln in open('../core/data/lines_exact.txt'):
    if not ln.startswith('L'): continue
    a,b=ln.split(':',1)[1].split('|')
    lines.append((sp.Matrix([sp.sympify(t) for t in eval(a)]).T, sp.Matrix([sp.sympify(t) for t in eval(b)]).T))
assert len(lines)==56
sig=[]
for ln in open('../core/data/symmetry_exact.txt'):
    m=re.search(r'sigma=(\[.*\])',ln)
    if m: sig.append(eval(m.group(1)))
assert len(sig)==32
# orbits
seen=set(); orbits=[]
for i in range(56):
    if i in seen: continue
    o=sorted(set(s[i] for s in sig)); orbits.append(o); seen|=set(o)
print('orbits',[len(o) for o in orbits]); 
for o in orbits: print(o)
lam=sp.symbols('lam'); grad=[sp.diff(F,v) for v in z]
res=[]
for i,(r0,r1) in enumerate(lines):
    x=lam*r0+r1; sub=dict(zip(z,list(x)))
    assert sp.simplify(sp.expand(F.subs(sub)))==0, i
    g=[sp.expand(gr.subs(sub)) for gr in grad]
    cols=[]
    for k in range(4):
        cols.append(sp.Poly(g[k],lam).all_coeffs()); cols.append(sp.Poly(sp.expand(lam*g[k]),lam).all_coeffs())
    def pad(c): c=[0]*(5-len(c))+list(c); return c
    M=sp.Matrix([pad(c) for c in cols]).T.applyfunc(sp.nsimplify)
    rhs=sp.Matrix(pad(sp.Poly(sp.expand(Gd.subs(sub)),lam).all_coeffs() if sp.expand(Gd.subs(sub))!=0 else [0]))
    M=M.applyfunc(lambda t: sp.radsimp(sp.expand(t))); 
    rM=M.rank(simplify=True); rA=M.row_join(rhs).rank(simplify=True)
    res.append(rM==rA); print(i,'rank M',rM,'rank aug',rA,'deforms1' if rM==rA else 'OBSTRUCTED',flush=True)
ob=[i for i in range(56) if not res[i]]
print('obstructed lines',ob,len(ob))
for k,o in enumerate(orbits): print('orbit',k,len(o),'obstructed' if set(o)<=set(ob) else ('mixed' if set(o)&set(ob) else 'deforms'))
json.dump(dict(orbits=orbits,obstructed=ob),open('a1_firstorder.json','w'))
