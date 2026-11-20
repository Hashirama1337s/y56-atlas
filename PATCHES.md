# PATCHES

Moki & Julio (AI-assisted) · version 1.0

Every change made to a file on its way into this archive. Sources are in the working folder; paths are relative to it (`../LEAN/...` is the lab Lean project next to it). The working-folder originals are untouched: everything was copied, nothing moved or deleted. "original sha256" is the sha256 of the source file before the change. Files not listed under "Sanitised copies" or "Authored and merged files" are byte-identical copies of their source (see FILELIST.md).

The core folder (`core/`) keeps its own history of the changes made when it was first staged and refereed: `core/PATCHES.md`.

## Sanitised copies

| shipped file | source | original sha256 | change |
|---|---|---|---|
| `checks/core-referee/REFEREE.md` | `referee-v1/REFEREE-V1.md` | `f64835b9c84a224c477fd20946b7902b644a9c1513447bdff138e7c6ae46b485` | lab-process sentence replaced x1; "Lead" -> "Editors'" x1; title: working folder name -> core/ x1; end-line "Written with AI assistance." added |
| `checks/core-referee/ref_checks.py` | `referee-v1/ref_checks.py` | `faf444617db7fdfad1628d6a488edc904eb1bac81c594016c051ff1cc045fa28` | default release root: local path -> ../../core relative to this file x1; import os added x1; referee folder derived from the script location instead of the local release path x1 |
| `checks/core-referee/ref_checks_core.py` | `referee-v1/ref_checks_core.py` | `9b9446a7168f46d592c99557746ff06d8d2a465d465a7e334ff0c34f07faafc8` | default release root: local path -> ../../core relative to this file x1; import os added x1 |
| `checks/core-referee/ref_conics.py` | `referee-v1/ref_conics.py` | `6dcdee636a95716fa2acae782caf643d91a5edc19dcb4e40b899f71c70b5a326` | default release root: local path -> ../../core relative to this file x1; import os added x1; referee folder derived from the script location instead of the local release path x1 |
| `checks/core-referee/ref_extra.py` | `referee-v1/ref_extra.py` | `d2f8dc1df98973cb067737e5d122cbbac4886dcc5299d820756ee2cd6cce7e97` | default release root: local path -> ../../core relative to this file x1; import os added x1; referee folder derived from the script location instead of the local release path x2 |
| `checks/core-referee/ref_extra2.py` | `referee-v1/ref_extra2.py` | `86ca7254108fcfe022abd358f32a53922fe850cebd64352425911f2676e31ef1` | default release root: local path -> ../../core relative to this file x1; import os added x1; referee folder derived from the script location instead of the local release path x2 |
| `checks/core-referee/ref_orbit8.py` | `referee-v1/ref_orbit8.py` | `df0b6120475bf0705d1bc882768cfd85abe44ff79ddf3ab30a08094368e2c3be` | import os added x1; referee folder derived from the script location x1 |
| `checks/pencil-referee/ref_conic.py` | `referee-s3/ref_conic.py` | `3dca3253e79080402e0093dfcbe8bfa8489d0372daa7ba06c72771c10833538a` | local data path -> ../../core/data/ (run from this folder) x1 |
| `checks/pencil-referee/ref_family.py` | `referee-s3/ref_family.py` | `29b4912463353fb7ec7c0a29d8f822d43c35657fbb3acac60d76fcce1b2d42b2` | local data path -> ../../core/data/ (run from this folder) x1 |
| `checks/pencil-referee/ref_sympl.py` | `referee-s3/ref_sympl.py` | `582f62b01e3ad820305453c4b34d418d190aebe056c8ad61302c00d7bbea612d` | local data path -> ../../core/data/ (run from this folder) x1 |
| `checks/pencil-referee/ref_y56.py` | `referee-s3/ref_y56.py` | `c2bf53e5b67f53721a249815d9813f55fbf354cbae7ba95be9fad095fc278724` | local data path -> ../../core/data/ (run from this folder) x1 |
| `checks/pencil-referee/ref_y56b.py` | `referee-s3/ref_y56b.py` | `3cce62e03e5aba253e8a6f14cdc20042097773b5cf68637195e2c3c0bdb622d7` | local data path -> ../../core/data/ (run from this folder) x1 |
| `checks/pencil-referee/run.sh` | `referee-s3/run.sh` | `c93847f4a93ad88ab5e332a46f073bfd9873d7a9cb80859f67d4f5aff9b73f6d` | local working-folder cd -> script folder x1; local Singular path -> $SINGULAR x1 |
| `family/faces/a_aut.py` | `veins/a_aut.py` | `2d3246664e4426d41bb7391945b42e7e03f8ff78e55b18f4f8aede613f174c7b` | local sisters folder -> ../../core/code/sisters x1; local sisters file path -> ../../core/code/sisters/ x1; local working-folder path -> current folder x1 |
| `family/faces/a_aut_gap.log` | `veins/a_aut_gap.log` | `7fafbddb4fab48525a5abeb17c6e0b50bf31ac97dfda0b92d0ef60af23664707` | local GAP install path in the error trace -> <GAP library> x5 |
| `family/faces/a_galois.py` | `veins/a_galois.py` | `4bbb4f5b7b8b9a51f0d59247931cf0c2e92b9a785d7f6e24fc392009f3236bbf` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x1 |
| `family/faces/a_mk.py` | `veins/a_mk.py` | `cdb2775d183edaa5cf3919e3920c3be620d46417839eadc3dee14e4a060f485b` | local sisters folder -> ../../core/code/sisters x1; local sisters file path -> ../../core/code/sisters/ x1; local working-folder path -> current folder x1 |
| `family/faces/b_anal.py` | `veins/b_anal.py` | `fd645b72afd29561fbd527f7c7db9e6c5777917494d83508a95bc9fa957a61cf` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x3 |
| `family/faces/b_assign.py` | `veins/b_assign.py` | `58999b053c14397e6885d45734035509b434d4aa6afdff4717104428298d6781` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x2 |
| `family/faces/b_gen.py` | `veins/b_gen.py` | `922d5519ce83d6aef0fb544121311f2d7728fc42f1c9bf808ed32cba4fd1950a` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x2 |
| `family/faces/b_run.log` | `veins/b_run.log` | `68bc10ef3a70802568b2fd9dd1f8c961e6dfd1cd25732f211e3d7b40cba9f166` | date/time-of-day lines from `date` removed x4 |
| `family/faces/b_run.sh` | `veins/b_run.sh` | `1209fc9ae17f4d96f697193b9f6f81284214617531b1eb7c54ef816febe26b3f` | local msolve path -> $MSOLVE x1; local working-folder cd -> script folder x1 |
| `family/faces/b_run2.log` | `veins/b_run2.log` | `9945606ebea6f93cf8c938a91d7076c9c099b7f65a5a3975f6831b3eff7d18fd` | date/time-of-day lines from `date` removed x8 |
| `family/faces/b_run_sep.log` | `veins/b_run_sep.log` | `bf096dc816a4075765650f001f60f48b338277a2aa620afd34b27fd9d1481e72` | date/time-of-day lines from `date` removed x8 |
| `family/faces/b_sep.py` | `veins/b_sep.py` | `458fe57f068ae8e390fd295cd912897ee5da0361fecab6953bf19563045dab9c` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x3 |
| `family/faces/c_fam.sh` | `veins/c_fam.sh` | `3198de9f970e767be097d517d8b3ac455aa0e9f560c456971f2228347c40aa81` | local working-folder cd -> script folder x1; local Singular path -> $SINGULAR x1 |
| `family/faces/c_family.py` | `veins/c_family.py` | `9ab99dc4d5f4a48fb6f56c1bc15dc1777e3328911fb0e0438341b89eb3fe6280` | local sisters folder -> ../../core/code/sisters x1; local sisters file path -> ../../core/code/sisters/ x1 |
| `family/faces/c_fermat.py` | `veins/c_fermat.py` | `1f028d29aa722bec750a5c47586fdc8bc894e58219b8612668bd7aaf5259032d` | local sisters folder -> ../../core/code/sisters x2; local sisters file path -> ../../core/code/sisters/ x1 |
| `family/faces/c_fermat_det.py` | `veins/c_fermat_det.py` | `1b2179721660b8be7b5fa31772f5984f4ea84107e647ab5a9cb87db3d3d10371` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x2 |
| `family/faces/c_fermat_lines.py` | `veins/c_fermat_lines.py` | `efdc680b1bc45a38a020ea68ee5f5d530a18d6c5df28473f6e61e3d42865ec00` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x1 |
| `family/faces/c_node.sh` | `veins/c_node.sh` | `7151fc0567b9946417960b2119e688b9879fcf7836317c3d0c195e8de5330a23` | local working-folder cd -> script folder x1; local Singular path -> $SINGULAR x1 |
| `family/faces/c_nodes_sister.py` | `veins/c_nodes_sister.py` | `05edf5bf1f3cea1320dc42cbfbfcd7d9fadbab66afa63b219de79cd1775cdced` | local sisters folder -> ../../core/code/sisters x1; local working-folder path -> current folder x3 |
| `family/faces/s5_portraits.py` | `sisters/s5_portraits.py` | `e19673e79a4d32f734606e6af204b98ce59e631008805cd2252f5fc58cd18007` | local sisters folder -> ../../core/code/sisters x1; local output folder -> ../../core/code/sisters/ x1 |
| `family/wall/f2_fermat.py` | `veins2/f2_fermat.py` | `e7d47e871ac85d99117fbc47e8f0dc56983b3ebc77f6bf869173c44943715559` | local sisters folder -> ../../core/code/sisters x1; local sisters file path -> ../../core/code/sisters/ x1 |
| `family/wall/l3_lattice.py` | `veins2/l3_lattice.py` | `188efbf5c4f9cfcb5e59a974b918cb36c46a351d2f8307f07ee1556d2c0a3658` | comment path -> shipped file x1; local source path -> ../../core/code/sisters/s2_lattice.py x1 |
| `family/wall/run_w1.sh` | `veins2/run_w1.sh` | `696d33b4b1b7e4edc3326dc6669e1aaaf6e70e09dbfefc8118ccd0bbea0d47f9` | local working-folder cd -> script folder x1; local Singular path -> $SINGULAR x1 |
| `lean/Y56_L1_neg.expected-error.txt` | `lean/Y56_L1_neg.expected-error.txt` | `f1831a1017985fc181d3576baf3fd613239f991c3a475d607e09c3a88fb6e97e` | local folder prefix removed from error locations x1; memory-cap wrapper line removed |
| `lean/Y56_L2_neg.expected-error.txt` | `lean/Y56_L2_neg.expected-error.txt` | `ebccc521643041d90cd6232f146adcb2be0c010cf46a72f57ee5b8130fdda418` | local folder prefix removed from error locations x10; memory-cap wrapper line removed |
| `lean/Y56_L3_neg.expected-error.txt` | `lean/Y56_L3_neg.expected-error.txt` | `b99a143c4d728ae31a0e6b6a378c5b1baedbe6cd06cab4f07a59606d15dc5956` | local folder prefix removed from error locations x4; memory-cap wrapper line removed |
| `lean/Y56_L5c_neg.expected-error.txt` | `lean/Y56_L5c_neg.expected-error.txt` | `09b3cf444649cd456d7f026f3092d56663cdca1f8c55a543b85956f5876374ac` | local folder prefix removed from error locations x1; memory-cap wrapper line removed |
| `lean/Y56_L6_neg.expected-error.txt` | `lean/Y56_L6_neg.expected-error.txt` | `0aa7d4c44ffe10acd9de4bba514fd2e54684a34c8ccabf091cbf6a3138afec34` | local folder prefix removed from error locations x2; memory-cap wrapper line removed |
| `lean/Y56_L7_neg.expected-error.txt` | `lean/Y56_L7_neg.expected-error.txt` | `92e02eca9055543e0a21cd46aadc543392a5d561363a26c82da007b279707285` | local folder prefix removed from error locations x2; memory-cap wrapper line removed |
| `lean/Y56_L8_neg.expected-error.txt` | `lean/Y56_L8_neg.expected-error.txt` | `a622c25858571dc6390d83c92b0b68524ba6b43a62e9034e56cc29e0131cec43` | local folder prefix removed from error locations x9; memory-cap wrapper line removed |
| `lean/Y56_Pencil_neg.expected-error.txt` | `lean/Y56_Pencil_neg.expected-error.txt` | `d4cbb40a389230d9cc2b6d5f06c64e77980640f2f3f56c39d8802225f747002c` | local folder prefix removed from error locations x1; memory-cap wrapper line removed |
| `lean/export_lean.py` | `lean/export_lean.py` | `792f80406ab9b7637d9bf09e81fd0f20ae7760343423ff9f89bb70d0af1dfd73` | docstring data folder STAGE-V1/data -> core/data x1; data path -> ../core/data x1 |
| `lean/recorded-run.log` | `lean/run_all.log` | `219e6b0ec972d50404d3faffd74fc2c9a782744903e4a933715f31ebf5ca786e` | renamed from run_all.log; local file paths -> file names; lab ledger ids and the lab gate's citation hint removed from the PASS lines; memory-cap wrapper lines removed; theorem lists and axiom printouts unchanged |
| `media/scripts/assemble.py` | `morph/assemble.py` | `3068408013079bc4791edfc7f206b345914368f247ddbabf47461a4ab5d1130b` | local folder -> current folder x1 |
| `media/scripts/render_morph.py` | `morph/render_morph.py` | `599f2fc6ff9dd2ba2065cf51a518dea526e42ad90b53c5bdc98103d194358885` | local output folder -> current folder x1; local input path -> current folder x1 |
| `media/scripts/track.py` | `morph/track.py` | `815b2f703d3f3d4f0ebf4cf6c6bc8d1e7b8b84affa77e1ad611cd2c506859c68` | local sys.path line removed x1; local input path -> current folder x1; local output path -> current folder x1 |
| `pencil/REPORT.md` | `s3-nl/REPORT.md` | `8fcd5b833334e134772b5888cb854a00a3b30134c4fd6f6c6bde4b8165b99c57` | title: lab label removed x1; lab-process sentence replaced by a pointer to the refereed statement x1; "Lead" -> "Editors'" x1; byline added under the title; end-line "Written with AI assistance." added |
| `pencil/RESULT.md` | `s3-nl/RESULT-v2.md` | `e68927758c97331dcaab99e6d211cd31877a36c6e7b722faf230347d12758271` | title: working label "S3 result v2" removed x1; pointer clarified x1; lab-tier wording removed; referee folder -> ../checks/pencil-referee/ x1; gate file -> top-level PRIOR-ART.md x1; "the lead" -> "the editors" x1; working-note pointer -> shipped evidence folder x1; Lean loose end updated to its final status x1; byline added under the title; end-line "Written with AI assistance." added |
| `pencil/a1_firstorder.py` | `s3-nl/a1_firstorder.py` | `6484229d7fd32412fe74a4a94e054d3aa09cb691b1876ebcb6b62a18da89e8a1` | data path ../STAGE-V1/data -> ../core/data x2 |
| `pencil/a2_lattice.py` | `s3-nl/a2_lattice.py` | `69b025a15a2023150255a6780ec1245a109bcd6d97dae83f152ae898d321b822` | data path ../STAGE-V1/data -> ../core/data x1 |
| `pencil/a3_special.py` | `s3-nl/a3_special.py` | `004fc98a3a09b1c7a15f0d1ed6a513eb120a45807d59a609965ca81e1bc00736` | data path ../STAGE-V1/data -> ../core/data x3 |
| `pencil/fano_s0.sing` | `s3-nl/fano_s0.sing` | `ca81e9979764406f47b6a4c9cccdd402266814d2d13e648b88ae70e4a3d0fe74` | comment pointer to the working folder -> shipped file x1 |
| `pencil/fano_s13o5.sing` | `s3-nl/fano_s13o5.sing` | `3a1dd7cca2b2e6b7ffd616be7c74e748bf1db245df9e79a0adf43e91e7d9cc10` | comment pointer to the working folder -> shipped file x1 |
| `pencil/fano_s5o2.sing` | `s3-nl/fano_s5o2.sing` | `1fbd69b91350e12589b0bd8c3bd38d78c8c4cade878e9bcace10aba90f241df2` | comment pointer to the working folder -> shipped file x1 |
| `pencil/overlattice/OVERLATTICE.md` | `s3-nl/overlattice/OVERLATTICE.md` | `b919c5dcc6d6fc6dc798608d01067e97e5049880fa8b37485a6245cb0f8d464d` | first-person wording neutralised x1; file reference RESULT-v2 -> RESULT.md x3; byline added under the title; end-line "Written with AI assistance." added |
| `pencil/overlattice/ov.py` | `s3-nl/overlattice/ov.py` | `21c3bc8a933a9dda90cef94fe0b8d2d4ce90e6b8f36aaff71777090f1aa41ce6` | data path -> ../../core/data x1 |
| `pencil/run.sh` | `s3-nl/run.sh` | `fd08351bfaf43fff777a5b840ae9e0537ae60e81d31efa986c9dadbf8fef2a69` | local working-folder cd -> script folder x1; local Singular path -> $SINGULAR x1 |
| `pencil/sd16/mk.py` | `s3-nl/sd16/mk.py` | `8ff162d28462ece9753632002d3c530516ea1de256e25cd5663acbe87c49e934` | local data path -> ../../core/data x1; local output path -> cwd x1 |
| `pencil/sd16/run.sh` | `s3-nl/sd16/run.sh` | `6b55be7f96d091a15c14cfde2f56fba7c1cc16cead1563e4bbb449668fbf4423` | local tool folder removed from PATH x1; local working-folder cd -> script folder x1; local GAP path -> $GAP x1 |
| `viewer/BUILD-NOTES.md` | `atlas-viewer/BUILD-NOTES.md` | `77e0600c59a4a9d6ea2a532c156753008a0225deebff97b9564e97697b19bf6a` | working status note removed x1; data folder STAGE-V1 -> core x1; working-folder pointer -> shipped file x1; pointer to shipped file x1; orbit name C -> S (editor gap 4) x1; orbit name C -> S (editor gap 4) x1; g12 caption status (editor gap 5) x1; oval status reworded to "EXACT separation, NUMERICAL placement" (editor gap 5) x1; end-line "Written with AI assistance." added |
| `viewer/build/build_data.py` | `atlas-viewer/build/build_data.py` | `3ae827c8628c31dba1cd68c3d6cae1cefac85496719c7fc9fd67ab6a7f906086` | docstring data folder x1; comment pointer x1 |
| `viewer/build/common.py` | `atlas-viewer/build/common.py` | `47633fd8bd0d10fc0505a3b4eada64c8e4740bc6483b6abf12b14cd6a8c32817` | data path -> ../../core/data x1 |
| `viewer/build/verify_report.json` | `atlas-viewer/build/verify_report.json` | `feaa23533094f1bc25f1403288e60fc91d761b1e15f0adac2ba6a38e65e293d6` | check label orbit C -> S (editor gap 4); results unchanged x1 |
| `viewer/build/verify_viewer.py` | `atlas-viewer/build/verify_viewer.py` | `095ef6a41c60284c54e6e38c3deb88a3c55fed0df0cc4efe6d055e91d0fb7cd5` | privacy-scan pattern shortened to path patterns (the shipped copy no longer lists the working-folder and name strings it scanned for) x1; orbit name C -> S (editor gap 4) x1; path-name literal written as a character class so the shipped text does not itself trip path scanners (same regex) x1 |
| `viewer/index.html` | `atlas-viewer/index.html` | `ef05b522cd724af052b71f66fb1cd1fae747f2b5631237be85820e0e80e11563` | orbit name C -> S (editor gap 4) x1; orbit chip C -> S (editor gap 4) x1; g12 caption: status "EXACT separation, NUMERICAL placement" (editor gap 5) x1 |
| `PAPER.md` | `atlas/PAPER.md` | `3b63e98ad181ac7ae90fa3d6baafed921fdb3dab1353a0fe1554b820f2e84f5e` | byline "draft" -> "version 1.0"; status label LEAN-CHECKED added; editor gap 1: Segre sentence now cites DIS (introduction, Corollary 1.2); editor gap 2: SD16 named from our own GAP IdGroup run (pencil/sd16/) in Theorem 5.1 item 6 and Theorem 7.1 item 2; editor gap 4: the 16-line orbit renamed S, orbits A (of L01) and B (of L03) defined in Theorem 5.1 item 3; editor gap 5: Figure 6 caption and the ovals paragraph carry "EXACT separation, NUMERICAL placement" with an evidence pointer; editor gap 8: Appendix A orbit column computed exactly (8 / S / A / B) from core/data/symmetry_exact.txt by a script, rows re-checked against core/data/lines_exact.txt (0 mismatches); Section 8 written from lean/LEAN-REPORT.md (setup, Table 8.1, axioms, controls, what is not formalised); LEAN-CHECKED pointers with theorem names in Sections 2 to 5 and 7.3; "Lean formalisation is being prepared" replaced by the checked statement; item 8 ("a machine-checked core") added to "What this paper adds"; evidence pointers to family/ added in Sections 5, 6, 7.4 to 7.6; figure paths media/ -> core/media/ and morph/ -> media/; Section 9: verify_all run from core/, pencil, family and Lean bullets added; open questions 1 and 12 updated (Lean lower bound only; line orbits now tabulated); pointer from the corrections section to CORRECTIONS.md; "at our gate(s)" -> "in our prior-art search(es)"; Lean added to the software list |
| `lean/LEAN-REPORT.md` | `lean/LEAN-REPORT.md` | `eb93cbd3ab3cfb8ed0c32473ac3ae92dfc0e98644a0bf28357435be10afde5b6` | lab gate tool and memory-cap wrapper named generically; ledger-row column and the probe-file line removed; "s3-nl finding 3" -> "../pencil/REPORT.md, finding 3"; Files section rewritten for the shipped folder (local folder path removed; run_all.sh and recorded-run.log; the development script is not shipped); loose end on the expected-error files updated (paths now removed); "second seat" and "gate" wording -> "second reader" / "the checking script"; "passes the gate" -> "passes the check"; byline added under the title; end-line "Written with AI assistance." added |
| `lean/lake-manifest.json` | `../LEAN/k3lean/lake-manifest.json` | `37a4ac880668fcfb618659102df9df4aab1afc51a77aa933cfeca72ce270bfa8` | package name k3lean -> y56lean (the pinned dependency revisions are unchanged) |

