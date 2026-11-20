# Y56 exact, part 2: the 20 conic-pair planes and the name of the symmetry group

F = 3e z0^2 z1 z2 + 3e z1 z2 z3^2 - e z1^3 z2 - e z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3, e = sqrt2.
Scripts: code/exact2/ (e1.py, f1.py, l1.py, l2.py, l3.py, grp.g). Results file: data/conic_pair_planes_exact.txt.

## Headline
- EXACT-VERIFIED: 20 of 20 line-free conic-pair planes, all with normals in Q(sqrt2). No larger field needed.
- Orbits under the order-32 group: 8 + 8 + 4 (matches the expected 8+8+4).
- Symmetry group = SmallGroup(32,43) = C8 : (C2 x C2) = the holomorph Hol(C8) = C8 x| Aut(C8). Identified in GAP, not by table.
- Cross-check with the paper (arXiv 2407.00493 v2, Remark 7.4): Y56 has 188 + 448 = 636 conics and 20 planes.
  188 = 148 (one irreducible conic in each two-line plane) + 20 x 2. Our 148 + 20 x 2 = 188. It adds up.

## What went wrong in part 1, and the corrected list
Part 1 (EXACT.md) said only 1 of the 20 numeric "conic-pair" planes is a true line-free conic pair, and matched the other 19 to line planes.
That recognition was CORRECT; the earlier numeric file (not shipped) was what was wrong, in two ways:
1. The earlier numeric file of 20 "conic-pair" planes: re-deriving each plane normal at full precision (the plane spanned by the refined mp points,
   normal by 3x3 minors, NOT n0 + T u, because the float n0, T are only orthonormal to 1e-16) gives normals exact to 1e-59. All 20 are
   in Q(sqrt2) (PSLQ, tolerance 1e-50). Exact incidence with lines_exact.txt: 19 planes contain lines (2 lines in 10 of them, 4 lines in 9
   of them); only plane #4, n = (sqrt2-1 : (3-sqrt2)/7 : (3-sqrt2)/7 : 1), is line-free (called plane #4 in that file). In the 19 others at least one of the
   stored "conic" factors has relative det ~1e-61, i.e. it is a line PAIR. So "conic1 x conic2 with no lines" was false for 19 of the 20.
2. The 20 numeric planes are therefore not the 20 planes of the paper. Of the true 20 that file holds only one (the 8 images of it under
   the group were never found by the numeric solver: it is a random-start search that mostly converges to line planes).

Search that found the true 20 (search script not shipped; its result is checked exactly by code/exact2/e1.py and code/verify_all.py check 5a): every line-free conic-pair plane has a non-trivial stabiliser (an orbit of 32 planes is impossible with
only 20 planes in total), hence is fixed by one of the 15 projective involutions of the group. For each involution g, take the real
eigenspaces of g^-T (fixed planes: a point, a pencil, or a net), and run multi-start Levenberg-Marquardt over (plane in that family,
conic q1, conic q2) on the section = q1 q2, keeping only solutions with both conics non-degenerate (relative det > 1e-4).
Seeds 0 and 1 (40 + 300 tries per eigenspace) produced 20 distinct planes; closing them under the 32 exact symmetries gave still 20.

Exact representatives (plane n.z = 0):
- A (orbit 8): n = (sqrt2-1 : (3-sqrt2)/7 : (3-sqrt2)/7 : 1)   [the one found in part 1]
- B (orbit 8): n = (1 : (2 sqrt2-1)/7 : (1-2 sqrt2)/7 : 1-sqrt2)
- C (orbit 4): n = (0 : sqrt2/4 : 1 : 0)   i.e. the plane 4 z2 + sqrt2 z1 = 0
All 20 members (exact images of A, B, C under the 32 matrices of symmetry_exact.txt) are listed in conic_pair_planes_exact.txt, each with its two conics.
Verification for EVERY one of the 20 (e1.py, sympy, exact):
 (i) no line of lines_exact.txt lies in the plane (exact incidence over Q(sqrt2));
 (ii) factor_list of the plane section over Q(sqrt2) gives exactly two factors of degree 2, each of multiplicity 1;
 (iii) the 3x3 matrix of each conic has non-zero determinant (in Q(sqrt2)), so each conic is irreducible over C, not only over Q(sqrt2).
 So both conics are defined over Q(sqrt2). Examples: orbit A det = 51/49 + 39 sqrt2/49 and -5271/4 - 3717 sqrt2/4;
 orbit C det = +-3/4 (or +-3/32) for both conics.
