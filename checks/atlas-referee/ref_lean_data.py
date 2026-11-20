"""Referee (atlas round): compare the data printed inside the Lean files with the release data.
Independent parser; does not import export_lean.py. Run from anywhere:
  py -3.11 ref_lean_data.py [archive folder; default ../..]
"""
import sys, re, json, ast, itertools
import sympy as sp

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../.."
L = ROOT + "/lean/"
D = ROOT + "/core/data/"
r2 = sp.sqrt(2)
out = []
def rep(tag, ok, msg=""):
    out.append(f"{'PASS' if ok else 'FAIL'} {tag} {msg}")
    print(out[-1], flush=True)

def zq(a, b):
    return sp.Integer(a) + sp.Integer(b) * r2

QRE = re.compile(r"q \(?(-?\d+)\)? \(?(-?\d+)\)?")

def parse_qlist_block(text, name):
    # def NAME : List (List Z2) := [ ... ]  -> list of lists of sympy numbers
    m = re.search(r"def " + name + r" : [^=]*:= \[", text)
    assert m, name
    i = m.end() - 1
    depth = 0
    for j in range(i, len(text)):
        if text[j] == '[': depth += 1
        elif text[j] == ']':
            depth -= 1
            if depth == 0: break
    body = text[i:j+1]
    return body

def rows_of_q(body):
    # split innermost lists
    rows = re.findall(r"\[([^\[\]]*)\]", body)
    res = []
    for r in rows:
        res.append([zq(a, b) for a, b in QRE.findall(r)])
    return res

def nat_list(text, name):
    m = re.search(r"def " + name + r" : [^=]*:= (\[.*)", text)
    return ast.literal_eval(m.group(1).replace("(", "[").replace(")", "]"))

def proj_eq(u, v):
    u = [sp.nsimplify(x) for x in u]; v = [sp.nsimplify(x) for x in v]
    for a, b in itertools.combinations(range(len(u)), 2):
        if sp.simplify(u[a]*v[b] - u[b]*v[a]) != 0: return False
    return any(x != 0 for x in u)

def span_eq(P, Q):
    # two lines given by two spanning vectors each: equal iff rank [P;Q] == 2
    M = sp.Matrix(P + Q).applyfunc(sp.nsimplify)
    return M.rank(simplify=True) == 2

# ---------- release data
lines = []
for ln in open(D + "lines_exact.txt"):
    if ln.startswith("L"):
        a, b = ln.split(":", 1)[1].split("|")
        lines.append([[sp.sympify(x) for x in ast.literal_eval(a.strip())],
                      [sp.sympify(x) for x in ast.literal_eval(b.strip())]])
rep("data.lines56", len(lines) == 56)
edges = [tuple(e) for e in json.load(open(D + "edges.json"))]
syms = []
for ln in open(D + "symmetry_exact.txt"):
    if ln.startswith("g"):
        m = re.match(r"g(\d+) c=(-?\d+) M=(\[.*\]) sigma=(\[.*\])", ln.strip())
        syms.append((int(m.group(2)), sp.Matrix(sp.sympify(m.group(3))), ast.literal_eval(m.group(4))))
rep("data.syms32", len(syms) == 32)

# ---------- lines: same U,V in every data-driven file, and same lines as the release file
UV = {}
for f in ["Y56_L1", "Y56_L2", "Y56_L3", "Y56_L6"]:
    t = open(L + f + ".lean", encoding="utf-8").read()
    UV[f] = (rows_of_q(parse_qlist_block(t, "LU")), rows_of_q(parse_qlist_block(t, "LV")))
base = UV["Y56_L1"]
for f in UV:
    rep(f"lean.LU_LV identical {f} vs L1", UV[f] == base)
bad = [i for i in range(56) if not span_eq([base[0][i], base[1][i]], lines[i])]
rep("lean.lines == lines_exact.txt (same line, projectively)", not bad, f"bad={bad}")

