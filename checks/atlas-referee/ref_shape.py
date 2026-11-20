import sympy as sp
a,b,s,t0,t3=sp.symbols("alpha beta s t0 t3")
Gs=lambda z0,z1,z2,z3: 4*z0**3*z3-4*z0*z3**3+2*z1*z2*(s*(z0**2+z3**2)-(z1**2+z2**2))
eqs=[a*b*(s-a**2-b**2), 2+a*b*(s-b**2), 1+a*b**3]
GE=sp.groebner(eqs,a,b,s,order="lex")
for name,(z1,z2) in {"z1=a z0, z2=b(z3-z0)":(a*t0,b*(t3-t0)),"z1=a z0, z2=b(z0-z3)":(a*t0,b*(t0-t3)),"z1=-a z0, z2=b(z3-z0)":(-a*t0,b*(t3-t0))}.items():
    P=sp.Poly(sp.expand(Gs(t0,z1,z2,t3)),t0,t3)
    cs=[sp.factor(P.coeff_monomial(t0**(4-k)*t3**k)) for k in range(5)]
    G=sp.groebner([c for c in cs if c!=0],a,b,s,order="lex")
    print(name,"| nonzero coeffs:",sum(1 for c in cs if c!=0),"| same ideal as paper's 3 eqs:",list(G.exprs)==list(GE.exprs))
    print("   ",cs)
# paper's converse point on the paper's stated shape
bb=sp.Rational(1,2)**sp.Rational(1,8); aa=-1/bb**3; ss=3*bb**2
P=sp.expand(Gs(t0,aa*t0,bb*(t3-t0),t3).subs(s,ss))
print("paper converse on stated shape, max|coef| =",max(abs(sp.N(c,30)) for c in sp.Poly(P,t0,t3).coeffs()))
P=sp.expand(Gs(t0,-aa*t0,bb*(t3-t0),t3).subs(s,ss))
print("with alpha=+1/beta^3, max|coef| =",max([abs(sp.N(c,30)) for c in sp.Poly(P,t0,t3).coeffs()]+[0]))
# the corrected shape of the paper (z2 = beta(z0 - z3)) at the paper's converse point alpha = -1/beta^3, beta = 2^(-1/8), s = 3 beta^2
P=sp.expand(Gs(t0,aa*t0,bb*(t0-t3),t3).subs(s,ss))
print("corrected shape z2=b(z0-z3), paper's converse point: max|coef| =",max([abs(sp.N(c,30)) for c in sp.Poly(P,t0,t3).coeffs()]+[0]))
