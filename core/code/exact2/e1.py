# Exact images of the 3 orbit representatives under the 32 exact symmetries; exact verification of all 20 planes.
import re, pickle, sympy as sp
E = '../../data/'
r = sp.sqrt(2)
Z = sp.symbols('z0 z1 z2 z3'); x, y, w = sp.symbols('x y w')
F = 3*r*Z[0]**2*Z[1]*Z[2]+3*r*Z[1]*Z[2]*Z[3]**2-r*Z[1]**3*Z[2]-r*Z[1]*Z[2]**3+4*Z[0]**3*Z[3]-4*Z[0]*Z[3]**3
syms = []  # (matrix string, line permutation) read from the shipped symmetry file
for ln in open(E+'symmetry_exact.txt'):
    if ln.startswith('g'):
        syms.append((re.search(r'M=(\[\[.*?\]\])', ln).group(1), eval(re.search(r'sigma=(\[.*\])', ln).group(1))))
Ms = [sp.Matrix(eval(s[0], {'sqrt': sp.sqrt})) for s in syms]
reps = {
 'A': [r-1, (3-r)/7, (3-r)/7, 1],
 'B': [1, (-1+2*r)/7, (1-2*r)/7, 1-r],
 'C': [0, r/4, 1, 0],
}
lines = []
for ln in open(E+'lines_exact.txt'):
    if not ln.startswith('L'): continue
    a, b = ln.split(':', 1)[1].split('|')
    lines.append([[sp.sympify(t) for t in eval(s)] for s in (a, b)])
def canon(n):
    n = [sp.radsimp(sp.simplify(t)) for t in n]
    i = [j for j in range(4) if n[j] != 0][-1]
    return tuple(sp.radsimp(sp.simplify(t/n[i])) for t in n)
def section(n):
    i = [j for j in range(4) if n[j] != 0][0]
    oth = [j for j in range(4) if j != i]
    sub = {Z[o]: v for o, v in zip(oth, (x, y, w))}
    sub[Z[i]] = -sum(n[j]*sub[Z[j]] for j in oth)/n[i]
    return sp.expand(sp.radsimp(sp.expand(F.subs(sub, simultaneous=True))))
def gram(fac):
    P = sp.Poly(fac, x, y, w); v = (x, y, w); H = sp.hessian(fac, v)/2
    return H.applyfunc(sp.radsimp)
out = []; allplanes = []
for name, n0 in reps.items():
    orb = []
    for M in Ms:
        n2 = canon(list(M.inv().T*sp.Matrix(n0)))
        if n2 not in orb: orb.append(n2)
    print(name, 'exact orbit size', len(orb), flush=True)
    for n in orb:
        inc = [k for k, (A, B) in enumerate(lines)
               if sp.radsimp(sp.expand(sum(a*b for a, b in zip(n, A)))) == 0 and sp.radsimp(sp.expand(sum(a*b for a, b in zip(n, B)))) == 0]
        G = section(n)
        fl = sp.factor_list(G, extension=r)
        facs = [(sp.Poly(f, x, y, w).total_degree(), e, f) for f, e in fl[1]]
        dets = [sp.radsimp(sp.expand(gram(f).det())) for d, e, f in facs if d == 2]
        ok = (inc == [] and sorted((d, e) for d, e, f in facs) == [(2, 1), (2, 1)] and all(d != 0 for d in dets))
        print('  ', [str(t) for t in n], 'lines', inc, 'degs', [(d, e) for d, e, f in facs], 'dets', [str(d) for d in dets], 'OK' if ok else 'FAIL', flush=True)
        out.append((name, [str(t) for t in n], ok, [str(f) for d, e, f in facs], [str(d) for d in dets]))
        allplanes.append(n)
print('total planes', len(allplanes), 'all OK', all(o[2] for o in out), 'distinct', len(set(allplanes)))
pickle.dump(out, open('e1_out.pkl', 'wb'))
with open('conic_pair_planes_exact.txt', 'w') as f:
    f.write('# 20 line-free conic-pair planes of Y56, normal (n0:n1:n2:n3), plane n.z=0, all over Q(sqrt2). Orbit labels A(8) B(8) C(4).\n')
    f.write('# each: section = Q1*Q2 factored over Q(sqrt2) into two irreducible conics, det of each conic matrix nonzero, no line of lines_exact.txt in plane\n')
    for name, n, ok, fa, de in out:
        f.write('%s %s verified=%s\n   Q1=%s\n   Q2=%s\n   det1=%s det2=%s\n' % (name, n, ok, fa[0], fa[1], de[0], de[1]))