## Authored and merged files

| shipped file | sources (original sha256) | what |
|---|---|---|
| `README.md` | `STAGE-V1/README.md` (`26fe114bd922a89403fe0b29f627ac489e6921b8f3870e19fe0cffde6def353a`) | new front page (story-ladder); folds the core README (STAGE-V1/README.md) with the pencil, Lean, viewer and family layers |
| `RESULTS.md` | `STAGE-V1/RESULTS.md` (`22dd1145f198f040e8c17412bd1c11c81f0d76239d10f89ca741d713d07891d6`); `s3-nl/RESULT-v2.md` (`e68927758c97331dcaab99e6d211cd31877a36c6e7b722faf230347d12758271`) | new; the core section (R1 to R19 and the 21 checks) is carried from STAGE-V1/RESULTS.md with paths prefixed core/ and R12/R19 updated; scorecard with Lean column, P1 to P9 from s3-nl/RESULT-v2.md, P10 (NS = N19, s3-nl/overlattice/OVERLATTICE.md) and P11 (SD16, s3-nl/sd16/sd16.out) added |
| `PRIOR-ART.md` | `STAGE-V1/PRIOR-ART.md` (`2811ad69e1f809e701ad8336e22749178e1ab37c4173ceca4db8e86d555d76ea`); `gate/PRIOR-ART-Y56.md` (`588e7f9ed16f6ba4a2fb3db4b0e0348a129d006985490173e04bffa87b02d12c`); `gate/PRIOR-ART-Y56-2.md` (`cdbfe7ba46983573cfc659b105c4c80eb59e2fe44bc96de0f10416599db53edf`); `gate/PRIOR-ART-S3.md` (`a5da7875d2fca4d3e27ff7cd6fad8d0cd57aadbce0109870f20114ee7e18daa6`) | new; merges STAGE-V1/PRIOR-ART.md, gate/PRIOR-ART-Y56.md, gate/PRIOR-ART-Y56-2.md and gate/PRIOR-ART-S3.md into verdict tables with locators, credit lines, search floors and dates; quotations replaced by locators; lab tool names, query-log paths and ledger lines removed |
| `CORRECTIONS.md` | `STAGE-V1/CORRECTIONS.md` (`16e76b84e2792f74351534c1d7a84bc0eaae549fb1dc00458db00f532e390c41`); `atlas/PAPER.md` (`3b63e98ad181ac7ae90fa3d6baafed921fdb3dab1353a0fe1554b820f2e84f5e`) | new; merges STAGE-V1/CORRECTIONS.md (items 1 to 7) with the paper corrections of atlas/PAPER.md (7 folded into 7, 8, 9) and adds items 10 to 12 from the final editing pass |
| `CITATION.cff` | `STAGE-V1/CITATION.cff` (`9d389a2823e637113c2d3f8ba3a4c362d627b8218b98b36e0674d510179ba059`) | new (title as specified, version 1.0, no DOI) |
| `LICENSE` | `STAGE-V1/LICENSE` (`9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411`) | copied unchanged from STAGE-V1/LICENSE (CC BY 4.0 text) |
| `LICENSE-CODE` | `STAGE-V1/LICENSE-CODE` (`9c5776de5bc7f9160808b81dc71ba6657d3118378bfe677f1484c5f18f8d51a3`) | new; MIT text as in STAGE-V1/LICENSE-CODE, scope extended to code, scripts, program inputs, lean/ and viewer/ |
| `PATCHES.md` | none | this file |
| `FILELIST.md` | none | new |
| `MANIFEST.sha256` | none | new (sha256 of every other file) |
| `core/README.md` | none | new short guide to the core folder (commands from STAGE-V1/README.md) |
| `pencil/README.md` | none | new index of the pencil files |
| `checks/README.md` | none | new: what each referee script re-derives |
| `family/README.md` | `veins/VEINS.md` (`f6c86cc734f86d1b0bddaf886bb24d86a7c98a3a2343ac6ad27d54f7e660084b`); `veins/VEINS-2.md` (`0d5f53582cc91d1eb5345329342d5b73f0fe35014e87ef9b93deb96ff9c99bfe`) | new: fact-to-file map for the faces, the wall and the Fermat end (replaces the working notes veins/VEINS.md and VEINS-2.md) |
| `media/CAPTIONS.md` | `MEDIA.md` (`d0f6bdea2d5e92205000e29f6afed7c2a873ab6bd514950018b59829ee459d7c`) | new passer-by captions for the pencil pictures (from the working media sheet MEDIA.md, reworded) |
| `lean/README.md` | `lean/LEAN-REPORT.md` (`eb93cbd3ab3cfb8ed0c32473ac3ae92dfc0e98644a0bf28357435be10afde5b6`) | new: build, theorems in plain words, axioms, controls, loose ends |
| `lean/lakefile.toml` | `../LEAN/k3lean/lakefile.toml` (`f070922fe2ccef83d2de1e8e2c54e62db1b38820ad71f635ce4046685cc2ddea`) | new; options and Mathlib pin as in the lab Lean project (../LEAN/k3lean/lakefile.toml), no library target |
| `lean/run_all.sh` | `lean/run_all.sh` (`0cedede2b94dc72e8f954e28660f605b39423bb19816acbeb314ac3ef349acf7`) | new; replaces lean/run_all.sh of the working folder (which called the lab gate): standard lake commands, axiom printout, keyword rejection, negative controls |

