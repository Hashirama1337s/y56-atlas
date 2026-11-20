# The Y56 Atlas: build notes

Moki & Julio (AI-assisted) · 2026-11-20 · viewer version 1.0

An interactive 3-D page for Y56, the smooth real quartic surface with 56 real lines (Degtyarev, Itenberg and Sertöz, arXiv:1601.04238). Open `index.html` from a web server (or any static host). It loads three.js r160 (`three@0.160.0`) from cdn.jsdelivr.net, so it needs an internet connection the first time it opens.

## Files

| file | size | what |
|---|---|---|
| `index.html` | 50.7 kB | the page: layout, captions, 3-D scene, controls |
| `core.js` | 12.8 kB | maths core, no graphics: ball projection, marching cubes, curve cutting at the glass, family-line formulas |
| `data/y56-data.js` | 1.62 MB | all curve samples and coefficients, generated (see below) |
| `build/common.py` | | loaders for the exact release data, shared maths |
| `build/build_data.py` | | writes `data/y56-data.js` from `core/data/*_exact.txt` (no hand-typed coordinates) |
| `build/node_check.mjs` | | runs `core.js` headless in node with the shipped data |
| `build/verify_viewer.py` | | the accuracy check (below); writes `build/verify_report.json` |
| `build/build_report.json`, `build/verify_report.json` | | outputs of the last build and check |

Shipped total: 1.69 MB.

Rebuild and re-check (from `build/`):

```
python build_data.py                         # about 30 s
python verify_viewer.py <three@0.160.0 package folder>   # about 1 min; needs node and `npm install three@0.160.0` somewhere
```

## How the picture is made

- **Coordinates.** The picture uses y with z1 = 2^(1/8) y1 and z2 = 2^(1/8) y2. In these coordinates the release equation F becomes exactly the family member G_s at s = 3/2^(1/4) (s^4 = 81/2), so the Y56 view and the family dial share one frame. Exact coordinates on the hover cards are in the release coordinates z.
- **Ball model.** Real projective space is the unit 3-sphere with opposite points identified. Each point is moved into the half-sphere around a centre c and projected stereographically, Y = E x / (1 + c.x), which fills the unit ball exactly once; opposite points of the glass are the same point. A line becomes a circular arc from one point of the glass to the opposite point. The centre is (0 : 1 : 1 : 0) in y, chosen because 16 of the 32 symmetries fix it, so the picture shows a four-fold turn about the vertical axis, mirrors and the point reflection. G_s(c) = -1 for every s, so the centre is off the surface along the whole dial.
- **Surface.** Marching cubes in the browser on a 124^3 grid (88^3 on small screens, 56^3 while the dial is dragged), normals from the gradient of the true function, cut exactly at the glass in the shader. Two sides of the sheet get two shades of blue.
- **Curves.** Python samples each line (160 points), conic (240 points) and face curve from the exact data; the browser cuts each curve where it crosses the glass (the crossing is located in R^4) and draws glowing tubes.
- **Family lines.** Computed live in `core.js` from the closed forms of pencil/RESULT.md (components C1 to C4 in pencil/REPORT.md, finding 1): 8 anchor lines in z1 = 0 or z2 = 0 for every s; for s >= 2 the 32 lines of components C1 to C4 from delta^4 - s^2 delta^2 + 4 = 0 and v = s + delta (C3, C4: C^2 = v or D^2 = v; C1, C2: D^2 = v/2); coincident lines (the wall) are merged. The 16 Y56-only lines (the orbit of L00) are added from the exact data only when the dial sits exactly at s^4 = 81/2 (the slider snaps to it within 0.012). Each family line is coloured by the Y56 orbit it becomes at s^4 = 81/2.
- **Six faces.** For each class representative g00, g02, g24, g01, g12, g13 (core/docs/SISTERS.md), real coordinates x with y = A x, A = [Q+ | i Q-] from the eigenvectors of the symmetric orthogonal matrix M/sqrt(lambda); the drawn surface is G_s*(A x)/phase (a real quartic). Real lines are the lines fixed by g; a conic is real when its plane is fixed and its Gram form becomes a real form; it is drawn when that form is indefinite. Each face has its own centre (the standard face uses the main one; the others use a centre chosen so that the glass cuts the surface as little as possible).

## Modes and captions

