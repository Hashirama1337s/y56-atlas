# Prior art and credits

Moki & Julio (AI-assisted) · version 1.0

## Fairness line

The surface Y56, its 56 real lines, the theorem that 56 is the most real lines a smooth real quartic can hold with Y56 the unique maximiser, its symmetry group of order 32, its six real structures and its genus-10 standard real part are the published work of Degtyarev, Itenberg and Sertöz (DIS, arXiv 1601.04238). The counts 636 conics and 20 line-free conic-pair planes are Degtyarev's (arXiv 2407.00493). The equation of the pencil is DIS's equation (9.4) with one coefficient freed. Nothing in this release changes any of that. We computed and proved what those papers and their relatives do not write out, and we credit every count to its authors.

## How we searched

Three searches, each with its own date.

| search | date | what it covered | newest literature seen |
|---|---|---|---|
| Core, pass 1 | 2026-11-19 | the surface, pictures, conics, coordinates, symmetry | arXiv and OpenAlex through September 2026 (newest citer of DIS: arXiv 2609.26862) |
| Core, pass 2 (follow-up) | 2026-11-19 | the same, plus figures in the counting papers, Karl's thesis, galleries | Semantic Scholar, OpenCitations and the arXiv API through 2026-11-19 |
| Pencil | 2026-11-20 | the pencil, its 40-line configuration, the jump set, the Noether–Lefschetz description, the real-line walk, the 8-nodal wall | arXiv API listing to 2026-11-19 (2611.26001); Semantic Scholar citers of DIS to 2026-09-22; Zenodo queried 2026-11-20 |

**Databases and sites.** The arXiv API, OpenAlex, Semantic Scholar, OpenCitations, Zenodo, GitHub, general web search, and the Imaginary.org galleries (two galleries opened). INSPIRE was tried for the pencil and found not to index this literature (a control query on quartic lines returned nothing), so it is not part of the floor.

**Search floor.** Every database in which a query returned zero hits also had a positive control query that is known to hit (for example the DIS and Degtyarev identifiers on the arXiv API, the title "Line arrangements on smooth quartics" on Zenodo, "surfex" on GitHub). A zero is therefore a real zero for that query, not a dead service. OpenAlex ran out of its daily budget on the later passes, so the later citer lists come from Semantic Scholar and OpenCitations; all 36 OpenAlex citers of DIS from the first pass are contained in the 41 Semantic Scholar citers. Web-search results were read at snippet level only. Every arXiv identifier below was checked against its title and authors.

**Aliases searched.** "Y56", "Y_56", "56 real lines", "real quartic with maximal number of real lines", Segre and Schur quartic (64 lines), planes cutting two conics, real split hyperplane sections ("h-fragments"), Heisenberg-invariant Kummer quartics, Fermat quartic 48 lines, X56 (the complex relative of Shimada and Shioda); for the pencil also "pencil / one-parameter family of quartics", "equilinear family", "Picard number 19 family", "lattice-polarized quartic", "Noether–Lefschetz" with lines, "symplectic SD16 / semidihedral / quasidihedral", "Fermat quartic deformation", "conics degenerate into lines", "40 lines", "8-nodal quartic".

## Verdicts: the core

Labels: TAKEN (already published), PARTIAL (published in part), OPEN (we found no earlier statement or picture in the sources we opened).

