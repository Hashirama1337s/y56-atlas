# Evidence for the family facts (the faces, the wall, the Fermat end)

Moki & Julio (AI-assisted) · 2026

This folder holds the scripts and transcripts behind the facts the paper uses from the six real faces and the pencil, other than the pencil theorem itself (that is in `../pencil/`). Everything here was run in the working folder; for release the absolute paths were replaced by relative ones (listed in `../PATCHES.md`). The scripts have not been re-run from this layout. They read helper modules and intermediate pickles from `../core/code/sisters/`, which the core scripts write when run from that folder (`s1_group.py`, `s2_lattice.py`, `s3_conics.py`, `s4_mesh.py`); the intermediate pickles of this folder are not shipped and are rewritten by the scripts that make them. Singular and msolve runs use `$SINGULAR` and `$MSOLVE` (default: the program on the PATH).

Status labels as in the paper: EXACT, NUMERICAL, ARGUED, CITED. Singular, msolve, GAP, sympy and igraph are trusted software, not proof assistants.

## faces/ (the six real faces, the three-parameter family, the Fermat route)

| fact in the paper | status | files |
|---|---|---|
| The line graph has 64 automorphisms by a second algorithm (igraph/bliss), the same 64 as a set as networkx; exactly 32 are realised projectively (Section 5, item 4) | EXACT | `a_aut.py`, `a_aut.log`; `a_galois.py`, `a_galois.log` (the Galois-twist coset, also in `../core/code/exact/galois_twist.py`); `a_mk.py`, `a_aut.g`, `a_aut_gap.log` (a GAP attempt that ran out of workspace; kept as a record, not used) |
| Ovals on bubbles: exact separation of the three spheres of $g_{12}$ and $g_{13}$ by two rational levels of an integer quadratic form, then oval placement $0/22/0$ and $4/12/4$ (Section 6) | EXACT separation, NUMERICAL placement | `b_gen.py` (real equations of each face, writes the msolve inputs), `b_g*.ms` and `b_g*.out` (msolve inputs and outputs), `b_run.sh` and its logs, `b_sep.py`, `b_sep.log` (the levels), `b_chk.py`, `b_chk.log`, `b_assign.py`, `b_assign.log` (placement, margins 5.76 and 4.19) |
| Morse counts of a quadratic height on all six faces, and the lattice-free proof of "three spheres" for $g_{12}$ (Section 6) | EXACT counts, NUMERICAL indices | `b_anal.py`, `b_anal.log`, `b_anal2.log` |
| Singular members of $a\operatorname{Im}(w^4) + \operatorname{Im}(p^2)(b\lvert w\rvert^2 + c\lvert p\rvert^2)$ are exactly $c^3(b^2 - 4ac)(b^2 + 4ac) = 0$ (Section 7.3, item 1) | EXACT | `c_fam.sing`, `c_fam.log`, `c_fam.sh` |
| The wall member has exactly 8 singular points (first, float-coordinate pass; superseded by the exact `../wall/w1`) | EXACT count, NUMERICAL coordinates | `c_node.sing`, `c_node.log`, `c_node.sh` |
| Real wall nodes per face, mesh Euler numbers on both sides of the wall, vanishing bubbles in $g_{12}$ (Section 7.6) | NUMERICAL (exact node counts in `../wall/f2_fermat`) | `c_family.py`, `c_family_nodes.log`, `c_family_mesh140.log`, `c_nodes_sister.py`, `c_nodes_sister.log` |
| Fermat route for $g_{02} \sim g_{24}$: twisted-conjugacy classes on the Fermat member (float pass), determinant signs of the 32 connecting maps, real lines on the Fermat member (Section 7.6) | NUMERICAL steps of an ARGUED route | `c_fermat.py`, `c_fermat.log`, `c_fermat_det.py`, `c_fermat_det.log`, `c_fermat_lines.py`, `c_fermat_lines.log` |
| Helper | | `s5_portraits.py` (real curves of each face; also renders the face portraits of `../core/media/`), imported by `b_anal.py`, `b_sep.py` and `b_assign.py` |

Run order in the working folder: `a_aut.py`, `a_galois.py`; `b_gen.py g12 g13` and `b_gen.py g01 g02 g24 g00`, `b_run.sh <faces>`, `b_sep.py g12 g13`, `b_run.sh g12_sep0 g12_sep1 g13_sep0 g13_sep1`, `b_chk.py`, `b_anal.py <faces>`, `b_assign.py`; `c_fam.sh`, `c_node.sh`, `c_family.py`, `c_nodes_sister.py`, `c_fermat.py`, `c_fermat_det.py`, `c_fermat_lines.py`.

## wall/ (the 8-nodal wall, the exact Fermat bridge, the deformation families)

| fact in the paper | status | files |
|---|---|---|
| The wall $W = G_2$ has exactly 8 ordinary nodes ($A_1$), in 2 rational orbits of 4; only 2 quadrics pass through them (Section 7.4) | EXACT (Singular over $\mathbb{Q}$) | `w1.sing`, `w1.log`, `run_w1.sh` |
| The wall carries 24 lines with Fano scheme of length 40 (stratified charts 39/23 and 1/1); positive control on the Fermat member: 48 lines, length 48 (Section 7.4) | EXACT | `w3.sing`, `w3.log`; control `w3c.sing`, `w3c.log` |
| (a) Explicit projective equivalence of $G_0$ with the Fermat quartic over $\mathbb{Q}(\zeta_8)(r)$, $r^2 = 1 - i$ (Section 7.5); (b) the six real structures merge into two classes on the Fermat member, by an exhaustive exact test over its 1536 automorphisms; (c) exact node coordinates in $\mathbb{Q}(t)$, $t = 2\cos(\pi/8)$, and real wall nodes per face $8/2/0/2/4/0$ (Sections 7.4, 7.6) | EXACT (our own field arithmetic; assumes the standard order-1536 description of the Fermat automorphisms) | `f2_fermat.py`, `f2_fermat.log` |
| Lattice invariants of $(H^2, \sigma^*, h)$ for the five non-standard faces agree within $\{g_{01}, g_{02}, g_{24}\}$ and within $\{g_{12}, g_{13}\}$: no lattice obstruction to the CITED deformation classes (Section 6) | EXACT | `l3_lattice.py`, `l3_lattice.log` |

The two-conic factorisations of the wall in the planes $z_1 = \pm z_2$ are hand identities (one line each), consistent with the Singular decomposition in `w1.log`; they are written out in the paper, Section 7.4.

Written with AI assistance.
