# PATCHES

Every sanitising change made to a staged copy. Originals in the working folder are untouched. sha256 is of the ORIGINAL file. Binary files and data files not listed here are byte-identical copies.

| staged file | source (working folder) | original sha256 | change |
|---|---|---|---|
| `code/exact/aut.py` | `exact/aut.py` | `f9c341917159ffd5899af0607fdfe33aa27cbad0598c836676935c7def56f0d4` | edges read from data/edges.json instead of edges.pkl |
| `code/exact2/e1.py` | `exact2/e1.py` | `251cba0419d53282485a3dd9f8fc54dbc99f55d65cfba081ecd2ac1c9eb2e0f3` | data path x1; symmetry matrices read from data/symmetry_exact.txt instead of syms.pkl |
| `code/exact2/f1.py` | `exact2/f1.py` | `2de0969c0202d7a710e23d8236c82a493ed693a23244963497d17698a76a8821` | data path x1; npz -> cwd x1; npz -> cwd x1; symmetry permutations read from data/symmetry_exact.txt instead of syms.pkl; render-data (npz) section removed |
| `code/exact2/l1.py` | `exact2/l1.py` | `e7693dd926cb524c167d2a1829f6d43118260c6e30af2be851c89f2c4467bf54` | pkl -> cwd x1; edges read from data/edges.json instead of edges.pkl |
| `code/exact2/l2.py` | `exact2/l2.py` | `16a884fdeab09ebc634a02f5e4c5d91fd63c788f68b23117c988cb50f29aec9a` | reads data/lat.txt and data/lat_lines.txt |
| `code/exact2/l3.py` | `exact2/l3.py` | `c604b73b1737865c9c9eeffc3d8ff12c81b6a7f01b0af36954eeee455c30c1b2` | reads data/lat.txt |
| `code/exact3/gen.py` | `exact3/gen.py` | `adc85ed0907d94c704d83a34b472615f5a12fee3c3fa166084d7c0671f35107e` | data path x1 |
| `code/exact3_v2/analyze.py` | `exact3/v2/analyze.py` | `f2b39af0c7bc4d6323169bf676cf3a478dbcc17acd1176e5c4142d819889c2fa` | reads data/logs/real_01.out and gb_01.out |
| `code/exact3_v2/run_ms.sh` | `exact3/v2/run_ms.sh` | `44c512fb36134beecb920acf5bdfbbbcf020b4ca4b24702a72077742a7f7f5f5` | msolve path -> $MSOLVE x1; WSL cd -> script dir x1 |
| `code/exact3_v2/run_real.sh` | `exact3/v2/run_real.sh` | `10db632fe96ba95d5a1394a54c5b795b98ba9a53c8c923a5b7570be310c5ad8f` | msolve path -> $MSOLVE x1; WSL cd -> script dir x1 |
| `code/sisters/q2.py` | `sisters/q2.py` | `b40281ce8d6c3ed20feb4232ff53f0ffc42e18198a80f4ead2cf313353efa6e8` | root path -> relative x1; data path x1; data paths now resolve relative to the file (../../data/...) |
| `code/sisters/s1_group.py` | `sisters/s1_group.py` | `069651130415c8ef6b33d67a600be11f8483bb298683e13d04f15c66987c17b8` | sys.path -> . x1; sisters pkl -> cwd x1 |
| `code/sisters/s2_lattice.py` | `sisters/s2_lattice.py` | `0607f6a03463f29d1d0e5dd8bfbb0ba42c3d251e6f519540d1c7de2a7e98adf2` | sys.path -> . x1; sisters pkl -> cwd x2 |
| `code/sisters/s3_conics.py` | `sisters/s3_conics.py` | `656b5e7b5f4405ea540e7c82d1d7203aecba0be8d0ea1f6663252f6eb7b5c25f` | sys.path -> . x1; sisters pkl -> cwd x2 |
| `code/sisters/s4_mesh.py` | `sisters/s4_mesh.py` | `81b171721b5ec272fdc455d8c60eadbeaf23c1ff27c2a5d3f797f9789e8e2385` | sys.path -> . x1; sisters pkl -> cwd x2 |
| `docs/EXACT-2.md` | `exact/EXACT-2.md` | `2f3fbbc0412906866de5eb0d80cb0625100e2db2920bc172ba97a536f6e7c47b` | doc path x1; doc path x1; doc path x1 |
| `docs/EXACT.md` | `exact/EXACT.md` | `9b8ad86ffd687ea24799cf643cde0a493646be6b78320feca1d849b09a8c65cf` | replaced the superseded "only 1 of 20 line-free planes" bullet with a pointer to EXACT-2.md |
| `docs/LINES-COUNT-2.md` | `exact3/LINES-COUNT-2.md` | `f0002dacaef95318189c81d4f15eebe6a41b1cb1b64a9dc8e1909773952e129c` | doc path x1; doc path x1 |
| `docs/LINES-COUNT.md` | `exact3/LINES-COUNT.md` | `5ec210135e8e16c83e9f88fc38f58c42c6631284a06ac08233b74613422ab425` | doc path x1; doc path x1 |
| `docs/SISTERS.md` | `sisters/SISTERS.md` | `1d6734f74f77b99ffb98985c09c8de300bdeab597c9598dbe2fc55c01d6ddb28` | doc path x1; removed lab name from the title line |
| `docs/EXACT.md` | editorial pass (release text) | n/a | data/ paths added to the three file lines; the numeric-file mention in section 2 reworded; the orbit line now states the 20 conic-pair planes form orbits 8, 8, 4 (EXACT-2.md); the stale "What remains" list replaced by a pointer to where each item was closed |
| `docs/EXACT-2.md` | editorial pass (release text) | n/a | header lists only shipped scripts; references to the unshipped numeric pickle, search scripts, render scripts and old renders reworded or pointed at CORRECTIONS.md and media/; "Loose end 1/2" headings renamed; added Addendum 3 (completeness closed by citation to Veniani 1708.01219 Table 1, text from the working notes) and pointers to it in the loose-ends list and in Addendum 2 (ii); the 12000-start search labelled NUMERICAL with scripts not shipped. Mathematics untouched |
| `docs/LINES-COUNT.md` | editorial pass (release text) | n/a | transcript names changed to the shipped paths (data/logs/fano_rerun.out, smooth.out); lab-process wording removed; first-transcript loose end reworded to point at the clean re-run; second-CAS bullet points to LINES-COUNT-2.md |
| `docs/LINES-COUNT-2.md` | editorial pass (release text) | n/a | Files section lists only shipped files (unshipped run logs removed) |
| `docs/SISTERS.md` | editorial pass (release text) | n/a | internal-process wording and references to unshipped working folders removed; T = [2,0,32] now cited to Veniani 1708.01219 Table 1 (DIS also lists it); deformation-family curiosity updated with the cited Kharlamov classification (CITED, no explicit path); the 64-automorphism loose end notes the second-algorithm count whose script is not shipped; the note about an empty video file removed; Files and Portraits sections list only shipped files; Curiosities heading marked as leads, not v1 claims |
| `media/CAPTIONS.md` | editorial pass (release text) | n/a | the opening sentence of each caption changed from "the one smooth real quartic surface that holds the maximum possible 56 straight lines" to "a smooth real quartic surface that holds 56 real straight lines" (see CORRECTIONS.md item 6); MANIFEST.sha256 needs regenerating |
| `README.md`, `RESULTS.md`, `PRIOR-ART.md`, `CORRECTIONS.md`, `LICENSE`, `LICENSE-CODE`, `CITATION.cff` | authored for release | n/a | new files (the README replaces the placeholder) |

