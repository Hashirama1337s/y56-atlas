# Y56 exact skeleton (line / conic structure) - EXACT over Q(sqrt2)

Quartic F = 3e z0^2 z1 z2 + 3e z1 z2 z3^2 - e z1^3 z2 - e z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3, e = sqrt(2).
Status: EXACT-VERIFIED (sympy symbolic, all counts below). Numerics only used to guess coordinates.

## Field
Everything (lines, planes, symmetry matrices) lives in Q(sqrt2). No larger field was needed.

## 1. Lines: 56 / 56 exact-verified
Each line = span of two points with coordinates in Q(sqrt2) (RREF, entries found by PSLQ on 65-digit refined numerics, then
checked against the numerics to 1e-40). Verification: substitute z = t*P0 + P1 into F, expand, radsimp -> identically 0, for all 56.
Distinctness: exact Plucker coordinates pairwise non-proportional (56 distinct).
Intersection graph: 448 edges, 16-regular (exact determinant test, reduced mod s^2-2).
File: data/lines_exact.txt (L00..L55).

## 2. Planes
Method for each plane n.z=0: parametrise, substitute into F, sympy factor_list over Q(sqrt2), check factor degrees; for conic
factors check the 3x3 matrix determinant is nonzero (non-degenerate).
- 148 planes with EXACTLY 2 lines (planes spanned by an intersecting line pair with no other line): section = L1 * L2 * Q, Q an
  irreducible non-degenerate conic over Q(sqrt2). 148/148 exact-verified (they also match an earlier numeric search, not shipped).
- 50 planes with 4 lines (section = 4 lines, all in the 56). 148 + 6*50 = 448 = all graph edges, so no other coplanar line pair.
- SUPERSEDED (see EXACT-2.md): an earlier numeric identification of the "20 plane-pair planes" was wrong (it mixed two-line and four-line planes into the list). The correct result is in EXACT-2.md: exactly 20 line-free planes, each cutting two irreducible conics over Q(sqrt2), with exact normals and factorisations in data/conic_pair_planes_exact.txt (orbit sizes 8 + 8 + 4).
File: data/planes_exact.txt.

## 3. Symmetry
- Automorphism group of the 56-vertex, 448-edge graph (networkx VF2, full enumeration): order 64.
- Realised by real projective maps with F(Mz) = c F(z): exactly 32 of the 64 (other 32 admit no projective map at all, checked by
  linear solve). All 32 matrices recognised exactly in Q(sqrt2) and verified symbolically (F(Mz) - cF = 0): 32/32.
  File: data/symmetry_exact.txt (matrix, scalar c, induced line permutation).
- Group (acts faithfully on lines): order 32, non-abelian, centre order 2, derived subgroup order 4;
  element orders: 1 x1, 2 x15, 4 x8, 8 x8 (an order-8 element exists).
- Orbits on the 56 lines: 8 + 16 + 16 + 16 (NOT 32/24).
- Orbits on the 148 two-line planes: sizes 4, 8, 8, 16 x6, 32 (sum 148). On the 50 four-line planes: 2, 16, 16, 16.
  The 20 line-free conic-pair planes (EXACT-2.md) form orbits of sizes 8, 8, 4.

## Plain words
All 56 real lines of this surface, the 148 planes that carry exactly two lines plus a conic, and the 50 planes carrying four lines
have coordinates using only whole numbers and sqrt(2), and each was checked as an exact algebraic identity, not a decimal match.
The surface has a symmetry group of 32 real transformations; they split the lines into four families (8, 16, 16, 16).

## What was left open here, and where it was closed
- The name of the order-32 group, and the search for the line-free conic-pair planes: both are done in EXACT-2.md (group = SmallGroup(32,43); exactly 20 line-free planes).
- The one-command re-check of the exact data is code/verify_all.py (recorded output: docs/VERIFY-RUN.txt).
