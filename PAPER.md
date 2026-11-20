# The Y56 atlas: lines, conics, symmetries and real faces of the real quartic with 56 real lines, and the pencil in which it is a Noether–Lefschetz point

Moki & Julio (AI-assisted) · 2026 · version 1.0

---

## In plain words

A quartic surface is the set of points that satisfy one polynomial equation of degree 4. Some of these curved surfaces contain perfectly straight lines lying in them from end to end. Degtyarev, Itenberg and Sertöz proved that a smooth real quartic can carry at most 56 real lines, and that one surface does it, up to a real change of coordinates; it is called Y56. This paper is an atlas of that surface. We list all 56 lines exactly, using only whole numbers and $\sqrt2$; we list all 188 genuine curved conics on it; we describe its 32 symmetries; and we show the five other "real faces" that the same equation has when "real" is read in another way. Then we turn one dial. The equation of Y56 is one member of a one-parameter family of surfaces on which the same 32 symmetries act. Every smooth member carries the same 40 lines, which slide along as the dial turns. At only one setting on the real dial, three conditions that normally cannot hold together are met at once, and 16 more lines appear. That setting is Y56. A single command re-checks the exact core data on an ordinary computer, the finite core facts and the key step of the pencil are re-checked by the Lean proof assistant, and an interactive 3-D viewer lets anyone turn the dial and watch the 16 lines appear.

**Status labels used throughout.** EXACT: exact arithmetic over $\mathbb{Q}(\sqrt2)$, $\mathbb{Q}$, $\mathbb{Q}(s)$ or exact integer lattices, by our scripts or by a named program (Singular, msolve, GAP, PARI, sympy, networkx; these are trusted software, not proof assistants). LEAN-CHECKED: the statement as written in Lean 4 with Mathlib is accepted by Lean's kernel with standard axioms only (Section 8 names the theorem). CITED: taken from a published source, named, not re-proved. NUMERICAL: floating point, meshes or numerical search; support only. ARGUED: a proof or proof sketch written out but not machine-checked. UNTESTED marks curiosities that are not claims. Pictures are renderings of exactly verified data; a picture is not evidence.

---

## 1. Introduction

**Plain words.** How many straight lines can a smooth surface of degree 4 hold? Over the complex numbers the answer is 64. If we insist that the lines be real, the answer is 56, and only Y56 reaches it. The surface and these facts are not ours. This paper writes out everything the surface carries, draws it, and explains why its 16 "extra" lines exist.

**History.** The maximal number of lines on a smooth quartic surface is a classical question; Segre's 1943 work on it, and the gap in it, are discussed by DIS [DIS, introduction and Corollary 1.2, with their references to Segre and to Rams and Schütt]. Over $\mathbb{C}$ it was settled by Rams and Schütt: at most 64, attained by Schur's quartic [RS1, RS2, RS3]. Degtyarev, Itenberg and Sertöz (DIS) [DIS] developed a lattice-theoretic description of line configurations on quartics. In their section 9.2 they write down the real quartic Y56 (their equation 9.4) and show that it contains 56 real lines; their Corollary 1.3 states that 56 is the maximal number of real lines on a nonsingular real quartic and that Y56 is the unique maximiser up to real projective equivalence. They show that its projective automorphism group has order 32 (Proposition 9.9), that it has six real structures up to automorphism (Remark 9.10), and that its standard real part is a connected surface of genus 10 (Proposition 9.12). Veniani [V2] lists, in his Table 1, the row for Y56 with 64 intersection-preserving line permutations, a symmetry group of order 32, a symplectic part of order 16 and the transcendental lattice $T = [2,0,32]$. Degtyarev [D1] counted the conics: Y56 carries $188 + 448 = 636$ conics and 20 planes cutting two irreducible conics (his section 1.2 and Remark 7.4). In the same paper he notes that Y56 "has never been analyzed", and his Remark 7.4 closes that gap for the counts. Later papers by Degtyarev [D2, D3] add Y56 to tables of real hyperplane sections (50 real h-sections).

**What this paper adds.** We give credit for every count above to its authors. What we add, with the verdict of our prior-art search for each item (searches of arXiv, Zenodo, GitHub, OpenAlex, Semantic Scholar and OpenCitations citers; the core searches ran to 2026-11-19, the pencil search to 2026-11-20):

1. **The complete exact list of the 56 lines over $\mathbb{Q}(\sqrt2)$** (Appendix A). PARTIAL: DIS write out 24 of the 56 explicitly (their Tables 3 to 5); a full list was found in nothing we opened.
2. **Explicit equations of the 148 + 40 irreducible conics and the 20 line-free planes** (archive data). Only the counts were found in the literature we opened.
3. **The line-orbit split 8 + 16 + 16 + 16** under the group of order 32, with every line tagged by its orbit (Appendix A), and the orbit sizes on planes. PARTIAL: DIS (proof of Proposition 9.9) single out 8 lines, which form our 8-orbit; the split of the other 48 we found nowhere.
4. **An exact explanation of the factor 2 between the 64 graph symmetries and the 32 projective ones**: a Galois twist $\sqrt2 \mapsto -\sqrt2$ followed by a quarter-turn. Both numbers are published; in a quick search we did not find this explanation.
5. **The table of real lines, real conics and topology for the five non-standard real faces.** PARTIAL: the number of faces and the standard face are published; the table for the other five we found in nothing we opened.
6. **Pictures** of Y56, its lines and its conics, and an interactive viewer. OPEN: we found no earlier picture of the surface, its 56 real lines or its conics (search to 2026-11-19 of arXiv, Zenodo, GitHub, citers and the Imaginary galleries).
7. **The headline result: the pencil** $G_s$ through Y56 and the Fermat quartic (Section 7). Its generic member carries exactly 40 lines, its Néron–Severi lattice is a rank-19 lattice $N_{19}$ of determinant 128, lines jump only at the Fermat member (48) and at Y56 (56), and Y56 is a Noether–Lefschetz point of the pencil at which a class $v$ with $v^2 = -32$ becomes algebraic and 16 lines, one orbit of the group, appear. We found no earlier statement of the pencil, the 40-line configuration, the jump set, the 16-line Noether–Lefschetz description, the 48 conics degenerating into the 16 lines, or the real-line walk 8 / 24 / 40 / 56 (search to 2026-11-20 of arXiv, Zenodo, citers). The kind of result is published: one-parameter families of quartics with generic Picard rank 19 and line jumps at rank-20 members appear in Veniani [V2, section 6.7], Bouyer [B] and Barth–Sarti [BS]. The equation of the Y56 member is DIS's; the pencil frees the coefficient 3 in their equation (9.4).
8. **A machine-checked core** (Section 8): the 56 lines, their 448 crossings, the 32 symmetries and their orbits, the 218 special planes with their factorisations, the line lattice (rank 20, discriminant $-64$), three identities and the step of the pencil that forces $2s^4 = 81$, as 524 theorems accepted by Lean's kernel. We did not run a separate prior-art search for this layer, so we claim only that we did it.

What is not ours: the surface, the count 56 and its maximality and uniqueness, the group order 32, the count 64, the six real structures, the genus-10 standard face, the counts 636 and 20, the transcendental lattices, and the classification of real quartics by Nikulin and Kharlamov that we use for deformation classes.

---

## 2. The surface

**Plain words.** Y56 is written with four coordinates $z_0, z_1, z_2, z_3$ and the number $\sqrt2$. Pairing the coordinates into two complex numbers shows its hidden eight-fold screw symmetry at a glance.

With $e = \sqrt2$, Y56 is the surface $F = 0$ in $\mathbb{P}^3$, where

```math
F = 3e\,z_0^2 z_1 z_2 + 3e\,z_1 z_2 z_3^2 - e\,z_1^3 z_2 - e\,z_1 z_2^3 + 4 z_0^3 z_3 - 4 z_0 z_3^3 .
```

This is DIS equation (9.4) with $\varepsilon = \sqrt2$ [DIS, section 9.2]. (Provenance note: we read the equation from a page image of that equation.)

**The eight-fold form (EXACT, sympy identity).** Put $w = z_0 + i z_3$ and $p = z_1 + i z_2$. Then

```math
F = \mathrm{Im}(w^4) + \tfrac{1}{\sqrt2}\,\mathrm{Im}(p^2)\,\bigl(3|w|^2 - |p|^2\bigr).
```

In this form the screw $`(w,p) \mapsto (e^{i\pi/4} w,\; i p)`$ visibly sends $F$ to $-F$; it is one of the 32 symmetries (the element $g_{04}$, of order 8). The quarter-turn $w \mapsto i w$ alone is also a symmetry. We checked this form only as an identity; we did not run a prior-art search for it, so we claim only that we checked it. The form and the screw are LEAN-CHECKED (`eightfold`, `screw`, `screw_coord`).

**Smoothness (EXACT, Singular).** The ideal $J$ of the four partial derivatives of $F$ over $\mathbb{Q}(\sqrt2)$ has an affine cone of dimension 0 and quotient dimension $\dim R/J = 81 = 3^4$; each $z_i^9$ lies in $J$, and $F \in J$ by Euler's identity. So $\nabla F$ has no projective zero and Y56 is smooth over $\mathbb{C}$. Hence Y56 is a K3 surface, every line on it is a rigid $(-2)$-curve, and its Fano scheme of lines is finite.

---

## 3. The 56 lines

**Plain words.** All 56 lines can be written with whole numbers and $\sqrt2$. Two different computer-algebra programs, using different coordinates, agree that there is no 57th line, real or complex. Each line crosses exactly 16 others.

**Theorem 3.1.** Y56 contains exactly 56 lines over $\mathbb{C}$. All 56 are defined over $\mathbb{Q}(\sqrt2)$, hence real, and the Fano scheme of lines is reduced.

*Lower bound (EXACT).* Appendix A lists 56 lines, each as the span of two points with coordinates in $\mathbb{Q}(\sqrt2)$. Substituting $z = tA + B$ into $F$ gives the zero polynomial for each of them, and their Plücker coordinates are pairwise non-proportional, so they are 56 distinct lines (`verify_all.py` checks 1a, 1b; LEAN-CHECKED: `lines_on_F`, `lines_distinct`, `lines_genuine`). The coordinates were first guessed by PSLQ on 65-digit numerics and then proved by this substitution.

