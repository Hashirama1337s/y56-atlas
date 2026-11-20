import re, itertools, sys
from fractions import Fraction
# --- real solutions
txt = open('../../data/logs/real_01.out').read()
head = re.match(r'\[(\d+), \[(\d+),', txt)
print("msolve header (dim code, #?)", head.groups())
body = txt[txt.index('[[[')+1:]
body = body.rstrip().rstrip(':').strip()
body = body.rstrip(']').rstrip()
# parse as nested python via evaluating fractions
def conv(m):
    return f'Fraction({m.group(1)},{m.group(2)})'
t2 = re.sub(r'(-?\d+)\s*/\s*2\^(\d+)', lambda m: f'Fraction({m.group(1)},2**{m.group(2)})', txt)
t2 = re.sub(r'(?<![\d)])(-?\d+)(?=\s*[,\]])', lambda m: m.group(1), t2)
t2 = t2.rstrip().rstrip(':')
data = eval(t2)
sols = data[1][1]
print("real solutions (a,b,c,d,s boxes):", len(sols))
sv = [ (float(sl[4][0]+sl[4][1])/2) for sl in sols]
print("s>0:", sum(1 for x in sv if x>0), " s<0:", sum(1 for x in sv if x<0))
# distinctness of boxes in (a,b,c,d,s)
mid = [tuple((x[0]+x[1])/2 for x in sl) for sl in sols]
print("distinct midpoints:", len(set(mid)))
# check boxes disjoint
def disj(A,B): return any(a[1]<b[0] or b[1]<a[0] for a,b in zip(A,B))
bad = sum(1 for i in range(len(sols)) for j in range(i) if not disj(sols[i],sols[j]))
print("overlapping box pairs:", bad)
# --- GB staircase (grevlex a>b>c>d>s) -> vdim
g = open('../../data/logs/gb_01.out').read()
body = g[g.index('[s^2-2'):]
polys = [p.strip() for p in re.split(r',\s*\n', body.strip().strip('[]:'))]
vars_ = ['a','b','c','d','s']
lms=[]
from sympy import Poly, symbols, sympify
V = symbols(vars_)
for p in polys:
    e = sympify(p.replace('^','**'))
    if not hasattr(e,'free_symbols') or isinstance(e, (list,tuple)):
        print("bad poly", p[:200]); sys.exit(1)
    P = Poly(e, *V)
    lm = max(P.monoms(), key=lambda m:(sum(m), tuple(-x for x in reversed(m))))  # grevlex: deg then smallest last var
    lms.append(lm)
print("GB elements:", len(lms))
# count standard monomials
def divisible(m):
    return any(all(m[i]>=l[i] for i in range(5)) for l in lms)
maxd = 40
cnt=0; frontier=[(0,0,0,0,0)]; seen=set(frontier)
while frontier:
    m=frontier.pop()
    if divisible(m): continue
    cnt+=1
    for i in range(5):
        n=list(m); n[i]+=1; n=tuple(n)
        if n not in seen: seen.add(n); frontier.append(n)
print("standard monomials (vdim over Q with s adjoined, with multiplicity):", cnt)