PSLQ note: representatives were recognised from double-precision normals (PSLQ over {1, sqrt2}, coefficients < 2000, tolerance 1e-12) and then
PROVED by the exact factorisation above, so the 60-digit step was not needed for B and C. Only the 20 numeric planes of part 1 were redone at 60 digits.

## The group
The 32 maps in symmetry_exact.txt act faithfully on the 56 lines (permutations sigma). Loaded into GAP 4 (the SmallGroups library) as a permutation group on 56 points:
- IdGroup = [32, 43]; StructureDescription = C8 : (C2 x C2); verified isomorphic to the holomorph Hol(C8) = C8 x| Aut(C8) by a separate GAP construction (IdGroup [32,43]).
- exponent 8; centre C2; derived subgroup C4; abelianisation C2 x C2 x C2; Frattini subgroup C4; nilpotency class 3; 11 conjugacy classes; 3 generators.
- elements: order 1 x1, order 2 x15, order 4 x8, order 8 x8 (agrees with part 1).
- subgroups: order 2: 15; order 4: 19; order 8: 15; order 16: 7; order 32: 1. Conjugacy classes of subgroups: 1, 5, 9, 11, 7, 1.
- irreducible complex characters: degrees 1 (x8), 2 (x2), 4 (x1).
- Of the 51 groups of order 32, only SmallGroup(32,43) has this element-order spectrum together with |Z|=2 and |G'|=4.
Certainty: complete. The identification is a GAP IdGroup computation, not a hand table. Install: passagemath-gap (GAP + smallgrp data) into WSL Ubuntu user site; versions listed in requirements.txt.

## Loose ends (as of this note; see Addendum 3 for what was closed afterwards)
1. Completeness of the 20 planes rests on (a) the search finding exactly 20, closed under the group, and (b) the paper's count of 20. It is not an independent
   exhaustive proof: the search is multi-start numerics inside the fixed-plane families of the 15 involutions, and the argument that every plane has a non-trivial
   stabiliser uses the total of 20 from the paper. A fully independent proof would be a lattice computation (conic classes c with c^2=-2, c.h=2, c.L in {0,1}
   for all lines, h-c also irreducible: 40 classes = 20 planes) or a Groebner/dual-surface count of 4-nodal planes. The lattice route is done in Addendum 2, and its last gap is closed by citation in Addendum 3.
2. The earlier numeric file is mis-described by its own name (19 of its 20 "conic-pair" planes are line planes). It is not shipped; use
   data/conic_pair_planes_exact.txt instead. The old statement "only 1 is a genuine line-free pair, the other 19 never searched" is superseded by this note.
3. Representatives B and C were recognised at double precision, then exactly proved; no 60-digit numerics exist for the 19 new planes (not needed for the proof).
4. Two numeric-vs-exact items from part 1 stay open: the exact conic factors of the 148 two-line planes are verified, but their orbit structure beyond the sizes listed in EXACT.md was not re-derived here.
5. The conics of the 20 planes are real and defined over Q(sqrt2); whether each has a non-empty real point set was not checked here (the paper states the 636 conics are real).

## Addendum (follow-ups)
- Real points: all 40 conics of the 20 planes are INDEFINITE (leading minors of the exact 3x3 Gram matrix in plane coordinates, signs decided exactly in Q(sqrt2); none definite),
  so every conic has real points. Script code/exact2/f1.py. Loose end 5 closed.
- Orbit sizes re-derived from the 32 exact induced line permutations (the sigma of symmetry_exact.txt; each plane = its line set): 148 two-line planes: 32,16x6,8,8,4 (=148);
  50 four-line planes: 16,16,16,2 (=50). Orbit images stay inside the plane lists. Matches EXACT.md; Loose end 4 closed.
