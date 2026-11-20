# Referee report: Y56 atlas v1.0 (ATLAS-V1), final release round

Seat: hostile referee, 2026-11-20. Archive not edited. My scripts and outputs are in this folder (`checks/atlas-referee/`).

## In plain words

The archive is in good shape. The data inside the Lean files match the release data exactly; I compared every printout by script. Core verify reruns 21/21, the manifest checks 316/316, and the privacy scan is clean. I found three mathematical errors in the text, and each needs a one-sentence fix:
1. The "full proof" of the 2s^4 = 81 step substitutes a line shape with the wrong sign. The paper's equations, and its claimed real solution, belong to z2 = β(z0 − z3), not z2 = β(z3 − z0).
2. "Aut(line graph) = Aut(Y56) ⋊ ⟨τ⟩" is false as written, because τ has order 4.
3. The NS = N19 argument cites "items 3 and 5" for finite index. It actually needs rank exactly 19 from the Bouyer-type argument, which the text says it supersedes.

The phrase "at s = 0 the surface is the Fermat quartic" is also too strong, because the equivalence holds only over C.

## Checks run

- ref_lean_data.out: the LU/LV printouts are identical in L1, L2, L3 and L6, and all 56 lines equal lines_exact.txt. NB/EDGES in L3, L6 and L8 equal edges.json, which equals the recomputed 4x4-determinant incidence (448).
- L2: MS equals the M matrices of symmetry_exact.txt entrywise, SIG equals sigma, and all 32 sym_gXX substitutions equal MS row by row with the same c. This closes the "two printouts in L2" loose end.
- I re-checked independently: F(Mz) = cF(z) for 32 maps; the 1792 line images; 16 maps with det(M)/c = +1; orbits 8+16+16+16; S = [0,6,10,11,12,19,29,33,35,36,42,44,48,50,54,55]; the 8-orbit; {0,6,23,24} is a listed P4 plane; the Gram matrix has rank 20; the det of the L8 basis block is -64; L6.PL equals planes_exact.txt.
- ref_l5normals.out: all 218 L5 normals and line lists match L6. The constants on both sides of every secP* identity are nonzero.
- Lean, run by me: Y56_Pencil.lean passes, axioms propext and Quot.sound / plus Classical.choice. Y56_L7.lean passes 9/9.
- recorded-run.log: 524 "ok" lines, with axiom sets none 1, propext 148, propext+Quot.sound 283, all three 92. These match the paper.
- verify_all_rerun.txt: "SUMMARY: 21 checks, 21 PASS, 0 FAIL, 92 s".
- sha256sum -c MANIFEST.sha256: 316/316 OK. Every file is listed except MANIFEST itself.
- Privacy:
  - No AI or product names, no personal names, no local paths and no clock times in md, html, logs or Lean.
  - The single hit is in viewer/data/y56-data.js inside a base64 float run. It is data.
  - The path regex in viewer/build/verify_viewer.py is the scanner itself.
- Number sample (31 numbers, all match their logs):
  - a2_lattice.log: "det -64 smith [2, 32]", "rank 19 ... det 128 smith [2, 8, 8]", "signature + 1 - 18", "v.v = -32", Smith of inclusion all 1.
  - a1_firstorder.log: rank 4 vs aug 5 on exactly S.
  - a3_special.log: "meeting (+,-) pairs: 48".
  - a4_checks.log: "16777216*(2*s**4 - 81)**2" = 2^24; 15 Sturm values; s=0 "lines 48 rank 20 det -64 smith [8, 8]".
  - special.log: "vdim 64", "2s4-81". graph_gen.log: four components with the paper's f1, f2, A, B.
  - r3_disc.log: s-2, s+2, s^2+4. c_fam.log: b^4c^3 - 16c^5.
  - w1.log: 8 and 8, radical. w3.log: "40 distinct lines: 24", charts 39/23 and 1/1.
  - f2_fermat.log: 1536; classes [[g00,g02,g13,g24],[g01,g12]]; real nodes 8/2/0/2/4/0; node coordinates match 7.4.
  - sd16.out: "16 [ 16, 8 ] QD16". gap_out.txt: [32,43], element orders, centre C2, derived C4.
  - s1_group.log: 64 and 32. s2_lattice.log: traces 20,4,4,4,-4,-4 and (r,a) = (1,1), (9,9), (13,9).
  - s4_mesh_260.log: lifted chi -36,-4,-4,-4,12,12. OVERLATTICE.md: 14 subgroups, 22 roots, 40 new classes.
