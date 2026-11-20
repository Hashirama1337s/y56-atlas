import re, sympy as sp
rows=[l for l in open('../../core/data/symmetry_exact.txt') if l.startswith('g')]
gens=[]
for l in rows:
    c=int(re.search(r' c=(-?\d+)',l).group(1))
    M=sp.Matrix(sp.sympify(re.search(r'M=(\[\[.*?\]\])',l).group(1)))
    sig=eval(re.search(r'sigma=(\[.*?\])',l).group(1))
    if sp.simplify(M.det()/c)==1: gens.append(sig)
print('symplectic count',len(gens))
P=['PermList(%s)'%[i+1 for i in s] for s in gens]
open('sd16.g','w').write('G:=Group(%s);;\nPrint(Size(G),"\n",IdGroup(G),"\n",StructureDescription(G),"\n");\nQUIT;\n'%(','.join(P)))