Copied unchanged from outside the Y56 working folder: `lean/lean-toolchain` from `../LEAN/k3lean/lean-toolchain` (`11c697aebe5b539d74f5069e497a588e7dfab1c4eeb74313f28357e351c55ca3`).

## Editor gaps applied (atlas/EDITOR-GAPS.md)

Items 1, 2, 4, 5, 7 and 8 were applied in this archive (item 3 needed no change; item 6, the Lean section, was filled from the Lean report). Each item is marked "[RESOLVED: how]" in the working copy of EDITOR-GAPS.md, which is not shipped.

## Final referee fixes (checks/atlas-referee/REFEREE-ATLAS.md)

Applied after the last release round; no data file, number, Lean file or script of the core changed. The letters are the referee's (B = blocking, N and L = non-blocking); the referee's exact texts were used, with grammar adapted where a sentence needed it. "previous sha256" is the manifest hash before the fix (the file is also edited by this release for the other items listed). The same wrong statements were searched for in every text file of the archive; the extra places that needed the same change are included in the rows below.

| edited file | previous sha256 | change |
|---|---|---|
| `PAPER.md` | `6574432b4b21bfd4f9c47cd8675ae38f110bf2cd890c938abec042bfa6fd25f8` | B1 (line shape z2 = beta(z0 - z3); the z3^4 coefficient vanishes, the other four generate the ideal of the three equations); B2 (Aut(line graph) = Aut(Y56) union tau Aut(Y56), index 2, extension splits); B3 (finite index needs rank exactly 19; "supersedes" -> "builds on"); B4 (Fermat quartic: disguised copy, over C); B5 (same 32 symmetries act; intro "equally symmetric"); N1 (one setting on the real dial; the wall on the positive dial, s^4 = 16 over C; abstract "only one setting on the real dial"); N4 (Theorem 7.1(1): 8 nodes exactly at s = +-2); L1 (L2 printouts compared by script; statement match by a referee); L2 (L8 row: cited rho <= 20 and L^2 = -2); L3 (Pencil row and item 7 / Section 8: algebra after substitution) |
| `README.md` | `5cf6e1469dc7e8423b6f6a55d990b93372bfb58668d00c9f93667c89a7bfdcdc` | B4; B5; N1 (headline and plain words); N2 (explanation "not found after a quick search"; "general mechanism is Bouyer's"); N3 (Fermat lattice numbers are in pencil/a4_checks.log part (d)); L1; L2 (scorecard: Gram matrix of the 56 lines, rank 20, 20 x 20 block of determinant -64); L3 ("the algebra after substitution") |
| `RESULTS.md` | `c41dea064a77dbcbf7c82f0fe012f0bd574c48607fc25e0ec19345f1c61f877e` | B3 (P6 "used by P10"); N4 (P1 table row and body); L3 (P7 table row and body: "the algebra after substitution") |
| `CITATION.cff` | `26e03502603eaa4e0486036ede13f6625862ede4130b3e657a09ecf6a69823a8` | B4 (a member projectively equivalent over C to the Fermat quartic, and an 8-nodal wall) |
| `PRIOR-ART.md` | `1a3e82261faba27964de82cb7ccb6e5fc4474cb1ec1e922e8c000671d79b735d` | N2 ("the explanation not found after a quick search") |
| `pencil/REPORT.md` | `ea77f01b2d3b0610d61b2040f58505cc5a076744137338bb94877aea08fe3572` | B1 (line shape z2 = beta(z0 - z3), with the z3^4 coefficient vanishing identically); N1 (plain words: "only one dial setting on the real dial") |
| `pencil/RESULT.md` | `a307752d918a68337c35ab25ff2ba6a2c380040aebf8e0d29f75b888546ca5b4` | B3 (loose end 1: "two routes, both using item 6's rank-19 argument"); N4 (8 nodes at s = +-2; count at s = +-2i not computed exactly) |
| `lean/README.md` | `76a2974653abdb03a544a47e93746f75ab565979b456da3b44390b76eab46816` | L1 (L2 printouts compared by script; statement match by a referee); L2 (L8 row: given rho <= 20 and L^2 = -2, cited); L3 (Pencil row: the three equations of Section 7.3; substitution not in Lean) |
| `lean/LEAN-REPORT.md` | `700979d63b65d6c987f32f245ab632207a15116fb04258662895ac208dc6547a` | L1 (same two replacements as lean/README.md) |
| `viewer/index.html` | `23052db8390d6d4b727559665c44e3630963c57b1e1e5fe88d18d670ef6a3be1` | N5 (message text: "plane z1 = 0 or z2 = 0"; text only, no code change) |
| `viewer/BUILD-NOTES.md` | `4bfb6e9ac42ce933e8a93d18888f2309e7f4334a415bedc14b4b4800b56000e4` | N5 ("8 anchor lines in z1 = 0 or z2 = 0") |

