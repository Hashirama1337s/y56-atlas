# Clean-room reproduction, Y56 release v1

Fresh copy of `code/`, `data/`, `requirements.txt` from this release, run with documented commands only. Of the raw outputs, only the l2 and l3 transcripts are shipped (`data/logs/l2.log`, `data/logs/l3.log`); the others were compared with the shipped files and matched as listed below.

## Environment
- Windows 11, Python 3.11.9: sympy 1.14.0, mpmath 1.3.0, networkx 3.6.1, numpy 2.4.4, scipy 1.17.1, scikit-image 0.26.0, python-flint 0.9.0 (all match requirements.txt)
- WSL2 Ubuntu 24.04.4, system Python 3.12.3, 15 GB RAM, 12 cores
- passagemath-singular / -msolve / -gap / -pari 10.8.14 (pip wheels); Singular system version code 44105 (4.4.1), msolve 0.10.1, GAP + SmallGroups data from passagemath-gap 10.8.14, PARI via cypari2
- Windows Python jobs under a memory cap (8 GB). WSL jobs under `ulimit -v`.

## Commands (relative to the release root)
```
# 1. all-in-one verification (Windows or any Python 3.11)
python code/verify_all.py

# 2. lattice completeness (needs cypari2 / passagemath-pari; run from code/exact2)
cd code/exact2 && python l2.py && python l3.py

# 3. symmetry group (GAP)
cd code/exact2 && gap -q grp.g < /dev/null

# 4. Fano scheme of lines and smoothness (Singular, about 4-5 min for fano)
cd code/exact3 && Singular -q fano.sing && Singular -q smooth.sing

# 5. independent msolve count (set MSOLVE to the msolve binary)
cd code/exact3_v2 && MSOLVE=<path to the msolve binary> bash run_ms.sh && MSOLVE=<path to the msolve binary> bash run_real.sh && python analyze.py

# 6. sisters (run from code/sisters, in this order; s4 takes a mesh size)
cd code/sisters && python s1_group.py && python s2_lattice.py && python s3_conics.py && python s4_mesh.py 160 && python s4_mesh.py 260
```
Note for item 2: PARI's parallel `qfminim` needs a large virtual address space. Under `ulimit -v 8000000` and under 24 GB it fails or hangs (details below). Run it with no virtual-memory cap, or at least 64 GB virtual. The real memory use is small (about 0.2 GB resident).

## Results

| run | command | expected | got | match |
|---|---|---|---|---|
| 1 | verify_all.py (memcap 8) | 21/21 PASS (docs/VERIFY-RUN.txt) | exit 0, 21 PASS, 0 FAIL, 95 s; transcript identical to the shipped one except per-check seconds | yes |
| 2a | l2.py | 636 classes (c.h=2, c^2=-2) = 448 line sums + 188 irreducible; 20 conic-pair planes; lattice rank 20 | 636, 448, 188, 20, 56 distinct line classes; qfsign [20,0] | yes (needs no VM cap, see note) |
| 2b | l3.py | disc group order 64, 3 isotropic classes, 4828 extra classes (docs/EXACT-2.md) | 64, 3, 4828 | yes |
| 3 | grp.g (GAP) | data/gap_out.txt, SmallGroup(32,43) | `cmp` byte-identical, IdGroup [32,43] | yes, identical |
| 4a | fano.sing | data/logs/fano_rerun.out: dim 0, vdim 56, 5 other charts std = 1, 0 of 56 lines failing | `cmp` byte-identical (sha256 a2549df7...183b), exit 0, 260 s | yes, identical |
| 4b | smooth.sing | data/logs/smooth.out: vdim 81, z_i^9 in J, reduce(F,G)=0 | diff empty, exit 0 | yes, identical |
| 5a | run_ms.sh | gb_01.out, par_01.out; 5 other charts "1 element" | gb_01.out (sha256 4e306e3a...) and par_01.out (f96703e1...) byte-identical to data/logs; 5 other charts give the unit ideal; exit 0, 18 s | yes, identical |
| 5b | run_real.sh | real_01.out | byte-identical (bb89f122...); exit 0, 7 s | yes, identical |
| 5c | analyze.py | analyze.log: 112 real boxes, 56 with s>0 and 56 with s<0, 0 overlaps, 85 GB elements, vdim 112 | diff empty (after the memcap line) | yes (but see finding 2) |
| 6a | s1_group.py | s1_group.log | identical except the `time` line (34.2 s vs 31.8 s) | yes |
| 6b | s2_lattice.py | s2_lattice.log | identical, 2 s | yes |
| 6c | s3_conics.py | s3_conics.log | identical except the `time` line (3.6 s vs 2.9 s) | yes |
| 6d | s4_mesh.py 160 and 260 | s4_mesh_160.log, s4_mesh_260.log (incl. chi, genus) | identical; 11 s and 41 s | yes |

Differences that exist: only timing values (verify_all per-check seconds and total, `time` lines of s1 and s3, wall times). The msolve banner and Singular output carry no timestamps and matched byte for byte.

## Findings and failures
1. **l2.py / l3.py fail or hang under the memory cap the other jobs use.** The first attempt under `ulimit -v 8000000` failed with `PariError: not enough memory`. The scripts allocate 2 GB and 3 GB PARI stacks, and PARI's parallel threads each ask for a large stack. A second attempt under 24 GB virtual hung after about 7.9 minutes with 0% CPU (futex wait, PARI printing "not enough memory, new thread stack" warnings); That one process was killed. The third attempt, with a 64 GB virtual limit, finished normally (l2 plus l3 about 47 s). The README says so. The code is not at fault on a machine with no virtual-memory cap, but a reader who copies the "ulimit -v 8 GB" habit will fail.
2. **analyze.py reads the shipped logs, not freshly generated output.** Per PATCHES.md it reads `data/logs/real_01.out` and `data/logs/gb_01.out`, while run_ms.sh and run_real.sh write into `code/exact3_v2/`. So `analyze.py` would pass even if the msolve runs were never repeated. In this clean room The gap was closed by `cmp`: freshly generated gb_01.out, par_01.out and real_01.out are byte-identical to the shipped ones, so the analysis stands. For the README, either tell the reader to compare the files, or point analyze.py at the fresh files.
3. **Release is self-contained for every run.** No run needed a file missing from code/, data/ or requirements.txt. Scripts that write pickles (sisters) write into the current directory and must be run from `code/sisters`; l2/l3 must be run from `code/exact2` (they use `../../data/...`). run_ms.sh and run_real.sh `cd` into their own folder and have no CRLF problem in the release.
4. **Items verify_all.py does not re-run** (fano, msolve, group id) were all re-run here separately (runs 3 to 5) and match.
5. Minor: the wall time the wrapper reported for l2.py (1 s) is not credible. It was run back to back with l3 and the two together took about 47 s. Treat l2 as seconds to tens of seconds.
6. Other Singular jobs were running in WSL at the same time and were left alone. At most two heavy jobs of the rerun ran at once. Only the rerun's own hung l2 and the l3 started after it were killed.
7. Not done: no release files were modified by the rerun. The ulimit variants, the kill and the retries are all documented above.

## Files
The l2 and l3 transcripts of the successful run are shipped as `data/logs/l2.log` and `data/logs/l3.log`. The other raw outputs of the rerun are not shipped.
