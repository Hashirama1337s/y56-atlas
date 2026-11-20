# Referee report: Y56 v1.0 core release (core/)

Hostile referee report on the v1.0 core release (now core/), 2026-11-20, saved by the editors. All fixes F1 to F11 were applied before release (core/PATCHES.md, section "Referee round 1").

**Editors' spot-check:** F1 is confirmed against data/logs/s1_group.log. The class sizes are g00 1 (56 lines), g01 4 (4), g02 4 (12), g12 4 (0), g13 2 (0), g24 1 (8). That is 16 real structures in total.

## In plain words

The mathematics holds. Every headline number was re-derived with independent code:
- the 56 lines and 448 crossings;
- the 32 symmetries and the orbits 8+16+16+16;
- the lattice: rank 20, invariant factors 1^18, 2, 32;
- the conic counts 636, 448, 188 and 20;
- the 64 graph automorphisms, found by a second algorithm;
- the six real faces, as Euler numbers -18, -2, -2, -2, 6, 6.

verify_all.py passes 21 of 21 in 147 s, and the manifest checks 75 of 75 OK.

The text needs fixing:
- R15's class sizes are mismatched with the faces.
- R9 says no l2 transcript is shipped, but one is.
- The README says "six of them" where there are 16 real structures.
- Two published facts are not credited: DIS Corollary 1.3 (56 is the maximum number of real lines, and Y56 is the unique surface reaching it, up to real projective change of coordinates) and Veniani's count of 64 graph automorphisms.
- The orbit-split verdict should be PARTIAL, not OPEN.

## Sources (opened by the referee)

- **DIS 1601.04238:**
  - Corollary 1.3: 56 is the maximal number of real lines on a nonsingular real quartic.
  - Section 9.2.
  - Proposition 9.9: order 32. The proof singles out four skew pairs meeting ten common lines, which is our 8-orbit [2,14,22,24,27,30,43,53] and contains m1 = L24 and m2 = L30.
  - Remark 9.10: six real structures up to automorphism.
  - Proposition 9.12: genus 10.
- **Veniani 1708.01219:** the Table 1 row Y56 | 64 | 32 | 16 | 64 | [2,0,32], and section 3.3, where O_h is the set of permutations preserving intersections.
- **Degtyarev 2407.00493:** section 1.2 gives 188 + 448 = 636 real conics. It also says Y56 "has never been analyzed". Remark 7.4.

## Verdicts

| Claim | Verdict |
|---|---|
| R1 | CORRECT (transcript) |
| R2 | CORRECT (re-derived) |
| R3 | CORRECT WITH FIXES (F7) |
| R4 | CORRECT (re-derived) |
| R5 | CORRECT WITH FIXES (F8) |
| R6, R7, R8 | CORRECT |
| R9 | CORRECT WITH FIXES (F2). The logic is sound: an index-k sublattice has disc k^2 · 64, which forces k = 1. |
| R10 | CORRECT as NUMERICAL |
| R11 | CORRECT (re-derived) |
| R12 | CORRECT WITH FIXES (F5) |
| R13 | CORRECT as trusted GAP output |
| R14 | CORRECT |
| R15 | WRONG as worded (F1) |
| R16 | NOT CHECKED |
| R17 | Euler numbers CORRECT; topology CITED |
| R18 | NOT CHECKED (CITED) |
| README | CORRECT WITH FIXES (F3, F4, F9, F10) |
| PRIOR-ART | CORRECT WITH FIXES (F4, F5, F6) |
| CORRECTIONS item 6 | CORRECT WITH FIXES (F4) |
| CAPTIONS | CORRECT WITH FIXES (F4) |
| Faceless rules | CORRECT. Optional: strip the "memcap: exit" lines from the logs. |

## Fixes

**F1 (blocking): R15.**
Replace: "up to conjugacy there are six, in classes of sizes 1, 4, 4, 4, 2, 1. They have 56, 12, 8, 4, 0, 0 real lines."
With: "up to conjugacy there are six (16 real structures in all), in classes of sizes 1, 4, 1, 4, 4, 2 with 56, 12, 8, 4, 0, 0 real lines respectively."
Also check docs/SISTERS.md line 34.

