"""export_lean.py: generate the Y56 Lean files from the shipped data files only.

Reads (all under ../core/data): lines_exact.txt, symmetry_exact.txt, edges.json,
planes_exact.txt, conic_pair_planes_exact.txt.  Writes self-contained Lean files
(each starts with `import Mathlib` and the shared prelude) next to this script.

Every number written to Lean is an element of Z[sqrt2] given as q a b = a + b*sqrt2.
Projective data (spanning vectors, normals) are scaled by a positive integer to clear
denominators; the scale is recorded in a comment.  Certificates computed here (cofactors,
coefficients of span relations, plane parametrisations) are only hints: Lean's kernel
re-checks every one of them, so none of this script is trusted.

Usage: py -3.11 export_lean.py [item ...]   (items: prelude L1 L7 L2 L3 L6 L5 pencil; default all)
"""
from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from math import lcm
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "core" / "data"
SQ2 = sp.sqrt(2)


# ------------------------------------------------------------------ Q(sqrt2) numbers
def parse_q2(s: str) -> tuple[Fraction, Fraction]:
    ex = sp.expand(sp.sympify(s))
    a = ex.coeff(SQ2, 0)
    b = ex.coeff(SQ2, 1)
    if sp.expand(a + b * SQ2 - ex) != 0 or not (a.is_rational and b.is_rational):
        raise ValueError(f"not in Q(sqrt2): {s}")
    return Fraction(int(sp.numer(a)), int(sp.denom(a))), Fraction(int(sp.numer(b)), int(sp.denom(b)))


def to_q2(ex) -> tuple[Fraction, Fraction]:
    ex = sp.expand(ex)
    a, b = ex.coeff(SQ2, 0), ex.coeff(SQ2, 1)
    assert sp.expand(a + b * SQ2 - ex) == 0 and a.is_rational and b.is_rational, ex
    return Fraction(int(sp.numer(a)), int(sp.denom(a))), Fraction(int(sp.numer(b)), int(sp.denom(b)))


def scale_vec(v: list[tuple[Fraction, Fraction]]) -> tuple[list[tuple[int, int]], int]:
    L = 1
    for a, b in v:
        L = lcm(L, a.denominator, b.denominator)
    out = [(int(a * L), int(b * L)) for a, b in v]
    assert L > 0
    return out, L


def lq(x: tuple[int, int]) -> str:
    a, b = x
    fa = f"({a})" if a < 0 else str(a)
    fb = f"({b})" if b < 0 else str(b)
    return f"q {fa} {fb}"


def lvec(v) -> str:
    return "[" + ", ".join(lq(x) for x in v) + "]"


def sym_q2(x: tuple[int, int]):
    return sp.Integer(x[0]) + sp.Integer(x[1]) * SQ2


# ------------------------------------------------------------------ polynomial printer
def lean_poly(ex, gens) -> str:
    """Print a polynomial with integer coefficients in gens as a Lean term."""
    P = sp.Poly(sp.expand(ex), *gens)
    terms = []
    for mon, c in P.terms():
        c = int(c)
        fac = []
        for g, k in zip(gens, mon):
            if k == 1:
                fac.append(str(g))
            elif k > 1:
                fac.append(f"{g} ^ {k}")
        body = " * ".join(fac)
        ac = abs(c)
        if body == "":
            t = str(ac)
        elif ac == 1:
            t = body
        else:
            t = f"{ac} * {body}"
        terms.append(("-" if c < 0 else "+", t))
    if not terms:
        return "0"
    out = ("-" if terms[0][0] == "-" else "") + terms[0][1]
    for sg, t in terms[1:]:
        out += f" {sg} {t}"
    return "(" + out + ")" if terms[0][0] == "-" and len(terms) == 1 else out


