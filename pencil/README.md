# pencil: the family through Y56 and the Fermat quartic

Moki & Julio (AI-assisted) · 2026

`RESULT.md` is the refereed statement of the pencil theorem (Theorem 7.1 of `../PAPER.md`); `REPORT.md` is the discovery report it supersedes where they differ. Everything here is EXACT unless a file says otherwise; Singular, sympy, python-flint and GAP are trusted software, not proof assistants. Python scripts run from this folder and read `../core/data/`; Singular inputs run with `bash run.sh <name> ...` (set `SINGULAR` to the Singular binary).

| file | what it computes | paper |
|---|---|---|
| `graph_gen.sing` → `graph_gen.log` | the four components $C_1$ to $C_4$ of the graph-chart Fano ideal over $\mathbb{Q}(s)$, with their closed forms | Thm 7.1 item 4 |
| `graph_generic.sing`, `graph_s*.sing`, `graph_sm3.sing`, `graph_wall_i.sing`, `graph_y56.sing` → `.log` (template `graph_tpl.sing`, list `glist.txt`) | the graph chart over $\mathbb{Q}(s)$ (length 32, 32 distinct lines) and spot checks at $s = 0, 1/3, 1, 9/4, 2, 5/2, 13/5, 3, 7, -3$, at $s = 2i$ and at Y56 (length 48, 48 distinct lines) | item 4 |
| `special.sing` → `special.log` | saturating by $C_1, \dots, C_4$ leaves length 64 with eliminant $2s^4 - 81$: the only extra graph lines are at Y56 | item 4 (jump set) |
| `meet.sing` → `meet.log` | lines meeting $z_0 = z_3 = 0$ for all $s$ at once: 8 for every $s$, 8 more only at $s = 0$ | item 4 |
| `fano_s0.sing`, `fano_s5o2.sing`, `fano_s13o5.sing` → `.log` | stratified-chart line counts in random coordinates: 48 at $s = 0$, 40 at $s = 5/2$ and $13/5$, all reduced | item 4 |
| `a1_firstorder.py` → `.log`, `.json` | which Y56 lines deform to first order along the pencil: exactly 40; the 16 others are obstructed (rank 4 against 5) | item 7 |
| `a2_lattice.py` → `.log`, `.json` | the lattice of the 40 persistent lines ($N_{19}$: rank 19, det 128, Smith $[2,8,8]$, signature $(1,18)$, primitive) and the complement class $v$, $v^2 = -32$ | items 5, 7 |
| `a3_special.py` → `.log` | the 16 special lines: their shapes, the plus and minus eights, incidences, the 48 meeting pairs and their planes | items 7, 8 |
| `a4_checks.py` → `.log` | the closed-form components lie on $G_s$ identically; Sturm counts of real lines at 15 values of $s$; the conic-determinant norm $2^{24}(2s^4 - 81)^2$; 40-digit Gram matrices at $s = 1, 5/2, 13/5, 3, 7i/3$ | items 5, 8, 9 |
| `a5_fermat.py` → `.log` | the Fermat-type member: the class orthogonal to the 40-line lattice pairs to $\pm1$ with the 8 extra lines and has square $-2$ (numerical incidence, exact algebra). The determinant $-64$ and Smith form $[8,8]$ of its 48-line lattice, quoted in `REPORT.md`, have no shipped transcript | Table 7.2 |
| `overlattice/` (`ov.py`, `ov2.py`, `ov2.log`, `N19.json`, `overlattice_results.json`, `OVERLATTICE.md`) | all 14 proper even overlattices of $N_{19}$ are excluded, each with explicit roots orthogonal to $h$ and extra degree-1 classes; with primitivity this gives $\mathrm{NS} = N_{19}$ for the very general member | item 6 |
| `sd16/` (`mk.py`, `sd16.g`, `sd16b.g`, `run.sh`, `sd16.out`) | GAP on the 16 symplectic maps as permutations of the 56 lines: size 16, IdGroup $[16,8]$, QD16 (= SD16). `mk.py` writes `sd16.g`; `sd16b.g` is the same group with the output written on one line, and is the file `run.sh` ran | Thm 5.1 item 6, Thm 7.1 item 2 |

`run.sh` and the scripts were run in the working folder; for release only their paths were made relative (`../PATCHES.md`).

Written with AI assistance.
