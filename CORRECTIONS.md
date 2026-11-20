# Corrections

Moki & Julio (AI-assisted) · version 1.0

Errors we made, found ourselves (or our referees found), and fixed before this release. Each one is a win: the shipped data, text and pictures are the corrected ones. Items 1 to 7 come from the core release (`core/`), items 8 to 10 from the pencil and the paper, items 13 to 17 from the final referee round (`checks/atlas-referee/`), items 11 and 12 from the final editing pass.

## 1. The numeric pass misidentified 19 of 20 conic-pair planes

A numeric search produced a list of 20 planes said to cut two conics and hold no line. Re-deriving the plane normals at full precision and testing them exactly showed that 19 of the 20 contain lines (10 hold two lines, 9 hold four), and in each of those at least one of the stored "conics" was really a pair of lines. Only one plane in that list was a true line-free conic-pair plane.
Fix: the true 20 planes were found by a numeric search inside the planes fixed by the 15 involutions of the group, then proved exactly over Q(sqrt2): 20 of 20, with orbits 8 + 8 + 4, and checked again by `core/code/verify_all.py` (checks 5a, 5b) and in Lean (`Y56_L5c.lean`, `Y56_L6.lean`). The earlier numeric file is not shipped.
Where: `core/docs/EXACT-2.md`, `core/data/conic_pair_planes_exact.txt`.

## 2. The old violet conic pictures showed line pairs

Every earlier conic picture drew 40 violet "conics" from that numeric list. Thirty-eight of the 40 were line pairs, not conics. Those pictures are not shipped. The pictures in `core/media/` use the corrected, exactly verified 40 conics.
Where: `core/media/y56_conics_v2_a.png`, `core/media/y56_conics_v2_sphere.png`.

## 3. Our first checker wrongly failed some of the 20 planes

While writing the one-command checker, its first test for the conic-pair planes (are the plane section and the product of the two listed conics proportional by a constant ratio?) reported failures on some of the 20 planes (our debugging notes examined three of them; the exact count of failures was not kept), although the data were right: the test was at fault, not the data. The shipped check 5a matches the section against a constant times the product by coefficients and passes 20 of 20.
Where: `core/code/verify_all.py`, check 5a. The record of the first attempt is not shipped.

## 4. The earlier rotation GIF looped by a 90-degree symmetry

The first rotation animation turned only one complex coordinate. A quarter turn of that coordinate is an exact symmetry of the surface, so the 180-degree sweep was two copies of one 90-degree loop, and the frames at 0 and 90 degrees were identical. It also carried the wrong violet set from item 2.
Fix: the screw loop in `core/media/y56_screw.gif` turns both coordinates at once (one twice as fast as the other) through an eighth of a turn; at the end the equation changes sign and the surface is the same, so the loop closes. This was checked numerically (6e-14), and the screw identity is now also checked in Lean (`screw`, `screw_coord`).
Where: `core/docs/SISTERS.md` section 4.

## 5. A first Singular transcript lost its first line

The first transcript of the line count lost its first line (a shell redirect overwrote it), and the first run printed a wrong dimension because a variable was left in the ring. The mathematics was unaffected; we re-ran the whole computation cleanly and ship that transcript (degree 56, other charts empty, 0 of 56 lines failing).
Where: `core/data/logs/fano_rerun.out`, `core/docs/LINES-COUNT.md`.

## 6. Picture captions said "maximum possible 56 lines"

Our working captions called Y56 the surface holding "the maximum possible 56 straight lines". Smooth quartic surfaces over the complex numbers can hold up to 64 lines (the Schur quartic; Rams and Schütt), so the wording was ambiguous: it is false for complex lines but true for real lines (DIS, Corollary 1.3). The released text states the real-line maximum with that credit.
Where: `core/media/CAPTIONS.md`, `README.md`.

## 7. Note on "only one line-free plane"; class sizes of the six faces; check 4d

An early note said only one of the 20 line-free planes was a genuine conic pair and the others had not been searched for. That note is replaced by a pointer to the exact result (`core/docs/EXACT.md`, `core/PATCHES.md`).
The core referee also found that in one draft the class sizes of the six real faces were attached to the wrong faces; they now read 1, 4, 1, 4, 4, 2 for the faces with 56, 12, 8, 4, 0, 0 real lines (16 real structures in all). At the same time check 4d of `verify_all.py` was extended to test that all 148 conics are nondegenerate (exact determinant nonzero).
Where: `RESULTS.md` R15, `core/docs/SISTERS.md`, `core/docs/VERIFY-RUN.txt`, `checks/core-referee/REFEREE.md` (fixes F1 and F8).

## 8. Y56 and the Fermat member are different K3 surfaces

Since the pencil joins Y56 to the Fermat-type member, an early working note treated them as possibly the same abstract K3 surface. We checked: the published transcendental lattices, $[2,0,32]$ for Y56 and $[8,0,8]$ for Fermat (DIS Table 2; Shimada and Shioda; Degtyarev), are not isometric, so the pencil joins genuinely different surfaces.
Where: `PAPER.md` sections 7.2 (item 6) and 7.5.

## 9. The first argument for generic rank 19 was wrong

