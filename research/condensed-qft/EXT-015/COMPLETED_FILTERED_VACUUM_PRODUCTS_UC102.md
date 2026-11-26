# EXT-015 follow-on / UC102 — a completed relative product and gluing over one vacuum

**Theorem.** The actual collision-moment observables on opens of the line are free complete filtered objects with one action of the quantum parameter $\hbar$ over the regulator scalar. For separated inputs their completed product represents the balanced filtered mapping space into arbitrary complete targets. Holding an arbitrary complete filtered coefficient object fixed, the product with the free model of an open satisfies Weiss descent in that open. This gives a common universal property for gluing and disjoint Wick multiplication on the admitted free scalar model.

## 1. The category with one quantum parameter

Use the fixed site, ZFC and the actual joint category $\mathsf J_{\mathbf C}$ of regulator module sheaves with flat parameter connection from UC099. Write $\mathcal D=D(\mathsf J_{\mathbf C})$ for its stable derived category, $\mathcal K$ for its full derived-complete sequence category in UC099.1, and $\mathcal L$ for the completion reflector. The filtration is decreasing with indices $n\ge0$. An object of $\mathcal K$ has tail limit zero. The cohomological grading of its complexes is separate from this filtration.

For $a\ge0$ use the upward filtration shift $T_a$ and its right adjoint $R_a$,

$$
(T_a X)_n=X_{\max(0,n-a)},\qquad (R_a Y)_n=Y_{n+a}.
\tag{UC102.1}
$$

These are left Kan extension and restriction along the translation of the decreasing index category by $a$. In the left Kan extension the relevant comma category has terminal object $\max(0,n-a)$, giving the displayed formula. Both preserve completeness by the coinitial tail of the limit, and $T_a$ commutes with $\mathcal L$ since it preserves the constant diagram and identifies the two tail limits in UC099.1. Thus $T_a$ is left adjoint to $R_a$ on the full complete category and preserves all colimits there. These shifts satisfy $T_aT_b=T_{a+b}$ with their canonical composition. Let $P_a(C)$ be the step with value $C\in\mathcal D$ for $n\le a$ and zero for $n>a$. It is complete, and its maps into $Y$ are $\mathrm{Map}_{\mathcal D}(C,Y_a)$ by the same left Kan extension from index $a$.

Denote by $\mathcal H$ the category of $X\in\mathcal K$ with a specified arrow $\mu_X:T_2X\to X$. This is the homotopy pullback of the arrow category along the map of endpoints $X\mapsto(T_2X,X)$. The single arrow represents multiplication by one $\hbar$ of weight two and cohomological degree zero. Its iterates represent the powers of the same parameter. Maps in this category include the coherent square commuting with this arrow. More explicitly the mapping space is the homotopy equalizer of the two maps

$$
\mathrm{Map}_{\mathcal K}(X,Y)
\rightrightarrows
\mathrm{Map}_{\mathcal K}(T_2X,Y),\qquad
f\mapsto f\mu_X,\quad f\mapsto\mu_Y T_2 f .
\tag{UC102.2}
$$

The forgetful functor to $\mathcal K$ creates colimits. For an input diagram the colimit of the action arrows has source $T_2$ of the underlying colimit because $T_2$ preserves colimits. The mapping-space property follows from (UC102.2), since limits of spaces commute with the equalizer. The functor also detects equivalences through the endpoint description. All these constructions take place with the $\mathbf C$ action and the flat parameter connection built into $\mathcal D$.

