# The Y56 pencil: refereed statement (2026-11-20)

Moki & Julio (AI-assisted) · 2026

This file supersedes the "Proved vs observed" section of REPORT.md (the discovery report, shipped beside it).

Sources:
- The REPORT.md findings were re-derived by a hostile referee with independent code. Its scripts and logs are in ../checks/pencil-referee/.
- Prior-art search: ../PRIOR-ART.md (section "The pencil").
- The editors re-derived the jump eliminant 2s^4 - 81 (sympy). They also checked two cited table rows in the opened sources:
  - Hashimoto 1012.2682, Table 10.1: the SD16 row has coinvariant rank 18.
  - Degtyarev 1608.06746, Table 1: T(Y56) = [2,0,32] and T(X56/Fermat) = [8,0,8].

## Theorem (statement the evidence supports)

Let G_s = Im(w^4) + Im(p^2)(s|w|^2 - |p|^2), with w = z0 + i z3, p = z1 + i z2 and s in C. Then:

1. **Smoothness.** X_s = {G_s = 0} is a smooth quartic K3 surface exactly when s^4 != 16 (referee's own discriminant: (s-2)(s+2)(s^2+4)). The wall members are singular; at s = +-2 they have exactly 8 ordinary nodes, at s = +-2i the node count is not computed exactly; see ../family/wall/ and PAPER.md section 7.4.
2. **Symmetry.** Every member carries the 32 block symmetries. Exactly 16 of them act symplectically, since det(M)/c = +1. That subgroup is SD16, matching Degtyarev-Rams 2301.04127 Table 1 for Y56.
3. **Rank at least 19.** Hashimoto's Table 10.1 gives SD16 a coinvariant lattice of rank 18, so every smooth member has Picard rank >= 19. This is a corollary of known theory, not a new result.
4. **Lines on a smooth member.** Each smooth member has a reduced Fano scheme. Reducedness follows from smoothness: H^0(N_L) = H^0(O(-2)) = 0. The scheme has exactly 40 lines, except:
   - 48 lines at s = 0, a member projectively equivalent to the Fermat quartic;
   - 56 lines at s^4 = 81/2, which is Y56 (DIS eq. 9.4 after z1, z2 -> 2^(-1/8) z1, z2).

   The jump set is complete: the referee's minimal-prime decomposition plus the meeting stratum show that no other s carries extra lines.
5. **The 40-line lattice.** The 40 persistent lines form a finite étale family over the smooth base. Their Gram matrix is constant (a theorem, by local constancy on a connected base). They span a primitive lattice N19 of rank 19, det 128, Smith form [2,8,8] and signature (1,18).
6. **Rank exactly 19 for the very general member.** Suppose it were 20. Then the period would be constant on the connected smooth base, so T would be the same for all smooth members. But T(X_0) = [8,0,8] and T(Y56) = [2,0,32], which are not isometric. The method is Bouyer's (1511.01781 sec 4.3).
7. **Y56 is a Noether-Lefschetz point of the pencil.**
   - Its 56-line lattice has rank 20 and det -64. The orthogonal complement of N19 is spanned by a class v with v.v = -32, v.h = 0 and v.L = ±4 on exactly 16 lines.
   - Those 16 lines are one orbit of the order-32 group: L00, L06, L10, L11, L12, L19, L29, L33, L35, L36, L42, L44, L48, L50, L54, L55.
   - They are the solutions of a three-equation system that is consistent only when 2 s^4 = 81.
8. **Conics.** There are 48 classes L+ + L- of degree 2 and square -2, all in the span of N19. None of them is a sum of two persistent lines (checked 0/48), so on a generic member each one is an irreducible rigid conic. At Y56 each splits into a meeting pair of special lines. In one explicit family, the norm of the conic determinant is a nonzero constant times (2s^4 - 81)^2.
9. **Real lines along real s.** The count is 8 for |s| < 2 and for s < -2, 24 at s = 2 (a singular member), 40 for s > 2 except at s = 3·2^(-1/4), and 56 there (Y56). The proof is exact: q(s - delta) = delta^4 - s^2 delta^2 + 4.

## Novelty (gate, 2026-11-20)

OPEN, meaning no published source found:
- the pencil as a family;
- the generic 40-line configuration (rank 19, det 128);
- the jump set {0, 81/2};
- the Noether-Lefschetz description of Y56 with v and the 16-line orbit;
- the 48 conics degenerating into the 16 lines;
- the real counts 8/24/40/56 along the pencil.

TAKEN:
- The kind of result: Veniani 1708.01219 sec 6.7, Bouyer 1511.01781, Barth-Sarti math/0301329.
- The Y56 member's equation (DIS).
- Rank >= 19 (via Hashimoto).

**Credit line:** "the pencil frees the coefficient 3 in Degtyarev-Itenberg-Sertoz's equation (9.4)".

## Loose ends

1. CLOSED 2026-11-20 (overlattice/OVERLATTICE.md): NS of the very general member is exactly N19. There are two routes, both using item 6's rank-19 argument.
   - Primitivity: N19 is primitive in NS(Y56), checked by the Smith form here and by the referee. NS(generic) is primitive in NS(Y56) and contains N19 with finite index, so the two are equal.
   - Enumeration: all 14 proper even overlattices fail. Each has (-2)-roots orthogonal to h and extra degree-1 (-2)-classes, with explicit witnesses.

   Status: EXACT (enumeration) plus ARGUED (the primitivity step), not refereed separately.
2. Only one family of the 48 conics has explicit equations. Their reality for real s is not determined.
3. The lattice of the wall member and the s = infinity end (a union of planes, not K3) are not analysed.
4. CLOSED 2026-11-20: the three-equation certificate of item 7 is kernel-checked in Lean (../lean/Y56_Pencil.lean, theorems pencil_forces and pencil_solvable).
5. The real counts for the other five real structures along the pencil are not computed.

Written with AI assistance.