- The conic pictures were re-rendered with the corrected 40 conics (see media/y56_conics_v2_a.png and CORRECTIONS.md).

## Addendum 2 (amber match, completeness, sphere render)
- Amber match (script and numeric file not shipped): each of the 148 float amber conics matched to the exact conic factor Q of its two-line plane in planes_exact.txt
  (Q from factor_list over Q(sqrt2), section = L1*L2*Q, exactly degrees 1,1,2). 148/148, one-to-one onto 148 distinct planes. Max plane-normal deviation 6.6e-14;
  max deviation of the normalised 3x3 conic matrix 5.1e-12.
- Completeness (code/exact2/l1.py, l2.py, l3.py; the search scripts for (iii) are not shipped). NOT a closed unconditional proof; what is established:
  (i) Lattice N = Z-span of the 56 lines and h: rank 20, |disc| 64, h in the line span with integer coordinates, h^2 = 4. All vectors c in N with c.h=2, c^2=-2
      (PARI qfminim, exact integer arithmetic): 636 classes = 448 sums of two meeting lines + 188 irreducible conic classes (c is irreducible iff not such a sum);
      the 20 unordered pairs {c, h-c} with both irreducible = exactly 20 conic-pair planes. So IF NS(Y56) = N, conics on Y56 are at most 188 (rigid, one class each);
      we exhibit 188 distinct exact conics (148 + 40), so they are all of them, and the planes with two irreducible conics are exactly our 20.
  (ii) NS = N is not proved by our computation alone (closed by citation in Addendum 3). rank 20 is the K3 maximum, so NS is a finite-index overlattice of N. The discriminant group has order 64 and only 3 non-zero classes with q = 0 mod 2Z (all of order 4);
      each of the three corresponding overlattices would add NO new lines but MANY new degree-2 (-2)-classes (extra conics, 4828 vectors counted over the three), i.e. they would give more than 636 conics.
      The paper's 188+448 = 636 count (Remark 7.4) excludes them, but that again uses the paper; an independent exclusion would need a transcendental-lattice / period argument. Not done.
  (iii) Independent numerical evidence (NUMERICAL; scripts not shipped): an unrestricted multi-start search over ALL planes (no symmetry assumption, 12000 starts, 2 seeds) returned 673 solutions with both conics nondegenerate;
      all 673 match one of the 20 exact planes (max dist 5e-11) and all 20 were hit; none new.
- Render: media/y56_conics_v2_sphere.png (stereographic S^3 model, 56 lines + 148 amber + 40 violet, EXPLORATORY title).

## Addendum 3 (completeness closed by citation)
- Veniani, arXiv 1708.01219, Table 1 (opened): the row for Y56 reads |Oh| 64, |Sym| 32, |Sp| 16, det T = 64, T = [2, 0, 32].
  T is the orthogonal complement of the rank-20 configuration in the unimodular K3 lattice, so |disc NS(Y56)| = det T = 64.
- Our lattice N (56 lines and h) has rank 20 and |disc| = 64 (Addendum 2). A sublattice of index k has discriminant k^2 times larger, so k = 1: N = NS(Y56).
- So the enumeration in Addendum 2 is complete: exactly 188 irreducible conics and exactly 20 line-free conic-pair planes, all over Q(sqrt2).
  This uses the published det T (not the 188 + 448 = 636 count) and the standard conic-class criterion. Status: exact lattice computation plus one cited input.
  The extra-overlattice worry in Addendum 2 (ii) is closed by this citation; no independent transcendental-lattice argument was made.

Note on data/planes_exact.txt: its last section header, "from the 20 numeric plane-pairs", refers to the superseded numeric list. The coordinates in that section (one plane, n = (sqrt2-1 : (3-sqrt2)/7 : (3-sqrt2)/7 : 1)) are the exact ones and equal orbit representative A of data/conic_pair_planes_exact.txt. The file is shipped byte-identical to its source and the header is left as is.
