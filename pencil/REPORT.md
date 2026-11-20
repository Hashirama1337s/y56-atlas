# Why 16 lines exist only at Y56: discovery report

Moki & Julio (AI-assisted) · 2026

Discovery report, 2026-11-20. Superseded where they differ by RESULT.md (the refereed statement) and by ../PRIOR-ART.md (loose end 10 is closed there).

**Editors' check (independent):** sympy Groebner elimination of the three-coefficient system for the axis-diagonal line shape gives exactly 2 s^4 - 81 (scratch check, exit 0). This agrees with special.log (E[1] = 2s4-81) and with graph_y56.log (length 48, distinct 48).

Labels:
- EXACT: Singular over Q or Q(s), or sympy exact.
- NUMERICAL: 40-digit mpmath with stated margins.
- CITED: a published theorem not re-proved.
- UNTESTED: not machine-checked.

Singular and sympy are trusted software, not kernel-checked. Nothing here is sealed or refereed, and no novelty is claimed.

## The family

G_s = Im(w^4) + Im(p^2)(s|w|^2 - |p|^2) = 4 z0^3 z3 - 4 z0 z3^3 + 2 z1 z2 (s(z0^2+z3^2) - (z1^2+z2^2)).

That is (a,b,c) = (1,s,-1), so kappa = -s^2.

- Y56 is s^4 = 81/2, i.e. s = 3/2^(1/4). The original Y56 coordinates are z1 and z2 rescaled by 2^(1/8).
- The wall is s^4 = 16.
- The Fermat type is s = 0.
- Over C the invariant is kappa^2 = s^4.

## Headline

Every member of the family carries the same 40 lines, and they move smoothly with s.

A line of the remaining kind must satisfy three equations in two unknowns. These are compatible only at kappa^2 = 81/2, which is Y56. There 16 extra lines appear at once, forming one orbit of the order-32 group (the orbit of L00).

On neighbouring members the 16 lines are replaced by 48 conics. At Y56 each of these conics breaks into two of the 16 lines.

In lattice terms, the 40 lines span rank 19 on every member, and Y56 has rank 20, with an explicit extra class. The Fermat-type member is the only other jump (8 extra lines, 48 in total).

## Findings

**1. The generic member has exactly 40 complex lines, and its Fano scheme is reduced (EXACT).**
- Graph chart: z1 = A z0 + B z3, z2 = C z0 + D z3. Over Q(s) the Fano ideal has length 32, is radical, and splits into four degree-8 components:
  - C1: C = -D, A = B = -(2D^5 - 3sD^3 + s^2 D), with f1(D) = 4D^8 - 8sD^6 + 5s^2D^4 - s^3D^2 + 1 = 0.
  - C2: C = D, A = -B = -(2D^5 - 3sD^3 + s^2 D), with f1(D) = 0.
  - C3: A = D = 0, B = -(C^5 - 3sC^3 + 2s^2C)/2, with f2(C) = C^8 - 4sC^6 + 5s^2C^4 - 2s^3C^2 + 4 = 0.
  - C4: B = C = 0, A = (D^5 - 3sD^3 + 2s^2D)/2, with f2(D) = 0.
- Each component lies on G_s identically in s (a4_checks.log, part a).
- Lines meeting z0 = z3 = 0, for every s: exactly 8 (meet.log). At s = 0, and only there, 8 more appear in z2 = ±i z1.
- Rational spot checks give length 32 and 32 distinct lines at s = 1/3, 1, 9/4, 5/2, 13/5, 3, 7 and -3.
- An independent stratified-chart method gives 40 lines, reduced, at s = 5/2 and at s = 13/5, and 48 at s = 0.

**2. In the whole complex family, lines jump only at kappa^2 = 81/2 and at 0 (EXACT).**
- Saturating by C1..C4 leaves a length-64 scheme whose eliminant in s is 2s^4 - 81 (special.log).
- At Y56: length 48 and 48 distinct (graph_y56.log), i.e. 32 + 16.
- disc f1 and disc f2 are constants times (s-2)^4 (s+2)^4 (s^2+4)^4. So the graph lines collide in pairs only at the wall, which has 8 simple lines and 16 double ones (EXACT).

**3. The 16 extra lines (EXACT).**
- They are L00, L06, L10, L11, L12, L19, L29, L33, L35, L36, L42, L44, L48, L50, L54 and L55: exactly one orbit of the order-32 group.
- Two independent identifications agree:
  - First-order test: dG/ds restricted to the line is not in the image of the normal-bundle map (rank 4 vs 5).
  - Shape: each of these lines pairs one axis form (z0, z3) with one diagonal form (z0 ± z3).
- Hand derivation: set z1 = alpha z0 and z2 = beta(z0 - z3). The z3^4 coefficient vanishes identically and the other four must vanish; they generate the same ideal as these three equations:
  - alpha beta (s - alpha^2 - beta^2) = 0
  - 2 + alpha beta (s - beta^2) = 0
  - 1 + alpha beta^3 = 0

  Together these force alpha^2 = 2 beta^2, beta^8 = 1/2 and s = 3 beta^2, so s^4 = 81/2. For the axis-axis and diagonal-diagonal shapes only two equations remain, so those lines exist for every s.

**4. The 40 lines deform; the 16 are limits of conics.**
- The 16 are isolated points of the relative Fano scheme (EXACT).
- The pairing with v splits the 16 into two sets of eight (EXACT):
  - plus: L06, L10, L29, L33, L35, L36, L50, L54;
  - minus: L00, L11, L12, L19, L42, L44, L48, L55.
