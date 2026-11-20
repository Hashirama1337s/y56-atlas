# Independent re-derivations by hostile referees

Moki & Julio (AI-assisted) · 2026

Before each result was fixed, a referee who had not written the original code re-derived its headline numbers with code of their own: own $\mathbb{Q}(\sqrt2)$ arithmetic, own parsers, own Singular inputs. Nothing here imports the release's own scripts; the referees read only the exact data files in `../core/data/`. Run the Python scripts from the folder they are in; the Singular inputs run with `bash run.sh <name> ...` (set `SINGULAR` to the Singular binary).

## core-referee/ (the core release, now `../core/`)

`REFEREE.md` is the referee's report: verdict per claim R1 to R19 and the fixes F1 to F11, all applied before release (see `../core/PATCHES.md`, section "Referee round 1").

| file | what it re-derives |
|---|---|
| `ref_checks_core.py` | (a) the 56 lines lie on $F$ and are distinct; (b) the 448 meeting pairs, 16-regular, equal to `edges.json`; (c) the 32 symmetries $F(Mz) = cF(z)$, their action on the lines, the group closure, the element orders and the line orbits $8 + 16 + 16 + 16$. The other scripts of this folder load it |
| `ref_checks.py` | the same as `ref_checks_core.py` plus (d): rank 20 and invariant factors $1^{18}, 2, 32$ of the line lattice. Its last step, a floating eigenvalue routine for the signature, runs out of precision and stops the script after (d) has printed; the referee computed the signature exactly in `ref_conics.py` instead. Re-run from this layout: (a) to (d) reproduced, then the same stop |
| `verify_run.txt` | the referee's own run of `../core/code/verify_all.py`: 21 of 21 |
| `ref_conics.py` → `ref_conics.out` | the line lattice $N$: a $\mathbb{Z}$-basis among the 57 generators, signature $(1,19)$, $\det = -64$; enumeration of conic classes ($c \cdot h = 2$, $c^2 = -2$): 636 = 448 + 188, and 20 pairs $\{c, h-c\}$ |
| `ref_extra.py`, `ref_extra2.py` → `ref_extra.out` | (i) the 64 line-graph automorphisms by an own backtracking search (a second algorithm, not networkx), with the 32 projective ones among them; (ii) the involution classes and their real lines; (iii) Euler numbers $2 - \operatorname{tr}(g \mid N)$ of the six faces: $-18, -2, -2, -2, 6, 6$; (iv) nondegeneracy of the 148 conics. `ref_extra2.py` is the final version of `ref_extra.py` (pruned search); both write `ref_extra.out`, and the shipped file is from the last run |
| `ref_orbit8.py` → `ref_orbit8.out` | the 8-orbit is $\{L02, L14, L22, L24, L27, L30, L43, L53\}$, contains DIS's lines $m_1 = L24$ and $m_2 = L30$, and is exactly the four skew pairs meeting ten common lines (DIS, proof of Proposition 9.9) |

## pencil-referee/ (the pencil theorem, `../pencil/RESULT.md`)

| file | what it re-derives |
|---|---|
| `r1_*.sing`, `r1b_*.sing` → `.log` (template `r1_tpl.sing`, `r1b_tpl.sing`) | at fixed members ($s = 0$, $2$, $11/7$, the non-real member $s = 1 + i$, and Y56): smoothness, and the number of lines in random rational coordinates, graph chart plus emptiness of the complementary stratum (items 1 and 4) |
| `r2_jump.sing` → `r2_jump.log` | the jump set over all complex $s$, own derivation by minimal primes (item 4) |
| `r2_meet.sing` → `r2_meet.log` | the lines meeting $\{z_0 = z_3 = 0\}$ for all $s$ at once, through the pencil of planes containing that line (item 4) |
| `r3_disc.sing` → `r3_disc.log` | which members are singular: elimination from the saturated Jacobian ideal, giving $(s-2)(s+2)(s^2+4)$ (item 1) |
| `ref_sympl.py` | which of the 32 block maps act symplectically on every member; the 16 symplectic ones and their group (item 2) |
| `ref_y56.py`, `ref_y56b.py` (writes `ref_pm.json`) | from the exact Y56 data: incidence, signature, $h$, the complement class $v$ with $v^2 = -32$, the index of $N_{19} + \mathbb{Z}v$, primitivity of $N_{19}$, and that the 16 lines with $v \cdot L = \pm 4$ form one orbit (items 5 and 7) |
| `ref_family.py` → `ref_family.log` | the family lines at $s_* = 3 \cdot 2^{-1/4}$ matched with the indices of `lines_exact.txt`; the conic-determinant norm; real line counts along real $s$ (items 7 to 9) |
| `ref_conic.py` (reads `ref_pm.json`) | for each meeting pair $(L^+, L^-)$ of special lines, that $L^+ + L^-$ lies in the span of the 40 persistent lines and is not a sum of two of them (item 8) |

`ref_sympl.py`, `ref_y56.py`, `ref_y56b.py` and `ref_conic.py` printed to the console; their transcripts were not kept, only the referee's verdicts (folded into `../pencil/RESULT.md`). Re-running them takes seconds.

## atlas-referee/ (the final release round: `../PAPER.md`, `../README.md`, `../lean/`)

`REFEREE-ATLAS.md` is the final referee's report: a verdict per claim, five blocking fixes (B1 to B5) and eight non-blocking ones (N1 to N5, L1 to L3), all applied before release (see `../PATCHES.md`, section "Final referee fixes", and `../CORRECTIONS.md`, items 13 to 17). The report says "Archive not edited": it describes the archive as it was before those fixes. The scripts read the archive from this layout (`../../lean/`, `../../core/data/`); run them from this folder.

| file | what it checks |
|---|---|
| `ref_shape.py` → `ref_shape.out` | the machine check of the substitution in Theorem 7.1, item 7: with $z_2 = \beta(z_3 - z_0)$ the vanishing coefficients do not generate the ideal of the three equations (and the paper's solution leaves coefficients up to 8); with $z_2 = \beta(z_0 - z_3)$ they do, and the paper's solution gives all coefficients 0. The shipped output is from a run of this layout under the memory cap |
| `ref_tau.py` → `ref_tau.out` | $\tau$ (Galois twist composed with $p \mapsto ip$) acts on the 56 lines with $\tau^2 \neq 1$ and $\tau^4 = 1$ |
| `ref_lean_data.py` → `ref_lean_data.out` | the data printed inside the Lean files (lines, symmetries, edges, planes) equal the release data files; links the two printouts of L2 |
| `ref_l5normals.py` → `ref_l5normals.out` | the 218 plane normals of L5 and their line lists equal those of L6 |
| `ref_wall2i.py` → `ref_wall2i.out` | NUMERICAL: the singular points of $X_s$ at $s = 2i$ (8 found), with controls $s = 2$ (8) and $s = 3$ (0) |
| `verify_all_rerun.txt` | the referee's own run of `../../core/code/verify_all.py`: 21 of 21 |

Written with AI assistance.