Our first argument for "the very general member has Picard rank exactly 19" said that a constant period would make all smooth members projectively equivalent, and used the different line counts (40, 48, 56) against that. A constant period does not give projective equivalence. The refereed version uses the non-isometric transcendental lattices of two members instead (Bouyer's method), and the overlattice computation now identifies the generic Néron–Severi lattice exactly as $N_{19}$.
Where: `pencil/RESULT.md` items 6 and loose end 1, `pencil/overlattice/OVERLATTICE.md`, `PAPER.md` Theorem 7.1 item 6.

## 10. The overlattice search bound did not reach degree-2 classes

The first overlattice run reported 0 classes of degree 2 and square $-2$ in $N_{19}$, which seemed to contradict the 48 conics of Theorem 7.1, item 8. The cause was the search bound: such classes lie outside it. The report now says that degree-2 counts were not measured; the exclusion of all 14 overlattices does not depend on them.
Where: `pencil/overlattice/OVERLATTICE.md` (Control, Loose ends).

## 11. "Ovals on bubbles" carried two different status labels

Our working notes called the placement of the conic ovals on the three spheres of the zero-line faces CERTIFIED, while the viewer notes called it "not proved". Both were imprecise. The separation of the three spheres is EXACT (msolve shows that two rational levels of a quadratic form miss the real surface); the placement of the ovals is NUMERICAL (a float evaluation with a margin, not interval arithmetic). Every document now says "EXACT separation, NUMERICAL placement".
Where: `PAPER.md` section 6 and Figure 6, `viewer/index.html`, `viewer/BUILD-NOTES.md`.

## 12. The letter C named two different orbits

The 16 lines that exist only at Y56 were called orbit "C" in the viewer and the paper draft, while "C" also names an orbit of four line-free planes. The 16-line orbit is now called S (for special) everywhere, and the other two 16-line orbits are A (the orbit of L01) and B (the orbit of L03); the paper's Appendix A tags every line, computed from the 32 line permutations.
Where: `PAPER.md` Theorem 5.1 item 3 and Appendix A, `viewer/index.html`, `viewer/BUILD-NOTES.md`, `viewer/build/verify_viewer.py`.

## 13. The line shape in the full proof of $2s^4 = 81$ had the wrong sign

The proof of Theorem 7.1, item 7, substituted the shape $z_2 = \beta(z_3 - z_0)$ into $G_s$ and claimed that three coefficients vanish. With that sign the vanishing coefficients do not generate the ideal of the three equations, and the stated real solution leaves coefficients up to 8. The three equations, the result $2s^4 = 81$ and the Lean theorems are unchanged: the shape that produces them is $z_2 = \beta(z_0 - z_3)$, for which the $z_3^4$ coefficient vanishes identically and the other four generate the same ideal as the three equations. Found by the final referee before release; the substitution is now a shipped machine check.
Fix: `PAPER.md` section 7.3 item 7, `pencil/REPORT.md`. Where: `checks/atlas-referee/ref_shape.py`, `ref_shape.out`.

## 14. "Aut(line graph) = Aut(Y56) semidirect-product <tau>" was not correct as written

The text wrote the group of the 64 line-graph symmetries as a semidirect product of the 32 projective ones with the group generated by $\tau$. But $\tau$ has order 4 on the lines, so $\langle\tau\rangle$ meets $\mathrm{Aut}(Y56)$ in $\tau^2$. The correct statement: the 64 symmetries are $\mathrm{Aut}(Y56)$ together with the coset $\tau\mathrm{Aut}(Y56)$, with $\mathrm{Aut}(Y56)$ of index 2; the extension splits, because the coset holds 16 involutions. The numbers (64, 32, element orders) were right. Found by the final referee before release.
Fix: `PAPER.md` section 5, item 5. Where: `checks/atlas-referee/ref_tau.out`.

## 15. A finite-index step cited items that did not give it

The argument that the Néron–Severi lattice of the very general member equals $N_{19}$ cited "items 3 and 5" for finite index. Finite index needs rank exactly 19, which comes from the earlier (Bouyer-type) argument, while item 3 alone gives only rank at least 19. The text also said item 6 "supersedes" that argument and the loose end called the two routes "independent"; both routes in fact use rank exactly 19. The conclusion is unchanged. Found by the final referee before release.
Fix: `PAPER.md` section 7.3 item 6 and the earlier argument, `RESULTS.md` P6, `pencil/RESULT.md` loose end 1.

## 16. "The Fermat quartic" and "the same 32 symmetries" were too strong

The member $s = 0$ is the Fermat quartic only over the complex numbers (its real points differ: 8 real lines against an empty real Fermat quartic), so the text now says "in disguise" or "projectively equivalent over C". "The same 32 symmetries for every setting" is now "the same 32 symmetries act on every setting", since the Fermat member has more (1536). Found by the final referee before release.
Fix: `README.md`, `PAPER.md`, `CITATION.cff`.

## 17. Wording precision: one setting, one wall, 8 nodes, novelty, Lean claims, a plane name

Smaller fixes from the same round, none changing a number: (a) "exactly one setting" and "the only wall" hold on the real dial; over the complex numbers there are four roots of $2s^4 = 81$ (all giving Y56) and the wall is $s^4 = 16$; (b) the wall members have exactly 8 ordinary nodes at $s = \pm 2$, while the count at $s = \pm 2i$ was not computed exactly; (c) the Galois-twist explanation is "not found after a quick search", and the general conic mechanism is credited to Bouyer; (d) the Fermat lattice numbers are in `pencil/a4_checks.log` part (d), not "quoted from the discovery report"; (e) the Lean scorecard says what is proved (Gram matrix data; rank and discriminant also need the cited $\rho \le 20$ and $L^2 = -2$), and that the substitution before the algebra is not in Lean; (f) the two L2 printouts and the statement match were compared by a referee's script and by reading; (g) a viewer message named the plane "y1 = 0 or y2 = 0" instead of "z1 = 0 or z2 = 0". Found by the final referee before release.
Where: `PATCHES.md`, section "Final referee fixes".
