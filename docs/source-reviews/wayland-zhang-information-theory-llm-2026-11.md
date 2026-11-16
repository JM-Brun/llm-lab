# Revue de source — Wayland Zhang, “Information Theory Is All You Need (to Understand LLMs)”

**Source:** [article original](https://waylandz.com/blog/information-theory-and-llm/) · [English/Chinese notebook repository](https://github.com/waylandzhang/information-theory-and-language-models) · [structured extraction](../../data/extractions/wayland-zhang-information-theory-llm-2026.yml)

**Scan status: text complete; media and notebook partially inspected.** The complete six-section article was retrieved directly on 2026-11-16. The repository landing page and notebook filenames were inspected. Notebook cells were not run; figures were not separately inspected; no reuse rights were established.

## Executive synthesis

The article is a useful high-level bridge between Shannon information theory, next-token prediction, cross-entropy training, attention, compression and computationally bounded notions of usable information. Its strongest material is the sequence from self-information to entropy to cross-entropy, and its explicit acknowledgement that attention is not mutual information in the strict mathematical sense.

Two sections need material qualification before being used as teaching claims:

1. **Landauer's principle does not prove a general limit on what a model can learn from a dataset.** Landauer's bound concerns the minimum heat dissipation associated with logically irreversible erasure at temperature (T). It is not a theorem about model architectures, generalization or the amount of information learned from finite samples.
2. **“Compression is intelligence” is a provocative thesis, not a mathematical identity.** Better predictive modelling can reduce ideal code length under a matched coding protocol. This is not sufficient to define intelligence, and it does not imply that every good compressor is a language model.

The V-information section is an interesting advanced direction. The linked primary paper has now been read in full and the concept is integrated as an advanced optional node, with a small predictor-family demonstration.

## 1. Source and pedagogical model

The article presents six sections in this order:

1. Information content and entropy.
2. Cross-entropy as the language-model training objective.
3. Attention as an analogy to mutual information.
4. A proposed thermodynamic bound.
5. Compression as a lens on intelligence.
6. V-information under computational constraints.

Its linked repository provides English and Chinese notebooks. The notebook is a useful lead for practical learning, but it has not yet been executed or independently checked. The article page identifies itself as a rewrite of an earlier piece dated 2025-03-27; the visible article page is dated 2026-02-17.

## 2. Technical audit by claim

| Topic | Assessment | Integration decision |
|---|---|---|
| Self-information (I(x)=-log_2p(x)) and entropy (H(X)=mathbb E[I(X)]) | Established definitions; in autoregressive modelling the conditioning context must be explicit | Already covered in the bilingual entropy lesson |
| Cross-entropy (H(P,Q)=H(P)+D_{KL}(P|Q)) | Correct when target (P), model (Q), support and logarithm base are consistently defined; minimizing over (Q) minimizes KL for fixed (P) | Link from entropy to the existing cross-entropy lesson; do not duplicate |
| Attention as mutual information | The article explicitly says the analogy is not strict MI. Attention weights are learned, input-dependent aggregation coefficients, not (I(X;Y)) | Add a concise misconception guard to the attention lesson |
| Landauer bound | The article's inference from erasure energy to a universal learning-information ceiling does not follow | Correct the claim in this review; defer a full thermodynamics lesson |
| Compression and intelligence | Predictive modelling and coding efficiency are formally connected, but compression is not a sufficient definition of intelligence | Keep the distinction in the compression synthesis and revision sheet |
| V-information | Promising computationally constrained framework; the primary paper is linked but only its abstract was inspected | Advanced reference only; no canonical concept yet |

## 3. The mathematical bridge worth teaching

For an autoregressive model:

[
p(x_{1:T})=prod_{t=1}^{T}p(x_tmid x_{<t}).
]

The realized token surprisal in bits is:

[
I_t=-log_2p(x_tmid x_{<t}).
]

For a target distribution (P) and a model distribution (Q):

[
H(P,Q)=H(P)+D_{KL}(P|Q).
]

This identity explains why minimizing cross-entropy over (Q), for a fixed target distribution (P), is equivalent to minimizing the KL mismatch. It does not mean that the true language entropy is known exactly from a finite corpus.

The ideal predictive code length is the sum of conditional surprisals. An actual lossless codec still needs a shared probability model, tokenizer, coding conventions and decoder. Model storage and protocol overhead must be counted before claiming net compression.

## 4. The three boundaries that must remain explicit

### Attention is not mutual information

Mutual information is a property of a joint distribution:

[
I(X;Y)=H(X)-H(Xmid Y).
]

An attention matrix contains normalized, context-dependent weights produced from learned queries and keys. Those weights do not directly estimate the mutual information between token variables, nor do they quantify how many bits one token contributes to another. The analogy may motivate a question about dependency, but the quantities are different.

### Landauer is not a learning-theory theorem

Landauer's principle concerns the physical cost of logically irreversible erasure. It does not establish that a model cannot generalize beyond literal examples in a finite training set. Statistical learning depends on the data-generating distribution, sampling assumptions, inductive bias, model class, objective and evaluation regime. A model cannot conjure evidence from nowhere, but it can infer regularities that were not explicitly enumerated in the observed sample.

### Compression is not a complete definition of intelligence

For a fixed source and coding protocol, a better predictive distribution can reduce expected ideal code length. That is a precise and useful connection. It does not prove that compression captures every dimension of intelligence, reasoning, agency, grounding or usefulness.

## 5. Project integration

- **Entropy:** existing French and English pages already explain entropy, surprisal and conditional prediction. Keep them canonical.
- **Cross-entropy:** existing pages already derive the loss and its relationship to KL. Link rather than copy.
- **Attention:** add one explicit note that attention weights are not mutual information.
- **Compression:** connect the article's slogan to the existing distinction between predictive compression, model compression and runtime memory.
- **V-information:** link the primary paper as optional advanced reading only.
- **Notebook:** create a small original standard-library experiment for entropy, cross-entropy, KL and mutual information; this companion experiment is now available in `experiments/information-theory-llm/`. Do not copy upstream notebook code or figures.

No new canonical concept ID is proposed. Existing concepts cover entropy-related training and self-attention; V-information remains a research extension.

## Audit statique du notebook anglais (18 cellules)

Le notebook anglais `information-theory-and-llm-en.ipynb` a été récupéré depuis le dépôt public et ses 18 cellules (Markdown et code) ont été inspectées statiquement. Le code n'a pas été exécuté ; les sorties graphiques enregistrées n'ont pas été traitées comme des résultats reproduits.

| Cellule / partie | Ce qu'elle fait | Audit et décision |
|---|---|---|
| 1–3 : logarithme, entropie binaire, surprise | Trace log₂, entropie binaire et exemples d'événements rares | Bonne intuition visuelle ; corriger la phrase qui assimile l'entropie maximale à l'information d'un événement individuel. |
| 4–6 : information mutuelle | Calcule une distribution jointe météo/parapluie, les entropies et la MI | Exemple mathématiquement pertinent ; le diagramme de Venn reste une représentation conceptuelle, pas une géométrie exacte des ensembles. |
| 8–9 : cross-entropy et KL | Compare une cible synthétique à trois distributions prédites | Bon exercice de décomposition ; l'ajout d'un epsilon dans les logarithmes est un artifice numérique à expliciter. |
| 10–11 : attention et « MI approximée » | Récupère ou simule une matrice d'attention, puis calcule pour chaque ligne une KL vers une distribution uniforme | **Erreur conceptuelle majeure :** cette KL ligne-par-ligne n'est pas l'information mutuelle entre variables aléatoires. Le titre et l'interprétation « association sémantique » ne sont pas justifiés. Le modèle chargé est BERT (encodeur bidirectionnel), pas un LLM autorégressif ; le chemin de secours utilise des poids simulés. Ne pas réutiliser ce panneau comme mesure de MI. |
| 12 : V-information | Résume l'article arXiv:2002.10689 et les familles de prédicteurs | Piste avancée utile, mais la formulation est très simplifiée ; vérifier le papier complet avant intégration canonique. |
| 13 : thermodynamique | Relie Landauer à une limite d'extraction d'information depuis les données | Même extrapolation non fondée que dans l'article : une borne physique d'effacement n'est pas une borne générale d'apprentissage. |
| 14–16 : compression | Présente des familles de codeurs puis propose une comparaison avec zlib | Bonne occasion d'expérimenter, mais ne pas assimiler directement l'entropie marginale empirique par caractère à la limite de compression d'une source dépendante. |
| 17 : zlib | Compare répétitions, texte anglais, texte mixte et chaîne aléatoire | La chaîne aléatoire n'a pas de graine fixe ; l'expérience n'est donc pas entièrement reproductible. L'entropie calculée ignore les dépendances entre caractères alors que zlib les exploite ; l'overhead et les conventions de mesure comptent. Refaire avec graine fixe et comparer aussi des coûts conditionnels ou bits/octet. |

### Décisions notebook

- **Réutiliser l'idée, pas le code ni les figures :** entropie binaire, exemple de distribution jointe, comparaison de distributions et compression zlib.
- **Corriger avant toute reprise :** panneau attention/MI, confusion entre entropie et surprise individuelle, inférence Landauer.
- **Renforcer la reproductibilité :** graine aléatoire fixe, dépendances/versionnement déclarés, résultats générés à l'exécution et séparation entre entropie marginale et coût de codage réel.
- **Ne pas copier :** aucun code ni figure upstream n'est repris ; les expériences du projet sont réécrites indépendamment.

## 6. Evidence and open work

- Directly inspected: full article text, page date and author; upstream repository landing page.
- Fully inspected: Xu et al. (ICLR 2020), including formal definitions, propositions, PAC estimation theorem, structure-learning algorithm, empirical sections, fairness discussion and conclusion.
- Statically inspected: all 18 cells of the English upstream notebook; it was not executed.
- Not inspected/reproduced: upstream notebook execution and outputs, article image bytes, authors' V-information experiment code/datasets, comments and all further-reading links.
- Rights: article text and figures remain link-only; no reuse permission established.

## 7. Operational conclusion

Use the article as a **conceptual map**, not as a single authority. Preserve its strong entropy/cross-entropy bridge, teach the attention/MI distinction explicitly, reject the Landauer inference as stated, qualify the compression/intelligence slogan, and teach V-information as an advanced, predictor-family-dependent quantity rather than as Shannon MI.


## 8. Primary-paper audit — predictive V-information

The linked primary paper is Xu, Zhao, Song, Stewart & Ermon, [*A Theory of Usable Information Under Computational Constraints* (ICLR 2020)](https://openreview.net/forum?id=r1eBeyHFDH), also available as [arXiv:2002.10689](https://arxiv.org/abs/2002.10689). The published paper was inspected beyond its abstract: definitions, propositions, PAC estimation theorem, structure-learning method, empirical sections, fairness discussion and conclusion.

### Definition and interpretation

For a predictive family \\(\\mathcal V\\), the paper defines the best achievable expected log loss with and without side information:

\\[
H_{\\mathcal V}(Y\\mid X)=\\inf_{f\\in\\mathcal V}\\mathbb E[-\\log f[X](Y)],
\\qquad
H_{\\mathcal V}(Y\\mid\\varnothing)=\\inf_{f\\in\\mathcal V}\\mathbb E[-\\log f[\\varnothing](Y)].
\\]

Then:

\\[
I_{\\mathcal V}(X\\to Y)=H_{\\mathcal V}(Y\\mid\\varnothing)-H_{\\mathcal V}(Y\\mid X).
\\]

The family \\(\\mathcal V\\) is part of the definition: it formalizes which predictors the observer can use. The paper imposes an optional-ignorance condition so a predictor can ignore side information; under its assumptions this supports non-negativity. With an unrestricted family, the definition recovers Shannon mutual information. Restricted families recover other notions, including variance-explained / coefficient-of-determination cases.

### What the paper establishes — and does not

- The quantity is directional in general: \\(I_{\\mathcal V}(X\\to Y)\\) need not equal \\(I_{\\mathcal V}(Y\\to X)\\).
- The Shannon data-processing inequality remains true for Shannon mutual information. The paper's claim that computation can increase usable information concerns a restricted observer's predictive ability, not creation of new Shannon information.
- A PAC-style estimation bound is proved under bounded log-loss and a controlled complexity term (Rademacher complexity of the predictor family). It is not a blanket guarantee for arbitrary high-capacity models or arbitrary datasets.
- The paper evaluates directed structure learning on synthetic high-dimensional data, gene-regulatory-network inference, Moving-MNIST frame ordering, and adversarial/fair representation settings. These are reported paper experiments; LLM attention is not one of the demonstrated applications.
- In the fairness experiments, information leakage depends on the attacker/predictor family. Low leakage to one discriminator does not prove invariance to every possible observer.

### Integration decision

Promote \\(v-information\\) to an **advanced optional concept**, not a core prerequisite. Link it to Shannon mutual information with an explicit contrast. The project's balanced-XOR demonstration illustrates model-family dependence; it does not reproduce the paper's PAC theorem or empirical experiments.