Authored new files (no original): code/verify_all.py, docs/VERIFY-RUN.txt, data/edges.json (exported from the working-folder edge list), README.md (placeholder), requirements.txt, media/CAPTIONS.md, PATCHES.md, FILELIST.md, MANIFEST.txt, MANIFEST.sha256.

Not sanitised, by decision: `code/exact3_v2/gen2.py` keeps its fixed random seed (the .ms inputs depend on it); `media/y56_screw_ffmpeg.mp4` keeps the encoder tag written by the video library (no personal data); `gb_01.out`, `real_01.out` and the .ms files are large numeric text (hex-scanned, clean).

Dropped from the release because they need working-folder numeric intermediates (pickles, json): exact/lines_exact.py, exact/planes5.py, exact/sym.py. Their outputs are the shipped data files, which verify_all.py re-checks. data/logs/par_01.out added for the msolve evidence.

Added in the final pass:

| staged file | source | change |
|---|---|---|
| `code/exact/galois_twist.py` | authored new (adapted from a working-folder check of the Galois twist) | self-contained: recomputes the 64 graph automorphisms from data/edges.json, reads the 32 realised permutations from data/symmetry_exact.txt, imports code/sisters/q2.py by relative path; transcript `data/logs/galois_twist.log` |
| `data/logs/galois_twist.log` | output of the script above, run from code/exact | none; the final memcap line is the run wrapper's note |
| `data/logs/l2.log`, `data/logs/l3.log` | transcripts of the clean-room run of `code/exact2/l2.py` and `l3.py` | copied unchanged (checked: no local paths) |
| `docs/CLEANROOM.md` | clean-room record | local paths removed: the output-folder references and the placeholder msolve path; first-person and working-folder wording neutralised ("staged release" to "release", "lab memory cap" to "memory cap", seat and install-log remarks removed); results table and findings unchanged |
| `README.md`, `RESULTS.md`, `docs/SISTERS.md`, `CORRECTIONS.md` | editorial | clean-room result, command list and the two operational notes added; Galois-twist script added to R12 evidence; loose ends updated; CORRECTIONS item 3 reworded to what the debugging files show (the count of 16 could not be confirmed from any file) |

