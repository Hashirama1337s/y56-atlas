import Mathlib

/-!
# Y56 pencil fact: the extra 16 lines need 2 s^4 = 81

For the axis-diagonal line shape in the pencil G_s, a line exists iff the three coefficient
equations
  alpha beta (s - alpha^2 - beta^2) = 0,  2 + alpha beta (s - beta^2) = 0,  1 + alpha beta^3 = 0
have a common solution. We prove: over ANY commutative ring, these force
  s = 3 beta^2, alpha^2 = 2 beta^2, 2 beta^8 = 1, and hence 2 s^4 = 81.
The certificate is an explicit chain of `linear_combination` steps (an ideal-membership
certificate checked by `ring`). Conversely, over the reals there is a solution with s^4 = 81/2.
-/

namespace Y56

/-- **Pencil fact.** Over any commutative ring, the three equations force s = 3 beta^2,
alpha^2 = 2 beta^2, 2 beta^8 = 1 and 2 s^4 = 81. -/
theorem pencil_forces {K : Type*} [CommRing K] (a b s : K)
    (h1 : a * b * (s - a ^ 2 - b ^ 2) = 0)
    (h2 : 2 + a * b * (s - b ^ 2) = 0)
    (h3 : 1 + a * b ^ 3 = 0) :
    s = 3 * b ^ 2 ∧ a ^ 2 = 2 * b ^ 2 ∧ 2 * b ^ 8 = 1 ∧ 2 * s ^ 4 = 81 := by
  -- a*b is a unit modulo h3 (its inverse is -b^2), so h1 gives s = a^2 + b^2
  have k1 : s - a ^ 2 - b ^ 2 = 0 := by
    linear_combination (-b ^ 2) * h1 + (s - a ^ 2 - b ^ 2) * h3
  have k2 : 2 + a ^ 3 * b = 0 := by linear_combination h2 - a * b * k1
  have k4 : a ^ 2 - 2 * b ^ 2 = 0 := by linear_combination a ^ 2 * h3 - b ^ 2 * k2
  have k5 : s - 3 * b ^ 2 = 0 := by linear_combination k1 + k4
  have k6 : 2 * b ^ 8 - 1 = 0 := by linear_combination (a * b ^ 3 - 1) * h3 - b ^ 6 * k4
  refine ⟨by linear_combination k5, by linear_combination k4, by linear_combination k6, ?_⟩
  linear_combination 2 * (s ^ 3 + 3 * b ^ 2 * s ^ 2 + 9 * b ^ 4 * s + 27 * b ^ 6) * k5 + 81 * k6

/-- **Converse (existence).** Over the reals the system has a solution, with 2 s^4 = 81
(b = (1/2)^(1/8), a = -2 b^5 = -1/b^3, s = 3 b^2). -/
theorem pencil_solvable :
    ∃ a b s : ℝ, a * b * (s - a ^ 2 - b ^ 2) = 0 ∧ 2 + a * b * (s - b ^ 2) = 0 ∧
      1 + a * b ^ 3 = 0 ∧ 2 * s ^ 4 = 81 := by
  set b : ℝ := (1 / 2 : ℝ) ^ ((1 : ℝ) / 8) with hbdef
  have hbpos : 0 < b := by positivity
  have hb8 : b ^ 8 = 1 / 2 := by
    rw [hbdef, ← Real.rpow_natCast, ← Real.rpow_mul (by norm_num)]
    norm_num
  -- a = -2 b^5 equals -1/b^3 because 2 b^8 = 1
  refine ⟨-2 * b ^ 5, b, 3 * b ^ 2, ?_, ?_, ?_, ?_⟩
  · linear_combination 8 * b ^ 8 * hb8
  · linear_combination (-4 : ℝ) * hb8
  · linear_combination (-2 : ℝ) * hb8
  · linear_combination 162 * hb8
end Y56
