# core: the refereed exact data of Y56

Moki & Julio (AI-assisted) · 2026

This folder is the v1.0 core of the atlas, with its internal layout unchanged so that every command below works from here. Its claims are R1 to R19 in `../RESULTS.md`; its prior-art verdicts, corrections and loose ends are in `../PRIOR-ART.md`, `../CORRECTIONS.md` and `../README.md`.

- `data/` exact coordinates of the 56 lines, the 32 symmetry matrices with their line permutations, the 148 + 50 line planes, the 20 conic-pair planes, the incidence list, the lattice data, and the transcripts of every Singular, msolve, GAP and PARI run (`data/logs/`).
- `code/` the scripts behind the data, and `code/verify_all.py`, the one-command exact check.
- `docs/` working notes on each exact computation, edited for release (`docs/CLEANROOM.md` records the clean-room rerun, `docs/VERIFY-RUN.txt` the recorded `verify_all.py` run).
- `media/` pictures of Y56 alone (lines, conics, the screw loop, the six faces) with `media/CAPTIONS.md`.
- `PATCHES.md` the sanitising and referee changes made when this core was first staged; `requirements.txt` the tool versions.

## Re-check

```
cd core
pip install sympy
python code/verify_all.py          # 21 exact checks over Q(sqrt2), about 1.5 to 2.5 minutes
```

The other commands, all run from `core/`:

```
cd code/exact2 && python l2.py && python l3.py        # lattice completeness (needs cypari2); transcripts data/logs/l2.log, l3.log
cd code/exact2 && gap -q grp.g < /dev/null           # the symmetry group (GAP)
cd code/exact3 && Singular -q fano.sing && Singular -q smooth.sing     # the Fano scheme of lines and smoothness
cd code/exact3_v2 && MSOLVE=<path to msolve> bash run_ms.sh && MSOLVE=<path to msolve> bash run_real.sh && python analyze.py
cd code/sisters && python s1_group.py && python s2_lattice.py && python s3_conics.py && python s4_mesh.py 160 && python s4_mesh.py 260
cd code/exact && python galois_twist.py
```

Do not run `l2.py` or `l3.py` under a small virtual-memory cap: PARI's parallel threads each reserve a large stack and the run fails or hangs (uncapped it uses under 0.2 GB). `analyze.py` reads the shipped logs in `data/logs/`; after re-running msolve, compare the fresh outputs with those logs using `cmp`.

Written with AI assistance.
