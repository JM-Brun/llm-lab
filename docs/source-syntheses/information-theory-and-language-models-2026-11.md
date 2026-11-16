# Information theory and language models — source synthesis

**Status:** updated source synthesis, anchored in Wayland Zhang (2026-02-17), the primary predictive V-information paper by Xu et al. (ICLR 2020), and the canonical LLM Lab explanations and definitions.

## 1. Learning question and scope

How do probability, uncertainty, next-token loss and compression connect — and where do attractive analogies stop being mathematically valid?

Canonical destinations: [entropy](../../site/fr/entropy.qmd), [cross-entropy](../../site/fr/cross-entropy.qmd), and [scaled dot-product attention](../../site/fr/scaled-dot-product-attention.qmd), with English counterparts. This dossier complements the existing scoring stage; it does not create a parallel route.

## 2. Source and contribution

| Source | Distinct contribution | Evidence type | Integration |
|---|---|---|---|
| [Wayland Zhang, Information Theory Is All You Need (2026)](https://waylandz.com/blog/information-theory-and-llm/) | A compact narrative connecting surprisal, entropy, cross-entropy, attention, Landauer, compression and V-information | Secondary tutorial; standard equations mixed with analogies and broad claims | Source record, extraction and technical review; selective additions to canonical pages |
| [Xu et al., A Theory of Usable Information under Computational Constraints (ICLR 2020)](https://arxiv.org/abs/2002.10689) | Formal predictive family, optional ignorance, predictive V-entropy and predictive V-information | Primary theoretical paper with definitions, properties and PAC-style estimation bounds | Advanced supporting concept and a bounded exact finite-family experiment |
| Canonical LLM Lab lessons | Contextualized token prediction, loss, perplexity and Transformer attention | Project explanations and mathematical derivations | Remain the teaching backbone; avoid duplicating entropy material |
| Shannon coding identities | Formal link between probability, expected code length and entropy | Mathematical result under source-coding assumptions | Reproducible toy experiment and revision sheet |

Detailed evidence and locators remain in the [article extraction](../../data/extractions/wayland-zhang-information-theory-llm.yml), [primary-paper extraction](../../data/extractions/xu-et-al-usable-information-2020.yml), [article review](../source-reviews/information-theory-wayland-zhang-2026-11.md), [notebook audit](../source-reviews/wayland-notebook-audit-2026-11.md), and [V-information review](../source-reviews/predictive-v-information-xu-2020.md).

## 3. Integrated synthesis

For an event with probability p, surprisal is -log(p). Its expectation is Shannon entropy. For target q and predictive distribution p, cross-entropy is the expected negative log probability assigned by p to outcomes from q, and decomposes as:

```text
H(q,p) = H(q) + D_KL(q || p)
```

When q and the conditioning context are fixed, H(q) is independent of model parameters, so minimizing cross-entropy is equivalent to minimizing forward KL. In ordinary one-hot next-token supervision, the per-token cross-entropy is exactly NLL. Log base determines units: base 2 gives bits; natural logarithms give nats.

A probabilistic predictor can support efficient coding: ideal information lengths are -log2(p). This is a connection between predictive quality and compression, not an equivalence between compression and intelligence.

## 4. Critical distinctions

- **Attention vs mutual information:** attention weights are normalized compatibility coefficients used to aggregate value vectors. Mutual information is defined from a joint distribution. The former is not an estimator of the latter.
- **Landauer vs statistical learning:** a physical lower bound on heat dissipation for logically irreversible erasure does not establish a universal bound on what a learner can infer from data.
- **Compression vs intelligence:** coding performance depends on corpus, tokenizer, representation and protocol; it does not by itself measure reasoning or general intelligence.
- **Predictive V-information:** Xu et al. define it as the reduction in optimal expected log-loss within a predictive family when side information is supplied. The family must satisfy optional ignorance. The unrestricted family recovers Shannon mutual information; restricted families produce a directional, model-class-relative quantity. Its empirical estimation guarantees depend on bounded log-probabilities and function-class complexity. The article's own informal paragraph does not establish its proposed attention-versus-bag-of-words comparison.

## 5. What changed in LLM Lab

1. Cross-entropy lessons now derive the KL decomposition, state support/fixed-target assumptions, distinguish bits and nats, and show the one-hot special case.
2. Attention lessons explicitly reject the identity between attention weights and mutual information.
3. The source catalogue, extraction and technical review preserve provenance and claim-level dispositions.
4. A bilingual revision resource and a deterministic experiment make the central identities reviewable and executable.
5. The companion notebook received a static 18-cell audit. Its purported attention-derived MI heatmap was identified as cellwise KL-to-uniform terms, not mutual information; the compression comparison was found to mix marginal character entropy with a dependency-aware finite-file compressor.
6. Predictive V-information was added as an advanced supporting concept, grounded in Xu et al., with an exact finite-family binary example and tests.
7. A deterministic compression experiment now compares marginal entropy, source entropy rate and zlib output on fixed-seed equal-length sequences.
8. Entropy content was not duplicated; speculative claims were not promoted to canonical facts.

## 6. Remaining limits and next steps

The companion notebook has been statically audited across all 18 cells, including code and saved textual outputs, but it has not been executed; its figures and runtime paths therefore remain unverified. The V-information toy experiment computes exact population risks for a finite, hand-specified predictive family; it is not a fitted-model estimate or a replication of Xu et al.'s experiments. A future architecture-level study should pre-register predictive families, use train/test splits, compare held-out log-loss baselines, report uncertainty, and control model-selection and compute budgets. A future compression study should compare compatible sequence-level coding costs and specify corpus, tokenizer, byte/bit units and overhead.

## 7. Operational conclusion

Teach the robust chain — surprisal → entropy → cross-entropy/NLL → KL → predictive coding — as the core. Teach attention/MI and Landauer as examples of analogies that require careful boundaries. Keep compression/intelligence as a rejected equivalence. Teach predictive V-information as an advanced, explicitly model-class-relative quantity, never as a synonym for Shannon mutual information or as an unsupported ranking of architectures.


## 5 bis. Contrôle expérimental : KL d'attention et information mutuelle

Un contre-exemple déterministe a été ajouté dans `experiments/information-theory/attention_kl_vs_mutual_information.py`, avec une fonction générale `mutual_information` testée dans le module de fondations.

Pour deux contextes équiprobables qui partagent tous deux la ligne (0,9 ; 0,1), la KL moyenne de chaque ligne vers l'uniforme vaut 0,531 bit, alors que l'information mutuelle contexte-clé vaut exactement 0 : la distribution de clé ne dépend pas du contexte. Cela suffit à réfuter l'identification générale entre KL-vers-uniforme et information mutuelle.

L'identité statistique correcte est \(I(X;Y)=\mathbb E_X[D_{KL}(P(Y\mid X)\|P(Y))]\), où la référence est la marginale de Y. Même cette identité ne transforme pas automatiquement les poids d'attention en probabilités conditionnelles : leur interprétation comme telles doit être justifiée séparément. Le cas de deux lignes opposées donne ici 0,531 bit pour les deux métriques, mais cette égalité numérique est accidentelle et disparaît dans le contre-exemple à lignes répétées.

Cette expérience ne mesure pas la qualité d'un Transformer entraîné ; elle isole uniquement la différence mathématique entre les quantités.