## Referee round 1 (fixes F1 to F11)

Text-only fixes after the referee read of v1.0, except F8 (one added check). Mathematics and data untouched.

| fix | files | change |
|---|---|---|
| F1 | `RESULTS.md` (R15), `docs/SISTERS.md` | class sizes corrected to "1, 4, 1, 4, 4, 2 with 56, 12, 8, 4, 0, 0 real lines respectively" (16 real structures in all); the old wording paired the sizes with the wrong faces |
| F2 | `RESULTS.md` (R9) | "no transcript of l2.py is shipped" replaced: transcripts are data/logs/l2.log and l3.log |
| F3 | `README.md` | "six of them" replaced by "16 of them, which fall into six kinds up to its symmetries" |
| F4 | `README.md`, `PRIOR-ART.md`, `CORRECTIONS.md`, `media/CAPTIONS.md`, `RESULTS.md` (R3, R15 credit) | DIS Corollary 1.3 credited (56 is the maximal number of real lines; Y56 unique); new PRIOR-ART row (TAKEN); CORRECTIONS item 6 reworded; the first sentence of every caption now reads "Y56 is the smooth real quartic surface with the most real straight lines possible, 56 (Degtyarev-Itenberg-Sertoz)." (supersedes the caption wording recorded in the `media/CAPTIONS.md` row above) |
| F5 | `RESULTS.md` (R12), `PRIOR-ART.md`, `README.md` | Veniani's count 64 (Table 1, column O_h(S)) credited; README status "EXACT (count also CITED: Veniani Table 1)" |
| F6 | `PRIOR-ART.md`, `README.md` | orbit-split verdict OPEN changed to PARTIAL (DIS proof of Proposition 9.9 singles out our 8-orbit) |
| F7 | `RESULTS.md` (R3), `README.md` | R3 status reworded (Singular Groebner basis, msolve cross-check probabilistic; "no line lies outside that chart (std(I + p01) = 1 in the other five charts)"); credit adds DIS section 9.2 with Theorem 1.1 and Corollary 1.3; README table row reworded |
| F8 | `code/verify_all.py`, `docs/VERIFY-RUN.txt`, `RESULTS.md` (R5) | code route: check 4d now also asserts that the exact determinant of each conic's 3x3 symmetric matrix is nonzero (all 148). One code line added, so the "lines N" citations in RESULTS for checks 4e to 7c moved by one. verify_all.py re-run: 21 of 21 pass; transcript replaced |
| F9 | `README.md`, `docs/CLEANROOM.md` | step 3 now `gap -q grp.g < /dev/null`; "about 90 seconds" changed to "about 1.5 to 2.5 minutes" |
| F10 | `README.md` | "the 636 plane conics (curved slices)" replaced by "all 636 conics (448 of them pairs of crossing lines, 188 genuine curves)"; "All 188 are real." replaced by "All 188 have real points (Degtyarev counted all 636 conics as real; the real points are our exact check)." |
| F11 | `README.md` (loose ends), `docs/EXACT-2.md` | note added: the last section header of `data/planes_exact.txt` ("from the 20 numeric plane-pairs") refers to the superseded numeric list, while its coordinates are the exact ones (equal to orbit representative A in `data/conic_pair_planes_exact.txt`). The data file itself is byte-identical to before |

The "memcap: exit ..." lines in `data/logs/` and `docs/VERIFY-RUN.txt` contain no paths and are left as they are.
