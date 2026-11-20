# Results

Moki & Julio (AI-assisted) · version 1.0

Y56 is the real smooth quartic surface F = 0 with e = sqrt2:

F = 3e z0^2 z1 z2 + 3e z1 z2 z3^2 - e z1^3 z2 - e z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3

and the pencil through it is G_s = Im(w^4) + Im(p^2)(s|w|^2 - |p|^2) with w = z0 + i z3, p = z1 + i z2; Y56 is the member s^4 = 81/2 after z1, z2 are rescaled by 2^(1/8).

Status labels: **EXACT** (exact arithmetic over Q(sqrt2), Q, Q(s) or exact integers, by the scripts shipped here or by the named program), **LEAN-CHECKED** (the statement as written in Lean 4 with Mathlib is accepted by Lean's kernel with standard axioms only; the theorem is named), **CITED** (taken from a published source, named), **NUMERICAL** (floating point; support only), **ARGUED** (a proof or proof sketch written out, not machine-checked). Programs (Singular, msolve, GAP, PARI, sympy, networkx) are trusted software, not proof assistants. The column "Lean" says which part of a claim is kernel-checked; "none" means the claim rests on the other evidence only.

R1 to R19 are the claims of the core (`core/`); P1 to P11 are the claims of the pencil (`pencil/`), with P1 to P9 the refereed theorem (`pencil/RESULT.md`); X1 is an identity used throughout. Lean files are in `lean/`; theorem names refer to the namespace `Y56`.

## Scorecard

| id | claim | status | Lean |
|---|---|---|---|
| R1 | Y56 is smooth over C | EXACT (Singular) | none (smoothness certificate not done) |
| R2 | 56 distinct lines with exact coordinates in Q(sqrt2) | EXACT | `lines_on_F`, `lines_distinct`, `lines_genuine` (Y56_L1) |
| R3 | exactly 56 lines over C, all real, reduced Fano scheme | EXACT (Singular); msolve cross-check probabilistic; count CITED | lower bound only (Y56_L1); "no 57th line" not in Lean |
| R4 | 448 meeting pairs, each line meets 16 others | EXACT | `meets_iff_edge`, `edge_counts` (Y56_L3) |
| R5 | 148 planes with exactly two lines; section = line x line x irreducible nondegenerate conic | EXACT | `planes_lines`, `inPlane_iff_listed` (Y56_L6); `secP2_000..147`, `conics_nondegenerate`, `conic_irreducible` (Y56_L5a) |
| R6 | 50 planes with four lines; 148 + 6 x 50 = 448 | EXACT | `plane_pairs_are_edges`, `edge_cover` (Y56_L6); `secP4_000..049` (Y56_L5b) |
| R7 | 20 line-free planes cutting two irreducible conics (40 conics) | EXACT | `pc_rows`, `dist_rows` (Y56_L6); `secPC_000..019`, `conics_nondegenerate` (Y56_L5c) |
| R8 | all 188 irreducible conics have real points | EXACT | none |
| R9 | exactly 636 conics (448 + 188) and 20 conic-pair planes | EXACT lattice computation + CITED determinant | Gram data only: `det_GB`, `rows_in_span`, `hyperplane_class` (Y56_L8); enumeration and NS = N not in Lean |
| R10 | 12000-start search finds nothing outside the 20 planes | NUMERICAL | n/a |
| R11 | 32 real projective symmetries, acting faithfully on the lines | EXACT; order CITED | `sym_g00`..`sym_g31`, `maps_lines`, `group_facts`, `group_closed`, `matrices_compose` (Y56_L2) |
| R12 | line graph has 64 automorphisms; the extra 32 come from the Galois twist | EXACT; count CITED | the twist identity only: `galois_twist` (Y56_L7) |
| R13 | the group is SmallGroup(32,43) = Hol(C8) | EXACT (GAP) | element orders only: `order_counts` (Y56_L2) |
| R14 | orbits: lines 8 + 16 + 16 + 16; planes 32, 16 x 6, 8, 8, 4 / 16, 16, 16, 2 / 8, 8, 4 | EXACT | line orbits only: `orbit_sizes` (Y56_L2) |
| R15 | six real faces: 56 / 12 / 8 / 4 / 0 / 0 real lines, class sizes 1, 4, 1, 4, 4, 2 | EXACT; number six CITED | none |
| R16 | real conics on the six faces: 188 / 14 / 12 / 12 / 28 / 28, with an oval 188 / 10 / 8 / 8 / 22 / 20 | EXACT | none |
| R17 | real parts: genus 10; genus 2 (three faces); three spheres (two faces) | EXACT (two methods) + CITED classification; meshes NUMERICAL | none |
| R18 | the three genus-2 faces form one deformation family, the two three-sphere faces another | CITED (with EXACT inputs) | none |
| R19 | pictures | renderings, not evidence | n/a |
| X1 | the eight-fold form of F and the eighth-turn screw | EXACT | `eightfold`, `screw`, `screw_coord` (Y56_L7) |
| P1 | X_s is smooth exactly when s^4 != 16; the wall members are singular, with exactly 8 nodes at s = +-2 | EXACT | none |
| P2 | every member carries the 32 block symmetries; 16 act symplectically, forming SD16 | EXACT; match CITED | none (the Y56 member's 32 symmetries: Y56_L2) |
| P3 | every smooth member has Picard rank at least 19 | CITED corollary (Hashimoto) | none |
| P4 | exactly 40 lines on every smooth member except s = 0 (48) and s^4 = 81/2 (56, Y56); reduced Fano scheme | EXACT; reducedness ARGUED | none |
| P5 | the 40 persistent lines span N19: rank 19, det 128, Smith [2,8,8], signature (1,18), primitive | EXACT lattice data; constancy ARGUED | none |
| P6 | rank exactly 19 for the very general member (Bouyer's method: T(X_0) and T(Y56) differ) | ARGUED with CITED lattices | none |
| P7 | Y56 is a Noether-Lefschetz point: v with v^2 = -32 on the 16 lines of orbit S, which exist only where 2s^4 = 81 | EXACT | the algebra after substitution: `pencil_forces`, `pencil_solvable` (Y56_Pencil) |
| P8 | 48 conic classes L+ + L- in N19, irreducible on a generic member, splitting into line pairs at Y56 | EXACT lattice; effectivity CITED (Riemann-Roch) | none |
| P9 | real lines along real s: 8 for \|s\| < 2 and s < -2; 24 at s = 2; 40 for s > 2, s != s*; 56 at s* | EXACT | none |
| P10 | NS of the very general member is exactly N19 | EXACT enumeration + ARGUED primitivity; not refereed separately | none |
| P11 | the 16 symplectic maps form SmallGroup(16,8) = QD16 = SD16 | EXACT (GAP IdGroup) | none |

Totals: 19 core claims, 11 pencil claims and one identity (31 rows); 13 of them are LEAN-CHECKED in whole or in part (R2 to R7, R9, R11 to R14, X1 and P7; the column says which part). The paper (`PAPER.md`) also states the facts about the wall, the Fermat end and the faces along the pencil (sections 7.4 to 7.6), with their evidence in `family/`.

## The core (R1 to R19)

Carried over from the refereed core release; paths are now under `core/`. Lean coverage is in the scorecard above.

### The 21 checks of verify_all.py

"Check" numbers refer to the 21 checks printed by `core/code/verify_all.py` (line numbers are lines of that file; recorded output in `core/docs/VERIFY-RUN.txt`). Checks marked "transcript" are recorded program outputs that `verify_all.py` does not re-run.

| check | line | what it tests |
|---|---|---|
| data loads | 55 | 56 lines, 32 symmetries, 148 + 50 line planes, 20 conic-pair planes |
| 1a, 1b | 59, 61 | each of the 56 lines lies on F = 0 (F(tA+B) is identically 0); the 56 lines are distinct |
| 2a, 2b | 68, 71 | 448 meeting pairs, 16-regular; `core/data/edges.json` equals the recomputed edge list |
| 3a, 3b, 3c, 3d | 83, 84, 87, 96 | 32 matrices with F(Mz) = cF(z); each maps line i to line sigma[i]; the 32 permutations form a group; line orbits 16 + 16 + 16 + 8 |
| 4a to 4e | 104, 107, 111, 130, 136 | the 448 meeting pairs lie in 148 two-line and 50 four-line planes; shipped plane list equals the recomputed one; each plane contains exactly its listed lines; sections factor as line x line x conic (148) and four lines (50) |
| 5a, 5b | 156, 158 | the 20 line-free planes: section = constant x Q1 x Q2 with Q1, Q2 irreducible and nondegenerate over Q(sqrt2); none of the 56 lines lies in them |
| 6a, 6b | 165, 167 | all 40 and all 148 conics have real points (Gram matrix not definite, signs exact) |
| 7a, 7b, 7c | 172, 173, 183 | plane orbits: 148 two-line planes 32, 16 x 6, 8, 8, 4; 50 four-line planes 16, 16, 16, 2; 20 conic-pair planes 8, 8, 4 |

### Claims

**R1. Y56 is smooth over C.**
Status: EXACT (Singular). The ideal of the partial derivatives has an affine cone of dimension 0 and quotient dimension 81 = 3^4, and F lies in it.
Where: `core/data/logs/smooth.out`, `core/code/exact3/smooth.sing`, `core/docs/LINES-COUNT.md`. Transcript.

**R2. Y56 contains 56 distinct lines whose coordinates are exact in Q(sqrt2).**
Status: EXACT. Each line is substituted into F and the result is identically zero; the 56 lines are pairwise distinct.
Where: `core/data/lines_exact.txt`; verify_all.py checks 1a, 1b (lines 59, 61).

**R3. Y56 has exactly 56 lines over C: no 57th line, real or complex; all 56 are real, over Q(sqrt2), and the Fano scheme is reduced.**
Status: EXACT (Singular Groebner basis over Q(sqrt2), trusted software); cross-check by msolve in its default Monte Carlo (probabilistic) mode. Singular: the Fano scheme has degree 56 in the main chart, and no line lies outside that chart (std(I + p01) = 1 in the other five charts). msolve (a different coordinate change, sqrt2 handled by a variable s with s^2 = 2): degree 112 = 2 x 56 and 112 real roots, 56 with s > 0. The lower bound 56 comes from R2.
Where: `core/data/logs/fano_rerun.out`; `core/data/logs/analyze.log`, `par_01.out`, `real_01.out`, `gb_01.out`; `core/docs/LINES-COUNT.md`, `core/docs/LINES-COUNT-2.md`. Transcripts. msolve ran in its default Monte Carlo mode.
Credit: the count 56 is published (DIS, section 9.2 with Theorem 1.1; Corollary 1.3).

**R4. The 56 lines meet in 448 pairs and each line meets exactly 16 others.**
Status: EXACT. Where: verify_all.py checks 2a, 2b (lines 68, 71).
The incidence types (4,4) for 32 lines and (3,7) for 24 lines are CITED (arXiv 1601.04238, Lemma 6.14); we use them only to colour the pictures.

**R5. 148 planes contain exactly two lines; each section is line x line x an irreducible nondegenerate conic over Q(sqrt2).**
Status: EXACT. Where: `core/data/planes_exact.txt`; verify_all.py checks 4a, 4b, 4c, 4d (lines 104 to 132). Check 4d tests that the conic is irreducible over Q(sqrt2) (factorisation) and also that it is nondegenerate (the exact determinant of its 3x3 symmetric matrix is nonzero, for all 148).

**R6. 50 planes contain exactly four lines, and 148 + 6 x 50 = 448 accounts for every meeting pair.**
Status: EXACT. Where: `core/data/planes_exact.txt`; checks 4a, 4e (lines 104, 137).

**R7. 20 planes contain no line and cut two irreducible conics each (40 conics), all over Q(sqrt2); exact normals and factorisations are listed.**
Status: EXACT. Where: `core/data/conic_pair_planes_exact.txt`; checks 5a, 5b (lines 157, 159); `core/docs/EXACT-2.md`. The orbit representatives are A and B (orbits of 8) and C (orbit of 4).

**R8. All 188 irreducible conics (148 + 40) have real points.**
Status: EXACT (exact sign of the Gram matrix in Q(sqrt2)). Where: checks 6a, 6b (lines 166, 168).

**R9. Completeness: Y56 has exactly 636 conics (448 pairs of meeting lines and 188 irreducible conics) and exactly 20 line-free conic-pair planes.**
Status: EXACT lattice computation plus one CITED input. The lattice N spanned by the 56 lines and the hyperplane class has rank 20 and |disc| 64; all vectors with c.h = 2 and c^2 = -2 are 636 classes, 448 sums of two meeting lines and 188 others; exactly 20 pairs {c, h - c} have both members irreducible. That N is the whole Neron-Severi lattice uses the published row for Y56 in Veniani, arXiv 1708.01219, Table 1 (det T = 64, T = [2, 0, 32]). The total 636 and the number 20 are also published (Degtyarev, arXiv 2407.00493, Remark 7.4); our argument does not use them.
Where: `core/data/lat.txt`, `core/data/lat_lines.txt`, `core/code/exact2/l1.py`, `l2.py`, `l3.py`; rank 20 and det -64 in `core/data/logs/s2_lattice.log`; `core/docs/EXACT-2.md` Addenda 2 and 3. verify_all.py does not re-run it; transcripts of l2.py and l3.py are data/logs/l2.log and data/logs/l3.log.

**R10. Numerical support for R9.** An unrestricted search over all planes (12000 starts, two seeds) returned 673 solutions with two nondegenerate conics; all 673 match one of the 20 exact planes and all 20 were hit.
Status: NUMERICAL. Where: `core/docs/EXACT-2.md` Addendum 2; the scripts are not shipped.

**R11. The symmetry group has order 32: 32 real projective maps with F(Mz) = cF(z), c in {1, -1, 4, -4}, acting faithfully on the lines.**
Status: EXACT (our check). The order 32 is also published and CITED (arXiv 1601.04238, Proposition 9.9; Veniani, 1708.01219, Table 1).
Where: `core/data/symmetry_exact.txt`; checks 3a, 3b, 3c (lines 83 to 87); `core/data/logs/s1_group.log`.

**R12. The line graph has 64 automorphisms; 32 are induced by projective maps and 32 are not.**
Status: EXACT count. The count 64 is also published: Veniani, arXiv 1708.01219, Table 1, column |O_h(S)| (permutations of the lines preserving intersections, section 3.3). The 64 come from a full enumeration by networkx; for each, the linear conditions for a projective map were solved exactly over Q(sqrt2): 32 have a one-dimensional solution and 32 have none.
Where: `core/data/logs/s1_group.log`, `core/code/exact/aut.py`, `core/docs/SISTERS.md` section 1.
The explanation of the other 32 is an exact identity: swapping sqrt2 and -sqrt2 (a Galois twist), followed by the quarter-turn (z1, z2) -> (-z2, z1), maps the surface to itself and permutes the 56 lines, so every symmetry of the line graph comes from a map of the surface defined over Q(sqrt2) (semilinear for the extra 32). Exact check, in `core/code/exact/galois_twist.py` (transcript `core/data/logs/galois_twist.log`): it recomputes all 64 graph automorphisms (networkx) and reads the 32 realised permutations from `core/data/symmetry_exact.txt`; then F(Ry) = F^Gal(y) holds identically (not minus), the twist tau permutes the 56 lines, tau is a graph automorphism that is not realised projectively, and tau times the 32 realised permutations is exactly the other 32. A second count of 64 by a different algorithm (igraph/bliss, the same 64 as a set) is now shipped: `family/faces/a_aut.py` and `a_aut.log`; the core referee found 64 by a third, own backtracking search (`checks/core-referee/ref_extra.out`). The identity F(Ry) = F^Gal(y) is LEAN-CHECKED (`galois_twist`).

**R13. The group is SmallGroup(32,43) = C8 : (C2 x C2) = the holomorph Hol(C8).**
Status: EXACT (GAP IdGroup and IsomorphismGroups; trusted software). Element orders 1 x1, 2 x15, 4 x8, 8 x8; centre C2; derived subgroup C4; 11 conjugacy classes.
Where: `core/data/gap_out.txt`, `core/code/exact2/grp.g`, `core/docs/EXACT-2.md`. Transcript. We did not search the literature for this name.

**R14. Orbits of the group.** On the 56 lines: 8 + 16 + 16 + 16. On the 148 two-line planes: 32, 16 x 6, 8, 8, 4. On the 50 four-line planes: 16, 16, 16, 2. On the 20 conic-pair planes: 8, 8, 4.
Status: EXACT. Where: checks 3d, 7a, 7b, 7c (lines 96, 173, 174, 184).

**R15. Six real faces.** A real structure is conjugation composed with an involution of the group; up to conjugacy there are six (16 real structures in all), in classes of sizes 1, 4, 1, 4, 4, 2 with 56, 12, 8, 4, 0, 0 real lines respectively.
Status: EXACT. The number six is also published (arXiv 1601.04238, Remark 9.10); the maximality of 56 and the uniqueness of Y56 are Corollary 1.3 there.
Where: `core/data/logs/s1_group.log`; `core/docs/SISTERS.md` section 1.

**R16. Real conics on the six faces** (in the order 56 / 12 / 8 / 4 / 0 / 0 lines): 188 / 14 / 12 / 12 / 28 / 28 conics invariant under the conjugation; of these, 188 / 10 / 8 / 8 / 22 / 20 have a real oval, the rest have no real points. In the zero-line face with 22 ovals, 4 further conics in fixed planes are swapped in pairs by the conjugation and are not counted.
Status: EXACT. Where: `core/data/logs/s3_conics.log`; `core/docs/SISTERS.md` section 2.

**R17. Topology of the real part, in the same order:** one connected surface of genus 10; one of genus 2 (three faces: 12, 8 and 4 lines); three spheres (two faces: 0 lines).
Status: EXACT by two methods that agree: the Lefschetz trace formula (Euler numbers -18, -2, -2, -2, 6, 6) and the lattice invariants with the Nikulin-Kharlamov classification (CITED, not re-proved). Meshes at grid sizes 160 and 260 give the same result (NUMERICAL cross-check). The standard face with genus 10 is also published (arXiv 1601.04238, Proposition 9.12) and is our positive control.
Where: `core/data/logs/s2_lattice.log`, `core/data/logs/s4_mesh_160.log`, `core/data/logs/s4_mesh_260.log`; `core/docs/SISTERS.md` section 3. The completeness input is the same cited lattice row as R9.

**R18. The three genus-2 faces (12, 8, 4 lines) are one deformation family of real quartics, and the two three-sphere faces are one.**
Status: CITED (Kharlamov's rigid-isotopy classification, as summarised in the Degtyarev-Kharlamov survey, arXiv math/0004134, section 3.5.4), with exact inputs (the real parts, and real lines in the genus-2 faces). No explicit deformation path was built; the class counts were read from tables in a rendered page.
Where: `core/docs/SISTERS.md` section 6, item 1.

**R19. Pictures.** Status: exploratory renderings of exactly verified data. Where: `core/media/`, captions in `core/media/CAPTIONS.md`; the pencil pictures are in `media/` with `media/CAPTIONS.md`. Pictures are not evidence for any claim above.

## The pencil (P1 to P11)

P1 to P9 are the refereed statement (`pencil/RESULT.md`); a hostile referee re-derived them with independent code (`checks/pencil-referee/`). P10 and P11 were added afterwards.

**P1. Smoothness.** X_s = {G_s = 0} is a smooth quartic K3 surface exactly when s^4 != 16; the discriminant is a constant times (s-2)(s+2)(s^2+4). The wall members are singular; at s = +-2 (the same surface up to (z1,z2) -> (i z1, i z2)) they have exactly 8 ordinary nodes; at s = +-2i the node count is not computed exactly.
Status: EXACT. Where: `checks/pencil-referee/r3_disc.log`; three-parameter form `family/faces/c_fam.log`; the wall `family/wall/w1.log`. Lean: none.

**P2. Symmetry.** Every member carries the 32 block symmetries; exactly 16 act symplectically (det(M)/c = +1), forming SD16, the symplectic group recorded for Y56 by Degtyarev and Rams (arXiv 2301.04127, Table 1).
Status: EXACT; match CITED. Where: `checks/pencil-referee/ref_sympl.py`; P11. Lean: none for the pencil (for Y56 itself the 32 symmetries are `sym_g00`..`sym_g31`).

**P3. Rank at least 19.** Hashimoto's Table 10.1 (arXiv 1012.2682) gives SD16 a coinvariant lattice of rank 18, so every smooth member has Picard rank at least 19.
Status: CITED corollary of known theory, not a new result. Lean: none.

**P4. Lines.** Every smooth member has a reduced Fano scheme with exactly 40 lines, except s = 0 (48 lines; projectively equivalent to the Fermat quartic) and s^4 = 81/2 (56 lines; Y56). No other s carries extra lines.
Status: EXACT (Singular over Q(s) and at spot values; jump set by saturation, eliminant 2s^4 - 81; referee's minimal primes and meeting stratum); reducedness ARGUED (on a smooth quartic H^0(N_L) = H^0(O(-2)) = 0). Where: `pencil/graph_*.log`, `pencil/special.log`, `pencil/meet.log`, `pencil/fano_*.log`; `checks/pencil-referee/r1_*.log`, `r2_jump.log`, `r2_meet.log`. Lean: none.

**P5. The 40-line lattice.** The 40 persistent lines form a finite étale family over the smooth base with constant Gram matrix; they span a primitive lattice N19 of rank 19, det 128, Smith form [2,8,8] and signature (1,18), containing h.
Status: EXACT lattice data (on Y56; the same Gram data at s = 1, 5/2, 13/5, 3, 7i/3 with NUMERICAL 40-digit incidence); constancy ARGUED (local constancy on a connected base). Where: `pencil/a2_lattice.log`, `pencil/a4_checks.log` part (d). Lean: none.

**P6. Rank exactly 19 for the very general member.** If it were 20, the period would be constant on the connected smooth base and all smooth members would share one transcendental lattice; but T(X_0) = [8,0,8] and T(Y56) = [2,0,32] (Degtyarev, arXiv 1608.06746, Table 1) are not isometric. Method: Bouyer (arXiv 1511.01781, section 4.3).
Status: ARGUED with CITED lattices; used by P10. Lean: none.

**P7. Y56 is a Noether–Lefschetz point.** In NS(Y56) (rank 20, det -64) the orthogonal complement of N19 is spanned by v with v^2 = -32, v.h = 0, v.L = +4 on L06, L10, L29, L33, L35, L36, L50, L54, -4 on L00, L11, L12, L19, L42, L44, L48, L55, and 0 on the other 40. These 16 lines are one orbit of the group (orbit S) and are the solutions of a three-equation system that is consistent only when 2s^4 = 81.
Status: EXACT. Where: `pencil/a1_firstorder.log` (first-order obstruction, rank 4 against 5), `pencil/a2_lattice.log` (v), `pencil/a3_special.log`, `pencil/special.log`; `checks/pencil-referee/ref_y56b.py`. Lean: the algebra after substitution, `pencil_forces` (over any commutative ring the equations force s = 3 beta^2, alpha^2 = 2 beta^2, 2 beta^8 = 1, 2 s^4 = 81) and `pencil_solvable` (a real solution exists), in `lean/Y56_Pencil.lean`.

**P8. Conics.** There are 48 classes L+ + L- of degree 2 and square -2, all in N19; none is a sum of two persistent lines (0 of 48), so on a generic member each is an irreducible rigid conic; at Y56 each splits into a crossing pair of special lines. In one explicit family the norm of the conic determinant is 2^24 (2s^4 - 81)^2.
Status: EXACT lattice and explicit family; effectivity CITED (Riemann–Roch). Where: `pencil/a3_special.log`, `pencil/a4_checks.log` part (c); `checks/pencil-referee/ref_conic.py`, `ref_family.log`. Lean: none.

**P9. Real lines along the real line.** For real s (standard real structure): 8 real lines for |s| < 2 and for s < -2; 24 at s = 2 (a singular member); 40 for s > 2, s != s*; 56 at s* = 3 * 2^(-1/4).
Status: EXACT (closed forms, q(s - delta) = delta^4 - s^2 delta^2 + 4; Sturm counts at 15 values). Where: `pencil/a4_checks.log` part (b); `checks/pencil-referee/ref_family.log`. Lean: none.

**P10. NS of the very general member is N19.** The discriminant group of N19 has order 128 and exactly 14 nontrivial isotropic subgroups; each of the 14 even overlattices contains roots orthogonal to h (22 or more) and 40 or more new degree-1 (-2)-classes, so none can be NS of a smooth member with exactly 40 lines; independently, N19 is primitive in NS(Y56), which forces NS(very general) = N19.
Status: EXACT enumeration + ARGUED primitivity (uses NS(Y56) = the 56-line lattice, which uses the CITED det T = 64); not refereed separately. Degree-2 classes were outside the search bound (CORRECTIONS item 10). Where: `pencil/overlattice/`. Lean: none.

**P11. The symplectic group.** GAP, run on the 16 symplectic maps as permutations of the 56 lines, gives size 16, IdGroup [16,8], structure description QD16 (quasidihedral, also called semidihedral SD16).
Status: EXACT (GAP; trusted software). Where: `pencil/sd16/sd16.out`. Lean: none.

## Not claimed

We do not claim: the upper bound "no 57th line" in Lean; NS(Y56) = N without the cited determinant; the orbits of the 188 conics; the abstract isomorphism type of the real faces beyond the cited classification; explicit deformation paths; the lattice of the wall member or the s = infinity end; real line counts of the five non-standard faces at generic members of the pencil; the reality of the 48 conics for real s. These are the open questions of `PAPER.md`, section 10, and the loose ends of `README.md`.

Written with AI assistance.