Start-here paragraph (on the page): "A straight line can lie inside a curved surface, the way straight steel beams make up a curved cooling tower. Y56 is a smooth surface cut out by a single equation of degree 4, and it holds 56 perfectly straight lines, all of them real: the most real lines any smooth real surface of degree 4 can hold, and Y56 is the only one that does it (Degtyarev, Itenberg and Sertöz proved this; with complex lines allowed, the record is 64). Spin it, touch a line to read its exact coordinates (whole numbers and √2), turn the family dial to watch 16 lines flash into existence at one single setting, and see the same equation through six different meanings of 'real'." Followed by "How to read the ball": "All of space, including its points at infinity (projective space), is drawn as this glass ball. Whatever leaves through the glass comes back in at the exactly opposite point, so a straight line shows up as an arc running from one side of the ball to the opposite side."

**1. Y56.** Surface plus the 56 lines as glowing tubes coloured by symmetry orbit: cyan = orbit of 8 (the anchor lines), pink = orbit A (16), green = orbit B (16), pale gold = orbit S (16, the Y56-only lines). Toggles: surface, each orbit, the 148 conics beside line pairs (amber), the 40 conics in line-free planes (violet), the 20 two-conic planes (violet film), the glass. Hover (mouse) or tap (touch) a line: it turns white, its 16 neighbours light up, and the card gives its name, orbit, role on the dial and exact coordinates. Hover a conic: the card gives its plane equation (exact) and its two lines, or its plane orbit; a violet conic also lights up its plane.
Caption: "The blue sheet is Y56 and every coloured tube is a perfectly straight line lying entirely on it: 56 real lines, the most a smooth real surface of degree 4 can hold. The colours are the four groups that the 32 symmetries of the surface shuffle among themselves (8, 16, 16 and 16 lines); each line crosses exactly 16 others." With conics on, it adds: "Amber and violet curves are conics (degree-2 ovals) on the surface: 148 sit beside a pair of crossing lines, and 40 come two by two in 20 flat planes that contain no line at all."

**2. Family dial.** Slider for s from 0 to 3 with snaps and buttons at 0 (Fermat type), 2 (the wall) and 3/2^(1/4) (Y56); the surface is re-meshed live and the real lines are redrawn from the formulas; live counter "real lines: N" (8 / 24 / 40 / 56); at the wall the 8 singular points are drawn in gold; arriving at Y56 flashes the counter and the 16 new lines.
Captions: s < 2: "Turn the dial s and the equation changes smoothly. Below the wall at s = 2 only the 8 anchor lines (cyan) are real; 32 more lines exist but are imaginary, invisible in a picture of real points." s = 0: "At s = 0 the surface is of Fermat type and only the 8 anchor lines are real; turn the dial to the right and watch what the wall does." s = 2: "The wall, s = 2: the surface pinches at 8 points (gold dots) and the 32 new lines arrive in 16 coincident pairs, so you see 8 + 16 = 24 lines." 2 < s, not Y56: "Past the wall, 8 + 32 = 40 lines are real and slide smoothly as you turn the dial. Sixteen more lines exist on just one member of the family: try to find it (or press Y56)." At Y56: "At exactly this setting, s^4 = 81/2, sixteen extra lines (pale gold) appear all at once: three conditions that normally cannot all hold together are met here and nowhere else. That surface is Y56, with 56 real lines."

**3. Six faces.** Six buttons (56 lines genus 10; 12, 8, 4 lines two handles; 0, 0 lines three bubbles); each shows that face's real surface, its real lines (coloured by Y56 orbit) and its real conic ovals (amber / violet). Common lead: "The same equation, read with six different meanings of 'real point', shows six different real surfaces with 56, 12, 8, 4, 0 and 0 real lines." Then per face:
- g00: "The usual meaning of real: one connected surface with ten handles, carrying all 56 real lines and all 188 conic ovals."
- g02: "A second meaning of real: one surface with two handles, carrying 12 real lines and 10 conic ovals."
- g24: "A third meaning of real: again two handles, with 8 real lines and 8 conic ovals, all from line-free planes (the 4 conics of its line-pair planes are real but have no real points)."
- g01: "A fourth meaning of real: two handles, 4 real lines and 8 conic ovals (2 amber, 6 violet)."
- g12: "No real lines at all: the surface falls apart into three separate bubbles, and all 22 conic ovals crowd onto one of the three while the other two stay bare (EXACT separation of the bubbles, NUMERICAL placement of the ovals)."
- g13: "No real lines and three bubbles again, but now 20 conic ovals, shared out among the bubbles; only the conics tell this face apart from the previous one."

Credit line on the page: Y56 and the maximality and uniqueness theorem to Degtyarev, Itenberg and Sertöz (arXiv:1601.04238); the count 636 to Degtyarev (arXiv:2407.00493); the exact line list, drawn conics, family dial and six-faces table to Moki & Julio (AI-assisted). Byline "Moki & Julio (AI-assisted)".