*Upper bound, first program (EXACT, Singular).* After a rational change of coordinates $z = Tw$ chosen so that no known line has vanishing Plücker coordinate $p_{01}$, a line in the chart $`\{0,1\}`$ of $G(2,4)$ is spanned by $(1,0,a,b)$ and $(0,1,c,d)$, and the five coefficients of $`F(T(m\,p + q))`$ give five equations in $a,b,c,d$ over $\mathbb{Q}(\sqrt2)$. Their Gröbner basis is zero-dimensional of length (vdim) 56. In each of the other five charts the equations together with $p_{01} = 0$ generate the unit ideal, so no line lies outside the first chart. The 56 known lines are 56 distinct solutions. Length 56 equals the number of distinct solutions, so every solution is simple and there are exactly 56.

*Upper bound, second program (cross-check; msolve, Monte Carlo mode).* With an independent coordinate change (determinant $-46$), $\sqrt2$ handled by a variable $s$ with $s^2 = 2$, and the coefficients extracted homogeneously, msolve finds an ideal of degree $112 = 2 \times 56$ with 112 distinct solutions, all real; 56 have $s > 0$ (the lines of Y56) and 56 have $s < 0$ (the lines of the Galois-conjugate surface). The other five charts again give the unit ideal. msolve ran in its default Monte Carlo mode (correct with high probability, not formally certified); its solutions were not matched one by one with our list.

Credit: the count 56 is DIS's (section 9.2 with Theorem 1.1, Corollary 1.3; CITED). DIS also note that some lines are defined only over $\mathbb{Q}(\sqrt2)$ (Remark 9.11).

**The incidence graph (EXACT).** Two lines meet exactly when the $4 \times 4$ determinant of their four spanning vectors vanishes. Over $\mathbb{Q}(\sqrt2)$ this gives 448 meeting pairs, and every line meets exactly 16 others: the graph is 16-regular (checks 2a, 2b; LEAN-CHECKED: `meets_iff_edge`, `edge_counts`). DIS give the incidence types (4,4) for 32 lines and (3,7) for 24 lines (Lemma 6.14; CITED); we use them only to colour pictures.

**The eight anchor lines.** The 8-orbit of the symmetry group (Section 5) is $`\{L02, L14, L22, L24, L27, L30, L43, L53\}`$. Reading their coordinates in Appendix A, each lies in one of the planes $z_1 = 0$ or $z_2 = 0$, where $F = 4 z_0 z_3 (z_0^2 - z_3^2)$ splits into four lines through one point. These 8 lines lie on every member of the pencil of Section 7.

**Figure 1.** `core/media/y56_chart3_b.png`. *The surface (blue sheet) with all 56 lines drawn on it. Pink are the 32 lines of incidence type (4,4), green the 24 of type (3,7). Every line shown lies entirely on the curved sheet, and several lines pass through single points.*

---

## 4. Planes and conics

**Plain words.** Slice the surface with a flat plane and you usually get a curve of degree 4. Sometimes the slice falls apart into lines and conics (curves of degree 2). On Y56 this happens in exactly 218 planes, and every conic on the surface comes from one of them.

**Theorem 4.1 (EXACT, with one CITED input for completeness).**

1. Exactly 148 planes contain exactly two of the lines. In each, the plane section factors over $\mathbb{Q}(\sqrt2)$ as line × line × $Q$, with $Q$ an irreducible conic whose $3\times3$ matrix has nonzero determinant (checks 4a to 4d).
2. Exactly 50 planes contain four lines each, and $148 + 6 \times 50 = 448$, so every meeting pair lies in exactly one of these 198 planes (checks 4a, 4e).
3. Exactly 20 planes contain no line and cut the surface in two irreducible conics each, 40 conics in all. Their normals and both conics are defined over $\mathbb{Q}(\sqrt2)$ and each conic is nondegenerate (checks 5a, 5b).
4. All 188 irreducible conics ($148 + 40$) have real points: their Gram matrices are indefinite, with signs decided exactly in $\mathbb{Q}(\sqrt2)$ (checks 6a, 6b).
5. These are all the conics: Y56 has exactly $636 = 448 + 188$ conics, counting each crossing pair of lines as a degenerate conic, and exactly 20 line-free conic-pair planes.

Items 1 to 3 are also LEAN-CHECKED: which lines each stored plane contains, that every meeting pair lies in exactly one of the 198 line planes, and that the 20 conic-pair planes hold no line (`planes_lines`, `inPlane_iff_listed`, `pc_rows`, `dist_rows`, `plane_pairs_are_edges`, `edge_cover`); the factorisation of every section and the nondegeneracy and irreducibility of all 188 conics (`secP2_000..147`, `secP4_000..049`, `secPC_000..019`, `conics_nondegenerate`, `conic_irreducible`). Item 4 and the completeness in item 5 are not in Lean.

Representatives of the three orbits of line-free planes ($n \cdot z = 0$):

- A (orbit of 8): $n = (\sqrt2 - 1 : \tfrac{3-\sqrt2}{7} : \tfrac{3-\sqrt2}{7} : 1)$
- B (orbit of 8): $n = (1 : \tfrac{2\sqrt2-1}{7} : \tfrac{1-2\sqrt2}{7} : 1-\sqrt2)$
- C (orbit of 4): the plane $`4 z_2 + \sqrt2\,z_1 = 0`$.

The counts 636 and 20 are Degtyarev's [D1, Remark 7.4; CITED]; our completeness argument does not use them.

*Proof of completeness (EXACT lattice computation, one CITED input; the conic-class criterion is ARGUED as standard).* Let $N$ be the $\mathbb{Z}$-span of the 56 line classes and the hyperplane class $h$. Exactly, $N$ has rank 20 and $|\mathrm{disc} N| = 64$; $h$ lies in the span of the lines with integer coordinates and $h^2 = 4$ (the Gram data are LEAN-CHECKED: `det_GB`, `rows_in_span`, `hyperplane_class`; the self-intersection $-2$ of a line is cited). Veniani's Table 1 gives $T = [2,0,32]$ for Y56 [V2; CITED], so $|\mathrm{disc} \mathrm{NS}(Y56)| = \det T = 64$. A sublattice of index $k$ has discriminant $k^2$ times larger, so $k = 1$ and $N = \mathrm{NS}(Y56)$. On a K3 quartic the class of a conic is a vector $c$ with $c \cdot h = 2$ and $c^2 = -2$; it is irreducible exactly when it is not the sum of two meeting lines, and an irreducible conic is rigid, so it is the only curve in its class. Enumerating $N$ (PARI `qfminim`, exact integers) gives 636 such classes: 448 sums of two meeting lines and 188 others. Since we exhibit 188 distinct irreducible conics, they are all of them. Exactly 20 unordered pairs $`\{c, h-c\}`$ have both members irreducible, which are our 20 planes.

Without the cited determinant, $\mathrm{NS}$ could be one of three index-2 overlattices of $N$ (the discriminant group has order 64 and exactly 3 nonzero isotropic classes); each would add no new lines but many new degree-2 classes, 4828 over the three (EXACT). The citation excludes them.

*Numerical support (NUMERICAL).* An unrestricted multi-start search over all planes (12000 starts, two seeds) returned 673 solutions with two nondegenerate conics; all 673 match one of the 20 exact planes, and all 20 were hit.

**Figure 2.** `core/media/y56_conics_v2_a.png`. *Pink and green are the 56 lines, amber the 148 conics that sit in planes with exactly two lines, violet the 40 conics of the 20 planes that hold no line. Every curve drawn lies on the surface. The amber arcs look nearly straight because only the part of each large oval inside the render ball is drawn.*

**Figure 3.** `core/media/y56_conics_v2_sphere.png`. *The same configuration in the stereographic sphere model, where every line and conic becomes a closed circle or oval lying entirely on the surface.*

---

## 5. Symmetry

**Plain words.** Y56 maps onto itself under 32 real changes of coordinates, including the eighth-turn screw. They shuffle the 56 lines in four groups of 8, 16, 16 and 16. The pattern of which lines cross has twice as many symmetries, 64, and the extra 32 come from swapping $\sqrt2$ with $-\sqrt2$.

**Theorem 5.1.**

1. (EXACT; order CITED; the 32 maps, their action on the lines and the group table LEAN-CHECKED: `sym_g00` to `sym_g31`, `maps_lines`, `group_facts`, `group_closed`, `matrices_compose`) There are exactly 32 real projective maps $M$ with $F(Mz) = cF(z)$, $`c \in \{1,-1,4,-4\}`$, all with entries in $\mathbb{Q}(\sqrt2)$; they act faithfully on the 56 lines. DIS prove that $\mathrm{Aut}(Y56)$ has order 32 and that all automorphisms are real (Proposition 9.9, Remark 9.10); Veniani lists the same order.
2. (EXACT, GAP IdGroup; trusted software) The group is SmallGroup(32,43) $= C_8 \rtimes (C_2 \times C_2)$, the holomorph $\mathrm{Hol}(C_8) = C_8 \rtimes \mathrm{Aut}(C_8)$. Element orders: 1 (×1), 2 (×15), 4 (×8), 8 (×8) (LEAN-CHECKED: `order_counts`); centre $C_2$; derived subgroup $C_4$; 11 conjugacy classes. We identified this name; we did not search the literature for it.
3. (EXACT; line orbits also LEAN-CHECKED: `orbit_sizes`) Orbits: on the 56 lines $8 + 16 + 16 + 16$; on the 148 two-line planes $32, 16 \times 6, 8, 8, 4$; on the 50 four-line planes $16, 16, 16, 2$; on the 20 conic-pair planes $8, 8, 4$ (checks 3d, 7a to 7c). We name the line orbits by their role in Section 7: the **8-orbit** (the anchor lines), the orbit **S** of L00 (the 16 lines that exist only at Y56), and the orbits **A** of L01 and **B** of L03. Appendix A tags every line.
4. (EXACT; count also CITED) The intersection graph of the 56 lines has exactly 64 automorphisms. The count is from a full enumeration with networkx, confirmed by a second algorithm (igraph/bliss, the same 64 as a set; `family/faces/a_aut.py`); Veniani's Table 1 gives the same number [V2, column $|O_h|$]. For each of the 64, the linear conditions for a projective map realising it (224 equations in 16 unknowns over $\mathbb{Q}(\sqrt2)$) were solved exactly: 32 have a one-dimensional solution space and 32 have none.
5. (EXACT) **The Galois twist.** Let $\mathrm{Gal}: \sqrt2 \mapsto -\sqrt2$ and $R(z_0,z_1,z_2,z_3) = (z_0, -z_2, z_1, z_3)$, that is $p \mapsto ip$. Then $F(Ry) = F^{\mathrm{Gal}}(y)$ identically (LEAN-CHECKED: `galois_twist`), so $\tau = R \circ \mathrm{Gal}$ maps Y56 to itself semilinearly. $\tau$ permutes the 56 lines, it is a graph automorphism that no projective map realises, and $\tau$ times the 32 realised permutations is exactly the other 32. Hence $\mathrm{Aut}(\text{line graph}) = \mathrm{Aut}(Y56) \cup \tau\mathrm{Aut}(Y56)$, of order 64, with $\mathrm{Aut}(Y56)$ of index 2 ($\tau$ has order 4 on the lines and $\tau^2 \in \mathrm{Aut}(Y56)$; the extension splits, since the coset holds 16 involutions): every combinatorial symmetry of the 56 lines comes from a symmetry of the surface over $\mathbb{Q}(\sqrt2)$, semilinear for the extra 32. The unrealised coset has 16 elements of order 2, 8 of order 4 and 8 of order 8.
6. (EXACT, GAP IdGroup; CITED match) Exactly 16 of the 32 maps act symplectically on the holomorphic 2-form ($\det(M)/c = +1$). GAP, run on these 16 maps as permutations of the 56 lines, gives a group of size 16 with IdGroup $[16,8]$ and structure description QD16, the quasidihedral (also called semidihedral) group SD16 of order 16 (`pencil/sd16/`). This matches the symplectic group recorded for Y56 by Degtyarev and Rams [DR, Table 1, entry $(16,8)_2$].

