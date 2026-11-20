# Y56 Lean report (kernel-checked finite facts)

Moki & Julio (AI-assisted) · 2026

Lean 4 (v4.36.0-rc2) with Mathlib (v4.36.0-rc2), run through a checking script under a 12 GB memory cap. Every file passed: no sorry, admit, axiom declaration or native_decide, and every theorem's `#print axioms` lists only standard axioms. Across the 10 positive files the 524 theorems print: none (1), propext (148), propext + Quot.sound (283), propext + Classical.choice + Quot.sound (92). Every finite computation uses `decide +kernel` on `Zsqrtd 2`, which is Z[sqrt 2] with kernel-evaluated arithmetic. Every polynomial identity uses `ring` or `linear_combination` with an explicit cofactor. Nothing relies on a trusted computer algebra system: the exporter's certificates are only hints, and the kernel re-checks each one.

The bridge to geometry is `iota s hs : Z[sqrt 2] ->+* R`, which sends sqrt 2 to any `s` with `s*s = 2`. It is injective whenever R has characteristic 0 (`iota_injective`, from Mathlib's `Zsqrtd.lift_injective`). So each statement holds over R and C, with s = sqrt 2.

"Time" below is the wall time of the recorded run, which includes about 18 s to load Mathlib.

## Results

| item | file | time | headline theorems |
|---|---|---|---|
| L1 | Y56_L1.lean | 29 s | lines_on_F, lines_distinct, lines_genuine |
| L7 | Y56_L7.lean | 19 s | eightfold, screw, screw_coord, galois_twist |
| Pencil | Y56_Pencil.lean | 18 s | pencil_forces, pencil_solvable |
| L2 | Y56_L2.lean | 114 s | sym_g00..sym_g31, maps_lines, group_facts, group_closed, matrices_compose, order_counts, orbit_sizes |
| L3 | Y56_L3.lean | 43 s | meets_iff_edge, edge_counts |
| L6 | Y56_L6.lean | 90 s | planes_lines, plane_rows, inPlane_iff_listed, line_in_plane_iff, pc_rows, dist_rows, plane_pairs_are_edges, edge_cover |
| L5 (148 two-line planes) | Y56_L5a.lean | 31 s | secP2_000..147, conics_nondegenerate, conic_irreducible |
| L5 (50 four-line planes) | Y56_L5b.lean | 25 s | secP4_000..049 |
| L5 (20 conic-pair planes) | Y56_L5c.lean | 22 s | secPC_000..019, conics_nondegenerate |
| L8 | Y56_L8.lean | 42 s | det_GB, rows_in_span, hyperplane_class |

## What each theorem says (plain words)

**L1**
- **lines_on_F.** Take any commutative ring with s*s = 2 and any of the 56 lines i. For all l, m, the point l*u_i + m*v_i satisfies F = 0. Proof:
  - `ring` gives a generic expansion of F(l u + m v) into 5 coefficients;
  - the kernel evaluates all 280 coefficients in Z[sqrt 2] and finds 0.
- **lines_distinct.** Over any characteristic-0 ring with s*s = 2: for i ≠ j, the spanning vectors of line i are not both linear combinations of those of line j. So the 56 lines are pairwise different. A 3x3 minor witness is checked for all 3080 ordered pairs.
- **lines_genuine.** Over a characteristic-0 domain: u_i and v_i are linearly independent, so each entry really is a line.

**L7**
- **eightfold.** Over the reals: F(z) = Im(w^4) + Im(p^2)(3|w|^2 - |p|^2)/sqrt 2, with w = z0 + i z3 and p = z1 + i z2.
- **screw.** G(zeta w, i p) = -G(w, p), with zeta = (1+i)/sqrt 2.
- **screw_coord.** Over any ring with s*s = 2: F(z0 - z3, -s z2, s z1, z0 + z3) = -4 F(z).
- **galois_twist.** F_e(z0, -z2, z1, z3) = F_{-e}(z), as a pure ring identity.

**Pencil** (new item from ../pencil/REPORT.md, finding 3)
- **pencil_forces.** Over ANY commutative ring (characteristic 0 is not even needed), the three equations force s = 3 beta^2, alpha^2 = 2 beta^2, 2 beta^8 = 1 and 2 s^4 = 81. The certificate is an explicit chain of six `linear_combination` steps. Its key move: alpha*beta is a unit modulo the third equation, with inverse -beta^2.
- **pencil_solvable.** The converse: a real solution exists, with beta = (1/2)^(1/8), alpha = -2 beta^5 and s = 3 beta^2.

**L2**
- **sym_gXX** (32 theorems). Over any ring with s*s = 2: F(M_g z) = c_g F(z), for the matrix and c listed in symmetry_exact.txt.
- **maps_lines.** Over a characteristic-0 field: M_g sends both spanning vectors of line i into line sigma_g(i). This is checked by Cramer for all 32 x 56 x 2 cases.
- **group_facts.** The following hold:
  - sigma_0 is the identity;
  - every sigma_g is a permutation of the 56 lines;
  - the 32 permutations are pairwise distinct;
  - every element has an inverse in the set.
- **group_closed.** The set is closed under composition: sigma_(tab g h) = sigma_g o sigma_h for all 1024 pairs.
- **matrices_compose.** M_g M_h is a nonzero multiple of M_(tab g h).
- **order_counts.** Element orders: 1 x1, 2 x15, 4 x8, 8 x8.
- **orbit_sizes.** The line orbits have sizes 16, 16, 8 and 16, with representatives L00, L01, L02 and L03. Every line lies in exactly one of them. So the orbit sizes are 8 + 16 + 16 + 16.

**L3**
- **meets_iff_edge.** Over a characteristic-0 domain, for i ≠ j: lines i and j share a nonzero point exactly when {i, j} is an edge of edges.json.
  - For an edge, an explicit common point is computed in the kernel.
  - For a non-edge, the 4x4 determinant det[u_i; v_i; u_j; v_j] is nonzero, and the Cramer identities (`ring`) exclude a common point.
- **edge_counts.** The graph has 448 edges and is 16-regular:
  - the neighbour lists are symmetric, loop-free and have 16 entries each;
  - they reproduce edges.json exactly;
  - so 1092 pairs of distinct lines are skew.
- The incidence types (4,4) x32 and (3,7) x24 were not done (see Loose ends).

**L6**
- **planes_lines** and **plane_rows / inPlane_iff_listed.** For each of the 198 stored planes, the lines it contains (computed from coordinates) are exactly the listed ones: 148 planes contain exactly 2 lines and 50 contain exactly 4.
- **line_in_plane_iff.** Gives the same fact for points over R.
- **pc_rows.** The 20 conic-pair planes contain no line.
- **dist_rows.** All 218 planes are pairwise different.
- **plane_pairs_are_edges.** Every pair of lines in a common stored plane is an edge, and 148*1 + 50*6 = 448.
- **edge_cover.** Each of the 448 edges lies in exactly one stored plane.

**L5**
- **secP2 / secP4 / secPC.** Over any ring with s*s = 2, for every plane, K * F(x p1 + y p2 + w p3) equals:
  - C * l1 * l2 * Q for the 148 two-line planes;
  - C * l1 l2 l3 l4 for the 50 four-line planes;
  - C * Q1 * Q2 for the 20 conic-pair planes.

  Here p_c = n_k e_c - n_c e_k spans the plane n.z = 0, and l_i is the equation of line i in plane coordinates (cross product).
- **conics_nondegenerate.** All 148 + 40 conics have a nonzero Hessian determinant in Z[sqrt 2].
- **conic_irreducible.** Such a conic is not a product of two linear forms over any characteristic-0 ring with s*s = 2, so it is irreducible over C.

**L8**
- **det_GB.** For the 20 lines L00..L16, L18, L19, L20, the 20x20 intersection matrix has `Matrix.det` = -64. Proof by an integer triangular certificate (A GB = T with A lower and T upper triangular) and `Matrix.det_mul`.
- **rows_in_span.** Every row of the 56x56 intersection matrix (-2 on the diagonal, 1 for an edge) is an integer combination of the 20 basis rows. So the lattice spanned by the line classes is free of rank 20 with discriminant -64.
- **hyperplane_class.** For h = L00 + L06 + L23 + L24 (a four-line plane): h.h = 4, and h.L = 1 for every line L.
- The -2 self-intersection of a line is cited (adjunction on a K3), not proved.

## Controls

Every item has a positive control: the true file passes the check. Each negative control below changes one input, and Lean rejects it. The error text is kept in `<name>_neg.expected-error.txt`.

| negative control | what was changed | how Lean failed |
|---|---|---|
| L1_neg | U[17][1] + 1 | `decide` proved the proposition false (coeffs_all) |
| L7_neg | galois_twist claimed without the sign change of e | ring: unsolved goals |
| Pencil_neg | claims 2 s^4 = 80 | ring failed |
| L2_neg | swapped 2 entries in row 1 of M_g05 | sym_g05 unsolved goals; span_all and others: decide false (10 errors) |
| L3_neg | one edge dropped | meet_all and edge_counts: decide false (3 errors) |
| L6_neg | one plane deleted | edge_cover and plane_pairs fail (2 errors) |
| L5c_neg | one conic coefficient 14 changed to 15 | ring failed |
| L8_neg | one adjacency entry changed | AG_entries and rel_rows: decide false (7 errors) |

## Files

All files are in this folder (see README.md for the build):
- `export_lean.py` generates every data-driven .lean file and the negative controls. It reads only the shipped text files in ../core/data. Run it as `python export_lean.py L1 L2 L3 L5 L6 L8 neg`.
- `Y56_L7.lean` and `Y56_Pencil.lean` were written by hand.
- `run_all.sh` reruns every check with standard `lake` commands. The recorded run of the checking script (theorem lists and `#print axioms` output for every theorem) is `recorded-run.log`.
- The .lean files contain no local paths and no AI or product names (scanned).

## Loose ends

- These items were not done: L4 (smoothness certificate), L9 (Hol(C8) identification, plane-orbit tables), L10 (real conics), L11, L12 (wall nodes, two-conic identity, Fermat bridge), L13 and L14. The L3 incidence types (4,4) x32 and (3,7) x24 were also not done, because their definition still has to be copied from EXACT.md.
- In L2, the explicit sym_gXX theorems and the table MS used by maps_lines and matrices_compose come from the same parse of symmetry_exact.txt. No Lean proof links the two printouts; the release referee compared them by script: identical (`checks/atlas-referee/ref_lean_data.out`).
- L5 recomputes the conics in its own plane coordinates. They were not compared with the Q1/Q2 strings in conic_pair_planes_exact.txt, which use a different parametrisation.
- Some standard geometric facts are not formalised:
  - "two distinct meeting lines span exactly one plane", so "no other plane contains 2 lines" rests on it together with edge_cover;
  - "a nondegenerate conic, or a non-proportional Pluecker pair, is the geometric statement", which is said in words only.
- L8 proves the Gram data of the line lattice only. NS(Y56) = N and the -2 self-intersections are cited, not proved.
- Large kernel checks are split into chunks, because unchunked they hit the 12 GB cap (bad_alloc or stack overflow). Peak memory with chunks is 9.2 to 10.5 GB.
- Lean warns about the deprecated names `Matrix.det_of_lowerTriangular` and `det_of_upperTriangular` in L8. These are warnings only.
- In the shipped `*_neg.expected-error.txt` files the local folder prefix was removed from the error locations and the memory-cap wrapper line was dropped; the error texts are otherwise as recorded.
- A referee matched every theorem statement with the sentence that quotes it in the paper (`checks/atlas-referee/REFEREE-ATLAS.md`).

Written with AI assistance.