# ---------- edges: L3/L6/L8 NB and EDGES vs edges.json
for f in ["Y56_L3", "Y56_L6", "Y56_L8"]:
    t = open(L + f + ".lean", encoding="utf-8").read()
    NB = nat_list(t, "NB")
    E2 = sorted({tuple(sorted((i, j))) for i in range(56) for j in NB[i]})
    rep(f"{f}.NB == edges.json", E2 == sorted(edges), f"{len(E2)} vs {len(edges)}")
    if "def EDGES" in t:
        EL = [tuple(x) for x in nat_list(t, "EDGES")]
        rep(f"{f}.EDGES == edges.json", EL == edges)
# independent incidence recompute: 4x4 det
inc = set()
for i, j in itertools.combinations(range(56), 2):
    M = sp.Matrix(lines[i] + lines[j])
    if sp.nsimplify(sp.expand(M.det())) == 0: inc.add((i, j))
rep("edges.json == recomputed 4x4-det incidence", sorted(inc) == sorted(edges), f"{len(inc)}")

# ---------- L2: MS table vs symmetry_exact.txt, SIG vs sigma, and sym_gXX statements vs MS
t2 = open(L + "Y56_L2.lean", encoding="utf-8").read()
body = parse_qlist_block(t2, "MS")
mats = re.findall(r"\[\[[^\]]*\](?:, \[[^\]]*\]){3}\]", body)
MS = [sp.Matrix(rows_of_q(m)) for m in mats]
rep("L2.MS has 32 matrices", len(MS) == 32)
rep("L2.MS == symmetry_exact M (entrywise)", all((MS[g] - syms[g][1]).applyfunc(sp.simplify) == sp.zeros(4) for g in range(32)))
SIG = nat_list(t2, "SIG")
rep("L2.SIG == symmetry_exact sigma", SIG == [s[2] for s in syms])
# sym_gXX: parse the substituted arguments and constant, compare with MS and c
z = sp.symbols("z0 z1 z2 z3"); s = sp.Symbol("s")
okc = True; okm = True; badg = []
for g in range(32):
    m = re.search(r"theorem sym_g%02d .*?:\n\s+F s (.*?)\n\s+= \((-?\d+)\) \* F s z0 z1 z2 z3" % g, t2, re.S)
    if not m: badg.append((g, "noparse")); continue
    args = m.group(1)
    # split top-level parenthesised args
    parts, depth, cur = [], 0, ""
    for ch in args:
        if ch == '(':
            depth += 1
            if depth == 1: cur = ""; continue
        if ch == ')':
            depth -= 1
            if depth == 0: parts.append(cur); continue
        if depth >= 1: cur += ch
    loc = dict(zip(["z0", "z1", "z2", "z3"], z)); loc["s"] = s
    exprs = [sp.sympify(p.replace("^", "**"), locals=loc) for p in parts]
    Mz = (MS[g].subs(r2, s) * sp.Matrix(z)) if False else None
    # MS entries are a + b*sqrt2 ; statement uses symbol s for sqrt2
    Ms = MS[g].applyfunc(lambda x: sp.expand(x).subs(r2, s))
    want = list(Ms * sp.Matrix(z))
    if len(exprs) != 4 or any(sp.expand(exprs[k] - want[k]) != 0 for k in range(4)):
        okm = False; badg.append((g, "matrix"))
    if int(m.group(2)) != syms[g][0]:
        okc = False; badg.append((g, "c"))
rep("L2.sym_gXX substitution == MS row-by-row (all 32)", okm, f"bad={badg}")
rep("L2.sym_gXX constant c == symmetry_exact c", okc)
# independent: F(Mz) = cF(z) with real sqrt2, and M maps line i to line sigma(i)
e = r2
def F(v): z0, z1, z2, z3 = v; return 3*e*z0**2*z1*z2 + 3*e*z1*z2*z3**2 - e*z1**3*z2 - e*z1*z2**3 + 4*z0**3*z3 - 4*z0*z3**3
okF = all(sp.expand(F(list(syms[g][1]*sp.Matrix(z))) - syms[g][0]*F(list(z))) == 0 for g in range(32))
rep("independent F(Mz)=cF(z) for 32 maps", okF)
okmap = all(span_eq([list(syms[g][1]*sp.Matrix(lines[i][0])), list(syms[g][1]*sp.Matrix(lines[i][1]))], lines[syms[g][2][i]]) for g in range(32) for i in range(56))
rep("independent M_g(line i) == line sigma_g(i) (1792)", okmap)
# symplectic count: det(M)/c == +1
sympl = [g for g in range(32) if sp.simplify(syms[g][1].det()/syms[g][0] - 1) == 0]
rep("symplectic det(M)/c=+1 count == 16", len(sympl) == 16, f"{len(sympl)}")
# orbits and orbit S
orb = {}
for r in range(56):
    orb.setdefault(frozenset(s_[2][r] for s_ in syms), None)
