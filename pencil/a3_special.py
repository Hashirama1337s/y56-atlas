# EXACT: structure of the 16 special lines: graph-matrix patterns, sign classes w.r.t. the NL class v, incidences, planes
import sympy as sp, json, itertools, re
from sympy.matrices.normalforms import smith_normal_form
d=json.load(open('a1_firstorder.json')); ob=d['obstructed']; v=json.load(open('a2_lattice.json'))['v_pair']
edges=set(map(tuple,json.load(open('../core/data/edges.json')))); 
meet=lambda i,j:(i,j) in edges or (j,i) in edges
lines=[]
for ln in open('../core/data/lines_exact.txt'):
    if not ln.startswith('L'): continue
    a,b=ln.split(':',1)[1].split('|')
    lines.append(sp.Matrix([[sp.sympify(t) for t in eval(a)],[sp.sympify(t) for t in eval(b)]]))
# graph form z1 = A z0 + B z3, z2 = C z0 + D z3 (Y56 coordinates): M = N[:, (1,2)]^T * inv(N[:, (0,3)])^T
pat={}
for i,N in enumerate(lines):
    X=N.extract([0,1],[0,3]); Y=N.extract([0,1],[1,2])
    if sp.simplify(X.det())==0: pat[i]='meets z0=z3=0'; continue
    M=(X.inv()*Y).T.applyfunc(lambda t: sp.radsimp(sp.simplify(t)))  # rows: z1,z2 ; cols: z0,z3
    A,B,C,D=M[0,0],M[0,1],M[1,0],M[1,1]
    z=lambda t: sp.simplify(t)==0
    if (z(B) and z(C)) or (z(A) and z(D)): p='axis type (z1,z2 prop. to z0,z3 in some order)'
    elif (z(A-B) and z(C+D)) or (z(A+B) and z(C-D)): p='diagonal type (z1,z2 prop. to z0+z3, z0-z3 in some order)'
    else:
        p='MIXED type: '+('z1' if (z(B) or z(A)) else 'z2')+' prop. to an axis form, other prop. to a diagonal form' if ((z(A) or z(B)) and (z(C-D) or z(C+D))) or ((z(C) or z(D)) and (z(A-B) or z(A+B))) else 'OTHER'
    pat[i]=p
from collections import defaultdict
g=defaultdict(list)
for i,p in pat.items(): g[p].append(i)
for p,l in g.items(): print(len(l),p,l)
mixed=sorted(i for i,p in pat.items() if p.startswith('MIXED'))
print('MIXED set == first-order-obstructed set:',mixed==sorted(ob))
plus=[i for i in ob if v[i]>0]; minus=[i for i in ob if v[i]<0]
print('v.L=+4:',plus); print('v.L=-4:',minus)
print('incidences within +:',sum(meet(i,j) for i,j in itertools.combinations(plus,2)),' within -:',sum(meet(i,j) for i,j in itertools.combinations(minus,2)))
pm=[(i,j) for i in plus for j in minus if meet(i,j)]; print('meeting (+,-) pairs:',len(pm),pm)
for i in ob: print(' L%02d meets special:'%i,[j for j in ob if j!=i and meet(i,j)],' persistent count:',sum(meet(i,j) for j in range(56) if j not in ob and j!=i))
# w = sum(+) - sum(-): pairing with every line
G=lambda i,j: -2 if i==j else (1 if meet(i,j) else 0)
wp=[sum(G(i,k) for i in plus)-sum(G(j,k) for j in minus) for k in range(56)]
print('w.L_k:',wp); print('w = -2 v ?',all(wp[k]==-2*v[k] for k in range(56)))
# planes
txt=open('../core/data/planes_exact.txt').read()
cnt=defaultdict(int)
for m in re.finditer(r'lines \[([0-9, ]+)\]',txt):
    L=[int(t) for t in m.group(1).split(',')]
    cnt[(len(L),sum(1 for t in L if t in ob))]+=1
    if len(L)==4 and sum(1 for t in L if t in ob)==2:
        sp_=[t for t in L if t in ob]; 
        if cnt[(4,2)]<=3: print('4-line plane',L,'special pair',sp_,'signs',[v[t] for t in sp_],'meet',meet(*sp_))
print('planes by (number of lines, number of special lines):',dict(cnt))