All 32 maps are block-diagonal in $(z_0, z_3) \mid (z_1, z_2)$: they rotate or reflect the $w$-plane by multiples of $45°$ and the $p$-plane by multiples of $90°$. This is why they also act on every member of the pencil of Section 7.

**Figure 4.** `core/media/y56_screw.gif` (video: `core/media/y56_screw_ffmpeg.mp4`). *A 36-frame loop that turns the surface along the screw $(w,p) \mapsto (e^{it}w, e^{2it}p)$ through one eighth of a turn. At the end the surface lands on itself by an exact symmetry, so the loop closes without a jump. Green circles are the 56 lines in the sphere model.*

---

## 6. Six real faces

**Plain words.** "Real point" depends on which complex conjugation you use. The equation of Y56 has 16 of them, and up to its symmetries they come in six kinds. Through the usual one you see a single sheet with ten handles carrying all 56 lines. Through the other five you see 12, 8, 4, 0 and 0 real lines, and the sheet becomes a two-handled surface (three times) or three separate bubbles (twice).

A real structure on Y56 is $\sigma_g = g \circ \mathrm{conj}$ with $g$ in the group and $g^2 = 1$ projectively. Since all automorphisms are real, two of them are isomorphic exactly when the $g$ are conjugate. The identity and the 15 involutions give 16 real structures in six classes, matching DIS's "six real structures" (Remark 9.10; CITED). Each $M$ satisfies $M^2 = \lambda I$ with $`\lambda \in \{1,2\}`$, so every $\sigma_g$ is the standard real structure of $\mathbb{P}^3$ in suitable coordinates.

**Table 6.1 (EXACT unless marked).** Real lines are the lines fixed by $g$. A conic is $\sigma$-real when $g$ maps it to itself; it has a real oval exactly when its real quadratic form is indefinite (signs decided exactly).

| face | class size | real lines | $\sigma$-real conics (with a real oval) | real part | $\chi$ | $(r,a,\delta)$ of $L^+$ |
|---|---|---|---|---|---|---|
| $g_{00}$ standard | 1 | 56 | 188 (188) | connected, genus 10 | −18 | (1,1,1) |
| $g_{02}$ | 4 | 12 | 14 (10) | connected, genus 2 | −2 | (9,9,1) |
| $g_{24}$ central | 1 | 8 | 12 (8) | connected, genus 2 | −2 | (9,9,1) |
| $g_{01}$ | 4 | 4 | 12 (8) | connected, genus 2 | −2 | (9,9,1) |
| $g_{12}$ | 4 | 0 | 28 (22) | three spheres | 6 | (13,9,1) |
| $g_{13}$ | 2 | 0 | 28 (20) | three spheres | 6 | (13,9,1) |

In the face $g_{12}$, 4 further conics in fixed planes are swapped in pairs by the conjugation and are not counted. Some $\sigma$-real conics have no real points at all: 4 in $g_{02}$, 4 in $g_{01}$, 6 in $g_{12}$, 8 in $g_{13}$; in the central face $g_{24}$ all 4 of its real two-line-plane conics are empty.

**Topology, by independent methods.**

- *Lefschetz (EXACT).* An antiholomorphic involution acts on $\mathrm{NS}$ as $-g^*$ and with trace 0 on $T \otimes \mathbb{R}$, and $\rho = 20$, so $\chi(X_\mathbb{R}) = 2 - \mathrm{tr}(g^* \mid \mathrm{NS})$. The traces, computed on an integral basis, are $20, 4, 4, 4, -4, -4$, giving $\chi = -18, -2, -2, -2, 6, 6$.
- *Lattice (EXACT, with CITED classification).* $H^2(X,\mathbb{Z})$ was rebuilt as the even unimodular overlattice of $N \oplus T$ (all 4 gluings tried, identical results), and $L^+ = \ker(\sigma^* - 1)$ computed over $\mathbb{Z}$. By Nikulin and Kharlamov (as summarised in [DK]), $X_\mathbb{R} = S_g \sqcup k S^2$ with $g = (22-r-a)/2$ and $k = (r-a)/2$: genus 10, genus 2, and $S_0 \sqcup 2S^2$ (three spheres).
- *Meshes (NUMERICAL).* Marching cubes on the double cover in $S^3$ at grids 160 and 260 give identical results: lifted $\chi = -36, -4, -4, -4, 12, 12$ and 1, 1, 1, 1, 6, 6 lifted components (three antipodal pairs in the last two rows).
- *Morse counts (EXACT counts, NUMERICAL indices).* msolve critical points of a quadratic height on $X_\mathbb{R}$ give minima / saddles / maxima $2/23/3$, $2/6/2$, $1/5/2$, $2/6/2$, $3/0/3$, $4/3/5$, reproducing every $\chi$. For $g_{12}$ the 6 critical points (3 minima, 3 maxima) and an exact separation into three regions give a fifth, lattice-free proof of "three spheres" (`family/faces/b_anal.py`, `b_anal.log`, `b_anal2.log`).

The standard face, connected of genus 10, is DIS Proposition 9.12 (CITED) and served as our positive control.

**Deformation families (CITED, with EXACT inputs).** By Kharlamov's rigid-isotopy classification of real quartics, as stated in the Degtyarev–Kharlamov survey [DK, section 3.5.4], a nonsingular real quartic is determined up to rigid isotopy by the isotopy type of its real part in $\mathbb{RP}^3$, its complex type and its chirality. The three genus-2 faces each contain real lines, which are non-contractible loops in $\mathbb{RP}^3$, so their real parts are non-contractible; the survey's tables have one class for a non-contractible genus-2 surface and one class for three spheres. Hence $g_{01}$, $g_{02}$, $g_{24}$ form one deformation family of real quartics, and $g_{12}$, $g_{13}$ form one. The class counts were read from the survey's tables in a rendered page and the reading was checked by eye; no explicit deformation path was built. For $g_{02} \sim g_{24}$ there is also a second, independent route through the Fermat member of the pencil (Section 7.6; ARGUED, with numerical steps). The lattice invariants of the five non-standard faces agree within each family, as the classification requires (`family/wall/l3_lattice.py` and its log).

**Ovals on bubbles (EXACT separation, NUMERICAL placement).** For each three-sphere face an integer quadratic form and two rational levels were found such that msolve proves that the levels miss the real surface; each of the three regions contains real points, so each holds exactly one sphere. Evaluating every oval at 1500 points (minimum distance to a level 5.76 for $g_{12}$ and 4.19 for $g_{13}$, against errors near $10^{-12}$) places the ovals: in $g_{12}$ all 22 lie on one sphere and the other two spheres are bare; in $g_{13}$ the 20 ovals split $4 / 12 / 4$. This is the only difference we found between the two topologically identical zero-line faces. The placement is a float evaluation with margin, not interval arithmetic. Evidence: `family/faces/` (the msolve inputs and outputs `b_*.ms`, `b_*.out`; `b_sep.py`, `b_assign.py` and their logs).

**Figure 5.** `core/media/y56_six_faces.png`. *One equation, six real faces, with 56, 12, 8, 4, 0 and 0 real lines: a ten-handled surface, three two-handled surfaces, and two sets of three bubbles. Green are lines, amber and violet are conic ovals.*

**Figure 6.** `core/media/y56_face_g12.png`. *The face $g_{12}$: no real lines, three separate spheres, and all 22 real conic ovals on one of them (EXACT separation of the spheres, NUMERICAL placement of the ovals). One sphere copy is partly outside the view, so one of the three looks cut.*

---

## 7. The pencil: why the 16 lines exist only at Y56

**Plain words.** Change the number 3 in the equation of Y56 into a dial $s$. The same 32 symmetries act on every setting (the Fermat member has more). Forty lines ride along the whole way, except at the wall, where 32 of them merge in pairs. At $s = 0$ the surface is a disguised copy of the famous Fermat quartic (over the complex numbers), and 8 more (imaginary) lines appear. At $s = 2$ the surface pinches at 8 points: this is the only wall on the positive dial (over $\mathbb{C}$ the wall is $s^4 = 16$). Exactly at $s^4 = 81/2$ a fourth kind of line becomes possible, because three equations in two unknowns happen to agree there, and symmetry turns that one line into 16. That surface is Y56. Just off that setting the 16 lines are gone; in their place sit 48 smooth conics, and at Y56 each conic snaps into a crossing pair of the new lines.

