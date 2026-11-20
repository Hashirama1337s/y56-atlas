# Y56 contains exactly 56 lines over C (exact computation)

F = 3 eps z0^2 z1 z2 + 3 eps z1 z2 z3^2 - eps z1^3 z2 - eps z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3, eps = sqrt2.

## Result
The Fano scheme of lines of Y56 = {F=0} in P^3 has degree (length) exactly **56** and the 56 exact lines in
`data/lines_exact.txt` are 56 distinct points of it. Hence the scheme is reduced, has exactly
56 points over C, all defined over Q(sqrt2) and real. There is no 57th line, real or complex.

## Method (Singular 4.x via passagemath-singular 10.8.14 under WSL; versions listed in requirements.txt)
1. Rational change of coordinates z = T w, T = [[1,3,2,-2],[-3,1,1,2],[-2,-1,-3,1],[2,-3,1,-3]] (det != 0),
   chosen (seed 7, gen.py) so that none of the 56 lines has vanishing Plucker coordinate p01 in w-coords.
2. Chart {0,1} of G(2,4): line = <p,q>, p=(1,0,a,b), q=(0,1,c,d). Substitute w = m p + q into F(Tw); the 5 coefficients
   of m^0..m^4 are 5 polynomials in (a,b,c,d) over Q(sqrt2) (ring `(0,s),(a,b,c,d,m)`, minpoly s^2-2).
   Groebner basis of I + (m): zero-dimensional, **vdim = 56** (multiplicity-counted number of solutions over C;
   vdim is invariant under base change to C).
3. Nothing lost at infinity of the chart: for each of the other 5 charts {i,j}, I_ij + (p01) has Groebner basis {1},
   i.e. every Fano point has p01 != 0 and so lies in chart {0,1}.
4. The 56 exact lines (transformed by T^-1, row-reduced to the chart) are 56 pairwise distinct points (exact check
   in Q(sqrt2), gen.py) and all 5 generators vanish at each (Singular check: 0 failures).
5. Lower bound 56 (distinct solutions) = upper bound 56 (degree) => all solutions simple, ideal radical, total 56 points.
   All have coordinates in Q(sqrt2) subset R => all 56 lines are real; they are by construction exactly lines_exact.txt.

## Smoothness (needed for finiteness/rigidity discussion; not strictly needed for the count above)
`smooth.sing`/`smooth.out`: J = (dF/dz0..dF/dz3) over Q(sqrt2): Groebner basis has dim 0 (only the origin in the
affine cone), vdim R/J = 81 = 3^4 (Milnor number of a smooth quartic, as expected), z_i^9 in J for i=0..3,
and F in J (Euler). So there is no projective zero of grad F: Y56 is smooth over C. (Hence a K3 surface, lines
are (-2)-curves, rigid, Fano scheme finite and reduced, consistent with the computed vdim 56 = 56 distinct points.)

## Files
code/exact3/gen.py (builds fano.sing from data/lines_exact.txt), code/exact3/fano.sing, data/logs/fano_rerun.out (Singular transcript; about four and a half minutes,
under 8 GB), code/exact3/smooth.sing, data/logs/smooth.out.

## Loose ends
- In the first transcript of this run the first line was overwritten by the shell `time` redirect (only the tail "...multiplicity) = 56" survived).
  vdim finite already implies dim 0. The first run printed dim=1 / vdim=-1 only because the free
  variable m was left in the ring; fixed by adding m to the ideal (not a mathematical issue). The shipped transcript is the clean re-run below.
- Singular is floating-free exact arithmetic but is trusted software, not a kernel-checked proof (no Lean certificate).
- The count is of lines in this specific equation; link to the equation being the intended Y56 relies on
  lines_exact.txt/F as supplied. T was fixed by seed 7; the argument does not depend on it (steps 3-5 verify it).
- Not re-run in a second CAS in this note (msolve gives a second derivation: LINES-COUNT-2.md); sympy groebner was not attempted (4-variable, sqrt2 coefficients, ~4 min in Singular).

## Clean re-run (2026-11-19)
data/logs/fano_rerun.out (same fano.sing, under WSL with a memory limit of 8 GB, exit 0) reads:
"CHART {0,1}: dim = 0   vdim (degree with multiplicity) = 56"; std(I + (p01)) = 1 in all 5 other charts; and "lines (of 56)
failing the 5 equations: 0". This closes the first-transcript loose end above.