The free action on $X\in\mathcal K$ has underlying object $\coprod_{j\ge0}^{\mathcal K} T_{2j}X$, with action sending the shifted summand indexed by $j$ to the one indexed by $j+1$. Here each coproduct is taken in the complete category. To see its free property, a map to $(Y,\mu_Y)$ is a family of $f_j:T_{2j}X\to Y$ with paths from $f_{j+1}$ to $\mu_Y T_2 f_j$. Over a prescribed $f_j$, the space of the next $f_{j+1}$ and its specified path to that value is contractible. The full space is the limit of these finite path towers, so projection to $f_0$ is an equivalence. Write $V_a$ for the free action on $P_a(\mathbf C)$. It represents $\mathrm{Map}_{\mathcal D}(\mathbf C,Y_a)$ in $\mathcal H$. At the strict model level $V_0$ is the shared completed vacuum $\mathbf C[[\hbar]]$. Indeed the free action creates the indicated copy of $\mathbf C$ in every even weight, and UC099.2 completes its underlying monomorphic sequence by the product of those weights. The action is the shift of the one formal series variable. The same calculation shifts the vacuum to $V_a$.

The endofunctor $T_a$ lifts to $\mathcal H$ by commuting with $T_2$. Its right adjoint there has underlying $R_a$ and action induced by the mate $T_2R_a\to R_aT_2$ followed by $R_a\mu_Y$. For clarity, at filtration $n$ this uses the transition from $Y_{a+\max(0,n-2)}$ to $Y_{\max(0,a+n-2)}$, then the action to $Y_{a+n}$. Under $T_a\dashv R_a$ the two maps in (UC102.2) are matched by this mate. This proves the adjunction in the action category. In particular the lifted $T_a$ preserves its complete colimits.

## 2. The actual moment model and its completed product

Fix the monomial basis of UC096.1 without the formal parameter: a generator has a component label $I$, block size $b\ge1$, and a polynomial dual coordinate indexed by $0\le j\le b$. Let $\mathcal M(U)$ be the set of monomials in these generators, including $1$. Its arity $a(m)$ is the sum of block sizes. A physical inclusion sends each component label to its containing component and has an induced weight-preserving map on this monomial basis. The same rule applies when components merge. The completed moment object $D^\wedge(U)$ is canonically

$$
D^\wedge(U)\simeq\coprod_{m\in\mathcal M(U)}^{\mathcal H} V_{a(m)} .
\tag{UC102.3}
$$

To verify this on the concrete models, below any finite total weight the displayed coproduct is the sum of the scalar copies indexed by $\hbar^j m$ for $a(m)+2j$ below the cutoff. Its filtration completion is the product of the weight pieces, by the strict quotient calculation of UC099. At a fixed weight the scalar copies are coproducts in the parameter sheaves. The action in (UC102.3) and the moment model are precisely multiplication by the same formal parameter. Thus (UC102.3) respects physical inclusions, the scalar action and the connection. The natural map from the actual source $\mathbf F_s^\wedge(U)$ to this model is an equivalence by UC096/099, and is linear for $\hbar$ at the level of the strict cochain representatives. Hence it is an equivalence in $\mathcal H$. The underlying colimits of UC099 are created in $\mathcal H$, so the actual Weiss descent equivalence also preserves the $\hbar$ action there.

For a fixed open $U$ and any $X\in\mathcal H$, define the completed product with its free observable model by

$$
\mathcal T_U(X)=\coprod_{m\in\mathcal M(U)}^{\mathcal H} T_{a(m)}X .
\tag{UC102.4}
$$

It is left adjoint to the product of the $R_{a(m)}$ on $\mathcal H$. In particular for every complete target $Y$,

$$
\mathrm{Map}_{\mathcal H}(\mathcal T_U(X),Y)
\simeq \prod_{m\in\mathcal M(U)}
 \mathrm{Map}_{\mathcal H}(X,R_{a(m)}Y).
\tag{UC102.5}
$$

This is the free-input balanced mapping property. For each independent monomial one supplies one filtered map from the other input at its shifted weight. Multiplying the free input by $\hbar$ gives the same result as applying the single action to that map. Equations (UC102.2) and (UC102.5) express this on full mapping spaces. For the strict graded polynomial representatives below any finite cutoff, (UC102.4) is exactly the free-vacuum relative tensor calculation: a generator with arity $a$ contributes the filtered shift of the second input, and its $\hbar$ powers act there. It also characterizes the completion by the actual coproduct in $\mathcal H$. Real linear changes among homogeneous basis generators are implemented by the column-finite coefficient maps between their coproduct summands and extend by completion. In the chosen model the physical structure maps use the displayed explicit monomial bases.

