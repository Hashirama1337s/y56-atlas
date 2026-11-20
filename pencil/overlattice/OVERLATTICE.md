# Overlattices of N19 (Y56 pencil): NS(very general) = N19

Moki & Julio (AI-assisted) · 2026

Code: ov.py (Gram, primitivity), ov2.py (discriminant group, subgroups, short-vector search); logs ov2.log, overlattice_results.json, N19.json (Gram, h, basis C: basis vector b_i = sum_j C[i][j] * L_keep[j]). All exact (python-flint HNF/SNF, Fractions); floats only to enumerate candidates, every hit re-evaluated exactly.

## Method
1. Gram of the 40 persistent lines from edges.json; Z-basis of the image lattice by HNF of [G | I]. Result: rank 19, det 128, Smith [2,8,8], signature (1,18), h integral in N19 with h.h = 4.
2. Discriminant group A = N*/N, |A| = 128: orders 1,2,4,8 occur 1,7,24,96 times. q (mod 2) takes values 0 (28 elements), +-1/4,+-3/4 etc. Isotropic nonzero elements: 27.
3. Isotropic subgroups (q = 0 on the whole subgroup) by closure: 15 including the trivial one: orders 1:1, 2:3, 4:5, 8:6. Every one gives an even overlattice (checked: Gram even integral, det 128/|H|^2, Smith [2,4,4], [2,2,2], [2]).
4. Short-vector search in each M: Q'(v) = -v.v + (v.h)^2/2 is positive definite on M; all of (a) roots with v.h=0 (Q'=2), (b) e^2=0,e.h=1,2 (Q'=1/2, 2), (c) (-2)-vectors of degree 1 (Q'=5/2) have Q' <= 5/2, so one Fincke-Pohst enumeration (LLL-reduced Gram) with bound 5/2 finds all.

## Control (H = 0, M = N19)
0 roots orthogonal to h, 0 isotropic e of degree 1 or 2, exactly 40 (-2)-vectors of degree 1 (the 40 lines, no extras). Degree-2 (-2) classes were outside the search bound (see loose ends).

## Fate of each overlattice
Every nontrivial isotropic H contains a subgroup of order 2, so M contains the index-2 overlattice. There are exactly 3 isotropic elements of order 2 (glue g, in N-basis coordinates of N*/N; only the nonzero coordinate listed):
| glue g | det M | root r, r^2=-2, r.h=0 (coords in basis b_i, 19 entries) |
|---|---|---|
| (1/2) at b_19 | 32, Smith [2,4,4] | (0,0,0,0,0,0,0,0,0,0,0,1,0,-1,0,0,0,0,1/2). Also 22 roots in total, 4 isotropic e of degree 2 (witness e = (0,..,-2) coefficient pattern in log), 40 new (-2) vectors of degree 1 |
| (1/2) at b_15 | 32, [2,4,4] | (0,0,0,0,1,0,0,1,0,0,0,0,0,0,-1/2,0,0,0,-1); 22 roots; 40 new degree-1 (-2) vectors |
| (1/2) at b_15 and b_19 | 32, [2,4,4] | (0,-1,-1,0,0,1,0,0,0,-1,0,0,0,0,3/2,1,0,1,-1/2); 22 roots; 40 new degree-1 (-2) vectors |
Hence all 14 nontrivial overlattices contain (-2)-vectors orthogonal to h (counts per overlattice from 22 up to 146, listed in overlattice_results.json) so (a) kills all. Independently (c) kills all: each has 40 to 312 new degree-1 (-2) classes, i.e. extra lines. (b): only some (4 isotropic e of degree 2 in three of them), not needed. Summary of all 14: roots_h0 in {22,62,66,126,146}, new lines in {40,120,280,312}.

(e) Nikulin: moot, no candidate survives; for the record l(A_N19)=3 = rank of T, so N19 itself needs 2-adic conditions; all overlattices have l <= 3.

## Independent argument (no enumeration needed)
The 56-line lattice for Y56 has rank 20; the inclusion N19 -> NS(Y56) has Smith form all 1s (primitive; computed in ov.py). NS(very general) is primitive in NS(Y56) (it is H^2(Z) intersect T_gen^perp, and T_Y56 is inside T_gen) and contains N19 with finite index. Primitivity of N19 in NS(Y56) therefore forces NS(very general) = N19. This needs det of the 56-line lattice = NS(Y56) (RESULT.md: T(Y56)=[2,0,32], det 64 matches).

## Conclusion
N19 = NS of the very general member, exactly. All 14 proper even overlattices are excluded, each with an explicit root orthogonal to h (and extra lines). No survivors.

## Loose ends
- Degree-2 (-2) counts in M (item d): the tally found 0 in N19 and in every M; the 48 conics L+ + L- have v^2 = -2+... = -2+2 = 0 for disjoint? They are sums of meeting lines (v^2 = -2-2+2 = -2), so 48 such classes should appear. My script reports deg2_m2 = 0, which contradicts RESULT.md item 8 (48 conics). Cause: the Q' bound for (v^2=-2, d=2) is 2+2 = 4 > 5/2, so those vectors were outside the enumeration bound. Not a contradiction, but the degree-2 counts were NOT measured.
- Likewise e of degree 2 has Q'=2 and is within bound (reported counts valid).
- Nikulin 2-adic check not run (moot).
- Whether to treat the specialization-primitivity argument as a theorem rests on Y56 being a smooth member in the pencil (RESULT.md item 4).

Written with AI assistance.
