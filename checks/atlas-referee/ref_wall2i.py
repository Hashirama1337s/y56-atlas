# count singular points of X_s at s = 2i (and s = 2 as control) by numerics on the gradient system
import mpmath as mp, itertools, random
mp.mp.dps=40
def G(z,s):
    z0,z1,z2,z3=z
    return 4*z0**3*z3-4*z0*z3**3+2*z1*z2*(s*(z0**2+z3**2)-(z1**2+z2**2))
def grad(z,s):
    z0,z1,z2,z3=z
    return [12*z0**2*z3-4*z3**3+2*z1*z2*s*2*z0,
            2*z2*(s*(z0**2+z3**2)-(z1**2+z2**2))+2*z1*z2*(-2*z1),
            2*z1*(s*(z0**2+z3**2)-(z1**2+z2**2))+2*z1*z2*(-2*z2),
            4*z0**3-12*z0*z3**2+2*z1*z2*s*2*z3]
def run(s,trials=400,seed=1):
    random.seed(seed); pts=[]
    for k in range(trials):
        c=[mp.mpc(random.gauss(0,1),random.gauss(0,1)) for _ in range(4)]
        # affine chart: random hyperplane c.z = 1
        def f(*x):
            z=list(x); g=grad(z,s); return g[:3]+[sum(ci*zi for ci,zi in zip(c,z))-1]
        x0=[mp.mpc(random.gauss(0,1),random.gauss(0,1)) for _ in range(4)]
        try:
            sol=mp.findroot(f,x0,tol=1e-30,maxsteps=60)
        except Exception: continue
        z=[sol[i] for i in range(4)]
        if max(abs(v) for v in grad(z,s))>1e-20: continue
        # normalise projectively
        j=max(range(4),key=lambda i:abs(z[i])); z=[v/z[j] for v in z]
        if not any(max(abs(a-b) for a,b in zip(z,p))<1e-15 for p in pts): pts.append(z)
    return pts
for s in [mp.mpf(2), mp.mpc(0,2), mp.mpf(3)]:
    p=run(s); print("s =",s,": distinct singular points found:",len(p))
