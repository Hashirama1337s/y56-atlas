# Task B step 3: with the msolve-certified separating levels q = t1, t2 (no real point of X_R on them),
# put (i) the exact critical points of b_anal (msolve boxes) and (ii) every real conic oval into the three regions.
import sys, re, pickle, numpy as np
from fractions import Fraction
sys.path.insert(0, '../../core/code/sisters')
import s5_portraits as S5
sep = pickle.load(open('b_sep_g12_g13.pkl', 'rb'))
def parse(fn):
    txt = open(fn).read().strip().rstrip(':')
    return eval(re.sub(r'(-?\d+)\s*/\s*2\^(\d+)', lambda m: f'Fraction({m.group(1)},2**{m.group(2)})', txt))[1][1]
for rep in sys.argv[1:]:
    d = sep[rep]; Q = d['Q']; t1, t2 = [float(t) for t in d['ts']]; T = d['T']
    def region(qv): return 0 if qv < t1 else (1 if qv < t2 else 2)
    # (i) exact critical points (boxes of width ~2^-60 or less) -> q value with interval bound
    crit = [sl for sl in parse('b_%s.out' % rep) if sl[4][0] > 0]
    cr = []
    for sl in crit:
        xm = np.array([float((b[0]+b[1])/2) for b in sl[:4]])
        qv = xm @ Q @ xm / (xm @ xm); cr.append(region(qv))
    print(f'{rep}: thresholds t1={d["ts"][0]} t2={d["ts"][1]}; critical points of h on the lift ({len(crit)}) per region:',
          [cr.count(k) for k in range(3)])
    lines, conics = S5.real_curves(rep)
    tally = {0: [], 1: [], 2: []}; margin = np.inf
    for C, kind in conics:
        X = T @ C.T; qv = np.einsum('in,ij,jn->n', X, Q, X)/np.sum(X**2, axis=0)
        regs = {region(v) for v in qv}; assert len(regs) == 1, (rep, 'oval crosses a separating level?!')
        k = regs.pop(); tally[k].append(kind)
        margin = min(margin, np.min(np.abs(qv - t1)), np.min(np.abs(qv - t2)))
    for k in range(3):
        print(f'   region {k}: {len(tally[k])} ovals ({tally[k].count("res")} two-line-plane, {tally[k].count("cpp")} pair-plane)')
    print(f'   min distance of any oval point (1500 per oval) from a separating level: {margin:.3f};  real lines: {len(lines)}')
