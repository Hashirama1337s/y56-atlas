# Y56: the six real forms, exact (Moki & Julio, 2026-11-19)

F = 3e z0^2 z1 z2 + 3e z1 z2 z3^2 - e z1^3 z2 - e z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3, e = sqrt2
  = Im(w^4) + Im(p^2)(3|w|^2 - |p|^2)/sqrt2, w = z0 + i z3, p = z1 + i z2.

Status: the counts and the topology below are EXACT (exact arithmetic in Q(sqrt2) and exact integer lattices). The meshes are
a numerical cross-check. The renders are EXPLORATORY. Nothing here is published elsewhere.

## The table

| real form sigma_g = g o conj | class (members) | real lines | sigma-real conics of the 188 (with a real oval) | real part | chi | (r,a,delta) of L+ | three methods agree? |
|---|---|---|---|---|---|---|---|
| g00 standard | 1 (g00) | 56 | 188 (188) | 1 surface, genus 10 | -18 | (1,1,1) | yes |
| g02 | 4 (g02 g05 g15 g18) | 12 | 14 (10) | 1 surface, genus 2 | -2 | (9,9,1) | yes |
| g24 central | 1 (g24) | 8 | 12 (8) | 1 surface, genus 2 | -2 | (9,9,1) | yes |
| g01 | 4 (g01 g07 g08 g25) | 4 | 12 (8) | 1 surface, genus 2 | -2 | (9,9,1) | yes |
| g12 | 4 (g12 g17 g27 g29) | 0 | 28 (22) | 3 spheres | 6 | (13,9,1) | yes |
| g13 | 2 (g13 g16) | 0 | 28 (20) | 3 spheres | 6 | (13,9,1) | yes |

Conic split (two-line-plane conics of 148 / plane-pair conics of 40; ovals in brackets):
g00 148(148)/40(40); g02 14(10)/0; g24 4(0)/8(8); g01 4(2)/8(6); g12 16(16)/12(6) (+ 4 pair conics in fixed planes swapped, so not real);
g13 12(8)/16(12).
"Three methods": Lefschetz trace, Nikulin lattice invariants, mesh at two grids (160, 260). Every component is orientable (an even-degree
surface in RP^3 is two-sided). The line counts 56/12/8/4/0/0 and the topology column are exact results by the methods below.

## 1. The real structures (s1_group.py, s1_group.log)
- The 32 listed maps satisfy F(Mz) = c F(z) exactly (c in {1,-1,4,-4}, real), and all 56 lines lie on F (sympy expand = 0).
- Aut(Y56) is exactly these 32. Every projective automorphism permutes the 56 lines and keeps the intersection graph. The graph has 64
  automorphisms (networkx, full enumeration). For each, the linear conditions "M maps line i into line pi(i)" (224 equations over Q(sqrt2),
  16 unknowns) were solved exactly: 32 have a 1-dimensional solution, 32 have none. The identity gives only scalars, so the action on lines
  is faithful. The 32 realised permutations are exactly the listed ones. All matrices are real, so complex solutions add nothing.
- Real structures: any real structure is sigma = g o conj with g in Aut and g g-bar = g^2 = 1 projectively. Two are isomorphic iff
  h g h-bar^-1 = g', and h-bar = h because all automorphisms are real, so this is ordinary conjugacy. The {1} + 15 involutions form
  6 classes of sizes 1,4,1,4,4,2 (16 real structures in all) with 56,12,8,4,0,0 real lines respectively, matching DIS Remark 9.10 ("six real structures").
- Each M satisfies M^2 = lambda I with lambda in {1,2} > 0, so every sigma_g is the standard real structure of P^3 in suitable coordinates
  (no quaternionic type with empty real P^3). sigma_g preserves Y because c is real.
