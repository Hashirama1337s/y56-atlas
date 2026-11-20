# Could NS be a proper overlattice of the line lattice N and carry extra lines/conics?  Check every cyclic isotropic overlattice N+Zd.
import cypari2
from fractions import Fraction as Fr
pari = cypari2.Pari(); pari.allocatemem(3*10**9)
L = open('../../data/lat.txt').read().split('\n'); r = int(L[0])
P2 = [list(map(int, L[1+i].split())) for i in range(r)]; hv = list(map(int, L[1+r].split())); gv = list(map(int, L[2+r].split()))
Gram = [[gv[i*r+j] for j in range(r)] for i in range(r)]
Gm = pari.matrix(r, r, [Gram[i][j] for i in range(r) for j in range(r)]); Gi = Gm**-1
gens = [tuple(Fr(int(pari.numerator(Gi[i, j])), int(pari.denominator(Gi[i, j]))) % 1 for i in range(r)) for j in range(r)]
D = {tuple([Fr(0)]*r)}; frontier = list(D)
while frontier:
    new = []
    for d in frontier:
        for g in gens:
            e = tuple((a+b) % 1 for a, b in zip(d, g))
            if e not in D: D.add(e); new.append(e)
    frontier = new
print('discriminant group order', len(D))
def q(d): return sum(d[i]*Gram[i][j]*d[j] for i in range(r) for j in range(r))
iso = [d for d in D if any(d) and q(d) % 2 == 0]
print('nonzero elements with q = 0 mod 2Z:', len(iso))
from math import lcm
newfound = 0
for d in iso:
    den = lcm(*[x.denominator for x in d])
    cols = [[den if i == k else 0 for i in range(r)] for k in range(r)] + [[int(x*den) for x in d]]
    Mx = pari.matrix(r, r+1, [cols[j][i] for i in range(r) for j in range(r+1)])
    Hn = pari.mathnf(Mx)   # r x r basis (columns), scaled by den
    B = [[Fr(int(Hn[i, j]), den) for j in range(r)] for i in range(r)]
    # P2 in new basis, scaled by den^2
    Bp = [[int(B[i][j]*den) for j in range(r)] for i in range(r)]
    Bm = pari.matrix(r, r, [Bp[i][j] for i in range(r) for j in range(r)])
    Pm = pari.matrix(r, r, [P2[i][j] for i in range(r) for j in range(r)])
    Q = Bm.mattranspose()*Pm*Bm      # = den^2 * P2'
    res = pari.qfminim(Q, 8*den*den, 10**7, 2)
    V = res[2]; nc = int(pari.matsize(V)[1])
    for c in range(nc):
        x = [int(V[i, c]) for i in range(r)]
        y = [sum(B[i][j]*x[j] for j in range(r)) for i in range(r)]
        if all(t.denominator == 1 for t in y): continue
        yi = y
        y2 = sum(yi[i]*Gram[i][j]*yi[j] for i in range(r) for j in range(r))
        hy = sum(yi[i]*hv[i] for i in range(r))
        if y2 == -2 and abs(hy) in (1, 2):
            newfound += 1; print('NEW class in overlattice: y^2=-2, y.h =', hy, 'denominator', den)
print('overlattices checked via', len(iso), 'cyclic isotropic classes; new lines/conic classes found:', newfound)
