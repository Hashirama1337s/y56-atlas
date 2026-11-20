import cypari2, itertools
pari = cypari2.Pari(); pari.allocatemem(2*10**9)
L = open('../../data/lat.txt').read().split('\n')
r = int(L[0]); P2 = [list(map(int, L[1+i].split())) for i in range(r)]
hv = list(map(int, L[1+r].split())); gv = list(map(int, L[2+r].split()))
Gram = [[gv[i*r+j] for j in range(r)] for i in range(r)]
lines = [list(map(int, l.split())) for l in open('../../data/lat_lines.txt').read().strip().split('\n')]
M = pari.matrix(r, r, [P2[i][j] for i in range(r) for j in range(r)])
print('P2 definite (qfsign):', pari.qfsign(M))
res = pari.qfminim(M, 8, 10**7, 2)    # all vectors with 2P<=8 (up to sign)
print('number of vectors (pairs +-):', res[0], 'max', res[1])
V = res[2]; ncol = int(pari.matsize(V)[1]); print('columns', ncol)
def ip(u, v): return sum(u[i]*Gram[i][j]*v[j] for i in range(r) for j in range(r) if u[i] and v[j])
def hdot(u): return sum(u[i]*hv[i] for i in range(r))
conics = []
for c in range(ncol):
    x = [int(V[i, c]) for i in range(r)]
    d = hdot(x)
    if d == -2: x = [-t for t in x]; d = 2
    if d != 2: continue
    if ip(x, x) != -2: continue
    conics.append(tuple(x))
print('classes with c.h=2, c^2=-2:', len(conics))
Lset = {tuple(l) for l in lines}; print('distinct line classes', len(Lset))
Ls = [tuple(l) for l in lines]
sums = set()
for i in range(56):
    for j in range(i+1, 56):
        if ip(Ls[i], Ls[j]) == 1: sums.add(tuple(a+b for a, b in zip(Ls[i], Ls[j])))
print('line-pair sums', len(sums), 'all among conic-classes:', sums <= set(conics))
irr = [c for c in conics if c not in sums]; print('irreducible conic classes (not a sum of two meeting lines):', len(irr), ' reducible:', len(conics)-len(irr))
H = tuple(hv_i for hv_i in [0]*r)
# h in coordinates: solve Gram*hx = hv
import fractions
Gm = pari.matrix(r, r, [Gram[i][j] for i in range(r) for j in range(r)]); hx = pari.matsolve(Gm, pari.matrix(r, 1, hv))
hx = [int(hx[i, 0]) for i in range(r)]
irrset = set(irr); pairs = set()
for c in irr:
    cp = tuple(h-a for h, a in zip(hx, c))
    if cp in irrset: pairs.add(frozenset([c, cp]))
print('planes with two irreducible conics (c and h-c both irreducible):', len(pairs))
