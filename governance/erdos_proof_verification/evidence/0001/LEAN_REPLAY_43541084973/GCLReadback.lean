import Erdos1.Resolutions.Erdos1_219usd_38h

example (d k W : ℕ) (hd : 0 < d) (hk : 0 < k)
    (a : Fin d → ℕ) (ha : ∀ i, 0 < a i)
    (hW : ∀ i, a i ≤ W) (hf : ErdosCounter.RelationFree a (2 ^ k)) :
    ∃ A : Finset ℕ, A.card = d * k ∧
      A ⊆ Finset.Icc 1 (2 ^ (k - 1) * W) ∧
      ErdosCounter.SumDistinct A :=
  ErdosCounter.exists_binary_block_set d k W hd hk a ha hW hf

example : ¬ (∃ C > (0 : ℝ), ∀ (N : ℕ) (A : Finset ℕ)
    (_ : Erdos1.IsSumDistinctSet A N), N ≠ 0 → C * 2 ^ A.card < N) :=
  Erdos1.erdos_1.disproof

#print axioms ErdosCounter.exists_binary_block_set
#print axioms Erdos1.erdos_1.disproof