# ------------------------------------------------------------------ data readers
def read_lines():
    U, V, scales = [], [], []
    for ln in (DATA / "lines_exact.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"L(\d+): (\[.*?\]) \| (\[.*?\])", ln)
        if not m:
            continue
        u = [parse_q2(x) for x in eval(m.group(2))]
        v = [parse_q2(x) for x in eval(m.group(3))]
        su, ku = scale_vec(u)
        sv, kv = scale_vec(v)
        U.append(su)
        V.append(sv)
        scales.append((ku, kv))
    assert len(U) == 56
    return U, V, scales


def read_sym():
    out = []
    for ln in (DATA / "symmetry_exact.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"g(\d+) c=(-?\d+) M=(\[\[.*?\]\]) sigma=(\[.*?\])", ln)
        if not m:
            continue
        Ms = eval(re.sub(r"(-?sqrt\(2\))", r"'\1'", m.group(3)))
        M = [[to_int_q2(x) for x in row] for row in Ms]
        out.append((int(m.group(1)), int(m.group(2)), M, eval(m.group(4))))
    assert len(out) == 32
    return out


def to_int_q2(x):
    a, b = parse_q2(str(x))
    assert a.denominator == 1 and b.denominator == 1
    return (int(a), int(b))


def read_planes():
    P2, P4, PC = [], [], []
    for ln in (DATA / "planes_exact.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"(P2|P4) (\[.*?\]) lines (\[.*?\])", ln)
        if m:
            n, k = scale_vec([parse_q2(x) for x in eval(m.group(2))])
            (P2 if m.group(1) == "P2" else P4).append((n, eval(m.group(3))))
            continue
    # the 20 line-free conic-pair planes are listed in conic_pair_planes_exact.txt (orbit labels A, B, C)
    for ln in (DATA / "conic_pair_planes_exact.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"([ABC]) (\[.*?\]) verified=True", ln)
        if m:
            n, k = scale_vec([parse_q2(x) for x in eval(m.group(2))])
            PC.append(n)
    return P2, P4, PC


def read_edges():
    return [tuple(e) for e in json.loads((DATA / "edges.json").read_text(encoding="utf-8"))]


# ------------------------------------------------------------------ shared prelude
PRELUDE = r'''import Mathlib

/-!
# Y56 shared prelude (generated by export_lean.py from the shipped data files)

Numbers live in `Z2 = Zsqrtd 2` (pairs (a, b) meaning a + b*sqrt 2, decidable equality,
computable ring operations, so the kernel can evaluate them with `decide +kernel`).
`iota s hs` is the ring map Z[sqrt 2] -> R sending sqrt 2 to any `s` with `s * s = 2`
(for example `Real.sqrt 2` in the reals, or either square root of 2 in the complex numbers).
It is injective whenever R has characteristic zero.
-/

namespace Y56

set_option linter.unusedVariables false

abbrev Z2 := Zsqrtd 2

/-- sqrt 2 inside Z[sqrt 2]. -/
def e2 : Z2 := ⟨0, 1⟩

/-- `q a b = a + b * sqrt 2`. -/
def q (a b : Int) : Z2 := ⟨a, b⟩

theorem two_not_square : ∀ n : ℤ, (2 : ℤ) ≠ n * n := by
  intro n h
  have h1 : n ≤ 1 := by nlinarith
  have h2 : -1 ≤ n := by nlinarith
  interval_cases n <;> omega

/-- The ring map Z[sqrt 2] -> R sending sqrt 2 to `s`. -/
def iota {R : Type*} [CommRing R] (s : R) (hs : s * s = 2) : Z2 →+* R :=
  Zsqrtd.lift ⟨s, by rw [hs]; norm_num⟩

theorem iota_e2 {R : Type*} [CommRing R] (s : R) (hs : s * s = 2) : iota s hs e2 = s := by
  simp [iota, e2]

theorem iota_q {R : Type*} [CommRing R] (s : R) (hs : s * s = 2) (a b : Int) :
    iota s hs (q a b) = (a : R) + (b : R) * s := by
  simp [iota, q]

theorem iota_injective {R : Type*} [CommRing R] [CharZero R] (s : R) (hs : s * s = 2) :
    Function.Injective (iota s hs) :=
  Zsqrtd.lift_injective _ two_not_square

/-- The Y56 quartic, with `e` standing for sqrt 2:
F = 3e z0^2 z1 z2 + 3e z1 z2 z3^2 - e z1^3 z2 - e z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3. -/
def F {R : Type*} [CommRing R] (e z0 z1 z2 z3 : R) : R :=
  3 * e * z0 ^ 2 * z1 * z2 + 3 * e * z1 * z2 * z3 ^ 2 - e * z1 ^ 3 * z2 - e * z1 * z2 ^ 3
    + 4 * z0 ^ 3 * z3 - 4 * z0 * z3 ^ 3

/-- Large kernel checks are split into chunks (separate declarations keep the kernel's memory
small); this glues the chunk results back together. -/
theorem forall_of_chunks (f : Nat → Bool) (B n : Nat) (hB : 0 < B)
    (h : ∀ c, c < n → (List.range' (c * B) B).all f = true) : ∀ i, i < n * B → f i = true := by
  intro i hi
  have hc : i / B < n := by rw [Nat.div_lt_iff_lt_mul hB]; exact hi
  apply List.all_eq_true.mp (h (i / B) hc) i
  rw [List.mem_range'_1]
  have h1 := Nat.div_add_mod i B
  have h2 := Nat.mod_lt i hB
  constructor
  · exact Nat.div_mul_le_self i B
  · rw [Nat.mul_comm]; linarith

/-- Entry k of row i of a table of vectors (0 when out of range). -/
def getZ (L : List (List Z2)) (i k : Nat) : Z2 := (L.getD i []).getD k 0

/-- 3 x 3 determinant with rows (a0 a1 a2), (b0 b1 b2), (c0 c1 c2). -/
def det3 {R : Type*} [CommRing R] (a0 a1 a2 b0 b1 b2 c0 c1 c2 : R) : R :=
  a0 * (b1 * c2 - b2 * c1) - a1 * (b0 * c2 - b2 * c0) + a2 * (b0 * c1 - b1 * c0)

theorem det3_map {R : Type*} [CommRing R] (f : Z2 →+* R) (a0 a1 a2 b0 b1 b2 c0 c1 c2 : Z2) :
    f (det3 a0 a1 a2 b0 b1 b2 c0 c1 c2)
      = det3 (f a0) (f a1) (f a2) (f b0) (f b1) (f b2) (f c0) (f c1) (f c2) := by
  simp only [det3, map_add, map_sub, map_mul]

/-- A vector in the span of the first two rows makes every 3 x 3 minor vanish. -/
theorem det3_span {R : Type*} [CommRing R] (x y : Nat → R) (a b : R) (c1 c2 c3 : Nat) :
    det3 (x c1) (x c2) (x c3) (y c1) (y c2) (y c3)
      (a * x c1 + b * y c1) (a * x c2 + b * y c2) (a * x c3 + b * y c3) = 0 := by
  unfold det3; ring

/-- The column triple left after dropping column d (d = 0..3). -/
def cols : Nat → Nat × Nat × Nat
  | 0 => (1, 2, 3)
  | 1 => (0, 2, 3)
  | 2 => (0, 1, 3)
  | _ => (0, 1, 2)

theorem cols_lt (d : Nat) : (cols d).1 < 4 ∧ (cols d).2.1 < 4 ∧ (cols d).2.2 < 4 := by
  rcases d with _ | _ | _ | d <;> simp [cols]

'''


def chunked(name: str, fname: str, N: int, B: int) -> str:
    """Lean text: chunk theorems name_c for f over range' (c*B) B, and `name : ∀ i, i < n*B -> f i = true`.
    f must be true on the padding N <= i < n*B (write f as `i ≥ N || ...`)."""
    n = -(-N // B)
    out = [f"theorem {name}_{c} : (List.range' {c * B} {B}).all {fname} = true := by decide +kernel"
           for c in range(n)]
    cases = "\n".join(f"    | {c}, _ => {name}_{c}" for c in range(n))
    out.append(f"theorem {name} : ∀ i, i < {n * B} → {fname} i = true :=\n"
               f"  forall_of_chunks {fname} {B} {n} (by norm_num) (fun c hc => match c, hc with\n"
               f"{cases}\n    | _ + {n}, h => absurd h (by omega))\n")
    return "\n".join(out)


def write(name: str, body: str):
    p = HERE / name
    p.write_text(body, encoding="utf-8")
    print(f"wrote {p.name} ({len(body)} chars)")


# ------------------------------------------------------------------ L1
def gen_L1(mutate=False):
    U, V, scales = read_lines()
    if mutate:  # negative control: perturb one entry of one line
        U = [list(u) for u in U]
        a, b = U[17][1]
        U[17][1] = (a + 1, b)
    e = sp.Symbol("e")
    u = sp.symbols("u0:4")
    v = sp.symbols("v0:4")
    l, m = sp.symbols("l m")

    def Fs(z0, z1, z2, z3):
        return (3 * e * z0**2 * z1 * z2 + 3 * e * z1 * z2 * z3**2 - e * z1**3 * z2 - e * z1 * z2**3
                + 4 * z0**3 * z3 - 4 * z0 * z3**3)

    expr = sp.expand(Fs(*[l * u[k] + m * v[k] for k in range(4)]))
    P = sp.Poly(expr, l, m)
    gens = [e, *u, *v]
    cdefs = []
    args = "(e u0 u1 u2 u3 v0 v1 v2 v3 : R)"
    for k in range(5):
        ck = P.coeff_monomial(l**k * m**(4 - k))
        cdefs.append(f"/-- coefficient of l^{k} m^{4 - k} in F(l u + m v) -/\n"
                     f"def C{k} {{R : Type*}} [CommRing R] {args} : R :=\n  {lean_poly(ck, gens)}\n")
    # sanity in python: all coefficients vanish for every (true) line
    if not mutate:
        for i in range(56):
            sub = {e: SQ2}
            for k in range(4):
                sub[u[k]] = sym_q2(U[i][k])
                sub[v[k]] = sym_q2(V[i][k])
            for k in range(5):
                assert sp.expand(P.coeff_monomial(l**k * m**(4 - k)).subs(sub)) == 0, (i, k)
    rhs = " + ".join(f"C{k} e u0 u1 u2 u3 v0 v1 v2 v3 * l ^ {k} * m ^ {4 - k}" for k in range(5))
    fa = "(f u0) (f u1) (f u2) (f u3) (f v0) (f v1) (f v2) (f v3)"
    maps = "\n".join(
        f"theorem C{k}_map {{R : Type*}} [CommRing R] (f : Z2 →+* R) (s : R) (h : f e2 = s)\n"
        f"    (u0 u1 u2 u3 v0 v1 v2 v3 : Z2) :\n"
        f"    C{k} s {fa} = f (C{k} e2 u0 u1 u2 u3 v0 v1 v2 v3) := by\n"
        f"  subst h; simp only [C{k}, map_add, map_sub, map_mul, map_pow, map_ofNat]\n"
        for k in range(5))
    scl = "; ".join(f"L{i:02d}: x{su},x{sv}" for i, (su, sv) in enumerate(scales) if (su, sv) != (1, 1))
    data = (f"/-- First spanning vector of each of the 56 lines (row i = line Li of lines_exact.txt,\n"
            f"scaled by a positive integer to clear denominators; scales: {scl}). -/\n"
            f"def LU : List (List Z2) := [\n  " + ",\n  ".join(lvec(x) for x in U) + "]\n\n"
            f"/-- Second spanning vector of each line (same scaling convention). -/\n"
            f"def LV : List (List Z2) := [\n  " + ",\n  ".join(lvec(x) for x in V) + "]\n\n"
            "def U (i k : Nat) : Z2 := getZ LU i k\ndef V (i k : Nat) : Z2 := getZ LV i k\n")
    body = PRELUDE + data + "\n" + "\n".join(cdefs) + f"""
theorem F_line {{R : Type*}} [CommRing R] (e u0 u1 u2 u3 v0 v1 v2 v3 l m : R) :
    F e (l * u0 + m * v0) (l * u1 + m * v1) (l * u2 + m * v2) (l * u3 + m * v3)
      = {rhs} := by
  simp only [F, C0, C1, C2, C3, C4]; ring

{maps}
/-- Kernel computation: the five coefficients vanish for every line. -/
def coeffsOK (i : Nat) : Bool :=
  decide (C0 e2 (U i 0) (U i 1) (U i 2) (U i 3) (V i 0) (V i 1) (V i 2) (V i 3) = 0) &&
  decide (C1 e2 (U i 0) (U i 1) (U i 2) (U i 3) (V i 0) (V i 1) (V i 2) (V i 3) = 0) &&
  decide (C2 e2 (U i 0) (U i 1) (U i 2) (U i 3) (V i 0) (V i 1) (V i 2) (V i 3) = 0) &&
  decide (C3 e2 (U i 0) (U i 1) (U i 2) (U i 3) (V i 0) (V i 1) (V i 2) (V i 3) = 0) &&
  decide (C4 e2 (U i 0) (U i 1) (U i 2) (U i 3) (V i 0) (V i 1) (V i 2) (V i 3) = 0)

theorem coeffs_all : (List.range 56).all coeffsOK = true := by decide +kernel

/-- **L1a.** For every ring R with an element s, s*s = 2 (e.g. R = ℝ or ℂ, s = √2), and every
line i of the list, every point l*u_i + m*v_i of the line lies on the surface F = 0. -/
theorem lines_on_F {{R : Type*}} [CommRing R] (s : R) (hs : s * s = 2) (i : Fin 56) (l m : R) :
    F s (l * iota s hs (U i 0) + m * iota s hs (V i 0)) (l * iota s hs (U i 1) + m * iota s hs (V i 1))
      (l * iota s hs (U i 2) + m * iota s hs (V i 2)) (l * iota s hs (U i 3) + m * iota s hs (V i 3))
      = 0 := by
  have h := List.all_eq_true.mp coeffs_all i (List.mem_range.mpr i.isLt)
  simp only [coeffsOK, Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨⟨h0, h1⟩, h2⟩, h3⟩, h4⟩ := h
  have he := iota_e2 s hs
  rw [F_line, C0_map _ s he, C1_map _ s he, C2_map _ s he, C3_map _ s he, C4_map _ s he,
    h0, h1, h2, h3, h4]
  simp
"""
    body += L1_DISTINCT + "\nend Y56\n"
    write("Y56_L1_neg.lean" if mutate else "Y56_L1.lean", body)


L1_DISTINCT = r'''
/-! ## Distinctness and genuine lines -/

/-- Minor of the 3 x 4 matrix (U j; V j; W) with W = V i (if w) or U i, column d dropped. -/
def minorZ (i j : Nat) (w : Bool) (d : Nat) : Z2 :=
  let c := cols d
  let W := fun k => if w then V i k else U i k
  det3 (U j c.1) (U j c.2.1) (U j c.2.2) (V j c.1) (V j c.2.1) (V j c.2.2) (W c.1) (W c.2.1) (W c.2.2)

def distOK (i j : Nat) : Bool :=
  i == j || [0, 1, 2, 3].any (fun d => decide (minorZ i j false d ≠ 0) || decide (minorZ i j true d ≠ 0))

theorem dist_all : (List.range 56).all (fun i => (List.range 56).all (fun j => distOK i j)) = true := by
  decide +kernel

/-- 2 x 2 minor (columns p, r) of the pair (U i, V i). -/
def pl (i p r : Nat) : Z2 := U i p * V i r - U i r * V i p

def indepOK (i : Nat) : Bool :=
  [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)].any (fun pr => decide (pl i pr.1 pr.2 ≠ 0))

theorem indep_all : (List.range 56).all indepOK = true := by decide +kernel

/-- **L1b.** Over any ring of characteristic zero with s*s = 2 (ℝ, ℂ, ...): for i ≠ j, line i is
not contained in the span of line j (so the 56 lines are pairwise different). -/
theorem lines_distinct {R : Type*} [CommRing R] [CharZero R] (s : R) (hs : s * s = 2)
    (i j : Fin 56) (hij : i ≠ j) :
    ¬ ∃ a b c d : R, ∀ k : Nat, k < 4 →
      iota s hs (U i k) = a * iota s hs (U j k) + b * iota s hs (V j k) ∧
      iota s hs (V i k) = c * iota s hs (U j k) + d * iota s hs (V j k) := by
  rintro ⟨a, b, c, d, h⟩
  have hne : (i : Nat) ≠ j := Fin.val_injective.ne hij
  have hc := List.all_eq_true.mp (List.all_eq_true.mp dist_all i (List.mem_range.mpr i.isLt)) j
    (List.mem_range.mpr j.isLt)
  simp only [distOK, Bool.or_eq_true, beq_iff_eq, hne, false_or, List.any_eq_true,
    decide_eq_true_eq] at hc
  obtain ⟨dd, -, hdd⟩ := hc
  have zero : ∀ w : Bool, iota s hs (minorZ i j w dd) = 0 := by
    intro w
    obtain ⟨h1, h2, h3⟩ := cols_lt dd
    have key := fun (x y : Nat) => (h x)
    cases w
    · simp only [minorZ, Bool.false_eq_true, ite_false, det3_map]
      rw [(h _ h1).1, (h _ h2).1, (h _ h3).1]
      exact det3_span (fun k => iota s hs (U j k)) (fun k => iota s hs (V j k)) a b _ _ _
    · simp only [minorZ, ite_true, det3_map]
      rw [(h _ h1).2, (h _ h2).2, (h _ h3).2]
      exact det3_span (fun k => iota s hs (U j k)) (fun k => iota s hs (V j k)) c d _ _ _
  rcases hdd with hdd | hdd
  · exact hdd ((iota_injective s hs) (by rw [zero false, map_zero]))
  · exact hdd ((iota_injective s hs) (by rw [zero true, map_zero]))

/-- **L1c.** Each pair (U i, V i) is linearly independent over any domain of characteristic zero
with s*s = 2, so each entry of the list really spans a line of P^3. -/
theorem lines_genuine {R : Type*} [CommRing R] [IsDomain R] [CharZero R] (s : R) (hs : s * s = 2)
    (i : Fin 56) (a b : R) (h : ∀ k : Nat, k < 4 → a * iota s hs (U i k) + b * iota s hs (V i k) = 0) :
    a = 0 ∧ b = 0 := by
  have hc := List.all_eq_true.mp indep_all i (List.mem_range.mpr i.isLt)
  simp only [indepOK, List.any_eq_true, decide_eq_true_eq] at hc
  obtain ⟨⟨p, r⟩, hmem, hpr⟩ := hc
  have hp : p < 4 := by simp at hmem; omega
  have hr : r < 4 := by simp at hmem; omega
  have hm : iota s hs (pl i p r) ≠ 0 := by
    intro h0; exact hpr ((iota_injective s hs) (by rw [h0, map_zero]))
  have e1 := h p hp
  have e2' := h r hr
  have ha : a * iota s hs (pl i p r) = 0 := by
    simp only [pl, map_sub, map_mul]
    linear_combination (iota s hs (V i r)) * e1 - (iota s hs (V i p)) * e2'
  have hb : b * iota s hs (pl i p r) = 0 := by
    simp only [pl, map_sub, map_mul]
    linear_combination (-(iota s hs (U i r))) * e1 + (iota s hs (U i p)) * e2'
  exact ⟨(mul_eq_zero.mp ha).resolve_right hm, (mul_eq_zero.mp hb).resolve_right hm⟩
'''


def lines_data(U, V, scales) -> str:
    scl = "; ".join(f"L{i:02d}: x{su},x{sv}" for i, (su, sv) in enumerate(scales) if (su, sv) != (1, 1))
    return (f"/-- First spanning vector of each of the 56 lines (row i = line Li of lines_exact.txt,\n"
            f"scaled by a positive integer to clear denominators; scales: {scl}). -/\n"
            f"def LU : List (List Z2) := [\n  " + ",\n  ".join(lvec(x) for x in U) + "]\n\n"
            f"/-- Second spanning vector of each line (same scaling convention). -/\n"
            f"def LV : List (List Z2) := [\n  " + ",\n  ".join(lvec(x) for x in V) + "]\n\n"
            "def U (i k : Nat) : Z2 := getZ LU i k\ndef V (i k : Nat) : Z2 := getZ LV i k\n\n"
            "/-- 2 x 2 minor (columns p, r) of the pair (U i, V i): a Pluecker coordinate of line i. -/\n"
            "def pl (i p r : Nat) : Z2 := U i p * V i r - U i r * V i p\n\n")


def Fsym(e, z0, z1, z2, z3):
    return (3 * e * z0**2 * z1 * z2 + 3 * e * z1 * z2 * z3**2 - e * z1**3 * z2 - e * z1 * z2**3
            + 4 * z0**3 * z3 - 4 * z0 * z3**3)


# ------------------------------------------------------------------ L2
def gen_L2(mutate=False):
    U, V, scales = read_lines()
    syms = read_sym()
    if mutate:  # negative control: swap two entries in row 1 of g05
        g, c, M, sig = syms[5]
        M = [list(r) for r in M]
        M[1][0], M[1][1] = M[1][1], M[1][0]
        syms[5] = (g, c, M, sig)
    s = sp.Symbol("s")
    z = sp.symbols("z0:4")
    thms = []
    for g, c, M, sig in syms:
        rows = [sum((sp.Integer(a) + sp.Integer(b) * s) * z[k] for k, (a, b) in enumerate(M[t])) for t in range(4)]
        D = sp.expand(Fsym(s, *rows) - c * Fsym(s, *z))
        qq, rr = sp.div(sp.Poly(D, s), sp.Poly(s**2 - 2, s))
        if not mutate:
            assert rr.is_zero, g
        Q = sp.expand(qq.as_expr())
        rl = " ".join(f"({lean_poly(r, [s, *z])})" for r in rows)
        proof = "ring" if Q == 0 else f"linear_combination ({lean_poly(Q, [s, *z])}) * hs"
        thms.append(
            f"/-- g{g:02d}: F(M z) = {c} F(z) for M = {M} (entries a + b*s). -/\n"
            f"theorem sym_g{g:02d} {{R : Type*}} [CommRing R] (s : R) (hs : s * s = 2) (z0 z1 z2 z3 : R) :\n"
            f"    F s {rl}\n      = ({c}) * F s z0 z1 z2 z3 := by\n  simp only [F]; {proof}\n")
    sigs = [x[3] for x in syms]
    n = len(sigs)
    idx = {tuple(sg): k for k, sg in enumerate(sigs)}
    tab = [[idx[tuple(sigs[g][sigs[h][i]] for i in range(56))] for h in range(n)] for g in range(n)]
    assert sigs[0] == list(range(56))

    def order(g):
        k, m = g, 1
        while k != 0:
            k, m = tab[g][k], m + 1
        return m
    orders = [order(g) for g in range(n)]
    orbits = {}
    for i in range(56):
        orbits.setdefault(frozenset(sg[i] for sg in sigs), i)
    reps = sorted(orbits.values())
    sizes = [len(next(o for o, r in orbits.items() if r == rep)) for rep in reps]
    Mdata = "[\n  " + ",\n  ".join("[" + ", ".join(lvec(r) for r in M) + "]" for _, _, M, _ in syms) + "]"
    body = PRELUDE + lines_data(U, V, scales) + "\n".join(thms) + f"""
/-! ## Table form of the 32 maps, induced permutations, group structure -/

/-- The 32 matrices (same entries as in the theorems sym_gXX above), index g = 0..31. -/
def MS : List (List (List Z2)) := {Mdata}

def M (g t c : Nat) : Z2 := ((MS.getD g []).getD t []).getD c 0

/-- sigma_g as listed in symmetry_exact.txt: line i goes to line sigma_g(i). -/
def SIG : List (List Nat) := {json.dumps(sigs)}

def sig (g i : Nat) : Nat := (SIG.getD g []).getD i 0

/-- Composition table (computed by the exporter, checked below): sigma_(tab g h) = sigma_g o sigma_h. -/
def TAB : List (List Nat) := {json.dumps(tab)}

def tab (g h : Nat) : Nat := (TAB.getD g []).getD h 0

def W (i : Nat) (w : Bool) (c : Nat) : Z2 := if w then V i c else U i c

/-- Coordinate t of M_g applied to the spanning vector W i w of line i. -/
def MW (g i : Nat) (w : Bool) (t : Nat) : Z2 :=
  M g t 0 * W i w 0 + M g t 1 * W i w 1 + M g t 2 * W i w 2 + M g t 3 * W i w 3

/-- Cramer test: m * x = a * U j + b * V j with m = pl j p r (nonzero) and a, b the Cramer numerators. -/
def spanAt (x : Nat → Z2) (j p r : Nat) : Bool :=
  decide (pl j p r ≠ 0) && (List.range 4).all (fun t =>
    decide (pl j p r * x t = (x p * V j r - x r * V j p) * U j t + (U j p * x r - U j r * x p) * V j t))

def PAIRS : List (Nat × Nat) := [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

def spanOK (g i : Nat) (w : Bool) : Bool := PAIRS.any (fun pr => spanAt (MW g i w) (sig g i) pr.1 pr.2)

def spanRow (g : Nat) : Bool := g ≥ 32 || (List.range 56).all (fun i => spanOK g i false && spanOK g i true)

{chunked("span_all", "spanRow", 32, 2)}

theorem div_span {{K : Type*}} [Field K] (m x a b u v : K) (hm : m ≠ 0) (h : m * x = a * u + b * v) :
    x = a / m * u + b / m * v := by
  field_simp; linear_combination h

/-- **L2b.** Over any field of characteristic zero with s*s = 2: M_g maps each spanning vector of
line i into line sigma_g(i) (so M_g maps line i into, hence onto, line sigma_g(i)). -/
theorem maps_lines {{K : Type*}} [Field K] [CharZero K] (s : K) (hs : s * s = 2) (g : Fin 32)
    (i : Fin 56) (w : Bool) :
    ∃ α β : K, ∀ t : Nat, t < 4 →
      iota s hs (M g t 0) * iota s hs (W i w 0) + iota s hs (M g t 1) * iota s hs (W i w 1)
        + iota s hs (M g t 2) * iota s hs (W i w 2) + iota s hs (M g t 3) * iota s hs (W i w 3)
      = α * iota s hs (U (sig g i) t) + β * iota s hs (V (sig g i) t) := by
  have hg := span_all g g.isLt
  simp only [spanRow, Bool.or_eq_true, decide_eq_true_eq, show ¬ ((g : Nat) ≥ 32) from by omega,
    false_or] at hg
  have h := List.all_eq_true.mp hg i (List.mem_range.mpr i.isLt)
  simp only [Bool.and_eq_true] at h
  have h' : spanOK g i w = true := by cases w; exact h.1; exact h.2
  simp only [spanOK, List.any_eq_true] at h'
  obtain ⟨⟨p, r⟩, -, hpr⟩ := h'
  simp only [spanAt, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range] at hpr
  obtain ⟨hm, heq⟩ := hpr
  have hm' : iota s hs (pl (sig g i) p r) ≠ 0 := fun h0 => hm (iota_injective s hs (by rw [h0, map_zero]))
  refine ⟨iota s hs (MW g i w p * V (sig g i) r - MW g i w r * V (sig g i) p) / iota s hs (pl (sig g i) p r),
    iota s hs (U (sig g i) p * MW g i w r - U (sig g i) r * MW g i w p) / iota s hs (pl (sig g i) p r),
    fun t ht => ?_⟩
  have hmw : iota s hs (MW g i w t) = iota s hs (M g t 0) * iota s hs (W i w 0)
      + iota s hs (M g t 1) * iota s hs (W i w 1) + iota s hs (M g t 2) * iota s hs (W i w 2)
      + iota s hs (M g t 3) * iota s hs (W i w 3) := by
    simp only [MW, map_add, map_mul]
  rw [← hmw]
  refine div_span _ _ _ _ _ _ hm' ?_
  rw [← map_mul (iota s hs), ← map_mul (iota s hs), ← map_mul (iota s hs), ← map_add (iota s hs)]
  exact congrArg (iota s hs) (heq t ht)

/-- Entry (a, b) of the matrix product M_g M_h. -/
def MM (g h a b : Nat) : Z2 := M g a 0 * M h 0 b + M g a 1 * M h 1 b + M g a 2 * M h 2 b + M g a 3 * M h 3 b

def IDX : List (Nat × Nat) := (List.range 4).flatMap (fun a => (List.range 4).map (fun b => (a, b)))

/-- M_g M_h is a nonzero multiple of M_(tab g h): with (a0, b0) the first nonzero entry of M_k,
MM(a, b) * M_k(a0, b0) = M_k(a, b) * MM(a0, b0) for all (a, b), and MM(a0, b0) is nonzero. -/
def projEq (g h : Nat) : Bool :=
  let k := tab g h
  match IDX.find? (fun ab => decide (M k ab.1 ab.2 ≠ 0)) with
  | none => false
  | some (a0, b0) => decide (MM g h a0 b0 ≠ 0) &&
      IDX.all (fun ab => decide (MM g h ab.1 ab.2 * M k a0 b0 = M k ab.1 ab.2 * MM g h a0 b0))

/-- **L2c (group).** sigma_0 is the identity; every sigma_g is a permutation of the 56 lines;
the 32 permutations are pairwise different; the set is closed under composition
(sigma_(tab g h) = sigma_g o sigma_h) and the matrices compose the same way up to a nonzero scalar;
every element has an inverse in the set. Hence the 32 maps form a group of order 32. -/
theorem group_facts :
    (SIG.length == 32 &&
     (List.range 56).all (fun i => sig 0 i == i) &&
     SIG.all (fun l => l.length == 56 && (List.range 56).all (fun x => l.contains x)) &&
     (List.range 32).all (fun g => (List.range 32).all (fun h => g == h || SIG.getD g [] != SIG.getD h [])) &&
     (List.range 32).all (fun g => (List.range 32).any (fun h => tab g h == 0))) = true := by
  decide +kernel

/-- Row g of the closure check: for every h, tab g h < 32 and sigma_(tab g h) = sigma_g o sigma_h. -/
def compRow (g : Nat) : Bool := g ≥ 32 || (List.range 32).all (fun h =>
  decide (tab g h < 32) && (List.range 56).all (fun i => sig (tab g h) i == sig g (sig h i)))

{chunked("group_closed", "compRow", 32, 4)}

/-- Row g of the matrix check: M_g M_h is a nonzero multiple of M_(tab g h) for every h. -/
def projRow (g : Nat) : Bool := g ≥ 32 || (List.range 32).all (fun h => projEq g h)

{chunked("matrices_compose", "projRow", 32, 4)}

def powIdx (g : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => tab g (powIdx g n)

/-- Order of g: least n in 1..8 with g^n = identity (0 if none). -/
def order (g : Nat) : Nat := ((List.range' 1 8).find? (fun n => powIdx g n == 0)).getD 0

/-- **L2d.** Element orders: 1 element of order 1, 15 of order 2, 8 of order 4, 8 of order 8. -/
theorem order_counts :
    (List.range 32).map order = {json.dumps(orders)} ∧
    ((List.range 32).map order).count 1 = 1 ∧ ((List.range 32).map order).count 2 = 15 ∧
    ((List.range 32).map order).count 4 = 8 ∧ ((List.range 32).map order).count 8 = 8 := by
  decide +kernel

/-- The orbit of line i: all images sigma_g(i). -/
def orbit (i : Nat) : List Nat := ((List.range 32).map (fun g => sig g i)).dedup

/-- **L2e.** Orbits on the 56 lines: representatives {reps} with sizes {sizes};
every line lies in exactly one of these orbits. -/
theorem orbit_sizes :
    {json.dumps(reps)}.map (fun r => (orbit r).length) = {json.dumps(sizes)} ∧
    (List.range 56).all (fun i => ({json.dumps(reps)}.filter (fun r => (orbit r).contains i)).length == 1) = true := by
  decide +kernel

end Y56
"""
    write("Y56_L2_neg.lean" if mutate else "Y56_L2.lean", body)


# ------------------------------------------------------------------ L3
L3_BODY = r'''
/-! ## Intersection graph -/

/-- 4 x 4 determinant with rows a, b, c, d (Laplace expansion along the first two rows). -/
def det4 {R : Type*} [CommRing R] (a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3 : R) : R :=
  (a0 * b1 - a1 * b0) * (c2 * d3 - c3 * d2) - (a0 * b2 - a2 * b0) * (c1 * d3 - c3 * d1)
  + (a0 * b3 - a3 * b0) * (c1 * d2 - c2 * d1) + (a1 * b2 - a2 * b1) * (c0 * d3 - c3 * d0)
  - (a1 * b3 - a3 * b1) * (c0 * d2 - c2 * d0) + (a2 * b3 - a3 * b2) * (c0 * d1 - c1 * d0)

theorem det4_map {R : Type*} [CommRing R] (f : Z2 →+* R)
    (a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3 : Z2) :
    f (det4 a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3) = det4 (f a0) (f a1) (f a2) (f a3)
      (f b0) (f b1) (f b2) (f b3) (f c0) (f c1) (f c2) (f c3) (f d0) (f d1) (f d2) (f d3) := by
  simp only [det4, map_add, map_sub, map_mul]

/-- Cramer: y1 * det = det with row 1 replaced by y1 a + y2 b + y3 c + y4 d. -/
theorem cramer1 {R : Type*} [CommRing R] (y1 y2 y3 y4 a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3 : R) :
    y1 * det4 a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3 =
      det4 (y1 * a0 + y2 * b0 + y3 * c0 + y4 * d0) (y1 * a1 + y2 * b1 + y3 * c1 + y4 * d1)
        (y1 * a2 + y2 * b2 + y3 * c2 + y4 * d2) (y1 * a3 + y2 * b3 + y3 * c3 + y4 * d3)
        b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3 := by
  simp only [det4]; ring

/-- Cramer: y2 * det = det with row 2 replaced by y1 a + y2 b + y3 c + y4 d. -/
theorem cramer2 {R : Type*} [CommRing R] (y1 y2 y3 y4 a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3 : R) :
    y2 * det4 a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 d0 d1 d2 d3 =
      det4 a0 a1 a2 a3 (y1 * a0 + y2 * b0 + y3 * c0 + y4 * d0) (y1 * a1 + y2 * b1 + y3 * c1 + y4 * d1)
        (y1 * a2 + y2 * b2 + y3 * c2 + y4 * d2) (y1 * a3 + y2 * b3 + y3 * c3 + y4 * d3)
        c0 c1 c2 c3 d0 d1 d2 d3 := by
  simp only [det4]; ring

/-- det [U i; V i; U j; V j] in Z[sqrt 2]. -/
def D (i j : Nat) : Z2 :=
  det4 (U i 0) (U i 1) (U i 2) (U i 3) (V i 0) (V i 1) (V i 2) (V i 3)
    (U j 0) (U j 1) (U j 2) (U j 3) (V j 0) (V j 1) (V j 2) (V j 3)

/-- i and j are adjacent in the stored graph (neighbour lists built from edges.json). -/
def isEdge (i j : Nat) : Bool := (NB.getD i []).contains j

/-- Minor of (U j; V j; W) with W = V i (if w) or U i, column d dropped. -/
def minorZ (i j : Nat) (w : Bool) (d : Nat) : Z2 :=
  let c := cols d
  let W := fun k => if w then V i k else U i k
  det3 (U j c.1) (U j c.2.1) (U j c.2.2) (V j c.1) (V j c.2.1) (V j c.2.2) (W c.1) (W c.2.1) (W c.2.2)

def PAIRS : List (Nat × Nat) := [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

/-- Candidate common point: a U i + b V i with (a, b) killing one 3 x 3 minor against line j,
written as c U j + d V j by Cramer (everything scaled by the Pluecker coordinate k = pl j p r). -/
def witnesses (i j : Nat) : List (Z2 × Z2 × Z2 × Z2) :=
  [0, 1, 2, 3].flatMap (fun d =>
    let a := minorZ i j true d
    let b := -minorZ i j false d
    PAIRS.map (fun pr =>
      let p := pr.1
      let r := pr.2
      let x := fun t => a * U i t + b * V i t
      let k := pl j p r
      (k * a, k * b, x p * V j r - x r * V j p, U j p * x r - U j r * x p)))

def witOK (i j : Nat) (w : Z2 × Z2 × Z2 × Z2) : Bool :=
  (decide (w.1 ≠ 0) || decide (w.2.1 ≠ 0)) && (List.range 4).all (fun t =>
    decide (w.1 * U i t + w.2.1 * V i t = w.2.2.1 * U j t + w.2.2.2 * V j t))

def meetOK (i j : Nat) : Bool :=
  i == j || (if isEdge i j then (witnesses i j).any (witOK i j) else decide (D i j ≠ 0))

def meetRow (i : Nat) : Bool := i ≥ 56 || (List.range 56).all (fun j => meetOK i j)

@CHUNK_MEET@

/-- Lines i and j (as lines over R) share a point: a nonzero point of line i lies on line j. -/
def Meets {R : Type*} [CommRing R] (s : R) (hs : s * s = 2) (i j : Nat) : Prop :=
  ∃ a b c d : R, (a ≠ 0 ∨ b ≠ 0) ∧ ∀ t : Nat, t < 4 →
    a * iota s hs (U i t) + b * iota s hs (V i t) = c * iota s hs (U j t) + d * iota s hs (V j t)

/-- **L3a.** Over any domain of characteristic zero with s*s = 2 (ℝ, ℂ, ...): for i ≠ j,
lines i and j meet exactly when {i, j} is one of the 448 listed edges. -/
theorem meets_iff_edge {R : Type*} [CommRing R] [IsDomain R] [CharZero R] (s : R) (hs : s * s = 2)
    (i j : Fin 56) (hij : i ≠ j) : Meets s hs i j ↔ isEdge i j = true := by
  have hne : (i : Nat) ≠ j := Fin.val_injective.ne hij
  have hi := meet_all i i.isLt
  simp only [meetRow, Bool.or_eq_true, decide_eq_true_eq, show ¬ ((i : Nat) ≥ 56) from by omega,
    false_or] at hi
  have hc := List.all_eq_true.mp hi j (List.mem_range.mpr j.isLt)
  simp only [meetOK, Bool.or_eq_true, beq_iff_eq, hne, false_or] at hc
  have inj := iota_injective s hs
  constructor
  · rintro ⟨a, b, c, d, hab, h⟩
    by_contra hE
    simp only [hE, Bool.false_eq_true, ite_false, decide_eq_true_eq] at hc
    have hD : iota s hs (D i j) ≠ 0 := fun h0 => hc (inj (by rw [h0, map_zero]))
    have z : ∀ t : Nat, t < 4 → a * iota s hs (U i t) + b * iota s hs (V i t)
        + (-c) * iota s hs (U j t) + (-d) * iota s hs (V j t) = 0 := by
      intro t ht; linear_combination h t ht
    have z0 := z 0 (by norm_num); have z1 := z 1 (by norm_num)
    have z2 := z 2 (by norm_num); have z3 := z 3 (by norm_num)
    have ha : a * iota s hs (D i j) = 0 := by
      simp only [D, det4_map]
      rw [cramer1 a b (-c) (-d), z0, z1, z2, z3]; simp [det4]
    have hb : b * iota s hs (D i j) = 0 := by
      simp only [D, det4_map]
      rw [cramer2 a b (-c) (-d), z0, z1, z2, z3]; simp [det4]
    rcases hab with hab | hab
    · exact hab ((mul_eq_zero.mp ha).resolve_right hD)
    · exact hab ((mul_eq_zero.mp hb).resolve_right hD)
  · intro hE
    simp only [hE, ite_true, List.any_eq_true] at hc
    obtain ⟨w, -, hw⟩ := hc
    simp only [witOK, Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq, List.all_eq_true,
      List.mem_range] at hw
    obtain ⟨hnz, heq⟩ := hw
    refine ⟨iota s hs w.1, iota s hs w.2.1, iota s hs w.2.2.1, iota s hs w.2.2.2, ?_, ?_⟩
    · rcases hnz with h0 | h0
      · exact Or.inl (fun h1 => h0 (inj (by rw [h1, map_zero])))
      · exact Or.inr (fun h1 => h0 (inj (by rw [h1, map_zero])))
    · intro t ht
      have e := congrArg (iota s hs) (heq t ht)
      simp only [map_add, map_mul] at e
      exact e

/-- Strictly increasing (lexicographic) list of pairs: hence no repeats. -/
def strictInc : List (Nat × Nat) → Bool
  | a :: b :: t => (decide (a.1 < b.1) || (a.1 == b.1 && decide (a.2 < b.2))) && strictInc (b :: t)
  | _ => true

/-- **L3b.** The neighbour lists: 56 lists, each with exactly 16 entries, no repeats, all < 56,
symmetric (j is a neighbour of i iff i is a neighbour of j), no loops; and the edge list of
edges.json is exactly the set of pairs (i, j), i < j, j a neighbour of i, listed in strictly
increasing order with 448 entries. So the graph "lines meet" (L3a) has 448 edges and is 16-regular;
1540 - 448 = 1092 pairs of distinct lines are skew. -/
theorem edge_counts :
    NB.length = 56 ∧
    (List.range 56).all (fun i => (NB.getD i []).length == 16 && !(NB.getD i []).contains i &&
       (NB.getD i []).all (fun j => decide (j < 56) && (NB.getD j []).contains i)) = true ∧
    (List.range 56).flatMap (fun i => ((NB.getD i []).filter (fun j => decide (i < j))).map (fun j => (i, j)))
      = EDGES ∧
    strictInc EDGES = true ∧ EDGES.length = 448 ∧ 56 * 55 / 2 - 448 = 1092 := by
  decide +kernel
'''


def gen_L3(mutate=False):
    U, V, scales = read_lines()
    E = read_edges()
    if mutate:  # negative control: drop one edge from the list
        E = E[1:]
    nb = [sorted({b for a, b in E if a == i} | {a for a, b in E if b == i}) for i in range(56)]
    body = (PRELUDE + lines_data(U, V, scales)
            + f"/-- The 448 edges of edges.json (pairs i < j of lines that meet). -/\n"
              f"def EDGES : List (Nat × Nat) := [{', '.join(f'({a}, {b})' for a, b in E)}]\n\n"
              f"/-- Neighbour lists, read off edges.json (checked against EDGES in edge_counts). -/\n"
              f"def NB : List (List Nat) := {json.dumps(nb)}\n"
            + L3_BODY.replace("@CHUNK_MEET@", chunked("meet_all", "meetRow", 56, 2)) + "\nend Y56\n")
    write("Y56_L3_neg.lean" if mutate else "Y56_L3.lean", body)


# ------------------------------------------------------------------ L6
def gen_L6(mutate=False):
    U, V, scales = read_lines()
    E = read_edges()
    P2, P4, PC = read_planes()
    assert (len(P2), len(P4), len(PC)) == (148, 50, 20), (len(P2), len(P4), len(PC))
    planes = P2 + P4
    if mutate:  # negative control: delete one two-line plane
        planes = planes[1:]
    n2 = 147 if mutate else 148
    nb = [sorted({b for a, b in E if a == i} | {a for a, b in E if b == i}) for i in range(56)]
    body = (PRELUDE + lines_data(U, V, scales)
            + f"def EDGES : List (Nat × Nat) := [{', '.join(f'({a}, {b})' for a, b in E)}]\n\n"
            + f"/-- Neighbour lists from edges.json (L3 proves: lines i, j meet iff j is in NB i). -/\n"
              f"def NB : List (List Nat) := {json.dumps(nb)}\n\n"
            + "/-- Normals of the stored planes (planes_exact.txt): first the 148 two-line planes, then the\n"
              "50 four-line planes; each scaled by a positive integer. Plane = {z : n . z = 0}. -/\n"
            + "def PN : List (List Z2) := [\n  " + ",\n  ".join(lvec(n) for n, _ in planes) + "]\n\n"
            + "/-- Lines listed for each stored plane in planes_exact.txt. -/\n"
            + f"def PL : List (List Nat) := {json.dumps([l for _, l in planes])}\n\n"
            + "/-- Normals of the 20 conic-pair planes (planes_exact.txt, PC rows). -/\n"
            + "def PCN : List (List Z2) := [\n  " + ",\n  ".join(lvec(n) for n in PC) + "]\n"
            + L6_BODY.replace("@CHUNK_PLANE@", chunked("plane_rows", "planeRow", len(planes), 11))
                     .replace("@CHUNK_COVER@", chunked("edge_cover", "coverRow", 448, 32))
                     .replace("@CHUNK_PC@", chunked("pc_rows", "pcRow", 20, 5))
                     .replace("@CHUNK_DIST@", chunked("dist_rows", "distRow", 218 - (198 - len(planes)), 6))
                     .replace("@NP@", str(len(planes))).replace("@N2@", str(n2))
            + "\nend Y56\n")
    write("Y56_L6_neg.lean" if mutate else "Y56_L6.lean", body)


L6_BODY = r'''
def dot (n : List Z2) (x : Nat → Z2) : Z2 :=
  n.getD 0 0 * x 0 + n.getD 1 0 * x 1 + n.getD 2 0 * x 2 + n.getD 3 0 * x 3

/-- Line i lies in the plane with normal n: n . U i = 0 and n . V i = 0. -/
def inPlane (n : List Z2) (i : Nat) : Bool := decide (dot n (U i) = 0) && decide (dot n (V i) = 0)

def linesIn (n : List Z2) : List Nat := (List.range 56).filter (inPlane n)

/-- Normals n, n' are proportional (same plane) iff all cross products vanish. -/
def sameNormal (n n' : List Z2) : Bool :=
  [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)].all (fun pr =>
    decide (n.getD pr.1 0 * n'.getD pr.2 0 = n.getD pr.2 0 * n'.getD pr.1 0))

def ALLN : List (List Z2) := PN ++ PCN

/-- **L6a.** For each stored plane, the lines it contains (computed from coordinates) are
exactly the listed ones; the first @N2@ contain exactly 2 lines, the last 50 exactly 4; the 20
conic-pair planes contain no line; all stored normals are nonzero and the @NP@ + 20 planes are
pairwise different. -/
theorem planes_lines :
    PN.length = @NP@ ∧ PL.length = @NP@ ∧
    PL.map List.length = List.replicate @N2@ 2 ++ List.replicate 50 4 ∧
    PCN.length = 20 ∧
    (ALLN.all fun n => n.any fun x => decide (x ≠ 0)) = true := by
  decide +kernel

/-- Row p: for every line i, line i lies in stored plane p iff it is listed for p. -/
def planeRow (p : Nat) : Bool :=
  p ≥ @NP@ || (List.range 56).all (fun i => inPlane (PN.getD p []) i == (PL.getD p []).contains i)

@CHUNK_PLANE@

/-- Row c: conic-pair plane c contains no line. -/
def pcRow (c : Nat) : Bool := c ≥ 20 || linesIn (PCN.getD c []) == []

@CHUNK_PC@

/-- Row a: normal a is not proportional to any other stored normal b (all @NP@ + 20 planes). -/
def distRow (a : Nat) : Bool :=
  a ≥ ALLN.length || (List.range ALLN.length).all fun b => a == b || !sameNormal (ALLN.getD a []) (ALLN.getD b [])

@CHUNK_DIST@

/-- Entry k of the normal of stored plane p. -/
def nrm (p k : Nat) : Z2 := (PN.getD p []).getD k 0

theorem inPlane_iff_listed (p : Fin @NP@) (i : Fin 56) :
    inPlane (PN.getD p []) i = (PL.getD p []).contains i := by
  have h := plane_rows p (by omega)
  simp only [planeRow, Bool.or_eq_true, decide_eq_true_eq, show ¬ ((p : Nat) ≥ @NP@) from by omega,
    false_or] at h
  have := List.all_eq_true.mp h i (List.mem_range.mpr i.isLt)
  simpa using this

/-- All pairs i < j of a list (as given, increasing). -/
def pairsOf : List Nat → List (Nat × Nat)
  | [] => []
  | x :: xs => xs.map (fun y => (x, y)) ++ pairsOf xs

def PLANEPAIRS : List (Nat × Nat) := PL.flatMap pairsOf

def isEdge (i j : Nat) : Bool := (NB.getD i []).contains j

/-- **L6b.** Every pair of lines lying in a common stored plane is an edge (the lines meet), and
there are @N2@ * 1 + 50 * 6 = 448 such pairs counted with multiplicity, as many as edges. -/
theorem plane_pairs_are_edges :
    PLANEPAIRS.length = 448 ∧ (PLANEPAIRS.all fun e => isEdge e.1 e.2) = true ∧
    EDGES.length = 448 ∧ @N2@ * 1 + 50 * 6 = 448 := by
  decide +kernel

/-- Row k of the edge cover: edge number k lies in exactly one stored plane (by its listed lines). -/
def coverRow (k : Nat) : Bool :=
  k ≥ 448 || (let e := EDGES.getD k (0, 0)
    (PL.filter (fun l => l.contains e.1 && l.contains e.2)).length == 1)

@CHUNK_COVER@

/-- **L6c.** Geometric reading of L6a over any ring of characteristic zero with s*s = 2:
line i lies in plane p (every point of the line satisfies n . z = 0) iff i is listed for p. -/
theorem line_in_plane_iff {R : Type*} [CommRing R] [CharZero R] (s : R) (hs : s * s = 2)
    (p : Fin @NP@) (i : Fin 56) :
    (∀ l m : R,
      iota s hs (nrm p 0) * (l * iota s hs (U i 0) + m * iota s hs (V i 0))
      + iota s hs (nrm p 1) * (l * iota s hs (U i 1) + m * iota s hs (V i 1))
      + iota s hs (nrm p 2) * (l * iota s hs (U i 2) + m * iota s hs (V i 2))
      + iota s hs (nrm p 3) * (l * iota s hs (U i 3) + m * iota s hs (V i 3)) = 0)
    ↔ (PL.getD p []).contains i = true := by
  rw [← inPlane_iff_listed p i]
  have inj := iota_injective s hs
  have hdot : ∀ x : Nat → Z2, iota s hs (dot (PN.getD p []) x) =
      iota s hs (nrm p 0) * iota s hs (x 0) + iota s hs (nrm p 1) * iota s hs (x 1)
      + iota s hs (nrm p 2) * iota s hs (x 2) + iota s hs (nrm p 3) * iota s hs (x 3) := by
    intro x; simp only [dot, nrm, map_add, map_mul]
  constructor
  · intro h
    have h1 := h 1 0
    have h2 := h 0 1
    simp only [inPlane, Bool.and_eq_true, decide_eq_true_eq]
    constructor
    · apply inj; rw [hdot, map_zero]; linear_combination h1
    · apply inj; rw [hdot, map_zero]; linear_combination h2
  · intro h l m
    simp only [inPlane, Bool.and_eq_true, decide_eq_true_eq] at h
    have e1 := congrArg (iota s hs) h.1
    have e2 := congrArg (iota s hs) h.2
    rw [hdot, map_zero] at e1 e2
    linear_combination l * e1 + m * e2
'''


# ------------------------------------------------------------------ L5
L5_HEAD = r'''
/-! ## Plane sections

Each plane n . z = 0 is parametrised by z = x p1 + y p2 + w p3 with p_c = n_k e_c - n_c e_k for
the three coordinates c other than a pivot k with n_k nonzero (so n . p_c = 0 and the p_c span
the plane). Conic coefficients are listed in the order (x^2, y^2, w^2, xy, xw, yw).
-/

/-- The conic with coefficient list c, evaluated over R via iota. -/
def conicEval {R : Type*} [CommRing R] (s : R) (hs : s * s = 2) (c : List Z2) (x y w : R) : R :=
  iota s hs (c.getD 0 0) * x ^ 2 + iota s hs (c.getD 1 0) * y ^ 2 + iota s hs (c.getD 2 0) * w ^ 2
    + iota s hs (c.getD 3 0) * x * y + iota s hs (c.getD 4 0) * x * w + iota s hs (c.getD 5 0) * y * w

/-- Determinant of the Hessian matrix [[2a, d, e], [d, 2b, f], [e, f, 2c]] of the conic. -/
def hess {R : Type*} [CommRing R] (a b c d e f : R) : R := det3 (2 * a) d e d (2 * b) f e f (2 * c)

def hessL (c : List Z2) : Z2 := hess (c.getD 0 0) (c.getD 1 0) (c.getD 2 0) (c.getD 3 0) (c.getD 4 0) (c.getD 5 0)

/-- A product of two linear forms has Hessian determinant 0 (polynomial identity). -/
theorem hess_product {R : Type*} [CommRing R] (a b c a' b' c' : R) :
    hess (a * a') (b * b') (c * c') (a * b' + a' * b) (a * c' + a' * c) (b * c' + b' * c) = 0 := by
  simp only [hess, det3]; ring

/-- A conic whose Hessian determinant is a nonzero element of Z[sqrt 2] is not a product of two
linear forms over any ring of characteristic zero with s*s = 2 (so it is irreducible, in
particular over ℝ and ℂ). -/
theorem conic_irreducible {R : Type*} [CommRing R] [CharZero R] (s : R) (hs : s * s = 2)
    (c : List Z2) (hc : hessL c ≠ 0) :
    ¬ ∃ a b d a' b' d' : R,
      iota s hs (c.getD 0 0) = a * a' ∧ iota s hs (c.getD 1 0) = b * b' ∧ iota s hs (c.getD 2 0) = d * d' ∧
      iota s hs (c.getD 3 0) = a * b' + a' * b ∧ iota s hs (c.getD 4 0) = a * d' + a' * d ∧
      iota s hs (c.getD 5 0) = b * d' + b' * d := by
  rintro ⟨a, b, d, a', b', d', h0, h1, h2, h3, h4, h5⟩
  apply hc
  apply iota_injective s hs
  have : iota s hs (hessL c) = hess (iota s hs (c.getD 0 0)) (iota s hs (c.getD 1 0))
      (iota s hs (c.getD 2 0)) (iota s hs (c.getD 3 0)) (iota s hs (c.getD 4 0)) (iota s hs (c.getD 5 0)) := by
    simp only [hessL, hess, det3, map_add, map_sub, map_mul, map_ofNat]
  rw [this, h0, h1, h2, h3, h4, h5, hess_product, map_zero]
'''


def plane_param(n):
    """pivot k (prefer a rational entry of small size), and the three spanning vectors p_c."""
    cand = [k for k in range(4) if n[k] != (0, 0)]
    k = min(cand, key=lambda t: (n[t][1] != 0, abs(n[t][0]) + abs(n[t][1])))
    others = [c for c in range(4) if c != k]
    ps = []
    for c in others:
        p = [(0, 0)] * 4
        p[c] = n[k]
        p[k] = (-n[c][0], -n[c][1])
        ps.append(p)
    return k, others, ps


def q2_mul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gen_L5(part):
    U, V, scales = read_lines()
    P2, P4, PC = read_planes()
    s, x, y, w = sp.symbols("s x y w")
    X = (x, y, w)

    def zq(a):  # Z2 pair -> expression in s
        return sp.Integer(a[0]) + sp.Integer(a[1]) * s

    def to_s(ex):  # Q(sqrt2)-expression -> s-expression (exact)
        ex = sp.expand(ex)
        return ex.subs(SQ2, s)

    def coeffs6(Qs):  # quadratic form in x,y,w with sqrt2 -> six Z2 pairs (must be integral)
        P = sp.Poly(sp.expand(Qs), *X)
        out = []
        for mon in [(2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]:
            a, b = to_q2(P.coeff_monomial(x**mon[0] * y**mon[1] * w**mon[2]))
            assert a.denominator == 1 and b.denominator == 1
            out.append((int(a), int(b)))
        return out

    def clear(ex):  # scale a polynomial over Q(sqrt2) to Z[sqrt2] coefficients by a positive integer
        P = sp.Poly(sp.expand(ex), *X)
        L = 1
        for c in P.coeffs():
            a, b = to_q2(c)
            L = lcm(L, a.denominator, b.denominator)
        return L

    def lean_lin(vec):  # Z2 coefficients on (x, y, w) -> Lean term in s, x, y, w
        return lean_poly(sum(zq(c) * v for c, v in zip(vec, X)), [s, x, y, w])

    thms, conics = [], []
    if part == "a":
        planes = [(n, ls, "P2") for n, ls in P2]
    elif part == "b":
        planes = [(n, ls, "P4") for n, ls in P4]
    else:
        planes = [(n, [], "PC") for n in PC]
    for idx, (n, ls, kind) in enumerate(planes):
        k, others, ps = plane_param(n)
        Pz = [sum(sym_q2(ps[j][t]) * X[j] for j in range(3)) for t in range(4)]   # sqrt2 form
        Fp = sp.expand(Fsym(SQ2, *Pz))
        lins = []
        for i in ls:
            cu = [U[i][c] for c in others]
            cv = [V[i][c] for c in others]
            cr = [q2_sub(q2_mul(cu[1], cv[2]), q2_mul(cu[2], cv[1])),
                  q2_sub(q2_mul(cu[2], cv[0]), q2_mul(cu[0], cv[2])),
                  q2_sub(q2_mul(cu[0], cv[1]), q2_mul(cu[1], cv[0]))]
            lins.append(cr)
        linprod = sp.Integer(1)
        for cr in lins:
            linprod *= sum(sym_q2(c) * v for c, v in zip(cr, X))
        rhs_parts = [f"({lean_lin(cr)})" for cr in lins]
        cs = []
        if kind == "PC":
            const, facs = sp.factor_list(Fp, *X, extension=SQ2)
            assert len(facs) == 2 and all(e == 1 and sp.Poly(f, *X).total_degree() == 2 for f, e in facs), (idx, facs)
            fl = [f for f, _ in facs]
            k1, k2 = clear(fl[0]), clear(fl[1])
            Q1, Q2 = sp.expand(k1 * fl[0]), sp.expand(k2 * fl[1])
            r = sp.nsimplify(const) / (k1 * k2)
            rest = Q1 * Q2
            cs = [coeffs6(Q1), coeffs6(Q2)]
        else:
            qq, rr = sp.div(sp.Poly(Fp, *X, extension=SQ2), sp.Poly(sp.expand(linprod), *X, extension=SQ2))
            assert rr.is_zero, (kind, idx)
            Q = sp.expand(qq.as_expr())
            if kind == "P2":
                kq = clear(Q)
                Q1 = sp.expand(kq * Q)
                r = sp.Rational(1, kq)
                rest = Q1
                cs = [coeffs6(Q1)]
            else:
                r = sp.expand(Q)   # a constant in Q(sqrt2)
                assert sp.Poly(r, *X).total_degree() <= 0
                rest = sp.Integer(1)
        ra, rb = to_q2(r)
        K = lcm(ra.denominator, rb.denominator)
        C = (int(ra * K), int(rb * K))
        # identity: K * F(P) = C * lines * rest   (all over Z[sqrt2])
        assert sp.expand(K * Fp - sym_q2(C) * linprod * rest) == 0, (kind, idx)
        nm = f"sec{kind}_{idx:03d}"
        cdefs = ""
        conic_terms = []
        for ci, c6 in enumerate(cs):
            cn = f"cq{kind}_{idx:03d}_{ci}"
            cdefs += f"def {cn} : List Z2 := {lvec(c6)}\n"
            conic_terms.append(f"conicEval s hs {cn} x y w")
            conics.append(cn)
        Ps = [lean_poly(to_s(Pz[t]), [s, x, y, w]) for t in range(4)]
        rhs = " * ".join([f"({lean_poly(zq(C), [s])})"] + rhs_parts + conic_terms)
        # cofactor for linear_combination: (K F(P) - C * lines * rest) in s, reduced mod s^2 - 2
        rest_s = sp.Integer(1)
        for c6 in cs:
            rest_s *= sum(zq(cc) * mm for cc, mm in zip(c6, [x**2, y**2, w**2, x*y, x*w, y*w]))
        lin_s = sp.Integer(1)
        for cr in lins:
            lin_s *= sum(zq(c) * v for c, v in zip(cr, X))
        Dd = sp.expand(K * Fsym(s, *[to_s(p) for p in Pz]) - zq(C) * lin_s * rest_s)
        qd, rd = sp.div(sp.Poly(Dd, s), sp.Poly(s**2 - 2, s))
        assert rd.is_zero, (kind, idx)
        cof = sp.expand(qd.as_expr())
        proof_lc = "ring" if cof == 0 else f"linear_combination ({lean_poly(cof, [s, x, y, w])}) * hs"
        unfold = (f"  simp only [{', '.join(['conicEval'] + [f'cq{kind}_{idx:03d}_{ci}' for ci in range(len(cs))])}, "
                  f"List.getD_cons_zero, List.getD_cons_succ, iota_q]\n  push_cast\n") if cs else ""
        thms.append(
            f"{cdefs}/-- {kind} plane #{idx}, normal {lvec(n)}, lines {ls}: {K} F = C * (lines) * (conics). -/\n"
            f"theorem {nm} {{R : Type*}} [CommRing R] (s : R) (hs : s * s = 2) (x y w : R) :\n"
            f"    {K} * F s ({Ps[0]}) ({Ps[1]}) ({Ps[2]}) ({Ps[3]})\n      = {rhs} := by\n"
            f"{unfold}  simp only [F]\n  {proof_lc}\n")
    body = PRELUDE + L5_HEAD + "\n" + "\n".join(thms)
    if conics:
        body += (f"\n/-- All conics of this file. -/\ndef CONICS : List (List Z2) := [{', '.join(conics)}]\n\n"
                 f"/-- **Nondegeneracy.** Every listed conic has nonzero Hessian determinant (so, by\n"
                 f"`conic_irreducible`, none is a product of two linear forms over ℝ or ℂ). -/\n"
                 f"theorem conics_nondegenerate : CONICS.length = {len(conics)} ∧ "
                 f"(CONICS.all fun c => decide (hessL c ≠ 0)) = true := by\n  decide +kernel\n")
    body += "\nend Y56\n"
    write(f"Y56_L5{part}.lean", body)


def q2_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


# ------------------------------------------------------------------ L8
def gen_L8():
    import random
    E = read_edges()
    adj = [[0] * 56 for _ in range(56)]
    for a, b in E:
        adj[a][b] = adj[b][a] = 1
    G = [[-2 if i == j else adj[i][j] for j in range(56)] for i in range(56)]

    def solve_rows(B):
        """Express every row of G as a rational combination of rows B (Gauss over Q); None if impossible."""
        n = len(B)
        M = [[Fraction(G[B[a]][m]) for m in range(56)] for a in range(n)]
        # least-squares free: solve c * M = row using pivot columns
        # row-reduce M^T style: find n pivot columns
        R = [row[:] + [Fraction(int(a == k)) for k in range(n)] for a, row in enumerate(M)]
        piv = []
        r = 0
        for col in range(56):
            p = next((t for t in range(r, n) if R[t][col] != 0), None)
            if p is None:
                continue
            R[r], R[p] = R[p], R[r]
            inv = 1 / R[r][col]
            R[r] = [v * inv for v in R[r]]
            for t in range(n):
                if t != r and R[t][col] != 0:
                    f = R[t][col]
                    R[t] = [vt - f * vr for vt, vr in zip(R[t], R[r])]
            piv.append(col)
            r += 1
        if r < n:
            return None
        coef = []
        for j in range(56):
            # c such that sum_a c_a M[a] = G[j]: using reduced rows, c = sum_t G[j][piv_t] * (combination t)
            c = [Fraction(0)] * n
            for t, col in enumerate(piv):
                for a in range(n):
                    c[a] += G[j][col] * R[t][56 + a]
            if any(sum(c[a] * M[a][m] for a in range(n)) != G[j][m] for m in range(56)):
                return None
            coef.append(c)
        return coef

    def det_frac(B):
        M = [[Fraction(G[a][b]) for b in B] for a in B]
        n, d = len(B), Fraction(1)
        for c in range(n):
            p = next((t for t in range(c, n) if M[t][c] != 0), None)
            if p is None:
                return Fraction(0)
            if p != c:
                M[c], M[p] = M[p], M[c]
                d = -d
            d *= M[c][c]
            for t in range(c + 1, n):
                f = M[t][c] / M[c][c]
                M[t] = [x - f * y for x, y in zip(M[t], M[c])]
        return d

    rng = random.Random(7)
    best = None
    for trial in range(4000):
        order = list(range(56))
        if trial:
            rng.shuffle(order)
        B = []
        for j in order:
            if len(B) == 20:
                break
            # keep leading principal minors nonzero (no pivoting needed in Lean's certificate)
            if det_frac(B + [j]) != 0:
                B.append(j)
        if len(B) < 20:
            continue
        d = det_frac(B)
        if abs(d) != 64:
            continue
        coef = solve_rows(B)
        if coef is None or any(x.denominator != 1 for c in coef for x in c):
            continue
        best = (B, d, coef)
        break
    assert best, "no basis found"
    B, d, coef = best
    n = 20
    GB = [[Fraction(G[a][b]) for b in B] for a in B]
    # LU without pivoting: L^{-1} GB = U ; A = diag(scale) L^{-1} integral, T = A GB
    Linv = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    Uu = [r[:] for r in GB]
    for c in range(n):
        assert Uu[c][c] != 0
        for t in range(c + 1, n):
            f = Uu[t][c] / Uu[c][c]
            Uu[t] = [x - f * y for x, y in zip(Uu[t], Uu[c])]
            Linv[t] = [x - f * y for x, y in zip(Linv[t], Linv[c])]
    A, T = [], []
    for i in range(n):
        sc = 1
        for x in Linv[i] + Uu[i]:
            sc = lcm(sc, x.denominator)
        A.append([int(x * sc) for x in Linv[i]])
        T.append([int(x * sc) for x in Uu[i]])
    for i in range(n):
        for j in range(n):
            assert sum(A[i][k] * GB[k][j] for k in range(n)) == T[i][j]
            if j > i:
                assert A[i][j] == 0
            if j < i:
                assert T[i][j] == 0
    PA = 1
    PT = 1
    for i in range(n):
        PA *= A[i][i]
        PT *= T[i][i]
    assert Fraction(PT, PA) == d
    nb = [sorted({b for a, b in E if a == i} | {a for a, b in E if b == i}) for i in range(56)]
    coefI = [[int(x) for x in c] for c in coef]
    S = [0, 6, 23, 24]
    body = PRELUDE + f"""
/-!
# Y56, item L8: the lattice spanned by the 56 line classes

G is the 56 x 56 intersection matrix of the lines: -2 on the diagonal (a line on a K3 surface is a
(-2)-curve: CITED, adjunction), 1 if the two lines meet, 0 otherwise ("meet" = adjacency in the
graph whose geometric meaning is proved in item L3). Proved here:
- the 20 lines BASIS have Gram matrix GB with det GB = {d} (exactly, as `Matrix.det`);
- every row of G is an integer combination of the 20 rows of BASIS.
Hence the numerical lattice spanned by the 56 classes (Z^56 modulo the kernel of G) is free of
rank 20 with discriminant {d}: the 20 basis classes are independent (det nonzero) and span.
Also: h = sum of the four lines of a four-line plane has h.h = 4 and h.L = 1 for every line L.
-/

def NB : List (List Nat) := {json.dumps(nb)}

def isEdge (i j : Nat) : Bool := (NB.getD i []).contains j

/-- Intersection numbers of the 56 lines. -/
def Gf (i j : Nat) : Int := if i = j then -2 else if isEdge i j then 1 else 0

def BASIS : List Nat := {json.dumps(B)}

def GBf (a b : Fin 20) : ℤ := Gf (BASIS.getD a 0) (BASIS.getD b 0)
def GB : Matrix (Fin 20) (Fin 20) ℤ := Matrix.of GBf

def AL : List (List Int) := {json.dumps(A)}
def TL : List (List Int) := {json.dumps(T)}

def Af (a b : Fin 20) : ℤ := (AL.getD a []).getD b 0
def Tf (a b : Fin 20) : ℤ := (TL.getD a []).getD b 0
def Am : Matrix (Fin 20) (Fin 20) ℤ := Matrix.of Af
def Tm : Matrix (Fin 20) (Fin 20) ℤ := Matrix.of Tf

theorem AG_entries : ∀ a b : Fin 20, (List.ofFn fun k : Fin 20 => Af a k * GBf k b).sum = Tf a b := by
  decide +kernel

theorem AG_eq : Am * GB = Tm := by
  ext a b
  rw [Matrix.mul_apply, ← List.sum_ofFn]
  exact AG_entries a b

theorem A_lower : ∀ a b : Fin 20, a < b → Af a b = 0 := by decide +kernel
theorem T_upper : ∀ a b : Fin 20, b < a → Tf a b = 0 := by decide +kernel

theorem A_diag : (List.ofFn fun i : Fin 20 => Af i i).prod = {PA} := by decide +kernel
theorem T_diag : (List.ofFn fun i : Fin 20 => Tf i i).prod = {PT} := by decide +kernel

/-- **L8a.** det GB = {d}. -/
theorem det_GB : GB.det = {d} := by
  have hA : Am.det = {PA} := by
    rw [Matrix.det_of_lowerTriangular Am (fun i j h => A_lower i j (by simpa using h)), ← List.prod_ofFn]
    exact A_diag
  have hT : Tm.det = {PT} := by
    rw [Matrix.det_of_upperTriangular (M := Tm) (fun i j h => T_upper i j h), ← List.prod_ofFn]
    exact T_diag
  have h := congrArg Matrix.det AG_eq
  rw [Matrix.det_mul, hA, hT] at h
  have hPA : ({PA} : ℤ) ≠ 0 := by norm_num
  apply mul_left_cancel₀ hPA
  rw [h]; norm_num

/-- Integer coefficients expressing row j of G through the 20 basis rows. -/
def COEF : List (List Int) := {json.dumps(coefI)}

def coef (j a : Nat) : Int := (COEF.getD j []).getD a 0

def relRow (j : Nat) : Bool :=
  j ≥ 56 || (List.range 56).all fun m =>
    Gf j m == ((List.range 20).map fun a => coef j a * Gf (BASIS.getD a 0) m).sum

{chunked("rel_rows", "relRow", 56, 4)}

/-- **L8b.** Every row of G is an integer combination of the 20 basis rows. -/
theorem rows_in_span (j : Nat) (hj : j < 56) (m : Nat) :
    Gf j m = ((List.range 20).map fun a => coef j a * Gf (BASIS.getD a 0) m).sum ∨ 56 ≤ m := by
  by_cases hm : m < 56
  · left
    have h := rel_rows j hj
    simp only [relRow, Bool.or_eq_true, decide_eq_true_eq, show ¬ (j ≥ 56) from by omega, false_or] at h
    have := List.all_eq_true.mp h m (List.mem_range.mpr hm)
    simpa using this
  · right; omega

/-- **L8c.** For the four-line plane with lines {S}: h = their sum has h.h = 4, and h.L = 1 for every
line L (each line meets the plane section once). -/
theorem hyperplane_class :
    (({json.dumps(S)}.map fun a => ({json.dumps(S)}.map fun b => Gf a b).sum).sum = 4) ∧
    (List.range 56).all (fun j => ({json.dumps(S)}.map fun a => Gf a j).sum == 1) = true := by
  decide +kernel

end Y56
"""
    write("Y56_L8.lean", body)


if __name__ == "__main__":
    items = sys.argv[1:] or ["L1"]
    if "L1" in items:
        gen_L1()
        gen_L1(mutate=True)
    if "L2" in items:
        gen_L2()
        gen_L2(mutate=True)
    if "L3" in items:
        gen_L3()
        gen_L3(mutate=True)
    if "L5" in items:
        for part in "abc":
            gen_L5(part)
        # negative control: perturb one coefficient of the first conic of the first conic-pair plane
        src = (HERE / "Y56_L5c.lean").read_text(encoding="utf-8")
        old = "def cqPC_000_0 : List Z2 := [q 14 0,"
        assert old in src
        write("Y56_L5c_neg.lean", src.replace(old, "def cqPC_000_0 : List Z2 := [q 15 0,", 1))
    if "L8" in items:
        gen_L8()
    if "neg" in items:  # negative controls for the hand-written files
        src = (HERE / "Y56_Pencil.lean").read_text(encoding="utf-8")
        old = "s = 3 * b ^ 2 ∧ a ^ 2 = 2 * b ^ 2 ∧ 2 * b ^ 8 = 1 ∧ 2 * s ^ 4 = 81 := by"
        assert old in src
        write("Y56_Pencil_neg.lean", src.replace(old, old.replace("= 81", "= 80"), 1))
        src = (HERE / "Y56_L7.lean").read_text(encoding="utf-8")
        old = "    F e z0 (-z2) z1 z3 = F (-e) z0 z1 z2 z3 := by"
        assert old in src
        write("Y56_L7_neg.lean", src.replace(old, "    F e z0 (-z2) z1 z3 = F e z0 z1 z2 z3 := by", 1))
    if "L6" in items:
        gen_L6()
        gen_L6(mutate=True)
