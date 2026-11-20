# Referee: for each meeting (+,-) pair of special lines, is L+ + L- in span(40)? Is it equal to La+Lb (a,b among the 40)?
import json, itertools, sympy as sp
from sympy import Matrix
D0='../../core/data/'
inc=set(tuple(sorted(e)) for e in json.load(open(D0+'edges.json')))
G=lambda i,j: -2 if i==j else (1 if (min(i,j),max(i,j)) in inc else 0)
pm=json.load(open('ref_pm.json')); plus,minus=pm['plus'],pm['minus']
SP=sorted(plus+minus); P40=[i for i in range(56) if i not in SP]
pairs=[(a,b) for a in plus for b in minus if G(a,b)==1]
print('meeting (+,-) pairs',len(pairs))
vec=lambda S:[sum(G(i,k) for i in S) for k in range(56)]   # pairing vector determines the class (NS nondegenerate, 56 lines span finite index)
M40=Matrix([[G(i,k) for k in range(56)] for i in P40]).T
two={tuple(vec([a,b])) for a,b in itertools.combinations_with_replacement(P40,2)}
inspan=0; issum=0
for a,b in pairs:
    w=Matrix(vec([a,b]))
    try:
        x,par=M40.gauss_jordan_solve(w); x=x.subs({p:0 for p in par})
        integral=all(t.is_integer for t in x); inspan+= integral  # rational solution exists; integrality of this particular solution is sufficient, not necessary
    except ValueError: pass
    issum+= tuple(vec([a,b])) in two
print('pairs with L+ + L- in Q-span of 40 (integral particular solution found):',inspan,' pairs equal to a sum of two of the 40 lines:',issum)
