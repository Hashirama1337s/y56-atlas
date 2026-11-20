"""Which lines form the 8-orbit; are DIS's m1={z0=z1=0}, m2={z2=z3=0} in it; skew pairs meeting 10 common lines."""
import os, sys
ROOT = sys.argv[1]
exec(open(os.path.dirname(os.path.abspath(__file__)) + '/ref_checks_core.py').read())
adj = [set() for _ in range(56)]
for i, j in E: adj[i].add(j); adj[j].add(i)
orbs = []; seen = set()
for i in range(56):
    if i in seen: continue
    o = sorted({p[i] for p in perms}); seen |= set(o); orbs.append(o)
o8 = [o for o in orbs if len(o) == 8][0]
print('8-orbit:', o8)
e = lambda k: [K(1) if t == k else K() for t in range(4)]
m1 = plucker(e(2), e(3)); m2 = plucker(e(0), e(1))
print('m1 index', PL.index(m1) if m1 in PL else None, ' m2 index', PL.index(m2) if m2 in PL else None)
pairs = [(i, j) for i in range(56) for j in range(i+1, 56) if j not in adj[i] and len(adj[i] & adj[j]) == 10]
print('skew pairs with 10 common neighbours:', len(pairs), pairs, ' lines covered:', sorted({x for pq in pairs for x in pq}))