- Sources OPENED (text extracted from the downloaded papers; not shipped):
  - Hashimoto 1012.2682, Table 10.1, txt lines 2622-2632: "26 | 16 | 8 | SD16 | 512 | 2^{+1}_7, 4^{+1}_7, 8^{+2}_II | 18". This gives coinvariant rank 18, and IdGroup number 8 confirms SD16 = QD16 = SmallGroup(16,8).
  - Bouyer 1511.01781 §4.3: "if a very general member of Y has Picard rank 20, then every member of Y is singular. Therefore Y parametrises a set of isomorphic surfaces."
  - Degtyarev–Rams 2301.04127 Table 1: "Y56 | 64 | (16, 8)2 | (1, 0) | ∗[2, 0, 32]".
  - Degtyarev 1608.06746 Table 1: "64 [2, 0, 32] Y56"; "64 [8, 0, 8] X56∗ ... X48".
- Own derivations:
  - Block scaling (z1,z2) → (iz1,iz2) maps G_s to G_{−s}. Rescaling the Galois conjugate F_{−e} gives s = ±i·s*, and the twist sends that surface back to Y56. So all four roots of s^4 = 81/2 are Y56: CORRECT.
  - x^4 − 2x^2 + 2 has Galois group D4, so K has degree 8: CORRECT.
  - ref_wall2i.out (NUMERICAL): s = 2i has 8 singular points. Controls: s = 2 gives 8, s = 3 gives 0.

## Verdicts

| claim | verdict | evidence / fix |
|---|---|---|
| Lean L1 lines_on_F / distinct / genuine | CORRECT | Statement over any ring with s·s = 2, specialised at √2. Non-containment for i ≠ j is distinctness. Data verified. |
| Lean L3 meets_iff_edge, edge_counts | CORRECT | iff only for i ≠ j, which matches "two different lines". |
| Lean L6, L5a-c | CORRECT | That no unstored plane holds two lines rests on a fact stated in words (disclosed). |
| Lean L2 | CORRECT | Printouts linked by my script. Fix L1 below. |
| Lean L8 / "lattice rank 20, disc −64" | CORRECT WITH FIXES | Lean proves Gram data. "Lattice" also needs ρ ≤ 20 and L² = −2 (cited). Fix L2. |
| Lean Pencil / P7 | CORRECT WITH FIXES | The algebra holds. The stated substitution is wrong (ref_shape.out: the stated shape with α = −1/β³ leaves coefficients up to 8; z2 = β(z0−z3) gives the same ideal). Fixes B1, L3. |
| P1 | CORRECT WITH FIXES | 8 nodes are EXACT only at s = 2. Fix N4. |
| P2, P3, P4, P5, P6, P8, P9, P11, X1 | CORRECT | Logs and sources above. |
| P10 | CORRECT WITH FIXES | Logical gap. Fix B3. |
| §5 item 5, ⋊⟨τ⟩ | WRONG | ref_tau.out: "tau^2 identity? False, tau^4 identity? True". Fix B2. |
| "s = 0 is the Fermat quartic" | CORRECT WITH FIXES | True only over C; the real points differ (8 real lines against an empty real Fermat). Fix B4. |
| "same 32 symmetries for every setting" | CORRECT WITH FIXES | The Fermat member has 1536 symmetries. Fix B5. |
| "exactly one setting" / "only wall" | CORRECT WITH FIXES | Four complex roots each. Fix N1. |
| Credits (DIS, Hashimoto, Bouyer, Veniani/Bouyer/Barth–Sarti) | CORRECT | Novelty wording is mostly consistent with PRIOR-ART. Fix N2. |
| Captions (media, viewer, figures) | CORRECT | Counts match P9 and 7.4. Viewer nit in N5. |

## Fixes, blocking (exact text)

**B1. PAPER.md §7.3, Item 7.**
- Old: "Take the shape $z_1 = \alpha z_0$, $z_2 = \beta(z_3 - z_0)$. Substituting into $G_s$, three coefficients must vanish:"
- New: "Take the shape $z_1 = \alpha z_0$, $z_2 = \beta(z_0 - z_3)$. Substituting into $G_s$, the $z_3^4$ coefficient vanishes identically and the other four must vanish; they generate the same ideal as the three equations"

Do the same in pencil/REPORT.md line 61 ("beta(z3 - z0)" becomes "beta(z0 - z3)").

**B2. PAPER.md §5, item 5.**
- Old: "Hence $\mathrm{Aut}(\text{line graph}) = \mathrm{Aut}(Y56) \rtimes \langle\tau\rangle$, of order 64:"
- New: "Hence $\mathrm{Aut}(\text{line graph}) = \mathrm{Aut}(Y56) \cup \tau\mathrm{Aut}(Y56)$, of order 64, with $\mathrm{Aut}(Y56)$ of index 2 ($\tau$ has order 4 on the lines and $\tau^2 \in \mathrm{Aut}(Y56)$; the extension splits, since the coset holds 16 involutions):"

**B3. PAPER.md §7.3, Item 6, and its echoes.**
- Old: "and it contains $N_{19}$ with finite index by items 3 and 5."
- New: "and it contains $N_{19}$ with finite index because the very general member has rank exactly 19 (the earlier argument below; item 3 gives only $\geq 19$) and by item 5. Both routes use rank exactly 19."