- Real lines = lines with g(l) = l (all 56 lines are conj-real). Each fixed line carries a real circle (2x2 action A, A^2 = lambda I, lambda > 0, exact).
- Real coordinates for portraits and meshes: M/sqrt(lambda) is symmetric orthogonal. A = [Q+ | i Q-] (orthonormal eigenbases) maps
  RP^3 onto the sigma_g-real points, and F(Ax) = phase * (real quartic). Eigen-sign splits: g00 4+0, g01/g02/g24 2+2, g12 1+3, g13 3+1.

## 2. Real conics (s3_conics.py, s3_conics.log)
- All 188 conics were rebuilt exactly. For each of the 148 two-line planes I solved F|plane = l1 l2 Q for Q, with the check
  exact. For the 20 pair planes, F|plane = c Q1 Q2 holds exactly with the listed factors.
- A conic is sigma_g-real iff g maps it to itself. For the 148 this means the plane is fixed. For pair planes the plane must be fixed and
  G^T Q G must be proportional to Q; otherwise the two conics are swapped.
- Real points: on the sigma-real coordinates s = [E+ | i E-] y, the conic becomes a real quadratic form. Its definiteness was decided
  from the exact sign pattern of the characteristic polynomial (Descartes rule, which is exact for real-rooted polynomials), with signs
  in Q(sqrt2) decided exactly. A definite form means a real conic with no real points.
- Positive control: standard form gives all 188 real, each with an oval (DIS/2407.00493 say all 636 conics are real).
- Numerical check: every drawn oval and line lies on the surface (|F| < 2e-14 relative), and the number of drawable ovals equals the exact count.

## 3. Topology, three ways
(a) Lefschetz (exact, s2_lattice.py). chi(X_R) = L(sigma) = 1 + tr(sigma*|H^2) + 1. sigma is antiholomorphic on a complex surface, so it
keeps the orientation of X: (-1)^2 = +1, which makes the H^0 and H^4 traces both 1. sigma* reverses every complex curve class:
sigma*[C] = -[sigma(C)] (DIS p.11 says the same). conj fixes each of the 56 lines, so sigma_g* = -g* on NS.
On T (x) R = (H^{2,0}+H^{0,2})_R, sigma* swaps H^{2,0} and H^{0,2}. In the basis (omega, omega-bar) its matrix is [[0,c-bar],[c,0]],
which has trace 0. rho = 20, so T (x) R is exactly this plane. Hence **chi(X_R) = 2 - tr(g*|NS)**. The trace was computed exactly on an
integral Z-basis of the line lattice. In table row order the traces are g00 20, g02 4, g24 4, g01 4, g12 -4, g13 -4, which gives
chi = -18, -2, -2, -2, 6, 6.
(b) Lattice (exact, s2_lattice.py; independent of chi for component counts).
- N = Z-span of the 56 lines is even, rank 20, disc -64, with discriminant group Z/2 x Z/32. T = [2,0,32] (Veniani 1708.01219 Table 1; the same lattice is listed in DIS), disc 64, so
  NS = N, using that cited row (see Loose ends).
- H^2(X,Z) is rebuilt as the even unimodular overlattice of N (+) T, glued by an anti-isometry of discriminant forms. There are exactly 4
  such gluings; all were tried, and every result below is identical for all 4.
- Each holomorphic g acts on A_N as eps = +-1, and eps equals det(M)/c (the action on the 2-form) for all 32 elements. This is a holomorphic
  consistency check, exact.
- sigma acts on T as diag(1,-1) or diag(-1,1). Gluing forces the one acting on A_T as -eps.
- L+ = ker(sigma* - 1) was computed over Z by HNF. It is 2-elementary in every case. a was cross-checked as the F2-rank of 1 + sigma*.
- Nikulin/Kharlamov: X_R = S_g + k S^2 with g = (22-r-a)/2 and k = (r-a)/2. The exceptions (10,10,0) and (10,8,0) do not occur.
  Results: standard (1,1,1) gives S_10; g01/g02/g24 (9,9,1) give S_2; g12/g13 (13,9,1) give S_0 + 2S^2, i.e. three spheres.
  The total F2-Betti number of X_R is 24 - 2a: 22 for the standard form and 6 for all five sisters.
