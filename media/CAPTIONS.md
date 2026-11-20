# Captions: the pencil pictures

Moki & Julio (AI-assisted) · 2026

These pictures show the family of Section 7 of the paper. They are exploratory renderings: the surfaces are marching-cubes meshes of the exact equations, and the real lines in the animation and the strip were tracked numerically. A picture is not evidence; the counts the pictures show agree with Theorem 7.1, item 9, which is EXACT. The pictures of Y56 alone (lines, conics, screw, six faces) are in `../core/media/` with their own captions.

The family is drawn as $\operatorname{Im}(w^4) + \operatorname{Im}(p^2)(b\lvert w\rvert^2 - \lvert p\rvert^2)$ with $b = \sqrt{\lvert\kappa\rvert}$, which is the paper's dial $s$ ($\lvert\kappa\rvert = s^2$): Y56 is $\lvert\kappa\rvert = 9/\sqrt2 \approx 6.364$ ($s = 3 \cdot 2^{-1/4}$), the wall is $\lvert\kappa\rvert = 4$ ($s = 2$), and the Fermat-type end is $\kappa = 0$. The labels written inside `y56_family_strip.png` use $\lvert\kappa\rvert$. Colours: amber = the 16 lines that exist only at Y56 (orbit S), cyan = the 8 anchor lines present on every member, pink = the other 32 lines, gold = the 8 pinch points of the wall. Sphere model: real projective space drawn in the stereographic sphere model of $S^3$ with a fixed camera.

## y56_to_fermat.gif (video: y56_to_fermat.mp4)

**Start here.** Y56 is the smooth real quartic surface that holds the most real straight lines possible, 56. Here it is bent step by step along a one-parameter family: the instant it leaves Y56 the real lines drop from 56 to 40, they fall to 24 at a "wall" where the surface pinches at 8 points, and only 8 are left beyond it, down to the Fermat-type end. The 16 amber lines exist only at the single exact setting of Y56 and vanish the moment the dial moves.

48 frames; the 6 paused frames are the wall, with the 8 pinch points glowing (each appears twice, because the sphere model covers projective space twice). Made by `scripts/track.py` (numerical line tracking: Levenberg-Marquardt refinement plus a fresh random search at every step), `scripts/render_morph.py` (frames) and `scripts/assemble.py` (GIF and strip). The MP4 is a video encoding of the same 48 frames; its encoding command is not shipped.

## y56_wall.png

**Start here.** This is the wall of the family: a quartic surface with exactly 8 pinch points (gold). Through them run four conics, two in each of the planes $z_1 = z_2$ and $z_1 = -z_2$; each plane holds 4 of the pinch points and cuts the surface in two conics that meet exactly there. The 8 pinch points have closed forms built from $\cos(\pi/8)$ and $\sin(\pi/8)$ (paper, Section 7.4).

The object is EXACT (nodes and conics factored exactly; evidence in `../family/wall/`); the picture is a rendering.

## y56_family_strip.png

**Start here.** Five snapshots of the same family from one camera: Y56, a step toward the wall, the wall, a step beyond it, and the Fermat-type end. The picture gets quieter as the real lines drop from 56 to 40, 24 and finally 8, and the surface loses sheets at the wall.

The line counts in the labels were found numerically and agree with the exact counts of Theorem 7.1, item 9.

## scripts/

`track.py`, `render_morph.py` and `assemble.py` produced the three pictures above; run them from `scripts/` in that order: `python track.py`, `python render_morph.py frames`, `python render_morph.py wall`, `python assemble.py` (they need numpy, pyvista, scikit-image and Pillow; the pictures were made this way in the working folder and were not re-rendered from this layout). `lines56_basis.npy` holds a floating-point orthonormal basis of each of the 56 lines of Y56 (the starting point of the tracking), and `lines_track.npz` is the tracking output used by the renderer. The rendered frames are not shipped; `render_morph.py` writes them to `frames/`.

Written with AI assistance.