## Accuracy check (verify_viewer.py, 2026-11-20): 53 of 53 pass

Float tolerance for curve points: |G| < 2e-6 on unit vectors (the data are stored as 32-bit floats).

| check | result |
|---|---|
| A1 56 lines x 160 points on G_s* | max |G| = 1.1e-7 |
| A2 same points in release coordinates on F | max |F| = 1.1e-7 |
| A3 every line point on the exact line of lines_exact.txt with the same index | 3.3e-8 |
| A4, A5 orbits 8 + 16 + 16 + 16, invariant under all 32 symmetries | pass |
| A6 each line meets 16 others | pass |
| B1 188 conics x 240 points on G_s* | max |G| = 8.8e-7 |
| B2 148 + 40 conics; B4 each of the 148 listed with the two lines of its plane | pass |
| B3 every conic point in its exact plane | 3.8e-8 |
| B5 each conic spans a plane (not degenerate) | pass |
| B6 the 20 drawn planes contain their 40 conics | 2.7e-8 |
| C0 to C4 six faces: A unitary and sigma-real (M conj(A) = A); drawn quartic = G_s*(A x)/phase (rel. 3e-15); counts (lines, sigma-real conics, ovals) = (56,188,188), (12,14,10), (8,12,8), (4,12,8), (0,28,22), (0,28,20), equal to the exact SISTERS table; drawn lines = lines fixed by g; every drawn face point satisfies |G| < 3.1e-7, is sigma-real and lies on its exact line or in its exact plane | pass |
| D1 family lines from core.js lie on G_s at 307 dial values | max |G| = 1.3e-7 |
| D2 real line counts: 8 for all s < 2, 24 at s = 2, 40 for s > 2, 56 at s^4 = 81/2 (incl. 1.9999, 2.0001, s* ± 0.001) | pass |
| D3 at s^4 = 81/2 the 40 formula lines are exactly the 40 non-special Y56 lines; with the 16 they give all 56 | pass |
| D4 the 16 Y56-only lines are one orbit (orbit S) | pass |
| E1 marching cubes (the browser code) | |f| at vertices <= 7e-4 of the field scale (grid interpolation) |
| E2 family coefficients at s* = standard-face quartic | 7.8e-15 |
| E3 curve pieces stay in the ball and end on the glass | pass |
| E4 the 8 gold points at the wall are singular (G = 0, gradient = 0) | 6e-17, 6e-11 |
| F1 shipped size | 1.69 MB |
| F2 no local paths, personal names or AI product names in shipped files | pass |
| F3 libraries only cdn.jsdelivr.net/npm/three@0.160.0 | pass |

Also observed: the build reproduces the six-faces table exactly (build_report.json), and the headless timing was 18 ms (field) + 33 ms (marching cubes) for the 96^3 Y56 mesh in node. In a desktop browser pane the full family rebuild took about 66 ms and a drag step about 35 ms. Phones were not measured.

## Loose ends

- Opening `index.html` straight from disk (file://) was not tested; it was tested through a local web server. Some browsers block module scripts on file:// pages; a static host (GitHub Pages or an artifact) avoids this.
- Touch input was tested only in a phone-size emulation in which taps arrive as mouse clicks; the tap-to-pin card path has not run on a real phone.
- The page needs the three.js files from jsdelivr; offline it shows a message after 12 s.
- The surface is a marching-cubes mesh, so its edges are accurate to the grid (one cell is about 0.017 of the ball radius); curves are accurate to float32.
- The amber conics often look almost straight and broken: most of the 148 are large ovals that cross the glass several times, so you see several near-straight pieces. They are drawn correctly (check B1, B3).
- "All 22 ovals on one bubble" (face g12): EXACT separation, NUMERICAL placement. msolve proves that two rational levels of an integer quadratic form miss the real surface, so the three bubbles are separated exactly; the placement of the 22 ovals on one of them is a float evaluation of every oval at 1500 points with a margin (minimum distance 5.76 to a level, errors near 1e-12), not interval arithmetic. Evidence: family/faces/ (b_*.ms, b_*.out, b_assign.py, b_assign.log).
- Each non-standard face has its own centre and frame, so the six faces cannot be compared point by point; only g00 shares the main frame.
- At the wall, each pair of coincident lines is drawn once, in the colour of one of the two.
- The family dial shows lines only: no conics, and the 48 conics that collapse onto the 16 Y56-only lines near s^4 = 81/2 are not drawn.
- No screw animation (the eighth-turn screw does not fix the centre, so it would need a re-mesh per frame).
- The light theme has no glow (normal blending); the dark theme is the intended look.

Written with AI assistance.