Also make these changes:
- PAPER: "Item 6 supersedes this by identifying the lattice itself." becomes "Item 6 builds on this and identifies the lattice itself."
- RESULTS P6: "superseded in strength by P10" becomes "used by P10".
- pencil/RESULT.md loose end 1: "two independent routes" becomes "two routes, both using item 6's rank-19 argument".

**B4. "s = 0 is the Fermat quartic".**
- README:
  - Old: "At $s = 0$ the surface is the famous Fermat quartic,"
  - New: "At $s = 0$ the surface is the famous Fermat quartic in disguise (the same surface over the complex numbers; its real points differ),"
- PAPER §7 plain words:
  - Old: "At $s = 0$ the surface is the famous Fermat quartic, and"
  - New: "At $s = 0$ the surface is a disguised copy of the famous Fermat quartic (over the complex numbers), and"
- CITATION.cff:
  - Old: "which also contains the Fermat quartic and one 8-nodal wall"
  - New: "which also contains a member projectively equivalent over C to the Fermat quartic, and an 8-nodal wall"

**B5. "Same 32 symmetries".**
- README and PAPER §7 plain words:
  - Old: "every setting gives a surface with the same 32 symmetries. Forty lines ride along the whole way." (PAPER: "Every setting gives ...")
  - New: "the same 32 symmetries act on every setting (the Fermat member has more). Forty lines ride along the whole way, except at the wall, where 32 of them merge in pairs."
- PAPER plain words, introduction:
  - Old: "a one-parameter family of equally symmetric surfaces"
  - New: "a one-parameter family of surfaces on which the same 32 symmetries act"

## Fixes, non-blocking

- **N1. One setting / one wall.**
  - README headline:
    - Old: "they exist at exactly one setting, because"
    - New: "they exist only where $2s^4 = 81$, one setting on the real dial (all four complex roots give Y56), because"
    - Then delete the trailing "only where $2s^4 = 81$" and replace it with "only there".
  - README plain words:
    - Old: "and at exactly one setting, $s^4 = 81/2$, sixteen"
    - New: "and only at $s^4 = 81/2$ (one setting on the real dial) sixteen"
  - PAPER §7:
    - Old: "this is the only wall."
    - New: "this is the only wall on the positive dial (over $\mathbb{C}$ the wall is $s^4 = 16$)."
- **N2. README novelty wording.**
  - Old: "(both numbers published; the explanation found nowhere)"
  - New: "(both numbers published; the explanation not found after a quick search)"
  - After "the 48 conics breaking into the 16 lines" insert " (the general mechanism is Bouyer's)".
- **N3. README loose end, Fermat lattice.**
  - Old: "are quoted from the discovery report; the shipped transcript (`pencil/a5_fermat.log`) shows only the orthogonal class."
  - New: "are in the shipped transcript `pencil/a4_checks.log`, part (d) (incidence numerical at 40 digits, algebra exact)."
- **N4. RESULTS P1 and PAPER Theorem 7.1(1).**
  - Old: "The wall members are singular with 8 nodes."
  - New: "The wall members are singular; at $s = \pm 2$ (the same surface up to $(z_1,z_2) \mapsto (iz_1, iz_2)$) they have exactly 8 ordinary nodes; at $s = \pm 2i$ the node count is not computed exactly."
- **N5. viewer/index.html line 747.** Change "plane y1 = 0 or y2 = 0" to "plane z1 = 0 or z2 = 0".
- **L1. Lean "two printouts" disclosure** (PAPER §8, lean/README, README loose ends).
  - Old: "a reader should compare them by eye."
  - New: "the release referee compared them by script: identical (checks/atlas-referee/ref_lean_data.out)."
  - Also drop "no second reader has yet matched every Lean statement..." and replace it with "a referee matched every Lean statement with the sentence that quotes it (checks/atlas-referee/REFEREE-ATLAS.md)."
- **L2. README scorecard.**
  - Old: "`LEAN-CHECKED` (lattice rank 20, discriminant $-64$)"
  - New: "`LEAN-CHECKED` (Gram matrix of the 56 lines: rank 20, a 20 × 20 block of determinant $-64$)"
  - In lean/README L8 row, after "discriminant $-64$" add "(given $\rho \le 20$ and $L^2 = -2$, cited)".
- **L3. PAPER §8 Pencil row.**
  - Old: "the three coefficient equations force"
  - New: "the three equations of Section 7.3 (equivalent to the coefficient equations; the substitution itself is not in Lean) force"
  - README scorecard: "(the three-equation step)" becomes "(the algebra after substitution)".

## What blocks release

Only B1 to B5. They are text edits, and no data, numbers or Lean files change. After the edits, re-hash the edited files into MANIFEST.sha256 and decode-scan once more.

**Overall: READY WITH FIXES.**

Single next strike: apply B1 to B5 and re-hash. Then add ref_shape.py as a shipped check, so the substitution in Item 7 is machine-tested and not only hand-derived.