If $U$ and $V$ are disjoint, the monomials on $U\sqcup V$ are the products of one monomial on each input, with weights added. Equations (UC102.3) and (UC102.4) give

$$
\mathcal T_U(D^\wedge(V))\simeq D^\wedge(U\sqcup V),
\qquad
\mathcal T_U\mathcal T_V(X)\simeq\mathcal T_{U\sqcup V}(X).
\tag{UC102.6}
$$

For the second equality, use that the shifts preserve complete coproducts and their indices add. This also works for finite families. The empty region has just the weight-zero monomial, so $\mathcal T_\varnothing$ is the identity and $D^\wedge(\varnothing)=V_0$. Naturality for inclusions of pairwise disjoint inputs into another physical open follows from applying the generator maps and multiplying their images there. The symmetry, unit and nested associativity diagrams hold by the same descriptions on tuples of input monomials. Through the actual comparison $\mathbf F_s^\wedge\to D^\wedge$ these are the admitted disjoint Wick maps. Specifically UC096 identifies the exterior product on the classicalized whole sources with the monomial product, and conjugation by $W_s$ gives the Wick maps of 111. The result at every finite weight is the relative tensor of the graded free polynomial models in UC076. Equations (UC102.4)–(UC102.6) give its universal completion.

## 3. Weiss descent with an arbitrary complete coefficient input

The functor $\mathcal T_U$ preserves colimits in $X$ by (UC102.5). There is also gluing in the physical open for a fixed arbitrary $X\in\mathcal H$. For an inclusion $U\subset V$, the arity-preserving monomial map induces the structure map on (UC102.4). Let $\{U_i\}$ be any nonempty Weiss cover of $U$ and $U_{\mathbf i}$ its labelled finite intersections. We prove the derived Čech augmentation

$$
\left|\,[q]\longmapsto
   \coprod_{\mathbf i=(i_0,\ldots,i_q)}^{\mathcal H}
         \mathcal T_{U_{\mathbf i}}(X)\,\right|
\simeq \mathcal T_U(X).
\tag{UC102.7}
$$

We first record how ordinary real vector complexes act on the fixed coefficient object. For $Z\in\mathcal D$ and an ordinary real cochain complex $A^\bullet$, form the sum-totalized real copower of $Z$ by $A^\bullet$. A real vector space with a basis acts by a coproduct of copies, and its linear maps give column-finite coefficient matrices. This construction is independent of the basis by the inverse change matrices. On complexes use the tensor differential and cochain signs. An acyclic real vector complex is contractible, and its contraction transfers by these same matrices. For a fixed real complex, a real splitting into its cohomology and contractible pairs reduces preservation of quasi-isomorphisms in $Z$ to exact coproducts of shifts. Thus the construction descends to derived objects. It preserves the real Čech realizations used here, since direct sums and the normalized alternating total assemble these matrices. Equivalently the real action uses ordinary real chain complexes as scalar coefficient diagrams and the skeletal colimits of their simplicial realizations.

Apply this copower levelwise to sequences, then apply completion. It commutes with $T_2$ because that shift reindexes the levels and commutes with completion. It thus acts on an arrow $T_2X\to X$ and preserves the indicated realizations in $\mathcal H$ by creation of colimits. For a discrete basis set the result is just a complete coproduct of copies of the input. This construction uses real scalar matrices acting in the joint module category and applies to any actual derived-complete $X$. It retains the connection since these scalars are constant.

