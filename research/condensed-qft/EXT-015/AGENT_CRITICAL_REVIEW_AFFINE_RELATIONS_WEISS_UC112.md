# EXT-015 follow-on / UC112 — critical review of completed gluing for the derived affine relations

**Disposition.** ACCEPT the frozen [UC111 theorem](AFFINE_RELATIONS_WEISS_DESCENT_UC111.md) at commit `dff5eb3ea9e80d8a56197436cd05710e8ab655e8`, proof blob `84565945085336d86ab731355f9029328018aec7`. The retained reference is `research/ext015-affine-relations-weiss-primary-20261126`. The distinct same-system nonauthor reviewer `diagonal_jets_critical_review` accepted the theorem without correction and verified all seven dependency blobs against both the protected input and frozen primary.

| Inference | Critical finding |
| --- | --- |
| Actual derived tensor for arbitrary opens | Each real monomial uses finitely many variables, so the UC108 graded bar and Koszul comparison works on the all-open generator lists of UC096. The coefficient construction preserves realization. |
| Signed shape and component inclusion | The group simultaneously permutes components and repeated-size factors. Its sign twist gives exactly the exterior quotient. The formula accounts for coincidence and label merger and preserves disjoint multiplication. |
| Finite and completed gluing | Each shape is controlled by its actual number of centers. Product patches cover when the Weiss order reaches this number. Averaging preserves exactness, the real copower gives the joint liquid comparison, and weight completion assembles it. The shared vacuum retains all empty-intersection terms. |
| Sharpness and degree | The proper-subunion cover has the asserted order. Projection onto the monomial using every component annihilates the entire source realization, so the class is genuinely missed after Čech totalization. Intrinsic degree and Čech degree have the stated separate roles. |

The review is a same-system mathematical check of this frozen result and its named dependencies.
