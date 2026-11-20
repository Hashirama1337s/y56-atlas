import Mathlib

/-!
# Y56, item L7: the eight-fold formula, the screw symmetry, the Galois twist

F = 3e z0^2 z1 z2 + 3e z1 z2 z3^2 - e z1^3 z2 - e z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3,  e = sqrt 2.
With w = z0 + i z3 and p = z1 + i z2:
  F = Im(w^4) + Im(p^2) (3|w|^2 - |p|^2) / sqrt 2.
-/

namespace Y56

/-- The Y56 quartic with `e` standing for sqrt 2. -/
def F {R : Type*} [CommRing R] (e z0 z1 z2 z3 : R) : R :=
  3 * e * z0 ^ 2 * z1 * z2 + 3 * e * z1 * z2 * z3 ^ 2 - e * z1 ^ 3 * z2 - e * z1 * z2 ^ 3
    + 4 * z0 ^ 3 * z3 - 4 * z0 * z3 ^ 3

/-- The complex form G(w, p) = Im(w^4) + Im(p^2) (3|w|^2 - |p|^2) / sqrt 2. -/
noncomputable def G (w p : ℂ) : ℝ :=
  (w ^ 4).im + (p ^ 2).im * (3 * Complex.normSq w - Complex.normSq p) / Real.sqrt 2

theorem im_pow_four (w : ℂ) : (w ^ 4).im = 4 * w.re ^ 3 * w.im - 4 * w.re * w.im ^ 3 := by
  simp [pow_succ, Complex.mul_im, Complex.mul_re]; ring

theorem im_sq' (p : ℂ) : (p ^ 2).im = 2 * p.re * p.im := by
  simp [pow_two, Complex.mul_im]; ring

/-- **L7.1 (eight-fold formula).** For all real z0..z3,
F(z) = Im(w^4) + Im(p^2) (3|w|^2 - |p|^2) / sqrt 2 with w = z0 + i z3, p = z1 + i z2. -/
theorem eightfold (z0 z1 z2 z3 : ℝ) :
    F (Real.sqrt 2) z0 z1 z2 z3 = G ⟨z0, z3⟩ ⟨z1, z2⟩ := by
  have hs : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  have hne : Real.sqrt 2 ≠ 0 := by positivity
  have key : 2 * z1 * z2 * (3 * (z0 * z0 + z3 * z3) - (z1 * z1 + z2 * z2)) / Real.sqrt 2
      = Real.sqrt 2 * (z1 * z2 * (3 * (z0 ^ 2 + z3 ^ 2) - (z1 ^ 2 + z2 ^ 2))) := by
    rw [div_eq_iff hne]
    linear_combination (-(z1 * z2 * (3 * (z0 ^ 2 + z3 ^ 2) - (z1 ^ 2 + z2 ^ 2)))) * hs
  simp only [G, im_pow_four, im_sq', Complex.normSq_mk]
  rw [key]; simp only [F]; ring

/-- The primitive 8th root of unity (1 + i)/sqrt 2. -/
noncomputable def zeta : ℂ := ⟨Real.sqrt 2 / 2, Real.sqrt 2 / 2⟩

theorem zeta_sq : zeta ^ 2 = Complex.I := by
  have hs : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  apply Complex.ext <;> simp [zeta, pow_two] <;> nlinarith [hs]

theorem zeta_pow_four : zeta ^ 4 = -1 := by
  rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, zeta_sq, Complex.I_sq]

theorem normSq_zeta : Complex.normSq zeta = 1 := by
  have hs : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  simp only [zeta, Complex.normSq_mk]; nlinarith [hs]

/-- **L7.2 (screw, complex form).** The map (w, p) -> (e^{i pi/4} w, i p) sends G to -G. -/
theorem screw (w p : ℂ) : G (zeta * w) (Complex.I * p) = - G w p := by
  simp only [G, mul_pow, zeta_pow_four, Complex.I_sq, Complex.normSq_mul, normSq_zeta,
    Complex.normSq_I]
  simp only [neg_one_mul, Complex.neg_im, one_mul]
  ring

/-- **L7.2' (screw, coordinate form).** Over any commutative ring with s * s = 2, the integral
matrix (z0 - z3, -s z2, s z1, z0 + z3) (= sqrt 2 times the screw) sends F to -4 F. -/
theorem screw_coord {R : Type*} [CommRing R] (s : R) (hs : s * s = 2) (z0 z1 z2 z3 : R) :
    F s (z0 - z3) (-(s * z2)) (s * z1) (z0 + z3) = -4 * F s z0 z1 z2 z3 := by
  simp only [F]
  linear_combination (-s * z1 * z2 * (-s ^ 2 * z1 ^ 2 - s ^ 2 * z2 ^ 2 + 6 * z0 ^ 2 - 2 * z1 ^ 2
    - 2 * z2 ^ 2 + 6 * z3 ^ 2)) * hs

/-- **L7.3 (Galois twist).** With R(z0, z1, z2, z3) = (z0, -z2, z1, z3):
F with e equals F with -e after R, i.e. F_e(R y) = F_{-e}(y). Pure polynomial identity. -/
theorem galois_twist {R : Type*} [CommRing R] (e z0 z1 z2 z3 : R) :
    F e z0 (-z2) z1 z3 = F e z0 z1 z2 z3 := by
  simp only [F]; ring

end Y56