Not changed on purpose: comments in `viewer/core.js` and `viewer/build/build_data.py` that still write the anchor-line plane as "y1 = 0 or y2 = 0" (code files; the viewer's own coordinates are called y there, the visible message and notes are fixed); `lean/Y56_Pencil.lean` (its header says "three coefficient equations"; Lean files are not edited after the kernel check, and Section 7.3 and the Lean table row now say what the theorem covers).

Working copies outside the archive (`s3-nl/REPORT.md`, `s3-nl/RESULT-v2.md`) were not edited in their bodies; a dated correction note was appended to each.

### New: `checks/atlas-referee/`

Copied from the referee's folder; sanitised as below. `ref_shape.out` was regenerated from this layout (see `checks/README.md`); the other `.out` files and `verify_all_rerun.txt` are byte for byte as recorded by the referee.

| shipped file | source | original sha256 | change |
|---|---|---|---|
| `checks/atlas-referee/REFEREE-ATLAS.md` | `referee-atlas/REFEREE-ATLAS.md` | `11d8cacaed6fde42f8271da21ca420411137a89d33dd120aa5cb29a56fcb0895` | local working-folder path of the referee's scripts -> this folder; local path of the extracted papers -> "text extracted from the downloaded papers; not shipped"; "referee-atlas/" -> "checks/atlas-referee/" in the quoted fix texts; the quoted 12-character fragment of a base64 data run (a spurious privacy-scan hit) removed |
| `checks/atlas-referee/ref_l5normals.py` | `referee-atlas/ref_l5normals.py` | `1121a4f0e6ae3f60d70aeec9f4bd9b30151db47beb84cb3bd667e7147e7cbbd1` | local archive path -> folder of the script ../../lean/ |
| `checks/atlas-referee/ref_tau.py` | `referee-atlas/ref_tau.py` | `0defbd9da8a00a0b126884d1bdd856689917458de03e9a73c291870bc1f0e2d0` | local archive path -> ../../core/data/lines_exact.txt relative to the script; `import os` added |
| `checks/atlas-referee/ref_lean_data.py` | `referee-atlas/ref_lean_data.py` | `7ea6f66dff2fddc246eb651aa32cfd977dd35d63be36caa110a685f6a80616ce` | archive folder argument now optional (default ../..); usage line in the docstring without local paths |
| `checks/atlas-referee/ref_shape.py` | `referee-atlas/ref_shape.py` | `ebfcc41a831c9c0edc11a0b76bc6b5e357b2ca8446052efd71a5b5a1fbec4be7` | added a last check: the corrected shape at the paper's converse point; output regenerated (`ref_shape.out`), the first run's traceback line of the original output is gone |
| `checks/atlas-referee/ref_shape.out` | `referee-atlas/ref_shape.out` | `314511448579414b5fe312755c58e285ad59ce25519c0eb90f062be9d4acf56e` | regenerated, run from this layout with `py -3.11 memcap.py 4 py -3.11 ref_shape.py` |
| `checks/atlas-referee/ref_l5normals.out` | `referee-atlas/ref_l5normals.out` | `7dd04c7281c8828b2a54bb1fad7b5669020212430d3a286657c8a86225820b4f` | none (byte-identical copy) |
| `checks/atlas-referee/ref_lean_data.out` | `referee-atlas/ref_lean_data.out` | `7c9448945adfa3bdb65fb16981819603c47dbc6ec190f6c4bd579172ed055d4c` | none (byte-identical copy) |
| `checks/atlas-referee/ref_tau.out` | `referee-atlas/ref_tau.out` | `6fa13deb2ab572111e113c14ddd23100d472a01aa9f29f0b1c336a25514f176b` | none (byte-identical copy) |
| `checks/atlas-referee/ref_wall2i.out` | `referee-atlas/ref_wall2i.out` | `fdf6ae6ca29bdb1b0e288c0400a0844f236f263f9d9d02404bdae13d026662bd` | none (byte-identical copy) |
| `checks/atlas-referee/ref_wall2i.py` | `referee-atlas/ref_wall2i.py` | `bfc55ab45a1137f729339c1e69e891103f02d697e763d9bf848cc6e9ae0e7442` | none (byte-identical copy) |
| `checks/atlas-referee/verify_all_rerun.txt` | `referee-atlas/verify_all_rerun.txt` | `c19321b8fc3d0639be8657f3fe06f46a97b05aa27b458b130a3c1ea86dee0985` | none (byte-identical copy) |

## Not shipped

| source | reason |
|---|---|
| `STAGE-V1/CITATION.cff` | superseded by the top-level CITATION.cff |
| `STAGE-V1/CORRECTIONS.md` | folded into the top-level CORRECTIONS.md |
| `STAGE-V1/FILELIST.md` | superseded by the top-level FILELIST.md |
| `STAGE-V1/LICENSE` | superseded by the top-level LICENSE |
| `STAGE-V1/LICENSE-CODE` | superseded by the top-level LICENSE-CODE |
| `STAGE-V1/MANIFEST.sha256` | superseded by the top-level MANIFEST.sha256 |
| `STAGE-V1/MANIFEST.txt` | superseded by the top-level MANIFEST.sha256 |
| `STAGE-V1/PRIOR-ART.md` | folded into the top-level PRIOR-ART.md |
| `STAGE-V1/README.md` | folded into the top-level README.md |
| `STAGE-V1/RESULTS.md` | folded into the top-level RESULTS.md |
| `atlas/EDITOR-GAPS.md` | editor checklist; stays in the working folder with each item marked [RESOLVED: how] |
| `atlas/PAPER-NUMBERS.md` | number-to-source table for the number check; stays in the working folder (paths there are working-folder paths) |
| `gate/` | prior-art working files: query logs, downloaded papers (src/, src2/, src3/), page renders; merged into PRIOR-ART.md; downloaded papers are never shipped |
| `lean/Probe.lean` | setup probe only, not a result |
| `lean/dev_check.sh` | development compile loop tied to the local Lean install; replaced by the shipped run_all.sh |
| `lean/run_all.sh` | runner tied to the local lab gate; replaced by a new run_all.sh (standard lake commands) |
| `morph/frames/` | 48 rendered frames (15 MB); regenerated by render_morph.py and packed into the GIF by assemble.py |
| `morph/t1.py` | spot probe of the numerical line search, not used for the pictures |
| `referee-s3/r1_s1.sing` | Singular input that was never run (no log) |
| `referee-s3/r1_s2i.sing` | Singular input that was never run (no log) |
| `referee-s3/ref_dbg.py` | one-off helper (source patch / debug re-exec); not part of the evidence |
| `referee-s3/ref_patch_once.py` | one-off helper (source patch / debug re-exec); not part of the evidence |
| `s3-nl/_patch.py` | one-off editing helper (patched a4_checks.py before its run); not part of the evidence |
| 8 files: `s3-nl/fano_gen.sing`, `s3-nl/fano_s1.sing`, `s3-nl/fano_s2.sing`, `s3-nl/fano_s3.sing`, `s3-nl/fano_s7.sing`, `s3-nl/fano_s9o4.sing`, `s3-nl/fano_tpl.sing`, `s3-nl/fano_y56.sing` | Singular input that was never run (no log); superseded by the graph_*.sing chart computations |
| `s3-nl/overlattice/chk.py` | one-off helper (text fix of OVERLATTICE.md / module availability probe) |
| `s3-nl/overlattice/fix.py` | one-off helper (text fix of OVERLATTICE.md / module availability probe) |
| `veins/VEINS-2.md` | working notes; the facts the paper uses are mapped to scripts and logs in family/README.md |
| `veins/VEINS.md` | working notes; the facts the paper uses are mapped to scripts and logs in family/README.md |
| 7 files: `veins/a_aut.pkl`, `veins/a_listed.pkl`, `veins/b_anal_g01_g02_g24_g00.pkl`, `veins/b_anal_g12_g13.pkl`, `veins/b_gen_g01_g02_g24_g00.pkl`, `veins/b_gen_g12_g13.pkl`, `veins/b_sep_g12_g13.pkl` | intermediate pickle, regenerated by the scripts that write it |
| 138 files: `veins/c_00_24_m0_r0.ms`, `veins/c_00_24_m0_r0.out`, `veins/c_00_24_m0_r1.ms`, `veins/c_00_24_m0_r1.out`, `veins/c_00_24_m0_r2.ms`, `veins/c_00_24_m0_r2.out`, `veins/c_00_24_m1_r0.ms`, `veins/c_00_24_m1_r0.out`, `veins/c_00_24_m1_r1.ms`, `veins/c_00_24_m1_r1.out`, `veins/c_00_24_m1_r2.ms`, `veins/c_00_24_m1_r2.out`, `veins/c_00_24_p0_r0.ms`, `veins/c_00_24_p0_r0.out`, `veins/c_00_24_p0_r1.ms`, `veins/c_00_24_p0_r1.out`, `veins/c_00_24_p0_r2.ms`, `veins/c_00_24_p0_r2.out`, `veins/c_00_24_p1_r0.ms`, `veins/c_00_24_p1_r0.out`, `veins/c_00_24_p1_r1.ms`, `veins/c_00_24_p1_r1.out`, `veins/c_00_24_p1_r2.ms`, `veins/c_00_24_p1_r2.out`, `veins/c_01_01_m0_r1.ms`, `veins/c_01_01_m0_r1.out`, `veins/c_01_01_m0_r2.ms`, `veins/c_01_01_m0_r2.out`, `veins/c_01_01_p0_r1.ms`, `veins/c_01_01_p0_r1.out`, `veins/c_01_01_p0_r2.ms`, `veins/c_01_01_p0_r2.out`, `veins/c_01_02_m0_r0.ms`, `veins/c_01_02_m0_r0.out`, `veins/c_01_02_m0_r1.ms`, `veins/c_01_02_m0_r1.out`, `veins/c_01_02_m0_r2.ms`, `veins/c_01_02_m0_r2.out`, `veins/c_01_02_m1_r0.ms`, `veins/c_01_02_m1_r0.out`, `veins/c_01_02_m1_r1.ms`, `veins/c_01_02_m1_r1.out`, `veins/c_01_02_m1_r2.ms`, `veins/c_01_02_m1_r2.out`, `veins/c_01_02_p0_r0.ms`, `veins/c_01_02_p0_r0.out`, `veins/c_01_02_p0_r1.ms`, `veins/c_01_02_p0_r1.out`, `veins/c_01_02_p0_r2.ms`, `veins/c_01_02_p0_r2.out`, `veins/c_01_02_p1_r0.ms`, `veins/c_01_02_p1_r0.out`, `veins/c_01_02_p1_r1.ms`, `veins/c_01_02_p1_r1.out`, `veins/c_01_02_p1_r2.ms`, `veins/c_01_02_p1_r2.out`, `veins/c_01_24_m0_r0.ms`, `veins/c_01_24_m0_r0.out`, `veins/c_01_24_m0_r1.ms`, `veins/c_01_24_m0_r1.out`, `veins/c_01_24_m0_r2.ms`, `veins/c_01_24_m0_r2.out`, `veins/c_01_24_m1_r0.ms`, `veins/c_01_24_m1_r0.out`, `veins/c_01_24_m1_r1.ms`, `veins/c_01_24_m1_r1.out`, `veins/c_01_24_m1_r2.ms`, `veins/c_01_24_m1_r2.out`, `veins/c_01_24_p0_r0.ms`, `veins/c_01_24_p0_r0.out`, `veins/c_01_24_p0_r1.ms`, `veins/c_01_24_p0_r1.out`, `veins/c_01_24_p0_r2.ms`, `veins/c_01_24_p0_r2.out`, `veins/c_01_24_p1_r0.ms`, `veins/c_01_24_p1_r0.out`, `veins/c_01_24_p1_r1.ms`, `veins/c_01_24_p1_r1.out`, `veins/c_01_24_p1_r2.ms`, `veins/c_01_24_p1_r2.out`, `veins/c_02_24_m0_r0.ms`, `veins/c_02_24_m0_r0.out`, `veins/c_02_24_m0_r1.ms`, `veins/c_02_24_m0_r1.out`, `veins/c_02_24_m0_r2.ms`, `veins/c_02_24_m0_r2.out`, `veins/c_02_24_m1_r0.ms`, `veins/c_02_24_m1_r0.out`, `veins/c_02_24_m1_r1.ms`, `veins/c_02_24_m1_r1.out`, `veins/c_02_24_m1_r2.ms`, `veins/c_02_24_m1_r2.out`, `veins/c_02_24_p0_r0.ms`, `veins/c_02_24_p0_r0.out`, `veins/c_02_24_p0_r1.ms`, `veins/c_02_24_p0_r1.out`, `veins/c_02_24_p0_r2.ms`, `veins/c_02_24_p0_r2.out`, `veins/c_02_24_p1_r0.ms`, `veins/c_02_24_p1_r0.out`, `veins/c_02_24_p1_r1.ms`, `veins/c_02_24_p1_r1.out`, `veins/c_02_24_p1_r2.ms`, `veins/c_02_24_p1_r2.out`, `veins/c_12_13_m0_r0.ms`, `veins/c_12_13_m0_r0.out`, `veins/c_12_13_m0_r1.ms`, `veins/c_12_13_m0_r1.out`, `veins/c_12_13_m0_r2.ms`, `veins/c_12_13_m0_r2.out`, `veins/c_12_13_m1_r0.ms`, `veins/c_12_13_m1_r0.out`, `veins/c_12_13_m1_r1.ms`, `veins/c_12_13_m1_r1.out`, `veins/c_12_13_m1_r2.ms`, `veins/c_12_13_m1_r2.out`, `veins/c_12_13_p0_r0.ms`, `veins/c_12_13_p0_r0.out`, `veins/c_12_13_p0_r1.ms`, `veins/c_12_13_p0_r1.out`, `veins/c_12_13_p0_r2.ms`, `veins/c_12_13_p0_r2.out`, `veins/c_12_13_p1_r0.ms`, `veins/c_12_13_p1_r0.out`, `veins/c_12_13_p1_r1.ms`, `veins/c_12_13_p1_r1.out`, `veins/c_12_13_p1_r2.ms`, `veins/c_12_13_p1_r2.out`, `veins/c_count.py`, `veins/c_count1.log`, `veins/c_gen1.log`, `veins/c_jobs1.json`, `veins/c_path.py`, `veins/c_run.sh`, `veins/c_run1.log`, `veins/c_t01_02_p.ms`, `veins/c_t01_02_p.out`, `veins/c_tags1.txt` | straight-line path search between real faces (not used by the paper: not diagnostic either way) |
| `veins2/dk_p29.png` | render of a page of a published survey (third-party page; cited instead) |
| 7 files: `veins2/scout_k.py`, `veins2/scout_k2.py`, `veins2/scout_k3.py`, `veins2/scout_k4.py`, `veins2/scout_k5.py`, `veins2/scout_t2.py`, `veins2/scout_t3.py` | scratch script that read a downloaded paper (paper not shipped) |
| `veins2/w2.log` | first attempt at the wall lines (primary decomposition) that timed out; superseded by w3 |
| `veins2/w2.sing` | first attempt at the wall lines (primary decomposition) that timed out; superseded by w3 |

Also not shipped from the working folder: everything not named in FILELIST.md (earlier renders, numeric intermediates and pickles, working notes, the clean-room and staging tool folders). The atlas paper draft `atlas/PAPER.md` is shipped only in its edited form, `PAPER.md`.

Written with AI assistance.