(c) Mesh (numerical, s4_mesh.py; logs s4_mesh_160.log, s4_mesh_260.log). The real locus F(Ax) = 0 was meshed on S^3 by stereographic
marching cubes. Box boundary has constant sign; there are 0 non-manifold edges; antipodal components are paired.
- Grid 160 and grid 260 give identical results:
  - chi(lift) = -36, -4, -4, -4, 12, 12;
  - lift components 1, 1, 1, 1, 6, 6. The six are 3 antipodal pairs, giving 3 spheres.
- These agree with (a) and (b) row by row. Positive control: standard form = connected genus 10 = DIS Prop 9.12.
Consistency checks:
- Smith inequality: b*(X_R;F2) <= 24. Values are 22 and 6.
- Euler-characteristic range -18 <= chi <= 20 holds.
- g + k <= 11 holds.
- The Comessatti-type relation chi = 2r - 20 holds in every row, with r from L+.

## 4. Portraits (EXPLORATORY; render scripts not shipped)
- Six portraits, one per face (v1 ships only media/y56_face_g12.png and the contact sheet below). These are S^3 double-cover models, stereographic from a pole kept away from the surface and the
  curves. Each is scaled to unit radius with the same camera, so the six read as a set. Real lines are green; ovals of two-line-plane
  conics are amber; ovals of pair-plane conics are violet.
- media/y56_six_faces.png: 2x3 contact sheet, in the order 56 / 12 / 8 / 4 / 0 / 0 lines.
- media/y56_screw.gif (36 frames) + media/y56_screw_ffmpeg.mp4: the standard Y56 under the continuous screw (w,p) -> (e^{it} w, e^{2it} p),
  t in [0, 45 deg). At t = 45 deg this is the symmetry g04 with F -> -F (checked numerically, 6e-14), so the loop closes seamlessly.
  The old GIF only repeated a 90-degree symmetry of w alone.

## 5. Prior art (2026-11-19)
Searches covered:
- 3 web searches;
- the arXiv API over https (5 queries, plus id lookups);
- Zenodo (2 queries);
- searches through 13 source texts read locally.

What was found:
- TAKEN: "six real structures, enumerated by conjugacy classes of involutions" (DIS 1601.04238 Remark 9.10); the standard form has 56 real
  lines and is connected of genus 10 (Prop 9.12); all 636 conics are real in the standard form (2407.00493 Remark 7.4).
- NOT FOUND: real-line counts, real-conic counts or topology of the five non-standard forms.
  - DIS give these only for Schur's X64 (Prop 9.3, lines only).
  - 2512.06833 discusses real h-fragments for Y56 only in the standard form.
  - 2608.05941 (real structures in equisingular strata of quartics; appeared after our first search pass) does not treat Y56 or real lines; text searched.
  - Zenodo 10.5281/zenodo.14360457 ("Line arrangements on smooth quartics") is software for line configurations; it has no real forms.

**Verdict: PARTIAL.** The existence and number of the six forms are taken. The table of lines, conics and topology for the five sisters
appears OPEN in what was checked. It is, however, a routine computation for lattice experts: Nikulin's theory plus DIS data.
Ceiling: a complete small table and a figure set completing a 2016 remark.

## 6. Curiosities (leads, not v1 claims; UNTESTED unless stated)
1. Five sisters, only two shapes. The lattice invariants are identical within the groups: g01, g02 and g24 all have (9,9,1), and g12 and
   g13 both have (13,9,1). By Nikulin-Kharlamov, (r,a,delta) fixes the coarse deformation class of a real K3. So the three genus-2
   sisters (12, 8 and 4 lines) are probably one deformation family of real K3 surfaces, seen at three different real quartic positions.
   The same holds for the two three-sphere sisters. Update: settled by citation, not by an explicit path. Kharlamov's rigid-isotopy classification, as summarised in the Degtyarev-Kharlamov survey (arXiv math/0004134, section 3.5.4), puts g01, g02 and g24 in one class and g12 and g13 in one class (CITED; the class counts were read from tables in a rendered page image, and no explicit deformation path was built).