| object | verdict | where it is (locator) |
|---|---|---|
| The surface, its equation, and that it holds 56 real lines | TAKEN | DIS, section 9.2, equation (9.4), with Theorem 1.1 |
| 56 is the maximal number of real lines on a smooth real quartic; Y56 is unique up to real projective equivalence | TAKEN | DIS, Corollary 1.3 |
| Symmetry group of order 32, all automorphisms real | TAKEN | DIS, Proposition 9.9 and Remark 9.10; independently Veniani, arXiv 1708.01219, Table 1 (row Y56: 64, 32, 16, T = [2,0,32]) |
| 64 intersection-preserving permutations of the lines | TAKEN | Veniani, Table 1, column of permutations preserving intersections (section 3.3); also DIS, Table 2 |
| Six real structures; the standard real part is connected of genus 10 | TAKEN | DIS, Remark 9.10 and Proposition 9.12 |
| 636 = 188 + 448 conics and 20 line-free planes, as numbers | TAKEN | Degtyarev, arXiv 2407.00493, section 1.2 and Remark 7.4 (counts only; the same paper notes that Y56 had not been analysed before) |
| 50 real hyperplane sections | TAKEN | Degtyarev, arXiv 2512.06833, section 3.1; arXiv 2509.24349, Remark 3.2 |
| Incidence types (4,4) x 32 and (3,7) x 24 | TAKEN | DIS, Lemma 6.14 (counts by valency, not group orbits) |
| Transcendental lattice T(Y56) = [2,0,32], so det T = 64 | TAKEN | Veniani, Table 1; DIS, Table 2; Degtyarev, arXiv 1608.06746, Table 1 |
| Exact coordinates of all 56 lines over Q(sqrt2) | PARTIAL | DIS, section 9.2, Tables 3 to 5, write out 24 of the 56 (2 + 10 + 12); the other 32 are described as residual generatrices of 16 quadrics, without coordinates. A full list was in nothing we opened |
| Explicit equations of the 188 irreducible conics and the 20 conic-pair planes | no explicit list found | 2407.00493 gives the counts only |
| A picture of Y56, or of any smooth real quartic showing its 56 real lines | OPEN | none found. DIS, Veniani, Degtyarev's papers and the Rams–Schütt papers have no such figure (raster images and vector drawings counted page by page; the only drawings, in 2509.24349 Figure 4, are graph diagrams). Nearest drawing: Maple plots of Heisenberg-invariant Kummer quartics with 16 real skew lines, arXiv math/0112195, a different surface |
| A picture of the 636 conics of Y56 | OPEN | none found |
| Orbit split of the 56 lines, 8 + 16 + 16 + 16 | PARTIAL | DIS, proof of Proposition 9.9, single out 8 lines (four skew pairs meeting ten common lines), which form our 8-orbit; the split of the other 48 we found nowhere |
| Table of real lines, real conics and topology for the five non-standard real faces | PARTIAL | the number of faces and the standard face are published; DIS give real-line data for Schur's quartic only (Proposition 9.3); 2512.06833 treats Y56 in its standard real form only; arXiv 2608.05941 (real structures in equisingular strata) does not treat Y56 |
| The factor 2 between the 64 graph symmetries and the 32 projective ones, explained by the Galois twist sqrt2 -> -sqrt2 composed with p -> ip | PARTIAL (both numbers published; the explanation not found after a quick search) | DIS Table 2 and Proposition 9.9; Veniani Table 1; DIS Remark 9.11 notes that some lines are defined only over Q(sqrt2). Quick search only |
| The group name SmallGroup(32,43), the plane orbit sizes, the eight-fold form of the equation, the Lean formalisation | not searched | worded as "identified", "checked" or "done", never as new results |

## Verdicts: the pencil