sizes = sorted(len(o) for o in orb)
rep("line orbit sizes 8+16+16+16", sizes == [8, 16, 16, 16], f"{sizes}")
S = sorted({s_[2][0] for s_ in syms})
Sclaim = [0, 6, 10, 11, 12, 19, 29, 33, 35, 36, 42, 44, 48, 50, 54, 55]
rep("orbit of L00 == paper's S list", S == Sclaim, f"{S}")
O8 = sorted({s_[2][2] for s_ in syms})
rep("orbit of L02 == paper's 8-orbit {02,14,22,24,27,30,43,53}", O8 == [2, 14, 22, 24, 27, 30, 43, 53], f"{O8}")
# anchor lines lie in z1=0 or z2=0
okanc = all(all(lines[i][k][1] == 0 for k in (0, 1)) or all(lines[i][k][2] == 0 for k in (0, 1)) for i in O8)
rep("8-orbit lines lie in z1=0 or z2=0", okanc)

# ---------- L8: Gram from NB; h = L00+L06+L23+L24 is a listed four-line plane
P4 = []
for ln in open(D + "planes_exact.txt"):
    if ln.startswith("P4"):
        P4.append(sorted(ast.literal_eval(ln.split("lines")[1].strip())))
rep("{0,6,23,24} is a listed four-line plane", [0, 6, 23, 24] in P4, f"#P4={len(P4)}")
G = sp.Matrix(56, 56, lambda i, j: -2 if i == j else (1 if tuple(sorted((i, j))) in set(edges) else 0))
rep("rank Gram (56 lines) == 20", G.rank() == 20)
B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20]
rep("det of L8 basis block == -64", G.extract(B, B).det() == -64)

# ---------- L6: PL vs planes_exact.txt
t6 = open(L + "Y56_L6.lean", encoding="utf-8").read()
PL = nat_list(t6, "PL")
PLd = []
for ln in open(D + "planes_exact.txt"):
    if ln.startswith("P2") or ln.startswith("P4"):
        PLd.append(sorted(ast.literal_eval(ln.split("lines")[1].strip())))
rep("L6.PL == planes_exact.txt line lists (order kept)", [sorted(x) for x in PL] == PLd, f"{len(PL)} vs {len(PLd)}")

# ---------- pencil: substitute the line shape into G_s
a_, b_, s_ = sp.symbols("alpha beta s"); t0, t3 = sp.symbols("t0 t3")
Gs = lambda z0, z1, z2, z3: 4*z0**3*z3 - 4*z0*z3**3 + 2*z1*z2*(s_*(z0**2 + z3**2) - (z1**2 + z2**2))
P = sp.Poly(sp.expand(Gs(t0, a_*t0, b_*(t3 - t0), t3)), t0, t3)
coeffs = [sp.factor(P.coeff_monomial(t0**(4-k)*t3**k)) for k in range(5)]
print("pencil coefficients t0^4..t3^4:", coeffs, flush=True)
eqs = [a_*b_*(s_ - a_**2 - b_**2), 2 + a_*b_*(s_ - b_**2), 1 + a_*b_**3]
Gb = sp.groebner(coeffs, a_, b_, s_, order="lex")
Ge = sp.groebner(eqs, a_, b_, s_, order="lex")
rep("ideal(5 coefficients) == ideal(paper's 3 equations)", list(Gb.exprs) == list(Ge.exprs), f"\n  coeffs-GB={Gb.exprs}\n  eqs-GB={Ge.exprs}")
elim = [x for x in Gb.exprs if x.free_symbols <= {s_}]
rep("eliminant in s", True, f"{elim}")

open(sys.argv[2] if len(sys.argv) > 2 else "ref_lean_data.out", "w").write("\n".join(out) + "\n")