Now fix an arity $a$. The real augmented Čech complex freely spanned by the monomials of arity $a$ of the intersection diagram is exact by the ordered-center calculation in UC096 §§2–3. In that proof, take real component chains and the real dual polynomial factors, then use the finite-group quotient before any scalar linearization. Each monomial map on overlaps is exactly the one in (UC102.3). The real exact complex has a splitting contraction, including its augmentation. Copower this chain calculation with $T_a X$ by the preceding construction. It proves (UC102.7) in that arity. The arity-zero complex is the constant full simplex on the cover labels, including every physically empty intersection. Its coefficient is $X$ with the existing action. Finally take the complete coproduct over arities. Colimits of those coproducts and colimits of the simplicial diagrams commute in $\mathcal H$. This proves (UC102.7).

Combining (UC102.6) with (UC102.7) gives the comparison between gluing the observables of $U$ before multiplying by those of a disjoint $V$, and multiplying on each patch with $V$ before gluing. Iterating proves the diagrams for independently chosen Weiss covers in a finite collection of separated regions. The identification is the actual natural Wick product by §2. The same proof shows the stronger statement (UC102.7) with arbitrary coefficient $X$, including nonsplit filtrations.

## 4. Controls and scope

On the vacuum at weight two, a model with two independent parameters has the two independent classes $\hbar_{\rm L}$ and $\hbar_{\rm R}$. Their difference belongs to the kernel of the comparison that sets them equal. In (UC102.4) the empty open uses the identity functor and the same $\mu_X$ on both sides, so there is just one parameter and one vacuum. This also checks the empty-intersection terms in (UC102.7).

For an actual nonsplit target use the finite example in UC099, with contractible level zero, level one $\mathbf C[0]$, zero at levels $n\ge2$, and zero action. Then $\mathrm{Map}_{\mathcal H}(V_1,Y)\simeq \mathrm{Map}_{\mathcal D}(\mathbf C,\mathbf C)$ contains the identity class, although the derived level zero of $Y$ vanishes. This detects the dependence on the filtered mapping space in (UC102.5). For an infinite-component test use the cover of UC096 §1 and a fixed separated interval as a second input. Multiplying each successive pair-block class by a mass-one one-slot class in the fixed interval raises that arity by one and retains its original component label. Each finite weight has the specified support, and the glued completed product retains the whole series. In the topology of the cover the same conclusion follows from (UC102.7).

This theorem concerns the completed relative product with the actual free moment models and arbitrary complete coefficient inputs. It proves the filtered balanced mapping property and gluing for those products. The analytic source and its comparison are the admitted renormalized free scalar on the line. The original REACH degree-two coefficient problem has its separate diagram.

## Exact inputs

Protected input ea18f28f7d7fc3acdb5d01b56a76ca9fa180173b. This is a bounded follow-on return.

| Principal input | Git blob |
| --- | --- |
| [RENORMALIZED_QUANTUM_STRUCTURE_111.md](RENORMALIZED_QUANTUM_STRUCTURE_111.md) | b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| [COMBINED_PARAMETER_LIQUID_REALIZATION_126.md](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [SOURCE_CONTROLLED_COMPLETED_WEISS_135.md](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md) | 62d91e9d5f38fc85cf2793507d887d526eccce7a |
| [ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md](ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md) | 1a876fb9009adcb881fcd0eca9ea672d38ee0a82 |
| [COLLISION_LIQUID_ALL_WEIGHTS_UC093.md](COLLISION_LIQUID_ALL_WEIGHTS_UC093.md) | 21c4c2f62714f44a307ecca01676ae7900cd8f3e |
| [COLLISION_LIQUID_WEISS_UC096.md](COLLISION_LIQUID_WEISS_UC096.md) | c4feef41ff9954cff6ccb3f503c3bfc617b3a920 |
| [JOINT_LIQUID_FILTERED_COMPLETION_UC099.md](JOINT_LIQUID_FILTERED_COMPLETION_UC099.md) | 8124c1c3d7283c8642536415b8b0064de49781e7 |
| [JOINT_LIQUID_COMPLETION_ACCEPTANCE_UC101.md](JOINT_LIQUID_COMPLETION_ACCEPTANCE_UC101.md) | 5799a290467fbc3e6d1151c7ab03166a0dbc4266 |
