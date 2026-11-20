# count msolve real solutions by sign of s (s = +sqrt2 is our surface; s = -sqrt2 is its Galois conjugate)
import re, sys
from fractions import Fraction
for fn in sys.argv[1:]:
    txt = open(fn).read().strip().rstrip(':')
    data = eval(re.sub(r'(-?\d+)\s*/\s*2\^(\d+)', lambda m: f'Fraction({m.group(1)},2**{m.group(2)})', txt))
    sols = data[1][1]
    sp_ = [sl for sl in sols if sl[4][0] > 0]; sn = [sl for sl in sols if sl[4][1] < 0]
    print(fn, 'dim-code', data[0], ' real solutions', len(sols), ' s>0:', len(sp_), ' s<0:', len(sn))
