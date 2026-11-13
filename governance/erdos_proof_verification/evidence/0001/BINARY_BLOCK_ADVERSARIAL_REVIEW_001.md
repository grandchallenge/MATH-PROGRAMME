# Erdős #1 binary-block transfer: separate Adversary pass

Scope: ERDOS-PV-0001-B. This is a logically separate
**Adversary** review of the bounded lemma reconstructed in
`BINARY_BLOCK_LEMMA_001.md`. It is not a second human review,
independent invention, a Lean proof, or a MATHCERT determination.

## Falsification questions and dispositions

1. **Can the integer relation premise be weakened to rational or real
   linear independence?** No. There are immediate nonzero real
   relations between positive scalar weights if at least two occur.
   The proof correctly uses bounded integer coefficients, not an
   impossible stronger independence condition.

2. **Is the coefficient bound uniform in the number of blocks?**
   For fixed $i$, the signed-digit sum contains exactly $k$ terms,
   so $|c_i|\leq 2^k-1$. The bound applies to each coefficient
   independently of $d$. PASS.

3. **Does $c_i=0$ force each signed digit to vanish?** Yes, because
   the lowest digit modulo two must be zero, and repeated division
   by two reduces the same signed-digit range. PASS; simple triangle
   arguments alone would not justify digitwise uniqueness.

4. **Could two distinct index pairs have the same weight and cause a
   loss of cardinality even if subset sums of the indexed sequence
   are unique?** No. Distinct singleton index-subsets would have equal
   sums in that case; the preceding result forbids this. PASS.

5. **Does failure of the bounded-relation premise break the intended
   conclusion?** For $(a,k)=((1,3),2)$, the nonzero relation
   $(3,-1)$ has both magnitudes less than four, and the resulting
   weights $[1,2,3,6]$ have $3=1+2$. The executable fixture
   reproduces 13 distinct sums from 16 subsets. The test should
   reject this *input*, not label the conditional theorem false.

6. **Can an elementary transfer proof alone resolve Erdős #1?** No.
   Construction of sufficiently large bounded-relation-free families
   with the sharp asymptotic parameters is a separate deep step
   belonging to the source disproof; it remains unverified here.
   The status of the original uniform conjecture comes from
   dated external literature and source provenance, not a new
   GCL kernel replay. This nonimplication must survive admission.

## Review outcome

**PASS for the bounded transfer lemma as a mathematical argument,**
including its hypotheses and strict limits. This is a role-scoped
internal adversarial analysis; it is not independent-human
mathematical review and provides no certification. Full dependency
and toolchain checking belong to Phase C.
