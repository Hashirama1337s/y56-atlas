# The machine-checked layer (Lean 4 + Mathlib)

Moki & Julio (AI-assisted) · 2026 · version 1.0

## In plain words

Programs such as Singular or GAP are trusted, not proved correct. A proof assistant re-checks a statement down to a few basic axioms, with a small trusted kernel. This folder moves the finite exact facts about Y56 that can be stated that way into Lean 4 with Mathlib: all 56 lines lie on the surface and are different, the 32 symmetries and their group table, the 448 crossings, the 218 special planes and how the surface splits in each of them, the rank and discriminant of the line lattice, three identities (the eight-fold form, the screw, the Galois twist), and the step of the pencil that forces $2s^4 = 81$. Ten files, 524 theorems, all accepted by Lean's kernel with standard axioms only. Nothing here relies on a computer algebra system: the generator script writes certificates, and the kernel re-checks every one.

## How to build and re-check

You need [elan](https://github.com/leanprover/elan) (the Lean version manager), git, and about 12 GB of free memory.

```
cd lean
lake exe cache get      # fetches Lean v4.36.0-rc2 (lean-toolchain) and the prebuilt Mathlib v4.36.0-rc2 (lakefile.toml, lake-manifest.json)
sh run_all.sh           # about 7 minutes; peak memory about 10 GB
```

`run_all.sh` checks the 10 positive files one at a time with `lake env lean`, prints `#print axioms` for every theorem, rejects any file containing `sorry`, `admit`, an `axiom` declaration or `native_decide`, then runs the 8 negative controls and requires each one to fail. It writes `run_all.log` and one `<name>.actual-error.txt` per control. To check one file only: `ONLY_POS=Y56_Pencil ONLY_NEG= sh run_all.sh`. If you already have a Lean project with this Mathlib built, set `LEAN_PROJECT` to its folder.

The pins are exact: `lean-toolchain` is `leanprover/lean4:v4.36.0-rc2`, and `lake-manifest.json` fixes the Mathlib commit of tag `v4.36.0-rc2` and its dependencies.

To regenerate the data-driven files from the release data: `python export_lean.py L1 L2 L3 L5 L6 L8 neg` (needs sympy; reads only `../core/data/`). `Y56_L7.lean` and `Y56_Pencil.lean` are written by hand.

The recorded run (theorem lists and axiom printouts of all 524 theorems, and the error counts of the controls) is `recorded-run.log`. The shipped `run_all.sh` was itself tested on `Y56_Pencil.lean` and its control: both behaved as recorded.

## The theorems, in plain words

Every finite computation uses `decide +kernel` on `Zsqrtd 2`, the ring $\mathbb{Z}[\sqrt2]$ with arithmetic evaluated by the kernel. Every polynomial identity uses `ring` or `linear_combination` with an explicit cofactor. The bridge to geometry is a ring map `iota s hs : Z[sqrt 2] ->+* R` sending $\sqrt2$ to any `s` with `s*s = 2`; it is injective in characteristic 0 (`iota_injective`), so each statement holds over $\mathbb{R}$ and $\mathbb{C}$.

| file | theorems | what is proved |
|---|---|---|
| `Y56_L1.lean` | `lines_on_F`, `lines_distinct`, `lines_genuine` | Every point of each of the 56 listed lines satisfies $F = 0$ (all 280 coefficients vanish in $\mathbb{Z}[\sqrt2]$); the 56 lines are pairwise different (a nonzero 3x3 minor for each of the 3080 ordered pairs); each pair of spanning vectors is linearly independent, so each entry is a genuine line. |
| `Y56_L7.lean` | `eightfold`, `screw`, `screw_coord`, `galois_twist` | $F = \mathrm{Im}(w^4) + \mathrm{Im}(p^2)(3\lvert w\rvert^2 - \lvert p\rvert^2)/\sqrt2$; the screw $(w,p) \mapsto (\zeta w, ip)$ with $\zeta = (1+i)/\sqrt2$ sends $G$ to $-G$; the same in coordinates, $F(z_0 - z_3, -\sqrt2 z_2, \sqrt2 z_1, z_0 + z_3) = -4F(z)$; and $F_e(z_0, -z_2, z_1, z_3) = F_{-e}(z)$, the Galois twist, as a pure ring identity. |
| `Y56_Pencil.lean` | `pencil_forces`, `pencil_solvable` | Over any commutative ring, the three equations of the 16 special lines (Section 7.3; equivalent to the coefficient equations, and the substitution itself is not in Lean) force $s = 3\beta^2$, $\alpha^2 = 2\beta^2$, $2\beta^8 = 1$ and $2s^4 = 81$ (six explicit `linear_combination` steps; the key move is that $\alpha\beta$ is a unit with inverse $-\beta^2$). Conversely a real solution exists. |
| `Y56_L2.lean` | `sym_g00` .. `sym_g31`, `maps_lines`, `group_facts`, `group_closed`, `matrices_compose`, `order_counts`, `orbit_sizes` | Each of the 32 matrices satisfies $F(Mz) = cF(z)$; each maps line $i$ onto line $\sigma(i)$ (checked for all 32 x 56 x 2 spanning vectors); the 32 permutations contain the identity, are pairwise distinct, are closed under composition (all 1024 products) and under inverses; matrix products agree with the permutation table up to a nonzero scalar; element orders are 1 (x1), 2 (x15), 4 (x8), 8 (x8); the line orbits have sizes 16, 16, 8, 16 with representatives L00, L01, L02, L03, so the split is 8 + 16 + 16 + 16. |
| `Y56_L3.lean` | `meets_iff_edge`, `edge_counts` | Two different lines share a point exactly when they are an edge of `core/data/edges.json` (an explicit common point for each edge; a nonzero 4x4 determinant for each non-edge); the graph has 448 edges, every line meets exactly 16 others, and 1092 pairs are skew. |
| `Y56_L6.lean` | `planes_lines`, `plane_rows`, `inPlane_iff_listed`, `line_in_plane_iff`, `pc_rows`, `dist_rows`, `plane_pairs_are_edges`, `edge_cover` | For each of the 198 stored line planes, the lines it contains are exactly the listed ones (148 with 2 lines, 50 with 4); the 20 conic-pair planes contain no line; all 218 planes are different; every pair of lines in a stored plane is an edge, $148 \cdot 1 + 50 \cdot 6 = 448$, and each of the 448 edges lies in exactly one stored plane. |
| `Y56_L5a.lean`, `Y56_L5b.lean`, `Y56_L5c.lean` | `secP2_000..147`, `secP4_000..049`, `secPC_000..019`, `conics_nondegenerate`, `conic_irreducible` | In every plane, a constant times $F$ restricted to the plane equals line x line x conic (148 planes), a product of four lines (50 planes) or conic x conic (20 planes); all 148 + 40 conics have nonzero Hessian determinant; such a conic is not a product of two linear forms, so it is irreducible over $\mathbb{C}$. |
| `Y56_L8.lean` | `det_GB`, `rows_in_span`, `hyperplane_class` | The 20 x 20 intersection matrix of the lines L00..L16, L18, L19, L20 has determinant $-64$ (Mathlib's `Matrix.det`, via an integer triangular certificate); every row of the 56 x 56 intersection matrix is an integer combination of those 20 rows, so the line lattice is free of rank 20 with discriminant $-64$ (given $\rho \le 20$ and $L^2 = -2$, cited); $h = L00 + L06 + L23 + L24$ has $h \cdot h = 4$ and $h \cdot L = 1$ for every line. |

## Axioms

Across the 10 positive files, `#print axioms` gives, for the 524 theorems: no axioms (1), `propext` only (148), `propext, Quot.sound` (283), `propext, Classical.choice, Quot.sound` (92). These are Lean's three standard axioms. No file contains `sorry`, `admit`, an `axiom` declaration or `native_decide`.

## Negative controls

Each control changes one input and must be rejected. The shipped `*_neg.expected-error.txt` files hold the recorded error text; the local folder prefix was removed from the error locations, and the line of the memory-cap wrapper was dropped. Otherwise they are as recorded.

| control | what was changed | how Lean failed |
|---|---|---|
| `Y56_L1_neg` | one coordinate of line L17 plus 1 | `decide` proved the coefficient check false |
| `Y56_L7_neg` | the Galois twist claimed without the sign change of $e$ | `ring`: unsolved goals |
| `Y56_Pencil_neg` | claims $2s^4 = 80$ | `ring` failed |
| `Y56_L2_neg` | two entries swapped in row 1 of the matrix $g_{05}$ | `sym_g05` unsolved goals; span and projectivity checks false (10 errors) |
| `Y56_L3_neg` | one edge dropped | meeting and edge-count checks false (3 errors) |
| `Y56_L6_neg` | one plane deleted | edge-cover and plane-pair checks fail (2 errors) |
| `Y56_L5c_neg` | one conic coefficient 14 changed to 15 | `ring` failed |
| `Y56_L8_neg` | one adjacency entry changed | certificate and row checks false (7 errors) |

## What is NOT formalised (loose ends)

- **Two printouts in L2 not linked by proof.** The 32 explicit `sym_gXX` theorems and the matrix table used by `maps_lines` and `matrices_compose` are generated from the same parse of `symmetry_exact.txt`, but no Lean proof links the two printouts. The release referee compared them by script: identical (`checks/atlas-referee/ref_lean_data.out`).
- **L5 coordinates vs the data file.** L5 recomputes the conics in its own plane coordinates; they were not compared with the conic strings in `core/data/conic_pair_planes_exact.txt`, which use a different parametrisation.
- **Geometry stated in words.** "Two distinct meeting lines span exactly one plane" (so "no other plane contains two lines" rests on it together with `edge_cover`), and "a nondegenerate conic, or a non-proportional Plücker pair, is the geometric statement" are said in words only.
- **Cited facts.** L8 proves the Gram data of the line lattice only. That the line lattice is the whole Néron–Severi lattice ($\mathrm{NS}(Y56) = N$, which uses the published $\det T = 64$) and that each line has self-intersection $-2$ (adjunction on a K3 surface) are cited, not proved.
- **Not done:** the smoothness certificate (L4), the identification of the group as $\mathrm{Hol}(C_8)$ and the plane-orbit tables (L9), real points on the conics (L10), the 636 lattice classes (L11), the wall nodes, two-conic identities and Fermat bridge (L12), the upper bound "exactly 56 lines over $\mathbb{C}$" (L13), the six-face traces (L14), and the incidence types (4,4) x 32 and (3,7) x 24.
- A referee matched every theorem statement with the sentence that quotes it (`checks/atlas-referee/REFEREE-ATLAS.md`).
- Large kernel checks are split into chunks; unchunked they exceed 12 GB. Lean prints deprecation warnings for two Mathlib names in L8 (warnings only).

`LEAN-REPORT.md` is the full report of the Lean work.

Written with AI assistance.
