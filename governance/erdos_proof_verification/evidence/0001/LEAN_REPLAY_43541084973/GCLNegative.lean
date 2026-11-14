import Erdos1.Resolutions.Erdos1_219usd_38h

-- Omit the bounded integer-relation-freedom hypothesis deliberately.
example (d k W : ℕ) (hd : 0 < d) (hk : 0 < k)
    (a : Fin d → ℕ) (ha : ∀ i, 0 < a i)
    (hW : ∀ i, a i ≤ W) :
    ∃ A : Finset ℕ, A.card = d * k ∧
      A ⊆ Finset.Icc 1 (2 ^ (k - 1) * W) ∧
      ErdosCounter.SumDistinct A := by
  exact ErdosCounter.exists_binary_block_set d k W hd hk a ha hW