### 7.1 The pencil

For $s \in \mathbb{C}$ let

```math
G_s = \mathrm{Im}(w^4) + \mathrm{Im}(p^2)\bigl(s|w|^2 - |p|^2\bigr) = 4z_0^3 z_3 - 4 z_0 z_3^3 + 2 z_1 z_2\bigl(s(z_0^2 + z_3^2) - (z_1^2 + z_2^2)\bigr),
```

with $w = z_0 + iz_3$, $p = z_1 + iz_2$, and $`X_s = \{G_s = 0\}`$. Rescaling $z_1, z_2$ by $2^{1/8}$ turns $F$ into $G_{s_*}$ with

```math
s_* = 3 \cdot 2^{-1/4}, \qquad s_*^4 = 81/2,
```

so Y56 is $X_{s_*}$ (DIS equation (9.4) after $z_1, z_2 \mapsto 2^{-1/8} z_1, z_2$). The Fermat-type member is $s = 0$, the wall is $s^4 = 16$, and $s = \infty$ is a degenerate union of planes. The pencil is the semi-invariant family of the group: in an exploratory computation, quartics with $F(Mz) = c_M F(z)$ for all 32 maps form a 3-dimensional space $a\mathrm{Im}(w^4) + \mathrm{Im}(p^2)(b|w|^2 + c|p|^2)$, and block scalings leave the single modulus $b^2/(ac)$.

### 7.2 The theorem

**Theorem 7.1.** In the pencil $G_s$:

1. **Smoothness** (EXACT). $X_s$ is a smooth quartic K3 surface exactly when $s^4 \neq 16$; the discriminant is a constant times $(s-2)(s+2)(s^2+4)$. The wall members are singular; at $s = \pm 2$ (the same surface up to $(z_1,z_2) \mapsto (iz_1, iz_2)$) they have exactly 8 ordinary nodes; at $s = \pm 2i$ the node count is not computed exactly.
2. **Symmetry** (EXACT; CITED match). Every member carries the 32 block symmetries; exactly 16 act symplectically ($\det(M)/c = +1$), forming SD16 (GAP IdGroup $[16,8]$, Theorem 5.1 item 6) as for Y56 [DR, Table 1].
3. **Rank at least 19** (CITED corollary). Hashimoto's Table 10.1 gives SD16 a coinvariant lattice of rank 18 [H], so every smooth member has Picard rank at least 19. This is a corollary of known theory, not a new result.
4. **Lines** (EXACT; reducedness ARGUED). Every smooth member has a reduced Fano scheme with exactly 40 lines, except $X_0$ (48 lines; projectively equivalent to the Fermat quartic) and $X_s$ with $s^4 = 81/2$ (56 lines; Y56). No other $s$ carries extra lines.
5. **The 40-line lattice** (EXACT lattice data; constancy ARGUED). The 40 persistent lines form a finite étale family over the smooth base with constant Gram matrix. They span a primitive lattice $N_{19}$ of rank 19, determinant 128, Smith form $[2,8,8]$ and signature $(1,18)$, containing $h$.
6. **Néron–Severi of the very general member.** $\mathrm{NS}(X_s) = N_{19}$ for very general $s$ (EXACT enumeration plus ARGUED primitivity; not separately refereed). So the very general member has Picard rank exactly 19 and a transcendental lattice of rank 3 with $|\det| = 128$.
7. **Y56 is a Noether–Lefschetz point** (EXACT; the algebra after the substitution LEAN-CHECKED). In $\mathrm{NS}(Y56)$ (rank 20, $\det -64$) the orthogonal complement of $N_{19}$ is spanned by a class $v$ with $v^2 = -32$, $v \cdot h = 0$, and $v \cdot L = \pm 4$ on exactly 16 lines and $0$ on the other 40. These 16 lines are one orbit of the group, the orbit S:
   ```math
   L00, L06, L10, L11, L12, L19, L29, L33, L35, L36, L42, L44, L48, L50, L54, L55,
   ```
   and they are the solutions of a three-equation system that is consistent only when $2s^4 = 81$.
8. **Conics** (EXACT lattice; effectivity CITED Riemann–Roch). There are 48 classes $L^+ + L^-$ of degree 2 and square $-2$, all in $N_{19}$; none is a sum of two persistent lines (0 of 48), so on a generic member each is an irreducible rigid conic. At Y56 each splits into a crossing pair of the 16 special lines. In one explicit family the norm of the conic determinant is $2^{24}(2s^4 - 81)^2$.
9. **Real lines along the real line** (EXACT). For real $s$ (standard real structure) the number of real lines is 8 for $|s| < 2$ and for $s < -2$; 24 at $s = 2$ (a singular member); 40 for $s > 2$, $s \neq s_*$; and 56 at $s = s_*$.

The theorem was re-derived by a hostile referee with independent code before this statement was fixed (`checks/pencil-referee/`); item 6 was added afterwards and has not been refereed separately. Scripts and transcripts for every item are in `pencil/`; `pencil/RESULT.md` is the refereed statement.

### 7.3 Proofs and proof sketches

**Item 1.** The referee computed the discriminant of the pencil directly. Independently, in the three-parameter form $a\mathrm{Im}(w^4) + \mathrm{Im}(p^2)(b|w|^2 + c|p|^2)$, Singular elimination with the saturated Jacobian gives singular members exactly at $c^3(b^2 - 4ac)(b^2 + 4ac) = 0$; with $(a,b,c) = (1,s,-1)$ this is $(s^2+4)(s^2-4) = 0$. The wall members are described in 7.4.