**F2 (blocking): R9.**
Replace: "verify_all.py does not re-run it, and no transcript of l2.py is shipped."
With: "verify_all.py does not re-run it; transcripts of l2.py and l3.py are data/logs/l2.log and data/logs/l3.log."

**F3 (blocking): README.**
Replace: "The same equation has six of them."
With: "The same equation has 16 of them, which fall into six kinds up to its symmetries."

**F4 (blocking): credit DIS Corollary 1.3.**
- README "In plain words": after "Y56 is one particular smooth surface of this kind.", insert "Degtyarev, Itenberg and Sertoz proved that 56 is the largest number of real lines a smooth real quartic can hold, and that Y56 is the only one (up to real projective change of coordinates) that reaches it; over the complex numbers the maximum is 64."
- README "What is ours": in the published facts, add "the theorem that 56 is the maximum number of real lines and Y56 the unique maximiser (Corollary 1.3)".
- PRIOR-ART: add the row "56 is the maximal number of real lines; Y56 unique | TAKEN | DIS Corollary 1.3".
- CORRECTIONS item 6: replace "so that wording overreached. The released captions say 56 real lines and make no maximality claim." with "so the wording was ambiguous: it is false for complex lines but true for real lines (DIS, Corollary 1.3). The released text states the real-line maximum with that credit."
- CAPTIONS: make the first sentence of each caption "Y56 is the smooth real quartic surface with the most real straight lines possible, 56 (Degtyarev-Itenberg-Sertoz)."

**F5: R12 and PRIOR-ART, Veniani's 64.**
- R12 Status: append "The count 64 is also published: Veniani, arXiv 1708.01219, Table 1, column |O_h(S)| (permutations of the lines preserving intersections, section 3.3)."
- PRIOR-ART, the symmetry row: add "; 64 intersection-preserving line permutations, |O_h| = 64 (same row)".
- README table, the 64-automorphisms row: set the status to "EXACT (count also CITED: Veniani Table 1)".

**F6: orbit split, OPEN to PARTIAL (in PRIOR-ART and README).**
New text: "PARTIAL: DIS (proof of Proposition 9.9) single out 8 lines, the four skew pairs meeting ten common lines, which form our 8-orbit; the split of the remaining 48 into 16 + 16 + 16 we found nowhere."

**F7: R3.**
- Replace "Status: EXACT, by two programs." with "Status: EXACT (Singular Groebner basis over Q(sqrt2), trusted software); cross-check by msolve in its default Monte Carlo (probabilistic) mode."
- Replace "the other five charts are empty" with "no line lies outside that chart (std(I + p01) = 1 in the other five charts)".
- Credit: "(DIS, section 9.2 with Theorem 1.1; Corollary 1.3)".
- README table row: replace "EXACT (substitution in F; Singular and msolve counts)" with "EXACT (substitution; Singular); msolve cross-check probabilistic; count also CITED (DIS)".

**F8: R5 nondegeneracy.** Check 4d does not test nondegeneracy; the referee found all 148 conics nondegenerate. Do one of these:
- add det(gram) != 0 to check 4d; or
- reword R5 to "irreducible over Q(sqrt2) (check 4d); nondegenerate by the line count R3 (an irreducible degenerate conic would be two further lines)".

**F9: re-check steps.**
- In step 3, use `gap -q grp.g < /dev/null`.
- Change "in about 90 seconds" to "in about 1.5 to 2.5 minutes".

**F10: README wording.**
- Replace "the 636 plane conics (curved slices)" with "all 636 conics (448 of them pairs of crossing lines, 188 genuine curves)".
- Replace "All 188 are real." with "All 188 have real points (Degtyarev counted all 636 conics as real; the real points are our exact check)."

**F11 (minor): data/planes_exact.txt.** The last section header, "(from the 20 numeric plane-pairs)", refers to the discredited numeric list. Note this in PATCHES.md, or drop the stale line.

## Overall verdict

READY WITH FIXES. F1 to F4 block release. All fixes are text-only.

Referee scripts and outputs are in this folder: ref_checks.py, ref_conics.py/.out, ref_extra2.py, ref_orbit8.py/.out, verify_run.txt.

Written with AI assistance.
