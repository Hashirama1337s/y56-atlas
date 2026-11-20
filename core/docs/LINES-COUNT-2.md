# Y56 line count, second independent derivation (msolve): 56 lines, all real

F = 3 eps z0^2 z1 z2 + 3 eps z1 z2 z3^2 - eps z1^3 z2 - eps z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3, eps = sqrt2.

## Result
| quantity | value |
|---|---|
| tool | msolve 0.10.1 (passagemath-msolve 10.8.14 wheel, WSL), exact Groebner basis + certified real-root isolation over Q |
| ideal degree, with multiplicity (standard monomials of the reduced GB in Q[a,b,c,d,s]) | **112 = 2 x 56** |
| distinct complex solutions (radical parametrisation degree) | **112 = 2 x 56** |
| real solutions (isolated by msolve, 128-bit boxes, pairwise disjoint) | **112**: 56 with s > 0, 56 with s < 0 |
| other 5 charts, with p01 = 0 added | reduced GB = {1} (empty) in all 5 |
| Y56 lines over C | **56**, all real, ideal radical (degree = distinct count) |
Agrees with Singular (vdim 56 over Q(sqrt2)).

## Independent setup (nothing reused from gen.py / fano.sing)
- Own coordinate change z = T w, T = [[3,4,-1,-4],[0,3,1,-4],[0,-4,-2,0],[-4,3,4,1]], det -46, from python random seed 20261119 (Singular used a different T, seed 7).
- sqrt2 handled by adjoining a variable s with s^2 - 2 in Q[a,b,c,d,s] (msolve works over Q only), not a number-field ring.
- Lines: for each pair {i,j}, chart p = e_i + (a,b) on the other two coords, q = e_j + (c,d). Line = {lam p + mu q}; F(T(lam p + mu q)) is a binary quartic in (lam, mu); its 5 coefficients (homogeneous extraction, not Singular's m-substitution) must vanish. Ideal I_ij = (5 coefficients, s^2-2).
- Chart {0,1}: msolve -g 2 (reduced GB), staircase count by own script (analyze.py) = 112; msolve -p 128 real isolation = 112 disjoint boxes.
- Charts {0,2},{0,3},{1,2},{1,3},{2,3}: I_ij + (p01) with p01 = p0 q1 - p1 q0 gives GB {1}. So every line has p01 != 0 in the T-coordinates and lies in chart {0,1}.

## Bookkeeping for sqrt2
The 112 solutions in (a,b,c,d,s) split by sign of s: 56 with s = +sqrt2 (lines of Y56 itself) and 56 with s = -sqrt2 (lines of the Galois-conjugate surface, which has the same count and is the image of the same solutions under the conjugation sqrt2 -> -sqrt2). Since the conjugation swaps the two halves bijectively, Y56 has 112/2 = 56 lines. This is also read directly from the isolated real roots (56 with s>0). The check relies only on s^2=2, so both embeddings are counted, nothing else is assumed. Degree equals distinct count, so all 56 are simple (Fano scheme reduced).

## Files
In code/exact3_v2/: gen2.py (setup), fano_01.ms and fano_*_p01.ms (msolve inputs), run_ms.sh, run_real.sh, analyze.py. In data/logs/: gb_01.out, par_01.out (parametrisation, degree 112), real_01.out (real roots), analyze.log. Install versions are listed in requirements.txt.

## Loose ends
- msolve is trusted software, not a kernel-checked proof; real-root boxes are certified by msolve but not re-verified by us. The GB staircase is our own count of msolve's output basis (assumes msolve's GB is correct).
- Not independently verified here that the 56 solutions equal lines_exact.txt (not needed for the count; coordinate change differs).
- msolve computes GB via modular (F4 mod p) + rational reconstruction, and its default is Monte Carlo (correct with high probability, not formally certified); the final GB is not re-verified by us by reduction. Singular agreement is the cross-check.