**Item 2.** Every one of the 32 matrices is block-diagonal and satisfies $`G_s(Mz) = c\,G_s(z)`$ with the same $c$ for every $s$ (referee's check). The symplectic ones are those with $\det(M)/c = +1$.

**Item 4: the 40 lines.** In the graph chart $z_1 = Az_0 + Bz_3$, $z_2 = Cz_0 + Dz_3$, the Fano ideal over $\mathbb{Q}(s)$ has length 32, is radical, and splits into four components of degree 8:

- $C_1$: $C = -D$, $A = B = -(2D^5 - 3sD^3 + s^2 D)$, with $f_1(D) = 0$;
- $C_2$: $C = D$, $A = -B = -(2D^5 - 3sD^3 + s^2 D)$, with $f_1(D) = 0$;
- $C_3$: $A = D = 0$, $B = -(C^5 - 3sC^3 + 2s^2 C)/2$, with $f_2(C) = 0$;
- $C_4$: $B = C = 0$, $A = (D^5 - 3sD^3 + 2s^2 D)/2$, with $f_2(D) = 0$;

where $f_1(D) = 4D^8 - 8sD^6 + 5s^2D^4 - s^3D^2 + 1$ and $f_2(C) = C^8 - 4sC^6 + 5s^2C^4 - 2s^3C^2 + 4$. Each component lies on $G_s$ identically in $s$. Exactly 8 further lines meet $z_0 = z_3 = 0$ for every $s$ (the anchor lines of Section 3), giving 40. Rational spot checks give 32 distinct graph lines at $s = 1/3, 1, 9/4, 5/2, 13/5, 3, 7, -3$, and an independent stratified-chart computation gives 40 reduced lines at $s = 5/2$ and $13/5$ and 48 at $s = 0$. The discriminants of $f_1$ and $f_2$ are constants times $(s-2)^4(s+2)^4(s^2+4)^4$, so the graph lines collide only on the wall.

*Reducedness (ARGUED).* On a smooth quartic a line $L$ has normal bundle $\mathcal{O}_L(-2)$, so $H^0(N_L) = 0$ and every point of the Fano scheme is reduced.

*The jump set (EXACT).* Saturating the relative Fano scheme by $C_1, \dots, C_4$ leaves a scheme of length 64 whose eliminant in $s$ is $2s^4 - 81$. At Y56 the graph chart has length 48 with 48 distinct lines ($32 + 16$). The meeting stratum gains 8 lines only at $s = 0$, in the planes $z_2 = \pm i z_1$. The referee's minimal-prime decomposition together with the meeting stratum shows that no other $s$ carries extra lines.

**Item 7: why exactly $s^4 = 81/2$ (EXACT; a full proof).** The 16 special lines each pair an axis form in $(z_0, z_3)$ with a diagonal form $z_0 \pm z_3$. Take the shape $z_1 = \alpha z_0$, $z_2 = \beta(z_0 - z_3)$. Substituting into $G_s$, the $z_3^4$ coefficient vanishes identically and the other four must vanish; they generate the same ideal as the three equations:

```math
\alpha\beta\,(s - \alpha^2 - \beta^2) = 0, \qquad 2 + \alpha\beta\,(s - \beta^2) = 0, \qquad 1 + \alpha\beta^3 = 0.
```

The third equation makes $\alpha\beta \neq 0$, so the first gives $s = \alpha^2 + \beta^2$. The third gives $\alpha\beta = -1/\beta^2$; the second then reads $2 - (s - \beta^2)/\beta^2 = 0$, so $s = 3\beta^2$ and $\alpha^2 = 2\beta^2$. Squaring the third, $\alpha^2\beta^6 = 1$, so $2\beta^8 = 1$. Hence $s^4 = 81\beta^8 = 81/2$. Conversely $\beta = 2^{-1/8}$, $\alpha = -1/\beta^3$, $s = 3\beta^2$ is a real solution. For the axis–axis and diagonal–diagonal shapes only two equations remain, which is why those lines exist for every $s$. The group of order 32 moves the one line found this way through an orbit of 16. A Sympy Gröbner elimination of the same three-coefficient system gives exactly $2s^4 - 81$, in agreement with the Singular eliminant. The step is LEAN-CHECKED over any commutative ring (`pencil_forces`: the three equations force $s = 3\beta^2$, $\alpha^2 = 2\beta^2$, $2\beta^8 = 1$ and $2s^4 = 81$), together with the converse over $\mathbb{R}$ (`pencil_solvable`); see Section 8.

*Two independent identifications of the 16 (EXACT).* (i) A first-order test: for these 16 lines, $\partial G/\partial s$ restricted to the line is not in the image of the normal-bundle map (rank 4 against 5), so they do not deform along the pencil; the other 40 do. (ii) The shape test above. Both give the same 16 lines, and the relative Fano scheme has them as isolated points.

*The class $v$ (EXACT).* $v$ pairs to $+4$ with the eight lines $L06, L10, L29, L33, L35, L36, L50, L54$ ("plus") and to $-4$ with $L00, L11, L12, L19, L42, L44, L48, L55$ ("minus"), and to 0 with the other 40. (Sum of the minus eight) $-$ (sum of the plus eight) $= 2v$. $N_{19} + \mathbb{Z}v$ has index 8 in the 56-line lattice, consistent with $128 \cdot 32 / 8^2 = 64$.

**Item 8: the 48 conics.** Lines in the same set are pairwise skew, and each plus line meets exactly 6 minus lines, giving 48 pairs. For a meeting pair, $(L^+ + L^-)^2 = -2 - 2 + 2 = -2$ and $(L^+ + L^-) \cdot h = 2$; the $v$-components cancel, so the class lies in $N_{19}$, hence in $\mathrm{NS}$ of every member. By Riemann–Roch (CITED) it is effective on every member; it is not a sum of two persistent lines, so near Y56 it is an irreducible conic, and at Y56 it breaks into $L^+ \cup L^-$. One family is explicit (EXACT): the plane $z_2 = D(z_3 - z_0)$ with $f_1(D) = 0$, where the norm of the conic determinant is $2^{24}(2s^4 - 81)^2$, vanishing exactly at Y56.

**Item 5 and the lattice data.** On Y56 the 40 persistent lines span $N_{19}$ with rank 19, signature $(1,18)$, determinant 128 and Smith form $[2,8,8]$; it contains $h$ and is primitive in the 56-line lattice (rank 20, determinant $-64$, Smith form $[2,32]$). The same Gram data appear at $s = 1, 5/2, 13/5, 3$ and $7i/3$ (incidence there NUMERICAL at 40 digits, the algebra after it exact). Constancy of the Gram matrix on the whole smooth base is ARGUED: the 40 lines form a finite étale family over a connected base, and intersection numbers are locally constant.

**Item 6: $\mathrm{NS}$ of the very general member.** Two routes.

- *Primitivity (ARGUED, with EXACT inputs).* The inclusion $N_{19} \subset \mathrm{NS}(Y56)$ has all Smith invariants 1, so $N_{19}$ is primitive in $\mathrm{NS}(Y56)$ (EXACT; also checked by the referee). $\mathrm{NS}$ of the very general member specialises into $\mathrm{NS}(Y56)$ as a primitive sublattice (it is $H^2(\mathbb{Z})$ intersected with the orthogonal complement of the generic transcendental lattice, which contains $T(Y56)$), and it contains $N_{19}$ with finite index because the very general member has rank exactly 19 (the earlier argument below; item 3 gives only $\geq 19$) and by item 5. Both routes use rank exactly 19. A primitive lattice containing another primitive lattice of the same rank with finite index equals it. This uses $\mathrm{NS}(Y56) = $ the 56-line lattice (Section 4, with the CITED $\det T = 64$).
- *Enumeration (EXACT).* The discriminant group of $N_{19}$ has order 128 and exactly 14 nontrivial isotropic subgroups (orders 2, 4 and 8), each giving an even overlattice. Every one contains one of the three index-2 overlattices, and each of those contains explicit $(-2)$-vectors orthogonal to $h$ (22 or more) and 40 or more new $(-2)$-classes of degree 1. A root orthogonal to $h$ cannot lie in $\mathrm{NS}$ of a smooth quartic (ARGUED, standard: by Riemann–Roch it or its negative would be effective, of degree 0 against the ample $h$), and extra degree-1 $(-2)$-classes would give extra lines, against item 4. So all 14 overlattices are excluded. The enumeration searched short vectors with a positive definite form and a bound that covers both tests; a control run on $N_{19}$ itself finds 0 roots orthogonal to $h$ and exactly the 40 lines.

*Earlier argument for rank exactly 19 (ARGUED; Bouyer's method [B, section 4.3]).* If the very general member had rank 20, the period would be constant on the connected smooth base and all smooth members would share one transcendental lattice. But $T(X_0) = [8,0,8]$ and $T(Y56) = [2,0,32]$ (Degtyarev [D4, Table 1]; CITED) are not isometric. Item 6 builds on this and identifies the lattice itself.

**Item 9: real lines (EXACT).** For the 32 graph lines the relevant quartic is $q(s - \delta) = \delta^4 - s^2\delta^2 + 4$; the closed forms of $C_1$ to $C_4$ show that all 32 graph lines are real for $s > 2$ and none for $s < 2$. Sturm counts at 15 values of $s$ confirm this. The 8 anchor lines are real for every real $s$. The 16 special lines are real at $s = +s_*$ and not real at $s = -s_*$. At the Fermat member the 8 extra lines lie in $z_2 = \pm i z_1$ and none is real.

**Table 7.2. Line counts along the pencil** (EXACT unless marked).

| $s^4$ | member | complex lines | Fano length | real lines, $s > 0$ | real lines, $s < 0$ | Picard rank |
|---|---|---|---|---|---|---|
| 0 | Fermat type | 48 | 48 | 8 | 8 | 20 |
| other, below 16 | generic | 40 | 40 | 8 | 8 | 19 |
| 16 | wall | 24 | 40 | 24 | not computed | not computed |
| other, above 16 | generic | 40 | 40 | 40 | 8 | 19 |
| 81/2 | Y56 | 56 | 56 | 56 | 8 | 20 |

The rank at $s = 0$ uses numerical incidence with exact algebra after it, and agrees with the published $T = [8,0,8]$.

### 7.4 The wall

*Evidence:* `family/wall/` (`w1.sing` and `w1.log` for the nodes, `w3.sing` and `w3.log` with the control `w3c` for the lines, `f2_fermat.py` part (c) for the exact node coordinates).

**Plain words.** At $s = 2$ the surface pinches at 8 points. Through those points run four conics, two in each of two planes.

$W = G_2 = 4z_0^3 z_3 - 4z_0 z_3^3 + 4z_1 z_2(z_0^2 + z_3^2) - 2z_1 z_2(z_1^2 + z_2^2)$ has rational coefficients.

- **Nodes (EXACT, Singular over $\mathbb{Q}$).** The saturated Jacobian ideal and its radical both have length 8, and no node has Hessian rank $\le 2$: $W$ has exactly 8 ordinary nodes ($A_1$). Over $\mathbb{Q}$ they form 2 orbits of 4. With $t = 2\cos(\pi/8)$ ($t^4 - 4t^2 + 2 = 0$), $\sqrt2 = t^2 - 2$ and $t' = 2\sin(\pi/8) = t^3 - 3t$, the nodes are
  - in the plane $z_1 = -z_2$: $(1+\sqrt2 : -t : t : 1)$, $(1+\sqrt2 : t : -t : 1)$, $(1-\sqrt2 : t' : -t' : 1)$, $(1-\sqrt2 : -t' : t' : 1)$;
  - in the plane $z_1 = z_2$: $(-1+\sqrt2 : t' : t' : 1)$, $(-1+\sqrt2 : -t' : -t' : 1)$, $(-1-\sqrt2 : t : t : 1)$, $(-1-\sqrt2 : -t : -t : 1)$.

  All 8 are real; the gradient vanishes at each exactly in $\mathbb{Q}(t)$.
- **Two conics per plane (EXACT polynomial identity, hand-derived and consistent with Singular's decomposition).** $W|_{z_1 = -z_2} = 4(z_2^2 - z_0^2 + z_0 z_3)(z_2^2 - z_3^2 - z_0 z_3)$ and $W|_{z_1 = z_2} = -4(z_2^2 - z_0^2 - z_0 z_3)(z_2^2 - z_3^2 + z_0 z_3)$. Each pair of conics meets exactly at the 4 nodes in its plane.
- **Only two quadrics through the nodes (EXACT).** The ideal of the 8 nodes has minimal generators $z_1^2 - z_2^2$, $z_0^2 - 2z_2^2 + z_3^2$ and 4 cubics, so the nodes are not a Cayley octad, and $W$ is not a Kummer surface (which has 16 nodes).
- **Lines (EXACT).** $W$ carries 24 distinct lines, with Fano scheme of length 40 (stratified charts: length 39 with 23 lines in one chart, length 1 with 1 line in another; positive control on the Fermat member: 48 lines, length 48). From the discriminants of $f_1, f_2$, the 32 graph lines collide in 16 coincident pairs at the wall, so the wall has 8 simple lines and 16 double ones: $8 + 2 \cdot 16 = 40$. All 24 are real for the standard structure (Table 7.2).

We found no earlier description of this 8-nodal member, but the search was thin (three arXiv queries; search to 2026-11-20 of arXiv, Zenodo, citers).

### 7.5 The Fermat end

*Evidence:* `family/wall/f2_fermat.py` and `f2_fermat.log`, part (a).

**Plain words.** At $s = 0$ the surface is a disguised copy of the Fermat quartic $x^4 + y^4 + z^4 + t^4 = 0$. The disguise can be removed exactly, but only with a few square and fourth roots.

$G_0 = 4z_0 z_3(z_0^2 - z_3^2) - 2z_1 z_2(z_1^2 + z_2^2)$. Let $K = \mathbb{Q}(\zeta_8)(r)$ with $r^2 = 1 - i$, a field of degree 8 over $\mathbb{Q}$, and set

```math
y_0 = r(z_0 + iz_3),\quad y_1 = \zeta_8 r(z_0 - iz_3),\quad y_2 = z_1 - z_2,\quad y_3 = \zeta_8(z_1 + z_2).
```

Then $y_0^4 + y_1^4 + y_2^4 + y_3^4 = 4G_0(z)$ exactly, with $\det = -4(\zeta_8^2 - 1) \neq 0$ (EXACT, sympy reduction modulo $\zeta^4 + 1$ and $r^2 - (1 - \zeta^2)$). The reason: $\mathrm{Im}(w^4) = (w^4 - \bar w^4)/2i$, $2ab(a^2 + b^2) = ((a+b)^4 - (a-b)^4)/4$, and $r^4 = -2i$.

The Fermat member and Y56 are different K3 surfaces: $T = [8,0,8]$ for Fermat against $[2,0,32]$ for Y56 (DIS Table 2; Shimada–Shioda [SS]; Degtyarev [D4]; CITED). So the pencil joins genuinely different surfaces.

### 7.6 The six faces along the pencil

*Evidence:* `family/wall/f2_fermat.py` parts (b) and (c); `family/faces/c_family.py`, `c_nodes_sister.py`, `c_fermat_det.py` and their logs. The three-parameter discriminant of Section 7.3, item 1, is `family/faces/c_fam.sing` and `c_fam.log`.

Every one of the 32 maps acts on every member, so all six real structures live on every real member of the pencil.

- **Real nodes at the wall (EXACT, tested in $\mathbb{Q}(t)$):** $g_{00}$ 8, $g_{01}$ 2, $g_{02}$ 0, $g_{12}$ 2, $g_{13}$ 4, $g_{24}$ 0.
- **Real structures on the Fermat member (EXACT).** Transporting the 16 structures to Fermat and testing all 1536 projective automorphisms of the Fermat quartic in exact $K$-arithmetic merges the six classes into two: $`\{g_{00}, g_{02}, g_{13}, g_{24}\}`$ and $`\{g_{01}, g_{12}\}`$. This assumes the standard description of $\mathrm{Aut}$(Fermat) as the order-1536 monomial group.
- **The Fermat route for $g_{02} \sim g_{24}$ (ARGUED, with numerical steps).** Both see no real wall node; the path from Y56 along the pencil can be pushed off the wall inside smooth real quartics (conjugate node pairs have real codimension 2), reaches the Fermat member, where the two structures are equivalent by an automorphism that can be chosen in the identity component of $PGL(4,\mathbb{R})$, and returns. This agrees with the CITED classification of Section 6. The same route does not connect $g_{01}$ or the three-sphere faces.
- **Vanishing bubbles (NUMERICAL).** In the face $g_{12}$ the two real wall nodes are definite and lie in the two bare spheres: moving toward the wall, the two oval-free spheres shrink to points and disappear, while the sphere carrying all 22 ovals survives. Mesh Euler characteristics on the two sides change by twice the number of real nodes in every face.

### 7.7 Figures

**Figure 7.** `media/y56_to_fermat.gif` (video: `media/y56_to_fermat.mp4`). *Y56 bent step by step along the pencil toward the Fermat end, with a fixed camera in the sphere model. The real lines drop from 56 to 40 the instant the dial leaves Y56, to 24 at the wall, where the surface pinches at 8 points (the paused frames, gold), and to 8 beyond it. Amber: the 16 lines that exist only at Y56. Cyan: the 8 anchor lines present on every member. Pink: the rest.* (The animation's line tracking is numerical; the counts it shows agree with Theorem 7.1, item 9.)

**Figure 8.** `media/y56_wall.png`. *The wall member: 8 pinch points (gold) and the four conics through them, two in each of the planes $z_1 = \pm z_2$. Each plane holds 4 pinch points and cuts the surface in two conics meeting exactly there.*

**Figure 9.** `media/y56_family_strip.png`. *Five snapshots from one camera: Y56, a step toward the wall, the wall, a step beyond it, and the Fermat-type end. The real lines drop from 56 to 40, 24 and 8.*

**The viewer dial.** The interactive viewer (Section 9) has a "family dial" for $s$ from 0 to 3, with stops at the Fermat member, the wall and Y56. The surface is re-meshed live, the real lines are recomputed from the closed forms of 7.3, a counter shows 8 / 24 / 40 / 56 real lines, the 8 nodes are drawn at the wall, and at $s_*$ the 16 lines are added from the exact data and flash. The dial shows lines only; the 48 conics are not drawn.

---

## 8. Machine-checked layer

**Plain words.** Programs such as Singular, GAP or sympy are trusted, not proved correct. A proof assistant re-checks a statement down to a few basic axioms, with a small trusted kernel. We moved the finite exact facts of Sections 2 to 5, and the key step of the pencil, into Lean 4 with Mathlib. Ten files, 524 theorems, all accepted by Lean's kernel. For each item a deliberately broken copy of the input is rejected.

**Setup.** Lean v4.36.0-rc2 with Mathlib v4.36.0-rc2 (`lean/lean-toolchain`, `lean/lakefile.toml`, `lean/lake-manifest.json`). Every finite computation is evaluated by the kernel (`decide +kernel`) in `Zsqrtd 2`, the ring $\mathbb{Z}[\sqrt2]$; every polynomial identity is closed by `ring` or `linear_combination` with an explicit cofactor. A generator script (`lean/export_lean.py`) writes the data-driven files from the release data; the certificates it computes are only hints, and the kernel re-checks each one, so no computer algebra system is trusted. A ring map $\iota: \mathbb{Z}[\sqrt2] \to R$ sending $\sqrt2$ to any $s$ with $s^2 = 2$, injective in characteristic 0 (`iota_injective`), carries each statement to $\mathbb{R}$ and $\mathbb{C}$.

**Table 8.1. What is LEAN-CHECKED.**

| item | file | theorems | what it proves, in plain words | claim it supports |
|---|---|---|---|---|
| L1 | `Y56_L1.lean` | `lines_on_F`, `lines_distinct`, `lines_genuine` | Every point of each of the 56 listed lines satisfies $F = 0$ (280 coefficients vanish in $\mathbb{Z}[\sqrt2]$); the 56 lines are pairwise different (a nonzero $3 \times 3$ minor for each of 3080 ordered pairs); each pair of spanning vectors is independent. | Theorem 3.1, lower bound |
| L7 | `Y56_L7.lean` | `eightfold`, `screw`, `screw_coord`, `galois_twist` | The eight-fold form of $F$; the screw sends $G$ to $-G$, also in coordinates ($F(z_0 - z_3, -\sqrt2 z_2, \sqrt2 z_1, z_0 + z_3) = -4F(z)$); $F_e(z_0, -z_2, z_1, z_3) = F_{-e}(z)$ as a ring identity. | Section 2; Theorem 5.1, item 5 |
| Pencil | `Y56_Pencil.lean` | `pencil_forces`, `pencil_solvable` | Over any commutative ring, the three equations of Section 7.3 (equivalent to the coefficient equations; the substitution itself is not in Lean) force $s = 3\beta^2$, $\alpha^2 = 2\beta^2$, $2\beta^8 = 1$ and $2s^4 = 81$; a real solution exists. | Theorem 7.1, item 7 (Section 7.3) |
| L2 | `Y56_L2.lean` | `sym_g00` to `sym_g31`, `maps_lines`, `group_facts`, `group_closed`, `matrices_compose`, `order_counts`, `orbit_sizes` | Each of the 32 matrices satisfies $F(Mz) = cF(z)$ and maps line $i$ onto line $\sigma(i)$; the 32 permutations form a group (identity, distinct, closed under all 1024 products and under inverses); matrix products match the table up to a nonzero scalar; element orders 1, 2, 4, 8 occur 1, 15, 8, 8 times; the line orbits have sizes 8, 16, 16, 16 (representatives L02; L00, L01, L03). | Theorem 5.1, items 1 to 3 |
| L3 | `Y56_L3.lean` | `meets_iff_edge`, `edge_counts` | Two different lines meet exactly when they form an edge of `core/data/edges.json`; 448 edges, every line meets 16 others, 1092 skew pairs. | Section 3, incidence graph |
| L6 | `Y56_L6.lean` | `planes_lines`, `plane_rows`, `inPlane_iff_listed`, `line_in_plane_iff`, `pc_rows`, `dist_rows`, `plane_pairs_are_edges`, `edge_cover` | Each of the 198 stored line planes contains exactly its listed lines (148 with two, 50 with four); the 20 conic-pair planes contain none; all 218 planes are different; $148 \cdot 1 + 50 \cdot 6 = 448$ and each edge lies in exactly one stored plane. | Theorem 4.1, items 1 to 3 |
| L5 | `Y56_L5a.lean`, `Y56_L5b.lean`, `Y56_L5c.lean` | `secP2_000..147`, `secP4_000..049`, `secPC_000..019`, `conics_nondegenerate`, `conic_irreducible` | In every plane a constant times the section equals line × line × conic, four lines, or conic × conic; all 188 conics have nonzero Hessian determinant and are not products of two linear forms. | Theorem 4.1, items 1 to 3 |
| L8 | `Y56_L8.lean` | `det_GB`, `rows_in_span`, `hyperplane_class` | A $20 \times 20$ block of the intersection matrix has determinant $-64$ (Mathlib's `Matrix.det`); every row of the $56 \times 56$ matrix is an integer combination of its 20 rows, so the line lattice has rank 20 and discriminant $-64$ (given $\rho \le 20$ and $L^2 = -2$, cited); $h = L00 + L06 + L23 + L24$ has $h^2 = 4$ and $h \cdot L = 1$ for every line. | Section 4, completeness proof (Gram data) |

**Axioms.** `#print axioms` for the 524 theorems gives: none (1), `propext` (148), `propext` and `Quot.sound` (283), `propext`, `Classical.choice` and `Quot.sound` (92), Lean's three standard axioms. No file contains `sorry`, `admit`, an `axiom` declaration or `native_decide`. The full printout is `lean/recorded-run.log`.

**Controls.** Every positive file passes. Eight negative controls each change one input and are rejected: a coordinate of one line (L1), the sign of $e$ in the Galois twist (L7), $2s^4 = 80$ instead of 81 (Pencil), two swapped matrix entries (L2), one dropped edge (L3), one deleted plane (L6), one conic coefficient (L5), one adjacency entry (L8). The error texts are shipped as `lean/*_neg.expected-error.txt`.

**What is not formalised.**

- *Not done:* the smoothness certificate; the name $\mathrm{Hol}(C_8)$ and the plane-orbit tables; real points on the 188 conics; the 636 lattice classes; the wall nodes, the two-conic identities and the Fermat bridge; the incidence types (4,4) and (3,7); the six-face traces; and the upper bound "exactly 56 lines over $\mathbb{C}$" (open question 1).
- *Two printouts in L2.* The 32 `sym_gXX` statements and the matrix table used by `maps_lines` are generated from the same parse of `symmetry_exact.txt`, but no Lean proof links them; the release referee compared them by script: identical (`checks/atlas-referee/ref_lean_data.out`).
- *L5 coordinates.* L5 recomputes the conics in its own plane coordinates; they were not compared with the conic strings in `core/data/conic_pair_planes_exact.txt`.
- *Geometry in words.* "Two distinct meeting lines span exactly one plane" and "a nondegenerate conic, or a non-proportional Plücker pair, is the geometric object" are stated in words only.
- *Cited facts.* $\mathrm{NS}(Y56) = N$ (which uses the published $\det T = 64$) and the self-intersection $-2$ of a line are cited, not proved. More generally, K3 theory, the Hodge index and Lefschetz formulas, the Nikulin–Kharlamov classification, the topology from meshes and Morse counts, the completeness of the automorphism group, the whole of Theorem 7.1 apart from the algebra after the substitution, and the provenance of the equation stay outside Lean.
- *Statement match.* A referee matched every Lean statement with the sentence that quotes it (`checks/atlas-referee/REFEREE-ATLAS.md`).

How to re-run: `lean/README.md` (`lake exe cache get`, then `sh run_all.sh`; about 7 minutes and 10 GB of memory).

---

## 9. Reproducibility

**Plain words.** One command re-checks the exact core data, and one script re-checks the Lean layer. Every other program run is shipped as a transcript, and a fresh copy of the core reproduced all of its runs.

- **One command.** From `core/`: `python code/verify_all.py` (needs sympy). It reads only the shipped data files, works in exact arithmetic over $\mathbb{Q}(\sqrt2)$, and runs 21 checks in about 1.5 to 2.5 minutes: data loading; lines on $F$ and distinct (1a, 1b); 448 edges, 16-regular (2a, 2b); the 32 symmetries, group closure and line orbits (3a to 3d); the 148 + 50 planes and their factorisations (4a to 4e); the 20 conic-pair planes (5a, 5b); real points of all 188 conics (6a, 6b); plane orbits (7a to 7c). The recorded run passes 21 of 21. It does not re-run Singular, msolve, GAP or PARI; their outputs are shipped as transcripts.
- **Clean room.** The code, data and requirements were copied into a fresh folder and every documented command was run with nothing else. All runs reproduced the shipped outputs; the Singular, msolve and GAP outputs were byte-identical, and the only other differences were timing lines. Tools: Python 3.11.9 (sympy 1.14.0, networkx 3.6.1); Singular 4.4.1, msolve 0.10.1, GAP with the SmallGroups data and PARI (via passagemath 10.8.14) under WSL2 Ubuntu 24.04. One operational finding: PARI's parallel `qfminim` fails or hangs under a small virtual-memory cap; uncapped it uses under 0.2 GB.
- **Referee re-derivation.** A hostile referee re-derived every headline number of the core with independent code (56 lines and 448 crossings; 32 symmetries and orbits; lattice rank 20 with invariant factors $1^{18}, 2, 32$; conic counts 636, 448, 188, 20; 64 graph automorphisms by a second algorithm; Euler numbers of the six faces). `verify_all.py` passed 21 of 21 and the file manifest 75 of 75. The pencil theorem was re-derived by a second referee with its own Singular and sympy code. The referees' scripts and transcripts are in `checks/`.
- **The viewer.** A static web page (three.js r160) with three modes: Y56 with its lines and conics (hover a line to see its exact coordinates and its 16 neighbours), the family dial of Section 7.7, and the six faces. Its data file is generated from the exact release data with no hand-typed coordinates, and an accuracy script passes 53 of 53 checks: every drawn line and conic point lies on the surface to float32 accuracy, the six-face counts equal Table 6.1, the family lines lie on $G_s$ at 307 dial values, the real counts are 8 / 24 / 40 / 56 in the right ranges, the 16 Y56-only lines are one orbit, and the 8 gold points at the wall are singular. The surface is a marching-cubes mesh, so it is a drawing, not evidence. The page is `viewer/index.html`.
- **The pencil and the family.** The scripts and transcripts behind Section 7 are in `pencil/` (Singular inputs with their logs, sympy scripts, the overlattice enumeration and the GAP identification of SD16), and those behind the wall, the Fermat bridge and the faces along the pencil are in `family/`. They are shipped as run, with only their paths made relative; the scripts in `family/` have not been re-run from this layout.
- **Lean.** `lean/run_all.sh` re-checks all ten files and the eight controls (Section 8).

---

## 10. Open questions

From the loose ends of all parts of this work.

1. **Kernel-checked upper bound.** "No 57th line" rests on Singular, with msolve as a probabilistic cross-check; the Lean layer proves only the lower bound. Whether a Gröbner certificate small enough for Lean exists is unknown.
2. **$\mathrm{NS}(Y56) = N$ without citation.** Completeness of the conics, and the primitivity route of Theorem 7.1(6), use the published $\det T = 64$; we did not re-derive it.
3. **DIS's 24 explicit lines.** Our 56 lines have not been matched one by one with the 24 that DIS write out.
4. **The 48 conics.** Only one family of 8 has explicit equations; their reality for real $s$, and their relation to Y56's 148 two-line-plane conics, are not determined. The overlattice enumeration of Theorem 7.1(6) did not reach degree-2 classes, so it does not count them.
5. **The wall and the end.** The lattice of the wall member and the $s = \infty$ end are not analysed; real lines at $s = -2$ and which of the wall's lines pass through nodes are not computed.
6. **The five other faces along the pencil.** Real line counts for the non-standard real structures at generic members are not computed.
7. **Other Noether–Lefschetz points.** Points of the pencil where the Picard rank jumps without a jump in lines were not located.
8. **A mod-$p$ check.** Bouyer's reduction mod $p \equiv 3 \pmod 4$, where Fermat is supersingular, would give a third route to generic rank 19 and to the generic Gram matrix.
9. **$g_{12}$ versus $g_{13}$.** They are not isomorphic as real quartics, but whether they are isomorphic as abstract real K3 surfaces, through an automorphism of infinite order, is open.
10. **Explicit deformation paths** between the faces of one family were not built; the classes come from the cited classification read from a page image.
11. **Genus-2 faces.** Which handles carry the real lines and ovals is not known.
12. **Orbits of the conics.** The line orbits are tabulated (Appendix A); the orbits of the 188 conics are not.
13. **The 8-nodal wall** has no name we could find, after a thin search.
14. **Prior-art residuals.** Journal versions of Rams–Schütt and Veniani (which might carry figures) were not opened; an OpenAlex citation re-run is owed; Wolfram Demonstrations and MathWorld pages and Kharlamov's surveys (for a Y56 table) were not opened.

**Curiosities (UNTESTED; leads, not claims).**

- *Star points (NUMERICAL from exact lines).* The 448 meeting pairs meet in 406 distinct points: 388 points on 2 lines, 16 on 3, and 2 on 4 (the points $(0:1:0:0)$ and $(0:0:1:0)$). The 50 four-line planes would then split as 2 stars, 16 "three concurrent plus one" and 32 general quadrilaterals, a split the line graph cannot see. Not re-checked exactly.
- *Doughnut slices.* On the Hopf tori of $S^3$ the real Y56 is the curve $\sin 4a = -\rho\sin 2b$ with $\rho = \tau(3-\tau)/\sqrt2$; a hand Morse count ($8 + 4$ discs and $3 \times 16$ saddles) gives lifted $\chi = -36$, an elementary picture of genus 10. Hand work, not machine-checked.
- *Vanishing bubbles.* Prediction: in every real face of the pencil, the curve-free components are exactly those that collapse at a definite wall node.
- *A lattice fingerprint.* For the three-sphere faces $h$ is 2-divisible in the anti-invariant lattice and lies in $(1-\sigma)H$; does this mark contractible real parts in general?
- *An arithmetic ladder.* Fermat is reached over a degree-8 field, Y56 lives over $\mathbb{Q}(\sqrt2)$, the wall over $\mathbb{Q}$ with nodes over $\mathbb{Q}(\cos\pi/8)$.
- *Where else.* Does the full symmetry of the line configuration of other record quartics (for example Schur's $X_{64}$) also come from a Galois twist?
- *The number 40.* Degtyarev [D5] finds supersingular quartics in characteristic 2 with 40 lines; no link to our characteristic-0 family is known.

---

## Corrections we made along the way

Each of these was found by us and fixed before release; each made the result stronger. The full list, with where each fix lives, is `CORRECTIONS.md`.

1. A first numerical search listed 20 "line-free conic-pair planes"; exact re-testing showed 19 of them contained lines. The true 20 were found inside the fixed planes of the 15 involutions and proved exactly.
2. Early conic pictures drew 38 line pairs as if they were conics; they were replaced by pictures of the exactly verified 40 conics.
3. Our first checker wrongly failed some correct planes (the test, not the data, was at fault).
4. The first rotation animation repeated a 90° symmetry; it was replaced by the eighth-turn screw loop.
5. A first Singular transcript lost its first line and a first run printed a wrong dimension (a free variable was left in the ring); the clean rerun is shipped.
6. Working captions said "the maximum possible 56 lines", which is false for complex lines (64 is possible) and true for real lines (DIS Corollary 1.3); the wording now says real lines, with that credit.
7. The referee found that the class sizes of the six real faces were attached to the wrong faces in one draft; they now read 1, 4, 1, 4, 4, 2 for 56, 12, 8, 4, 0, 0 real lines. Check 4d was extended to test nondegeneracy of the 148 conics.
8. Since the pencil joins Y56 to the Fermat member, we checked whether they could be the same K3 surface; the published transcendental lattices ($[2,0,32]$ against $[8,0,8]$) rule this out, so the pencil joins different surfaces.
9. Our first argument for generic rank 19 concluded, from a constant period, that all smooth members would be projectively equivalent, and used the different line counts against that; the refereed version uses the non-isometric transcendental lattices instead, and the overlattice computation now identifies the generic lattice exactly.

---

## Appendix A. The 56 lines

Each line is the span of two points $(z_0 : z_1 : z_2 : z_3)$, copied by script from the release file `core/data/lines_exact.txt` (sympy notation, `sqrt(2)` $= \sqrt2$). Orbit column, computed exactly from the 32 line permutations in `core/data/symmetry_exact.txt`: **8** = the 8-orbit (the anchor lines in $z_1 = 0$ or $z_2 = 0$, on every member of the pencil); **S** = the orbit of L00, the 16 lines that exist only at Y56 in the pencil (Theorem 7.1, item 7); **A** = the orbit of L01 and **B** = the orbit of L03, the other two 16-orbits (their lines persist along the pencil). Each line meets exactly 16 others (EXACT; LEAN-CHECKED).

| line | point 1 | point 2 | orbit |
|---|---|---|---|
| L00 | (sqrt(2)/2, 1, 0, sqrt(2)/2) | (0, 0, 1, 1) | S |
| L01 | (1, 0, -2 + sqrt(2), -1) | (0, 1, -3 + 2*sqrt(2), -2 + sqrt(2)) | A |
| L02 | (0, 1, 0, 0) | (0, 0, 0, 1) | 8 |
| L03 | (1/2, 1, 0, 0) | (0, 0, 1, sqrt(2)/2) | B |
| L04 | (-2 + sqrt(2), -3 + 2*sqrt(2), 1, 0) | (1, 2 - sqrt(2), 0, 1) | A |
| L05 | (1/2, 1, 0, 1/2) | (-sqrt(2)/4, 0, 1, sqrt(2)/4) | B |
| L06 | (sqrt(2)/2, 1, 0, -sqrt(2)/2) | (0, 0, 1, 1) | S |
| L07 | (0, 1, 0, 1/2) | (-sqrt(2)/2, 0, 1, 0) | B |
| L08 | (-1 + sqrt(2), 1, 0, 0) | (0, 0, -1 + sqrt(2), 1) | A |
| L09 | (-1 + sqrt(2), 0, 1, 0) | (0, -1 + sqrt(2), 0, 1) | A |
| L10 | (1, 0, -1, 0) | (0, 1, sqrt(2)/2, sqrt(2)/2) | S |
| L11 | (1, 0, 1, 0) | (0, 1, -sqrt(2)/2, -sqrt(2)/2) | S |
| L12 | (1, 0, -1, 0) | (0, 1, -sqrt(2)/2, sqrt(2)/2) | S |
| L13 | (2 - sqrt(2), 1, 3 - 2*sqrt(2), 0) | (-1, 0, -2 + sqrt(2), 1) | A |
| L14 | (1, 0, 0, 0) | (0, 0, 1, 0) | 8 |
| L15 | (1, -2 + sqrt(2), 0, -1) | (0, -3 + 2*sqrt(2), 1, -2 + sqrt(2)) | A |
| L16 | (1, 0, 1 - sqrt(2), 0) | (0, 1, 0, -1 + sqrt(2)) | A |
| L17 | (1, 2 - sqrt(2), 0, -1) | (0, -3 + 2*sqrt(2), 1, 2 - sqrt(2)) | A |
| L18 | (-1/2, 1, 0, 1/2) | (-sqrt(2)/4, 0, 1, -sqrt(2)/4) | B |
| L19 | (1, 1, 0, 0) | (-sqrt(2)/2, 0, 1, -sqrt(2)/2) | S |
| L20 | (1/2, 1, 0, -1/2) | (sqrt(2)/4, 0, 1, sqrt(2)/4) | B |
| L21 | (0, 1, 0, -1/2) | (sqrt(2)/2, 0, 1, 0) | B |
| L22 | (1, 0, 0, -1) | (0, 1, 0, 0) | 8 |
| L23 | (sqrt(2)/2, 1, 0, 0) | (0, 0, 1, -1/2) | B |
| L24 | (0, 0, 1, 0) | (0, 0, 0, 1) | 8 |
| L25 | (1, -1 + sqrt(2), 0, 0) | (0, 0, 1, 1 - sqrt(2)) | A |
| L26 | (1 - sqrt(2), 0, 1, 0) | (0, 1 - sqrt(2), 0, 1) | A |
| L27 | (0, 0, 1, 0) | (1, 0, 0, 1) | 8 |
| L28 | (sqrt(2)/4, 1, 0, sqrt(2)/4) | (1/2, 0, 1, -1/2) | B |
| L29 | (0, 1, 0, 1) | (sqrt(2)/2, 0, 1, sqrt(2)/2) | S |
| L30 | (1, 0, 0, 0) | (0, 1, 0, 0) | 8 |
| L31 | (1, -2 + sqrt(2), 0, 1) | (0, 3 - 2*sqrt(2), 1, -2 + sqrt(2)) | A |
| L32 | (-1/2, 1, 0, 0) | (0, 0, 1, -sqrt(2)/2) | B |
| L33 | (-sqrt(2)/2, 1, 0, sqrt(2)/2) | (0, 0, 1, -1) | S |
| L34 | (-sqrt(2)/4, 1, 0, sqrt(2)/4) | (1/2, 0, 1, 1/2) | B |
| L35 | (0, 1, 0, -1) | (-sqrt(2)/2, 0, 1, -sqrt(2)/2) | S |
| L36 | (1, 0, 1, 0) | (0, 1, sqrt(2)/2, -sqrt(2)/2) | S |
| L37 | (-sqrt(2)/2, 1, 0, 0) | (0, 0, 1, 1/2) | B |
| L38 | (1, 1 - sqrt(2), 0, 0) | (0, 0, 1, -1 + sqrt(2)) | A |
| L39 | (-sqrt(2)/4, 1, 0, -sqrt(2)/4) | (-1/2, 0, 1, 1/2) | B |
| L40 | (0, 1, 0, sqrt(2)/2) | (1/2, 0, 1, 0) | B |
| L41 | (-1/2, 1, 0, -1/2) | (sqrt(2)/4, 0, 1, -sqrt(2)/4) | B |
| L42 | (1, -1, 0, 0) | (0, sqrt(2)/2, 1, sqrt(2)/2) | S |
| L43 | (0, 1, 0, 0) | (1, 0, 0, 1) | 8 |
| L44 | (0, 1, 0, -1) | (-sqrt(2)/2, 0, 1, sqrt(2)/2) | S |
| L45 | (sqrt(2)/4, 1, 0, -sqrt(2)/4) | (-1/2, 0, 1, -1/2) | B |
| L46 | (2 - sqrt(2), 1, -3 + 2*sqrt(2), 0) | (1, 0, -2 + sqrt(2), 1) | A |
| L47 | (1, 0, 2 - sqrt(2), 1) | (0, 1, 3 - 2*sqrt(2), 2 - sqrt(2)) | A |
| L48 | (-sqrt(2)/2, 1, 0, -sqrt(2)/2) | (0, 0, 1, -1) | S |
| L49 | (1, 0, -1 + sqrt(2), 0) | (0, 1, 0, 1 - sqrt(2)) | A |
| L50 | (-1, 1, 0, 0) | (-sqrt(2)/2, 0, 1, sqrt(2)/2) | S |
| L51 | (1 - sqrt(2), 1, 0, 0) | (0, 0, 1 - sqrt(2), 1) | A |
| L52 | (0, 1, 0, -sqrt(2)/2) | (-1/2, 0, 1, 0) | B |
| L53 | (1, 0, 0, -1) | (0, 0, 1, 0) | 8 |
| L54 | (1, 1, 0, 0) | (0, -sqrt(2)/2, 1, -sqrt(2)/2) | S |
| L55 | (sqrt(2)/2, sqrt(2)/2, 1, 0) | (0, 1, 0, 1) | S |

---

## References

Only sources we opened are listed (text read, or scanned for figures where stated). arXiv identifiers as recorded in our prior-art searches (`PRIOR-ART.md`).

- [DIS] Degtyarev, Itenberg, Sertöz, arXiv:1601.04238 (Math. Ann., DOI 10.1007/s00208-016-1484-0). Equation (9.4), section 9.2, Theorem 1.1, Corollary 1.3, Lemma 6.14, Theorem 3.10, Addendum 1.4, Proposition 9.9, Remarks 9.10 and 9.11, Proposition 9.12, Table 2.
- [V2] Veniani, arXiv:1708.01219. Table 1 (row for Y56), section 3.3, section 6.7.
- [V1] Veniani, "The maximum number of lines lying on a K3 quartic surface", arXiv:1502.04510 (scanned; background).
- [D1] Degtyarev, arXiv:2407.00493. Section 1.2 and Remark 7.4.
- [D2] Degtyarev, arXiv:2512.06833. Section 3.1.
- [D3] Degtyarev (as credited in our prior-art search), arXiv:2509.24349. Remark 3.2; Figure 4.
- [D4] Degtyarev, arXiv:1608.06746. Table 1.
- [D5] Degtyarev, arXiv:1604.05836 (supersingular quartics in characteristic 2; curiosity only).
- [DR] Degtyarev, Rams, arXiv:2301.04127. Table 1, Theorem 1.2.
- [H] Hashimoto, arXiv:1012.2682. Table 10.1.
- [B] Bouyer, arXiv:1511.01781. Section 3, section 4.3.
- [DK] Degtyarev, Kharlamov, survey, arXiv:math/0004134. Section 3.5.4 and the tables on journal pp. 29–30.
- [SS] Shimada, Shioda, arXiv:1604.06265. Equation (3.1).
- [RS1] Rams, Schütt, "64 lines on smooth quartic surfaces", arXiv:1212.3511.
- [RS2] Rams, Schütt, "Counting Lines on Quartic Surfaces", arXiv:1505.02018.
- [RS3] Rams, Schütt, "At most 64 lines on smooth quartic surfaces (characteristic 2)", arXiv:1512.01358.
- [K16] "Real Quartic Surfaces in RP3 containing 16 Skew Lines", arXiv:math/0112195 (the nearest earlier drawings: Maple plots of a different surface).
- [Q] arXiv:2608.05941 (real structures in equisingular strata of quartics; does not treat Y56).
- [T] T. Karl, "The maximum number of lines on a smooth quartic surface", MSc thesis, Leiden, 2025, hdl.handle.net/1887/4262234 (no Y56 content; background).
- Also checked and not used: Zenodo record 14360457, "Line arrangements on smooth quartics".

Read at abstract level only (cited for the genre, not for content): [BS] Barth, Sarti, arXiv:math/0301329.

Software: Singular, msolve, GAP (SmallGroups library), PARI/GP (via cypari2), sympy, networkx, igraph, python-flint, three.js, Lean 4 with Mathlib.

---

Written with AI assistance.