- Lines in the same set are pairwise skew. Each plus line meets 6 minus lines, which gives 48 pairs.
- For each pair, L+ + L- is in the 40-line lattice. By Riemann-Roch (CITED) it is effective on every member, so it is a conic near Y56 that breaks into the two lines at Y56. That gives 48 conics.
- One family is explicit (EXACT): the plane z2 = D(z3 - z0) with f1(D) = 0. The norm of its conic determinant is 2^24 (2s^4 - 81)^2.

**5. Lattice: rank 19 for the generic member, 20 at Y56. Y56 is a Noether-Lefschetz point of the pencil.**
- On Y56 the 40 lines span N19 (EXACT):
  - N19 has rank 19, signature (1,18), det 128 and Smith form [2,8,8].
  - It contains h and is primitive in the 56-line lattice, which has rank 20, det -64 and Smith form [2,32].
- The same Gram data appears at s = 1, 5/2, 13/5, 3 and 7i/3. Incidence there is NUMERICAL at 40 digits; the algebra after it is exact.
- Every member therefore has rank at least 19.
- The very general member has rank exactly 19 by a Torelli argument (CITED Torelli; argued, not refereed, no mod-p check). If it were 20, the period map would be constant and all smooth members would be projectively equivalent. But smooth members carry 40, 48 or 56 lines, so this is impossible.
- The extra class v (EXACT):
  - v.v = -32 and v.h = 0.
  - v.L is 0 on the 40 lines, +4 on the plus eight and -4 on the minus eight.
  - (sum of the minus eight) - (sum of the plus eight) = 2v.
  - N19 + Zv has index 8 in the 56-line lattice.

**6. Real lines along the real pencil (EXACT).**
- q(s - delta) = delta^4 - s^2 delta^2 + 4. So the 32 graph lines are all real for s > 2 and none is real for s < 2.
- Sturm counts at 15 values of s confirm this.
- The 16 special lines are real at s = +3/2^(1/4) and not real at -3/2^(1/4).
- So 56 / 40 / 24 / 8 is now EXACT.

**7. Fermat-type member, s = 0.**
- 48 lines: the 40 plus 8 in z2 = ±i z1, none of them real (EXACT).
- The lattice has rank 20, det -64 and Smith form [8,8] (numerical incidence, exact algebra).
- The class u has u.u = -2.

## Table (kappa^2 = s^4)

| kappa^2 | member | complex lines | Fano length | real, s>0 | real, s<0 | rank |
|---|---|---|---|---|---|---|
| 0 | Fermat type | 48 | 48 | 8 | 8 | 20 |
| other, below 16 | generic | 40 | 40 | 8 | 8 | 19 |
| 16 | wall | 24 | 40 | 24 | not computed | not computed |
| other, above 16 | generic | 40 | 40 | 40 | 8 | 19 |
| 81/2 | Y56 | 56 | 56 | 56 | 8 | 20 |
| non-real | generic | 40 | 40 | n/a | n/a | 19 (one sample) |

## Proved vs observed

Proved by exact computation:
- (i) Exactly 40 reduced lines for s^4 not in {0, 16, 81/2}.
- (ii) More than 40 lines only at s = 0 (48 lines) and at s^4 = 81/2 (56 lines).
- (iii) The 16 lines form one orbit; the 40 lines span a primitive sublattice of rank 19 and det 128, whose complement is generated by a class of square -32.
- (iv) Real counts: 8 for s < 2, 24 at s = 2, 40 for s > 2, and 56 at s = 3/2^(1/4).

Argued: constancy of the Gram matrix (5 numerical samples); the Torelli argument for rank 19; the Riemann-Roch step for the 48 conics.

Cited: NS(Y56) = the line lattice, with T = [2,0,32].

## Plain words

Think of one dial that reshapes the surface. Forty straight lines ride along the whole way. Another kind of line needs three conditions met with only two adjustable numbers, and that happens at only one dial setting on the real dial: Y56. Symmetry then makes 16 copies of it. Just off that setting the 16 lines are 48 gently curved conics, and at Y56 each conic snaps into a crossed pair of lines. Every surface in the family has 19 independent curve classes; Y56 has 20.

## Prior-art leads (ids resolve to these titles; content not re-read)

1601.04238; 1708.01219; 1706.05734; 1608.06746; 1212.3511; 0812.2377; math/0506416. No search was run for the pencil, for the 40-line configuration (rank 19, det 128), or for the jump set.

## Loose ends

1. Very general rank 19 rests on the Torelli argument, which is not refereed and has no mod-p check.
2. The constancy of the 40-line Gram matrix is checked numerically at 5 values only.
3. The 48 conics:
   - they exist by the lattice and Riemann-Roch argument;
   - only one family of 8 is explicit;
   - their reality and their place among the 148 two-line planes are not done.
4. Whether N19 is all of NS of the generic member is undecided.
5. kappa = infinity and the wall's lattice are not analysed.
6. The kappa^2 invariant and the 32 block symmetries are hand derivations. Extra symmetries at special members were not examined.
7. The rank at s = 0 uses numerical incidence.
8. Other Noether-Lefschetz points of the pencil were not located.
9. Not computed: real lines on the wall for s < 0, and real counts for the sister real structures.
10. No prior-art gate has been run.
11. Unused fano_*.sing files remain. _patch.py is a one-off helper.

Written with AI assistance.