2. All five sisters have a = 9 (total Betti 6, i.e. (M-9)-surfaces), while the standard form is an (M-1)-surface. The sisters sit at the
   poor end; only the standard form is near-maximal.
3. A lopsided bubble (numerical): in the g12 form, all 22 real conic ovals lie on ONE of the three spheres and the other two carry no
   real curve at all. In g13 the 20 ovals split 4 / 12 / 4. This geometric difference separates the two topologically identical
   zero-line forms. Exact proof not attempted; a centraliser/symmetry argument should decide it.
4. Real but invisible conics. Some sigma-real conics are definite and so have no real points: 4 in g02, 4 in g01, 6 in g12, 8 in g13.
   In the central form g24, all 4 of its real two-line-plane conics are empty. Exact.
5. g12 and g13 cannot be told apart by real lines or by topology, only by conics (22 vs 20 ovals; 4 swapped pair conics in g12). They are
   not isomorphic as real quartics (not conjugate in Aut). Whether they become isomorphic as abstract real K3 surfaces, through a
   non-projective automorphism of the infinite group Aut(X), is an open question here.

## Loose ends
- NS = N (the line lattice is primitive) is taken from the published transcendental lattice (T = [2,0,32], disc 64 = |disc N|; Veniani 1708.01219 Table 1). EXACT-2.md, Addendum 3, gives the argument. Everything else in part (b) is exact given this.
- Isomorphism of real structures is taken up to projective automorphisms (the 32), as in DIS. Isomorphism as abstract real K3 surfaces
  (infinite Aut) was not studied; see curiosity 5.
- The use of (r,a,delta) -> topology relies on the Nikulin/Kharlamov theorem, which is cited, not re-proved. The Lefschetz chi and the mesh
  are independent of it, and they agree.
- Singular is not used here; exact arithmetic is own Python (Fractions in Q(sqrt2)) plus python-flint HNF and sympy Smith forms. These are
  trusted software, not kernel-checked.
- Graph automorphism count 64 is from networkx VF2 (full enumeration) in the shipped scripts. A later check with a second algorithm (igraph, bliss) also gave 64; that script is not part of v1.0. The Galois-twist explanation of the 32 unrealised automorphisms is checked by `code/exact/galois_twist.py` (transcript `data/logs/galois_twist.log`). GAP gave the group of order 32.
- The oval-to-sphere assignment (curiosity 3) is numerical (nearest mesh vertex, max distance 0.05 in stereographic units).
- Renders: in the animation the S^3 double cover runs off to infinity and is clipped at the box edge, so some sheets are cut. The g12
  portrait shows one sphere copy partly outside the view.
- The genus-2 surfaces' real lines and ovals were not assigned to handles (no "where are the lines on the S_2" picture).
- Prior art: no paywalled journal versions were opened. Kharlamov's surveys on real K3s were not opened for a Y56 table.

## Files
- Exact pipeline (code/sisters/): q2.py (Q(sqrt2) arithmetic and loaders); s1_group.py, s2_lattice.py, s3_conics.py; logs in data/logs/ (s1_group.log, s2_lattice.log, s3_conics.log).
- Mesh: code/sisters/s4_mesh.py; logs data/logs/s4_mesh_160.log and s4_mesh_260.log.
- Pictures: media/y56_six_faces.png, media/y56_face_g12.png, media/y56_screw.gif, media/y56_screw_ffmpeg.mp4. The render scripts and the oval-to-sphere script are not part of v1.0.