| object | verdict | where it is (locator) |
|---|---|---|
| The pencil G_s through Y56 (s^4 = 81/2), the Fermat-type member (s = 0) and an 8-nodal member (s^4 = 16) | OPEN as a family; the Y56 member's equation TAKEN | DIS, section 9.2, equation (9.4): one fixed coefficient 3, no family. Normalisation checked: rescaling z1, z2 by 2^(-1/8) gives s = 3 * 2^(-1/4) |
| Genre: a one-parameter rank-19 family whose special members are record quartics | TAKEN as a genre (different configuration) | Veniani, arXiv 1708.01219, section 6.7 (the Z52 family, with X64 and X60' as special members) |
| Genre and method: one-parameter families through the Fermat quartic, rank 19 from two non-isomorphic special members | TAKEN as a genre and a method (24 or 32 lines, not 40) | Bouyer, arXiv 1511.01781, section 3 (family list) and section 4.3 (the argument we use for P6) |
| Genre: pencils of symmetric K3 surfaces, rank 19 generic with rank-20 special members | TAKEN as a genre (quotient K3s, not lines on quartics) | Barth and Sarti, arXiv math/0301329 (abstract level only) |
| The generic member has exactly 40 lines; the 40-line configuration has rank 19 and det 128 | OPEN for this configuration; existence of some quartic with 40 lines, and of some real one with 40 real lines, TAKEN abstractly | DIS, Addendum 1.4 and Lemma 6.22; Degtyarev and Rams, arXiv 2301.04127, classify configurations of more than 48 lines only |
| Lines jump only at s = 0 (48) and s^4 = 81/2 (56) | OPEN | no source treats line jumps along a family through Y56; the one-parameter families of 2301.04127 all have at least 49 lines; DIS Theorem 3.10 gives only the general correspondence between equilinear families and configurations |
| Upper limit for one-parameter families (context) | TAKEN (context; 40 < 52, no conflict) | Degtyarev, arXiv 1608.06746, section 1 (52 lines is the maximum for an equilinear one-parameter family) |
| Y56 as a Noether–Lefschetz point of the pencil: class v with v^2 = -32, the 16 extra lines one orbit of the group | OPEN | Degtyarev and Rams, Table 1, list Y56's symplectic group (16,8) of index 2 and T = [2,0,32], but no rank-19 sublattice, no class of square -32 and no family degenerating to Y56 |
| Rank at least 19 on every member, from the symplectic SD16 action | PARTIAL: a consequence of known theory | Hashimoto, arXiv 1012.2682, Table 10.1 (SD16: coinvariant rank 18), with the SD16 action verified on every member (P2) |
| The 16 lines arise as degenerations of 48 conics | OPEN for Y56; the general mechanism TAKEN | Bouyer, 1511.01781, abstract (conics that degenerate into lines in his families) |
| Fermat and Y56 as rank-20 members with det T = 64 | TAKEN (their lattices); agrees with our numbers | Degtyarev, 1608.06746, Table 1 (Y56: [2,0,32]; X56 and Fermat: [8,0,8]); Shimada and Shioda, arXiv 1604.06265, equation (3.1) |
| Real line counts along the real pencil, 8 / 24 / 40 / 56 | OPEN as a walk; each count TAKEN as an attainable value | DIS, Addendum 1.4 (the realised real counts include 8, 24, 40 and 56); no source follows real lines along a family |
| The 8-nodal member at s^4 = 16 with 24 lines (16 of them double in the Fano scheme) | OPEN, thin search | three arXiv field queries returned nothing relevant |
| NS of the very general member equals N19 | not searched separately | covered by the configuration searches above |

**Credit line for the pencil.** The pencil frees the coefficient 3 in Degtyarev–Itenberg–Sertöz's equation (9.4).

## Most dangerous neighbours

Degtyarev, with Rams, Itenberg and Sertöz: he owns the equilinear-family machinery and the classification above 48 lines, wrote that Y56 had not been analysed (2407.00493) and has since added Y56 to tables of real hyperplane sections. Extending his classification down to 40 lines, or listing the rank-19 sub-configurations of Y56, would produce our 40-line family as one row. Veniani is second (explicit equations of rank-19 families), and the Leiden line-counting group third.

## Credit

- Degtyarev, Itenberg, Sertöz (arXiv 1601.04238): the surface and its equation (9.4), Theorem 1.1, Corollary 1.3, the group order 32 (Proposition 9.9), the six real structures (Remark 9.10), the genus-10 standard face (Proposition 9.12), the incidence types (Lemma 6.14), the transcendental lattices (Table 2), Theorem 3.10 and Addendum 1.4; and the discussion of Segre's 1943 work (introduction, Corollary 1.2).
- Degtyarev (arXiv 2407.00493): the counts 636 and 20; (arXiv 2512.06833, 2509.24349): the 50 real hyperplane sections; (arXiv 1608.06746): T(Y56) and T(Fermat), and the 52-line bound for families.
- Degtyarev and Rams (arXiv 2301.04127): the symplectic group of Y56 and the classification above 48 lines.
- Veniani (arXiv 1708.01219): Table 1 (T = [2,0,32], which closes the completeness of the conics, and the count 64), section 6.7.
- Hashimoto (arXiv 1012.2682): Table 10.1, the coinvariant rank 18 of SD16.
- Bouyer (arXiv 1511.01781): the two-special-members method for generic rank 19.
- Shimada and Shioda (arXiv 1604.06265): T(Fermat).
- Rams and Schütt (arXiv 1212.3511, 1505.02018, 1512.01358): 64 lines over C; Karl's 2025 Leiden thesis: background.
- Nikulin and Kharlamov, as summarised by Degtyarev and Kharlamov (arXiv math/0004134, section 3.5.4): the classification of real quartics used for the deformation families.
- Tools: Singular, msolve, GAP with the SmallGroups library, PARI/GP, sympy, networkx, igraph, python-flint, three.js, Lean 4 and Mathlib.

## Sources opened

Text read, in full or in part: arXiv 1601.04238, 1708.01219, 2407.00493, 2512.06833, 2509.24349, 2506.22733, 2609.10751, 2607.07898, 2607.10090, 2512.06145, 2602.11742, 1604.06265, math/0112195, 2608.05941, 1608.06746, 2301.04127, 1706.05734, 1604.05836, 1511.01781, 2102.08163, 1012.2682, math/0606100, math/0004134. Scanned for figures: 1212.3511, 1505.02018, 1512.01358, 1502.04510, the Shimada Istanbul slides, and Karl's 2025 Leiden master thesis (115 pages; no mention of Y56, real lines or Degtyarev; its images are a title-page logo and code listings). Read at abstract level only: Barth–Sarti math/0301329, Page–Ryan–Smith (Forum of Mathematics, Sigma, 2026), Rams–Schütt 2504.00778. Zenodo record 14360457 ("Line arrangements on smooth quartics", Magma code) was checked and has no images or real forms. Downloaded papers are not shipped.

## Loose ends

- Journal versions of the Rams–Schütt and Veniani papers (which might carry figures the arXiv versions lack) were not opened.
- An OpenAlex citation re-run is owed (the service was out of budget on the later passes); Semantic Scholar lists no citers of 2407.00493 yet (index lag, not a floor).
- Wolfram Demonstrations and MathWorld pages for line-rich quartics were not opened, and Kharlamov's surveys were not opened for a Y56 table.
- The 8-nodal wall had a thin search (three arXiv queries); the Galois-twist explanation had a quick search only.
- Prior art for the group name, the plane orbit sizes, the eight-fold form and the Lean layer was not searched.
- Curiosity, not a claim: Degtyarev (arXiv 1604.05836) finds supersingular quartics in characteristic 2 with 40 lines; no link to our characteristic-0 family is known.

Written with AI assistance.
