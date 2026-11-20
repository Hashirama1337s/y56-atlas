# Task B setup (EXACT): real equations G_g(x) = F(A_g x) for the sister real structures, with A_g = [E+ | i E-]
# (exact eigenvectors of M_g over Q(sqrt2), NOT normalised), and msolve inputs for the critical points of an even
# Morse function h(x) = x^T Q x / |x|^2 on X_R (well defined on RP^3) via the lift to S^3.
import sys, pickle, sympy as sp
sys.path.insert(0, '../../core/code/sisters')
from q2 import load_syms
r = sp.sqrt(2); z = sp.symbols('z0:4'); x = sp.symbols('x0:4'); s = sp.Symbol('s')
F = 3*r*z[0]**2*z[1]*z[2] + 3*r*z[1]*z[2]*z[3]**2 - r*z[1]**3*z[2] - r*z[1]*z[2]**3 + 4*z[0]**3*z[3] - 4*z[0]*z[3]**3
S = {nm: (c, M) for nm, c, M, _ in load_syms()}
QH = sp.Matrix([[7, 2, -3, 1], [2, -5, 4, 2], [-3, 4, 3, -1], [1, 2, -1, -2]])   # generic integer symmetric (fixed, documented)
out = {}
for rep in sys.argv[1:]:
    c, M = S[rep]; M = sp.Matrix([[e.sym() for e in row] for row in M])
    lam = sp.nsimplify((M*M)[0, 0]); sl = sp.sqrt(lam)
    Ep = (M - sl*sp.eye(4)).nullspace(); Em = (M + sl*sp.eye(4)).nullspace()
    Ep = [sp.simplify(v) for v in Ep]; Em = [sp.simplify(v) for v in Em]
    A = sp.Matrix.hstack(*Ep, *[sp.I*v for v in Em])
    Ax = A*sp.Matrix(x)
    G = sp.expand(F.subs(dict(zip(z, list(Ax))), simultaneous=True))
    xr = sp.symbols('x0:4', real=True); Gc = G.subs(dict(zip(x, xr)))
    Gre, Gim = sp.expand(sp.re(Gc)), sp.expand(sp.im(Gc))
    # reality check: F(A x) is real (c/lambda^2 = 1) or purely imaginary (c/lambda^2 = -1, e.g. g02) for real x
    assert Gre == 0 or Gim == 0, (rep, 'neither real nor imaginary')
    G = (Gre if Gim == 0 else Gim).subs(dict(zip(xr, x)))
    G = sp.expand(G); Gs = sp.expand(G.subs(r, s))
    den = sp.lcm([sp.fraction(sp.together(t))[1] for t in sp.Add.make_args(Gs)])
    Gs = sp.expand(Gs*den)
    grad = [sp.diff(Gs, xi) for xi in x]
    Qx = list(QH*sp.Matrix(x))
    Mm = sp.Matrix([Qx, list(x), grad])
    minors = [sp.expand(Mm[:, [j for j in range(4) if j != k]].det()) for k in range(4)]
    eqs = [Gs, sp.expand(sum(xi**2 for xi in x) - 1)] + minors + [s**2 - 2]
    fn = 'b_%s.ms' % rep
    with open(fn, 'w') as f:
        f.write('x0,x1,x2,x3,s\n0\n')
        f.write(',\n'.join(str(e).replace('**', '^') for e in eqs) + '\n')
    out[rep] = dict(A=A, G=G, eigsplit=(len(Ep), len(Em)), QH=QH)
    print(rep, 'eigen split +%d -%d' % (len(Ep), len(Em)), ' A =', A.tolist())
    print('   G =', G)
pickle.dump(out, open('b_gen_%s.pkl' % '_'.join(sys.argv[1:]), 'wb'))
