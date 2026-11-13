# Audit éditorial du parcours principal — valeur pédagogique et profondeur intellectuelle

> **Statut : diagnostic préliminaire, à confirmer.** Ce document conserve les constats et décisions de cadrage issus de l'audit initial du parcours principal. Il ne constitue pas une validation exhaustive du contenu publié : la lecture intégrale des 18 pages dans les deux langues et la vérification du rendu navigateur restent à effectuer.

- Projet : [LLM Lab](https://jm-brun.github.io/llm-lab/)
- Parcours : [LLM overview (FR)](https://jm-brun.github.io/llm-lab/fr/llm-overview.html)
- Skill éditoriale associée : `.agents/skills/learning-path-excellence/SKILL.md` (PR [#1076](https://github.com/JM-Brun/llm-lab/pull/1076))
- Date du diagnostic initial : 13 novembre 2026

## 1. Objectif éditorial

Le parcours doit satisfaire deux publics sans se scinder artificiellement en un cours débutant et une annexe experte :

1. **Lecteur débutant ou en révision** : comprendre le concept, son utilité, son mécanisme et ses prérequis sans être bloqué par des détails prématurés.
2. **Lecteur expérimenté** : trouver sur chaque page au moins un apport intellectuel concret — distinction subtile, hypothèse, compromis, limite, résultat empirique, perspective historique ou lien systémique — qui dépasse la reformulation d'un cours standard.

L'ambition est de compiler et synthétiser les meilleures idées pédagogiques et techniques disponibles, en construisant une progression propre à LLM Lab. Il ne s'agit ni de copier une ressource de référence, ni d'ajouter mécaniquement un encart « pour experts » à chaque page.

## 2. Périmètre et niveau de confiance

Le diagnostic préliminaire a porté sur les 18 pages principales inventoriées ci-dessous, avec une lecture de structures et de contenus, une comparaison structurelle de dix couples français/anglais et un premier benchmark de ressources externes.

**Ce qui est établi à ce stade :**
- le périmètre de 18 pages est identifié ;
- la progression générale et plusieurs distinctions conceptuelles structurantes sont repérées ;
- des zones prioritaires d'enrichissement éditorial ont été identifiées ;
- dix couples FR/EN ont fait l'objet d'une comparaison structurelle.

**Ce qui n'est pas encore établi :**
- la lecture approfondie et exhaustive des 18 pages dans les deux langues ;
- la vérification systématique de l'équivalence pédagogique et scientifique FR/EN ;
- le contrôle visuel de chaque page dans le navigateur ;
- la validation de chaque proposition sur le contenu et les exemples effectivement affichés.

Les classements ci-dessous sont donc des **priorités provisoires**, et non des verdicts définitifs sur l'exactitude ou la qualité de chaque page.

## 3. Inventaire du parcours

Les 18 pages recensées :

1. `llm-overview`
2. `generation`
3. `text-data`
4. `embedding-space`
5. `positional-encoding`
6. `contextualized-representations`
7. `transformer`
8. `queries-keys-values`
9. `scaled-dot-product-attention`
10. `causal-masking`
11. `logits`
12. `probabilites`
13. `entropy`
14. `vraisemblance`
15. `cross-entropy`
16. `loss`
17. `gradients`
18. `training-loop`

## 4. Diagnostic transversal

### 4.1 Fondations déjà prometteuses

Le parcours possède plusieurs choix pédagogiques solides à préserver :

- il distingue l'architecture, l'apprentissage et l'inférence ;
- il suit une progression conceptuelle globalement cohérente ;
- il distingue les représentations initiales des représentations contextualisées ;
- il sépare génération, scoring probabiliste et apprentissage ;
- il utilise des pages d'approfondissement pour accueillir certaines dérivations et certains détails ;
- il cherche à limiter les répétitions entre pages.

Le principal enjeu n'est donc pas d'augmenter uniformément la longueur du parcours. Il est de faire en sorte que chaque page apporte une idée qui mérite d'être retenue, y compris par un lecteur qui connaît déjà les grandes lignes des Transformers.

### 4.2 Relations à rendre plus explicites

Le parcours gagnerait à mieux montrer les liens entre les notions, plutôt que de les laisser comme une succession de chapitres :

- entropie prédictive ↔ incertitude de la distribution du modèle ;
- vraisemblance ↔ évaluation probabiliste ;
- cross-entropy ↔ objectif d'apprentissage ;
- gradients ↔ dynamique d'optimisation ;
- attention ↔ communication et mélange d'information entre positions ;
- tokenisation ↔ coût, couverture linguistique et longueur du contexte ;
- prefill/decode ↔ architecture des systèmes d'inférence ;
- représentations contextualisées ↔ limites de l'interprétabilité.

Ces liens doivent renforcer la progression cumulative : une notion introduite sur une page doit être réutilisée ensuite avec un sens précis.

## 5. Priorisation éditoriale provisoire

### 5.1 Priorité élevée — première vague

| Page | Apport distinctif à rechercher | Pourquoi cela compte |
|---|---|---|
| `text-data` | Conséquences concrètes de la tokenisation : fragmentation, artefacts, différences entre langues, coût en tokens et longueur de contexte. | La tokenisation n'est pas un simple prétraitement neutre ; elle affecte couverture, coût et comportement observable. |
| `logits` | Montrer que les logits sont des scores relatifs ; expliquer l'invariance de softmax à l'ajout d'une constante et, si pertinent, le rapprochement prudent avec les modèles d'énergie. | Éviter de traiter les logits comme des probabilités ou des mesures absolues de confiance. |
| `positional-encoding` | Discuter les symétries, l'invariance au déplacement selon les mécanismes, et les limites de généralisation lorsque la longueur de contexte augmente. | Relier le choix d'encodage aux capacités et limites réelles du modèle. |
| `scaled-dot-product-attention` | Présenter l'attention comme un mécanisme de sélection/routage et de mélange d'information ; expliquer pourquoi les poids d'attention ne constituent pas automatiquement une explication du raisonnement. | Faire comprendre à la fois le mécanisme utile et les limites d'interprétation de ses visualisations. |
| `vraisemblance` | Relier vraisemblance, log-vraisemblance et perplexité ; expliquer la dépendance à la tokenisation et les précautions nécessaires pour comparer des modèles. | Éviter les comparaisons naïves de scores et donner un sens opérationnel à l'évaluation probabiliste. |
| `training-loop` | Donner une intuition de la dynamique d'optimisation et de la généralisation ; relier données, paramètres, calcul et compromis d'entraînement. | Faire passer le lecteur de la boucle algorithmique à la compréhension de l'entraînement comme système. |

Pour chaque page de cette vague : établir d'abord ce qui est déjà expliqué, identifier le manque réel, sélectionner des sources fiables, proposer un apport qui soit propre à LLM Lab, puis modifier les versions FR et EN et valider les deux.

### 5.2 Priorité intermédiaire — deuxième vague

| Page | Apport distinctif à rechercher |
|---|---|
| `llm-overview` | Replacer le LLM comme système probabiliste et distinguer prédiction linguistique, compétence comportementale et compréhension du monde, sans réduire abusivement l'une à l'autre. |
| `generation` | Expliquer KV cache, latence, débit, coût marginal d'un token et compromis entre stratégies de décodage. |
| `contextualized-representations` | Montrer comment les représentations évoluent selon les couches et pourquoi leur interprétation est difficile. |
| `transformer` | Expliquer le flux résiduel comme espace de communication ; préciser la complémentarité entre attention et MLP. |
| `queries-keys-values` | Déconstruire les analogies anthropomorphiques et expliquer que les têtes apprennent des sous-espaces et transformations spécialisés. |
| `causal-masking` | Distinguer causalité computationnelle (contrainte d'accès à l'information future) et compréhension de la causalité dans le monde. |

### 5.3 Pages dont les fondations semblent déjà intéressantes

Ces pages paraissent contenir des distinctions utiles à préserver et à vérifier, plutôt que de les enrichir par principe :

- `embedding-space` : distinction entre adresse d'une ligne, vecteur et représentation contextualisée ;
- `probabilites` : température, calibration et distinction entre probabilité et vérité ;
- `entropy` : dispersion prédictive et surprise d'un événement observé ;
- `cross-entropy` : distribution cible, probabilité attribuée à l'observation et pénalité ;
- `loss` : conventions de masquage et de réduction ;
- `gradients` : sensibilité locale, rétropropagation et mise à jour des paramètres.

Cette appréciation est provisoire : une page « déjà intéressante » peut encore avoir des imprécisions, des lacunes de progression ou une version linguistique moins aboutie.

## 6. Références de benchmark et rôle de chaque ressource

Ces ressources sont complémentaires. Elles servent de références pour comparer des approches pédagogiques et des niveaux de profondeur, pas de modèles à reproduire.

1. **3Blue1Brown — Attention in Transformers, step by step**  
   https://www.3blue1brown.com/lessons/attention/  
   Apport à étudier : visualisation du mécanisme et de l'enchaînement des opérations. Utile pour vérifier qu'une explication donne une intuition dynamique, pas seulement une formule.

2. **Jay Alammar — The Illustrated Transformer**  
   https://jalammar.github.io/illustrated-transformer/  
   Apport à étudier : suivi visuel des représentations et des tenseurs à travers le réseau. Utile pour rendre concret le devenir des données à chaque étape.

3. **Stanford CS336 — Language Modeling from Scratch**  
   https://cs336.stanford.edu/  
   Apport à étudier : vision systémique couvrant données, tokenisation, architecture, entraînement, systèmes, efficacité, évaluation et alignement. C'est un cours avancé : il constitue une référence de profondeur et de couverture, pas le niveau de prérequis à imposer au parcours principal.

4. **DeepLearning.AI — How Transformer LLMs Work**  
   https://www.deeplearning.ai/courses/how-transformer-llms-work  
   Apport à étudier : progression accessible et articulation entre tokenisation et composants Transformer.

**Synthèse recherchée pour LLM Lab :** combiner la force visuelle de 3Blue1Brown, le suivi des représentations de Jay Alammar, la perspective système de Stanford CS336 et la progression accessible de DeepLearning.AI. La valeur propre de LLM Lab doit venir de leur articulation, de la précision des distinctions et d'expériences contrôlées qui permettent au lecteur de vérifier ses intuitions.

## 7. Grille d'examen applicable à chaque page

Quatre dimensions éditoriales à intégrer naturellement — sans en faire obligatoirement quatre sections fixes :

- **A — Mécanisme :** le lecteur peut-il expliquer ce qui se passe, dans quel ordre et sur quelles données ?
- **B — Motivation :** comprend-il pourquoi ce mécanisme ou ce choix de conception existe, et quel problème il résout ?
- **C — Recul critique :** connaît-il les hypothèses, limites, compromis et idées reçues importantes ?
- **D — Système :** sait-il relier cette notion à l'entraînement, à l'inférence, aux capacités du modèle ou aux autres composants ?

Deux tests doivent être appliqués :
- **Test débutant :** après lecture, une personne motivée mais novice peut-elle reformuler l'idée et suivre un exemple sans dépendre d'un savoir non introduit ?
- **Test expérimenté :** une personne connaissant déjà les bases repart-elle avec au moins une distinction, un résultat, une limite ou un lien qu'elle n'aurait pas obtenu d'une explication conventionnelle ?

La profondeur doit être progressive : intuition, mécanisme, formalisation, implications et limites. Les détails avancés ne doivent pas casser le fil principal.

## 8. Plan de travail

### Vague 1 — six pages prioritaires

Ordre de travail initial : `text-data`, `logits`, `positional-encoding`, `scaled-dot-product-attention`, `vraisemblance`, `training-loop`.

Pour chaque page :
1. lire la page française et sa version anglaise en entier ;
2. examiner les pages liées et les prérequis pour éviter les doublons et les ruptures ;
3. comparer avec les références pertinentes et, si nécessaire, consulter des sources primaires ;
4. consigner le diagnostic : points forts, lacunes, risques de confusion ;
5. formuler l'apport distinctif et son emplacement dans la progression ;
6. modifier les deux langues en conservant une équivalence de fond ;
7. vérifier liens, formules, exemples, navigation et rendu ;
8. mettre à jour la fiche de valeur de la page et le présent document.

### Vague 2 — enrichir sans dégrader

Reprendre les pages de priorité intermédiaire et les pages déjà solides. Le critère n'est pas « ajouter du contenu », mais « ajouter une valeur démontrable sans répéter une autre page ni alourdir inutilement l'explication ».

### Vague 3 — audit cumulatif du parcours

Relire les 18 pages comme une expérience unique :
- vérifier les prérequis et les transitions ;
- vérifier que les notions sont réutilisées correctement ;
- supprimer les répétitions et combler les trous ;
- vérifier que les frontières conceptuelles restent nettes ;
- vérifier la cohérence FR/EN ;
- tester la progression depuis les intuitions initiales jusqu'à la compréhension systémique.

## 9. Conditions de validation

Un enrichissement ne doit être considéré comme terminé que si :

- il résout une lacune identifiée, et non un besoin abstrait de longueur ;
- il est scientifiquement exact et correctement nuancé ;
- il aide le débutant sans infantiliser le lecteur expérimenté ;
- il apporte une valeur identifiable à un lecteur déjà familier du sujet ;
- il est placé sur la bonne page et ne crée pas de doublon ;
- il renforce les liens avec le reste du parcours ;
- les versions française et anglaise sont cohérentes ;
- les exemples, équations, liens et renvois sont vérifiés ;
- le rendu est contrôlé lorsque les moyens le permettent ;
- les limites de vérification restantes sont déclarées explicitement.

## 10. Décision éditoriale

Le chantier doit commencer par les six pages de la vague 1. Le diagnostic actuel fournit une carte de priorisation, pas une autorisation à réécrire sans examen. Chaque modification doit être justifiée par une lacune vérifiée, documentée par des sources, et évaluée selon le double public du parcours.

Le principe directeur est simple : **chaque page doit être une porte d'entrée pour le novice et une occasion de réflexion pour le lecteur expérimenté.**


---

# Addendum — page audit 1/6: `text-data`

**Status:** first page of wave 1 reviewed and enriched in both languages. This is a source-level review of the Quarto files and neighboring canonical pages; the rendered browser experience and CI build have not yet been verified.

## Page identity and ownership

- FR: `site/fr/text-data.qmd`
- EN: `site/en/text-data.qmd`
- Practice: `site/fr/exercises/text-data.qmd` and `site/en/exercises/text-data.qmd`
- Role: core Understand lesson, following generation and preceding embedding lookup.
- Canonical boundary: explain the prompt path from text to tokens, IDs and initial embeddings. Corpus selection/cleaning belongs to `corpus-preparation`; tokenizer algorithms to `tokenization-strategies`; empirical design and multilingual comparisons to `tokenizer-design-evaluation`; Unicode details to `unicode-text`.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | How does an ordinary text prompt become the discrete input consumed by a language model? |
| Beginner outcome | Trace text → tokenizer → tokens → IDs → embedding lookup, and distinguish IDs from vectors and contextual representations. |
| Experienced-reader value already present | The page distinguishes vocabulary size from embedding dimension; prompt encoding from corpus preparation; and absolute position embeddings from RoPE's use inside attention. |
| Best-source contribution | The existing companion material uses Hugging Face's component-level view of a tokenizer pipeline, inspectable BPE examples, and research on multilingual representation cost. |
| LLM Lab synthesis | Connect the input representation to context budgets and system cost while preserving the conceptual boundary between the core prompt path and optional tokenizer engineering. |
| Weak element before this change | The page stated that tokenization affects sequence length and compute cost, but left the practical implications mostly implicit. It did not make the unequal token-budget consequences of multilingual segmentation concrete for a core-route reader. |
| Change made | Added a compact bilingual callout on context-budget consumption, sequence-processing cost, multilingual variation, and the distinction between representation efficiency and language quality. Added a corresponding self-check to both exercise pages. |
| Depth placement | Core consequence on this page; tokenizer metrics, empirical comparisons, and algorithm details remain in the linked Deepen pages. |
| Validation | Source files fetched from the repository; edits applied to both language versions and both exercise pages; FR/EN content intentionally parallel. Render, link checker, and CI remain unverified. |

## Why this is the right addition

The core page already had a strong pipeline explanation and explicitly warned that token IDs are not semantic quantities. Rewriting the whole page or importing tokenizer algorithms would have duplicated the existing Deepen material. The higher-value gap was the system-level consequence:

1. At a fixed context limit, tokenization determines how much source text can fit alongside history, retrieved material, instructions and generated output.
2. Longer sequences mean more positions to process and can raise inference time or cost, although the exact effect depends on architecture, implementation, hardware and service.
3. The same content translated into different languages can occupy different token budgets. This is a representation-cost difference, not by itself evidence of a model capability gap or a language-quality ranking.

The page now states those consequences without pretending that token count alone predicts downstream quality. It hands off empirical measurement to the existing tokenizer-evaluation page rather than reproducing its metrics and literature review.

## Research basis already curated in the companion evaluation page

The existing `tokenizer-design-evaluation` pages provide a more detailed and appropriately qualified research synthesis:

- Goldman et al. (2024), [Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance](https://aclanthology.org/2024.findings-acl.134/): studies empirical relationships between compression and downstream results; correlation is not a universal causal selection rule.
- Schmidt et al. (2024), [Tokenization Is More Than Compression](https://aclanthology.org/2024.emnlp-main.40/): argues that compression alone does not capture every relevant tokenizer property.
- Ali et al. (2024), [Tokenizer Choice For LLM Training: Negligible or Crucial?](https://aclanthology.org/2024.findings-naacl.247/): studies tokenizer effects on decoder-only model training cost and downstream performance under specified model, language and evaluation conditions; individual reported cost differences must not be generalized as universal inference penalties.
- Arnett et al. (2025), [Explaining and Mitigating Crosslingual Tokenizer Inequities](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5b91cefbfa52340af2f16f249572dc76-Abstract-Conference.html): analyzes cross-language compression differences across many tokenizer configurations, but does not train LLMs in that study to establish downstream quality effects.
- Chiu (ACL 2026), [TokLens: A Multilingual Lens on Tokenizer Quality for LLMs](https://aclanthology.org/2026.acl-srw.18/): proposes multilingual intrinsic metrics and reports associations in bounded benchmark settings; the observed relationships are correlational and do not establish causal tokenizer effects.

The detailed study summaries and caveats remain on the companion page. The core lesson links there rather than duplicating its research table.

## Double-audience test after the change

- **Beginner:** can explain why a context limit is counted in tokens, why tokenization changes the amount of text that fits, and why fewer tokens do not mean more meaning.
- **Experienced reader:** is prompted to distinguish representation efficiency, context allocation, system cost and downstream language quality—four quantities that are easy to conflate.
- **Remaining opportunity:** a later exercise or controlled experiment could compare token counts for parallel texts using pinned tokenizer revisions and report distributions by language and text type. That experiment should live in Practice/experiment, not be simulated with invented counts on this concept page.

## Files changed in this page pass

- `site/fr/text-data.qmd`
- `site/en/text-data.qmd`
- `site/fr/exercises/text-data.qmd`
- `site/en/exercises/text-data.qmd`

**Not claimed:** no full site render, visual inspection, learner study, or CI run has been completed as part of this page pass.


---

# Addendum — page audit 2/6: `logits`

**Status:** second page of wave 1 reviewed and enriched in both languages. Source-level review only; rendered browser experience and CI build remain unverified.

## Page identity and ownership

- FR: `site/fr/logits.qmd`
- EN: `site/en/logits.qmd`
- Practice: `site/fr/exercises/logits.qmd` and `site/en/exercises/logits.qmd`
- Role: core Understand lesson between causal masking and output probabilities.
- Canonical boundary: define the vocabulary score vector, its dimensions and local ranking; the next page owns softmax, probability distributions, temperature and calibration.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | What does the model produce immediately before a next-token probability distribution is formed? |
| Beginner outcome | Understand that the output head produces one real-valued score per vocabulary item, and that scores are not probabilities. |
| Experienced-reader value already present | The page connects the final hidden state to a vocabulary-sized output projection and notes that cross-entropy implementations can consume unnormalized logits directly. |
| Best-source contribution | The existing PyTorch CrossEntropyLoss documentation gives an implementation-level contract: the loss expects unnormalized logits. The adjacent probability lesson supplies the softmax mathematics and temperature interpretation. |
| LLM Lab synthesis | Make the distinction between absolute score level and relative score differences explicit, then connect the invariance to the next page's softmax treatment. |
| Weak element before this change | The page warned that raw logits depend on scale and offset, but did not explain what that means. A reader could still treat a large positive logit as an absolute confidence signal. |
| Change made | Added a worked common-offset example, `(2, 1)` versus `(102, 101)`, explaining why both produce the same softmax distribution. Clarified that multiplying logits by a positive factor can change distribution concentration while preserving ranking. Added a matching exercise in both languages. |
| Depth placement | The page gives the invariant and its intuition; the probability page retains the formal softmax properties, probability ratios and temperature treatment. |
| Validation | Source files fetched; FR/EN pages and exercise pages updated in parallel. No rendered-site or CI verification yet. |

## Why this is the right addition

The important distinction is not merely that logits may be positive or negative. Their absolute origin is arbitrary for softmax: adding a common constant to every component changes neither the normalized distribution nor the ranking. Differences between logits determine probability ratios. By contrast, positive rescaling can change the distribution's concentration, which is why temperature can alter sampling behavior without changing the argmax.

This provides a concrete experienced-reader insight while remaining accessible through a two-number example. It also clarifies why raw logits from different prompts or models should not be compared as if they were absolute confidence measurements. The adjacent probability page already contains the formal invariance and temperature relationships; it now acts as the mathematical follow-through rather than having that material copied into this lesson.

## Double-audience test after the change

- **Beginner:** can explain why a logit of 100 is not automatically stronger evidence than a logit of 2, and why scores must be interpreted relative to the rest of the vector.
- **Experienced reader:** can state the softmax shift invariance, distinguish offset from scale, and connect the latter to temperature.
- **Remaining opportunity:** a small numerical comparison in the probability lesson could explicitly compute the same distribution for the two shifted vectors, if that would aid the derivation. Avoid duplicating the current concept-page example verbatim.

## Files changed in this page pass

- `site/fr/logits.qmd`
- `site/en/logits.qmd`
- `site/fr/exercises/logits.qmd`
- `site/en/exercises/logits.qmd`

**Not claimed:** no full site render, visual inspection, learner study, or CI run has been completed as part of this page pass.


---

# Addendum — page audit 3/6: `positional-encoding`

**Status:** third page of wave 1 reviewed and enriched in both languages. Source-level review only; rendered browser experience and CI remain unverified.

## Page identity and ownership

- FR: `site/fr/positional-encoding.qmd`
- EN: `site/en/positional-encoding.qmd`
- Practice: `site/fr/exercises/positional-encoding.qmd` and `site/en/exercises/positional-encoding.qmd`
- Role: core Understand lesson between embedding lookup and contextualized representations.
- Canonical boundary: explain why order must enter the computation and distinguish absolute encodings, relative mechanisms, RoPE and causal visibility. Mathematical derivations remain in the sinusoidal and RoPE deep dives.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | How can a Transformer distinguish sequences whose tokens are the same but occur in a different order? |
| Beginner outcome | Understand why content-only attention is permutation equivariant, where positional information enters, and why causal masking is a separate constraint. |
| Experienced-reader value already present | The page includes a permutation-equivariance derivation and an optional derivation of the fixed-shift property of sinusoidal encodings. It correctly classifies RoPE as a relative mechanism rather than a third disjoint family. |
| Best-source contribution | Vaswani et al. (2017) establishes the original sinusoidal design; Su et al. (2021) gives the RoPE formulation. The existing deep dives derive their geometry and discuss implementation and extrapolation limitations. |
| LLM Lab synthesis | Connect the mathematical ability to compute positional signals with the separate empirical question of whether a trained model generalizes to longer contexts. |
| Weak element before this change | The core page explained insertion points and the mathematical structure but did not surface the crucial distinction between computing a positional signal at a new index and reliably using that position beyond the training regime. |
| Change made | Added a bilingual callout: computability of sinusoidal positions and the existence of RoPE do not by themselves guarantee long-context extrapolation. Added a matching practice question. Corrected the exercise-page closing criterion, which had inaccurately called absolute encodings, relative mechanisms and RoPE “three families”. |
| Depth placement | The core page states the general caveat; the sinusoidal and RoPE deep dives retain the detailed analysis of frequencies, scaling methods, implementation conventions and evaluation. |
| Validation | FR/EN source files and exercises updated in parallel. The exercise terminology now matches the canonical classification in both lessons. No rendered-site or CI verification yet. |

## Why this is the right addition

This page was already one of the stronger candidates in the initial diagnostic. It is not a generic introduction: the permutation-equivariance argument, the distinction between absolute and relative information, the exact insertion point of RoPE, and the optional sinusoidal shift derivation provide real intellectual value.

The missing high-level insight was a common extrapolation misconception. A positional formula may be defined for arbitrary indices, but the trained network's behaviour at those indices is a separate empirical question. The same caution applies to RoPE: the mechanism alone does not guarantee reliable long-context use. The detailed deep dives already explain the relevant conditions, so the core page needed only a concise warning and a handoff.

The review also caught a small but genuine conceptual inconsistency in the exercises: RoPE is explicitly described in the lesson as a member of the relative family, but the exercise summary asked learners to distinguish “three families”. That wording is now corrected to distinguish absolute encodings from relative mechanisms and to identify RoPE as one example of the latter.

## Double-audience test after the change

- **Beginner:** can distinguish “the formula returns a vector” from “the model can use that position reliably”.
- **Experienced reader:** is reminded that positional extrapolation is a property of the trained system and its context-extension recipe, not a guarantee conferred by a positional encoding in isolation.
- **Remaining opportunity:** the next audit should check whether `generation` and `llm-computational-complexity` explain the operational distinction between nominal context length, usable context and inference cost without duplicating this positional caveat.

## Files changed in this page pass

- `site/fr/positional-encoding.qmd`
- `site/en/positional-encoding.qmd`
- `site/fr/exercises/positional-encoding.qmd`
- `site/en/exercises/positional-encoding.qmd`

**Not claimed:** no full site render, visual inspection, learner study, or CI run has been completed as part of this page pass.


---

# Addendum — page audit 4/6: `scaled-dot-product-attention`

**Status:** fourth page of wave 1 reviewed. The core lesson already meets much of the dual-audience ambition; the only change in this pass is a matching practice question in French and English. Source-level review only; rendered browser experience and CI remain unverified.

## Page identity and ownership

- FR: `site/fr/scaled-dot-product-attention.qmd`
- EN: `site/en/scaled-dot-product-attention.qmd`
- Practice: `site/fr/exercises/scaled-dot-product-attention.qmd` and `site/en/exercises/scaled-dot-product-attention.qmd`
- Role: core Understand lesson after Q/K/V and before causal masking.
- Canonical boundary: explain the full scaled dot-product attention computation and weighted aggregation; the scaling derivation belongs to `attention-score-scaling`, causal visibility to `causal-masking`, and Q/K/V roles to the preceding lesson.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | How does a position use learned compatibility scores to aggregate information from other accessible positions? |
| Beginner outcome | Follow scores → scaling → optional mask → row-wise softmax → weighted sum of values, and distinguish scores, weights and output vectors. |
| Experienced-reader value already present | The page explicitly rejects the interpretation of attention weights as semantic relevance or causal explanation. Its counterexample follows the contribution through `alpha_ij v_j`, notes that the value-vector norm matters, and traces the signal through output projection, residual connections, normalization and MLP. |
| Best-source contribution | Vaswani et al. (2017) grounds the scaled dot-product formulation. The project's dedicated scaling page supplies a Gaussian-assumption derivation and a numerical simulation, while the Q/K/V lesson explains the distinct routing and content paths. |
| LLM Lab synthesis | The page already gives a strong local-to-system explanation and a rigorous interpretive boundary. The improvement opportunity was to make the attention-weight caveat an explicit learner check, not to add another explanatory section. |
| Weak element before this change | The key caveat was explained in the lesson but not tested in the dedicated practice page, which contained only a numerical softmax calculation. |
| Change made | Added a bilingual exercise asking whether a weight of 0.95 proves the largest output contribution or causal importance. The worked answer uses the norm of `alpha_ij v_j` and the later transformations to explain why not. |
| Depth placement | The full argument remains in the core lesson; the exercise checks transfer of that argument. The scaling derivation remains in its Deepen page. |
| Validation | FR/EN exercise sources updated in parallel; LaTeX norm delimiters were checked and corrected. No rendered-site or CI verification yet. |

## Why no main-page rewrite was made

The preliminary prioritization correctly identified this page as a place where the distinction between attention and explanation matters, but the detailed source inspection shows that the published page already treats it unusually well. It explicitly explains that a high weight is only a relative aggregation weight, not a causal claim, and goes beyond the generic warning by examining the direct vector contribution and subsequent network transformations.

Adding a second generic “attention is not explanation” box would have duplicated existing content and weakened editorial economy. The appropriate correction was to reinforce the insight in practice instead.

## Double-audience test

- **Beginner:** can calculate the attention weights and explain that they are relative weights used to combine value vectors, not percentages of semantic relevance.
- **Experienced reader:** can distinguish attention weight, vector contribution, downstream influence and causal importance.
- **Remaining opportunity:** a later experiment could compare attention-weight visualizations with intervention-based changes to outputs, but it should be a controlled Practice experiment and must not imply that one intervention metric is a universal explanation method.

## Files changed in this page pass

- `site/fr/exercises/scaled-dot-product-attention.qmd`
- `site/en/exercises/scaled-dot-product-attention.qmd`

**Not claimed:** no full site render, visual inspection, learner study, or CI run has been completed as part of this page pass.


---

# Addendum — page audit 5/6: `vraisemblance` / `likelihood`

**Status:** fifth page of wave 1 reviewed in French and English, including the dedicated exercise pages and the adjacent entropy, cross-entropy and loss lessons. A small bilingual clarification is added; source-level review only.

## Page identity and conceptual boundary

- FR: `site/fr/vraisemblance.qmd`; EN: `site/en/likelihood.qmd`
- Practice: `site/fr/exercises/vraisemblance.qmd` and `site/en/exercises/likelihood.qmd`
- Role: evaluate the probability assigned to an already observed token sequence under fixed model parameters.
- Boundary: entropy describes the spread of a predictive distribution before observing a target; sequence likelihood multiplies conditional probabilities of observed targets; cross-entropy expresses the penalty against a target distribution at a position; loss aggregates valid local penalties into an objective.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | How does a model score a known sequence, and what does that score mean? |
| Beginner outcome | Understand reference-prefix scoring, the chain-rule product, log-likelihood and NLL without confusing scoring, generation and training. |
| Experienced-reader value already present | The page correctly distinguishes teacher-forced scoring from autoregressive generation and parameter updates; it also discusses context-window limits, tokenizer dependence and reduction conventions. |
| Adjacent-page check | `entropy` distinguishes predictive entropy from realized surprisal; `cross-entropy` derives the one-position target penalty and its relation to NLL; `loss` covers masking, target alignment, reduction and perplexity. The conceptual handoffs are sound and mostly non-duplicative. |
| Exercise check | FR/EN exercises correctly state that the chain rule requires no token-independence assumption, distinguish sequence NLL from mean per-token NLL, and connect the mean to one-hot cross-entropies. |
| Gap found | The main likelihood lesson explained NLL and comparison conventions but did not explicitly state the familiar bridge from mean NLL to perplexity, although the exercise hub and adjacent loss lesson already referred to perplexity. |
| Change made | Added a concise bilingual paragraph: for natural-log mean NLL, `PPL = exp(mean NLL)`; interpreted it as the geometric mean of inverse observed-token probabilities; and reiterated that corpus, tokenizer, evaluated positions and reduction must be compatible for comparison. Linked the detailed metric discussion to the Loss lesson. |
| Depth placement | Kept implementation details, masks and batch aggregation in `cross-entropy` and `loss`; did not duplicate their explanations in the likelihood page. |
| Validation | Reviewed source content of both lessons, both exercise pages, entropy, cross-entropy and loss. The new FR/EN paragraph uses the same formula and qualifications. No rendered-site, browser or CI validation is claimed. |

## Why this is the right addition

The page already explains the probability of an observed sequence and the transformation from product to sum. The missing conceptual bridge was not another derivation of NLL, but a clear statement of what the commonly reported perplexity is mathematically and what it does not measure. The geometric-mean interpretation makes the exponentiation less arbitrary, while the comparison caveat prevents readers from treating perplexity as tokenizer-independent or as a direct measure of answer quality.

The audit also confirms that several likely additions would be redundant: the chain rule and independence caveat are already tested in the exercises; entropy versus observed surprise is handled by the preceding page; one-token cross-entropy and valid-target masking belong to the next page; batch reduction and metric interpretation belong to Loss. No broad rewrite is warranted.

## Double-audience test

- **Beginner:** can explain that perplexity is the exponential of mean token NLL and is not a truth or answer-quality score.
- **Experienced reader:** can connect perplexity to the geometric mean of inverse token probabilities and identify tokenizer, corpus, target-position and reduction constraints on comparisons.
- **Remaining opportunity:** a future controlled experiment could show how tokenization changes token-level perplexity for the same text, but it should report the tokenizer and evaluation protocol explicitly rather than imply a universal cross-tokenizer conversion.

## Files changed in this page pass

- `site/fr/vraisemblance.qmd`
- `site/en/likelihood.qmd`
- `docs/audits/learning-path-excellence-audit.md`

**Not claimed:** no full site render, visual inspection, learner study, or CI run has been completed as part of this page pass.


---

# Addendum — page audit 6/6: `training-loop`

**Status:** sixth page of wave 1 reviewed in French and English, with a cross-check against `loss` and `gradients`. One mathematical qualification is tightened in both languages. Source-level review only.

## Page identity and conceptual boundary

- FR: `site/fr/training-loop.qmd`; EN: `site/en/training-loop.qmd`
- Role: connect the forward pass, loss, backpropagation, optimizer update, repeated batches and held-out validation into one training process.
- Boundary: `loss` owns target alignment, masking and reduction; `gradients` owns differentiation and the basic update derivation; this page owns the iteration-level system, optimizer role, train/validation/test distinction, overfitting and pretraining scale. Optimizer internals, schedules, clipping and distributed training are explicitly deferred.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | What actually changes the model during training, and how can we tell whether repeated updates generalize? |
| Beginner outcome | Follow one update, distinguish gradient from optimizer, understand epochs and stochastic batches, and read training versus validation curves. |
| Experienced-reader value already present | The page includes a runnable minimal language-model experiment with a held-out split, a reproducible seed, qualitative assertions, and explicit limits on what the toy table demonstrates. It explains why validation-guided decisions make the validation score optimistic and why a test split must remain reserved. |
| Adjacent-page check | `loss` supplies the target/mask/reduction contract; `gradients` supplies the derivative and SGD update. The training-loop lesson correctly links these without reproducing their derivations. |
| Bilingual check | The main FR and EN lessons have matching conceptual sequence, toy experiment, caveats and self-check questions. A dedicated `exercises/training-loop.qmd` file was not present at the expected paths; the main lesson itself contains three worked self-check questions, so no missing exercise page is assumed. |
| Gap found | One warning about cross-entropy having “no finite minimum on a perfectly fitted dataset” was broader than the mathematical condition warrants. The asymptotic statement applies to perfectly separable one-hot targets with unregularized softmax logits, not universally to every objective or dataset. |
| Change made | Qualified the statement identically in FR and EN: for perfectly separable one-hot targets without regularization, softmax cross-entropy can approach zero as logit confidence grows, without reaching zero at finite logits. Explicitly stated that this is not universal. |
| Depth placement | Kept schedules, clipping, optimizer internals and distributed training out of the core page, as its scope promises. The toy experiment remains the distinctive advanced contribution rather than adding a generic expert callout. |
| Validation | Reviewed both lesson sources and adjacent loss/gradient explanations. The FR/EN qualification is conceptually aligned. No code execution, full site render, browser inspection, or CI pass is claimed for this page audit. |

## Why this is the right correction

The original sentence compressed a useful intuition into a statement that could be read as a theorem about all perfectly fitted datasets. For ordinary unregularized softmax classification with one-hot targets that are perfectly separable, increasing the logit margin can keep lowering cross-entropy toward zero; finite logits still assign nonzero probability to alternatives. But non-separable data, soft targets, regularization, or other objective terms change that conclusion. Naming the assumptions makes the statement useful to an advanced reader without burdening the beginner with a full optimization detour.

The page otherwise needs no broad rewrite. Its strongest contribution is the compact, executable experiment showing that training loss can keep falling while held-out validation loss turns upward, together with a clear warning that this tiny lookup-table model is not a Transformer and does not prove a universal curve shape.

## Double-audience test

- **Beginner:** can identify the optimizer update as the operation that changes parameters and explain why validation data must not update them.
- **Experienced reader:** can distinguish the stochastic batch gradient from the full-data gradient, recognize validation-selection optimism, and state the assumptions behind the softmax cross-entropy asymptote.
- **Remaining opportunity:** a future extension could compare fixed-step SGD with a learning-rate schedule or AdamW on the same controlled toy problem, but it should preserve the fixed data split and report optimizer state and stopping rules. This belongs in a reproducible experiment, not another prose subsection.

## Files changed in this page pass

- `site/fr/training-loop.qmd`
- `site/en/training-loop.qmd`
- `docs/audits/learning-path-excellence-audit.md`

**Not claimed:** no full site render, visual inspection, learner study, code execution, or CI validation has been completed as part of this page pass.


---

# Addendum — second-wave audit 1/6: `llm-overview`

**Status:** French and English overview lessons and their exercise hubs reviewed. No content change is warranted in this pass; source-level review only.

## Page identity and role

- FR: `site/fr/llm-overview.qmd`; EN: `site/en/llm-overview.qmd`
- Practice: `site/fr/exercises/llm-overview.qmd` and `site/en/exercises/llm-overview.qmd`
- Role: orient the reader to what an LLM predicts, how a token distribution is used, and how architecture, training and application-level use differ.
- Boundary: this is a system overview, not a substitute for the canonical lessons on tokenization, Transformer internals, probabilities, generation, likelihood or training.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | What is an LLM, what does it compute, and how does that computation become a useful application? |
| Beginner outcome | Explain next-token prediction, context and fixed parameters; distinguish generating, scoring and learning; distinguish LLM, Transformer and GPT. |
| Experienced-reader value already present | The page separates model computation from token selection, scoring from evaluation, base models from foundation models, and model-generated tool requests from application-side execution. It also states that a role label does not enforce a policy and that persistent memory requires application-side storage. |
| Bilingual check | The French Asterix and English Monty Python hooks are deliberate localizations, not a conceptual mismatch. Both versions retain the same conceptual progression and distinguish the fictional scene from the original LLM Lab continuation used for calculations. Exercise hubs are aligned on fine-tuning, RAG, tool execution and message roles. |
| Gap found | No critical conceptual gap found in the reviewed source. The page is long for an overview, but its first-minute summary, “cross-cutting overview” note and explicit first-pass reading guidance make the intended progressive reading visible. |
| Change made | None. Rewriting the page to shorten it would risk removing useful system-boundary distinctions; duplicating the detailed mechanics would blur the canonical lesson boundaries. |
| Depth placement | Keep the overview's role as a map of the system. Defer mechanisms and derivations to the linked canonical lessons; retain tool orchestration and application memory as system-level distinctions rather than Transformer internals. |
| Validation | Reviewed both main lessons and both exercise hubs. No rendered browser inspection, learner study or CI validation is claimed. |

## Why no rewrite was made

The overview already contributes more than a generic definition: it teaches readers not to conflate a model with the application around it. In particular, it distinguishes a model's structured tool-call request from actual tool execution, message-format roles from Transformer layers, and context-window contents from persistent memory. These are useful conceptual boundaries for readers moving from model fundamentals to deployed systems.

The page is information-dense, but it explicitly marks itself as cross-cutting and offers a first-pass route through the essential concepts. The better editorial choice is to preserve that layering and avoid turning the overview into another detailed chapter.

## Double-audience test

- **Beginner:** can explain next-token prediction and distinguish generation, scoring and training without memorizing every implementation term.
- **Experienced reader:** can identify where the model ends and application orchestration, retrieval, persistent storage and evaluation begin.
- **Remaining opportunity:** a future visual systems map could make the boundary between model, inference runtime and surrounding application even more explicit, but only if it clarifies rather than duplicates the existing three-use and application diagrams.

---

# Addendum — second-wave audit 2/6: `generation`

**Status:** French and English generation lessons and their exercise hubs reviewed. No content change is warranted in this pass; source-level review only.

## Page identity and role

- FR: `site/fr/generation.qmd`; EN: `site/en/generation.qmd`
- Practice: `site/fr/exercises/generation.qmd` and `site/en/exercises/generation.qmd`
- Role: explain autoregressive inference as a loop of prediction, selection, feedback and stopping for a model whose parameters are fixed.
- Boundary: the page owns the generation loop, prefill/decode distinction, selection strategies and context constraints. Transformer internals, probability derivations, and training updates remain in their respective lessons.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | How does a next-token distribution become a complete response, and what changes at each step? |
| Beginner outcome | Trace predict → select → append → continue/stop; understand that the selected token changes the next context while model parameters remain fixed. |
| Experienced-reader value already present | The page distinguishes the forward pass, token-selection rule and complete generation loop; explains prefill versus incremental decode and the KV cache; separates the advertised context window from the tokens actually available to the response; and identifies application-level stopping and output validation. |
| Bilingual check | Both versions cover the same mechanism and caveats. Their running examples are intentionally localized (Asterix in French; Monty Python in English), while both distinguish the source scene from the original LLM Lab continuation. Exercise hubs align on stochastic sampling, temperature, fixed parameters and prefill versus teacher forcing. |
| Gap found | No critical conceptual or mathematical gap found in the reviewed source. The temperature examples are consistent with the stated distribution: squaring probabilities for `tau=0.5` and taking square roots for `tau=2` gives the displayed normalized values. |
| Change made | None. The core page already has a clear beginner route and progressive detail; advanced filters are handed off to the dedicated decoding-strategies lesson rather than expanded redundantly. |
| Depth placement | Keep KV-cache and prefill/decode explanations here at the inference-system level; leave attention internals to Q/K/V and causal attention lessons, and leave advanced decoding trade-offs to the dedicated strategy page. |
| Validation | Reviewed both main lessons and both exercise hubs. Numerical temperature table checked algebraically. No code execution, rendered browser inspection, learner study or CI validation is claimed. |

## Why no rewrite was made

The strongest pedagogical move is the separation of three levels: the network's forward computation, the decoding rule that selects a token, and the generation loop that repeats until a stopping condition. The page then builds from an accessible three-step trace to notation, prefill/decode, caching, temperature and context-window constraints. The distinction between teacher forcing and prefill is explicitly tested in both exercise hubs.

The main opportunity is not another prose subsection. It is a possible later controlled experiment comparing generation strategies while holding model, prompt and random seed protocol fixed. That experiment belongs in Practice or the decoding-strategies lesson.

## Double-audience test

- **Beginner:** can trace a token being selected and fed back, and explain why generation does not update model parameters.
- **Experienced reader:** can distinguish prefill latency from incremental decode, identify what KV caching avoids recomputing, and explain why a larger context window does not guarantee correct use of every supplied token.
- **Remaining opportunity:** test greedy, sampling, temperature and KV-cache behaviour in a controlled, reproducible experiment, without presenting one decoding strategy as universally best.


---

# Addendum — second-wave audit 3/6: `contextualized-representations`

**Status:** French and English lessons reviewed. No content change is warranted in this pass; source-level review only.

## Page identity and role

- FR: `site/fr/contextualized-representations.qmd`; EN: `site/en/contextualized-representations.qmd`
- Role: explain why the same token ID retrieves the same initial embedding but can produce different hidden states after position-aware Transformer processing.
- Boundary: the embedding table and token IDs belong to `embedding-space`; positional mechanisms belong to `positional-encoding`; the Transformer page locates the blocks; detailed attention interactions are deferred to Q/K/V and attention lessons.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | If two occurrences share one token ID, how can the model represent their different contexts? |
| Beginner outcome | Distinguish a static lookup from later hidden states, and identify where position and accessible context enter the computation. |
| Experienced-reader value already present | The page separates lexical ambiguity (`bank`) from cross-token reference (`it` / `the animal`), and explicitly warns that contextualization does not guarantee clean geometric clusters matching human senses. It also distinguishes absolute positional addition from RoPE's rotation of Q/K inside attention. |
| Bilingual check | FR/EN conceptual structure, examples, caveats and self-check questions align. Both state the assumption that the visible word is represented by the same token ID and warn that a visible word may split into several tokens. |
| Gap found | No critical conceptual gap found. The page carefully avoids attributing semantic disambiguation to the embedding lookup or claiming that one attention head necessarily performs coreference resolution. |
| Change made | None. The current page is appropriately concise relative to the advanced companion and Transformer/attention lessons. |
| Depth placement | Preserve the advanced page for formal treatment and use this page to anchor the same-ID/same-lookup versus context-dependent-state distinction. |
| Validation | Reviewed both lesson sources and checked the handoffs to embedding-space, positional encoding and Transformer. No rendered browser or learner validation is claimed. |

## Double-audience test

- **Beginner:** can explain why the lookup is identical but later hidden states can differ.
- **Experienced reader:** can distinguish tokenization, position injection, contextual computation and semantic interpretation, without overclaiming a particular geometry or attention-head function.

---

# Addendum — second-wave audit 4/6: `transformer`

**Status:** French and English lessons and exercise hubs reviewed. A mathematical overstatement about normalization is corrected in both languages and in both exercise answer sets.

## Page identity and role

- FR: `site/fr/transformer.qmd`; EN: `site/en/transformer.qmd`
- Practice: `site/fr/exercises/transformer.qmd` and `site/en/exercises/transformer.qmd`
- Role: locate the decoder-only GPT architecture, follow a forward pass through Transformer blocks to logits, and distinguish attention, MLP, residual stream, normalization and output head.
- Boundary: Q/K/V projections, attention computation and causal visibility are handed to their canonical lessons; decoding and token selection remain in generation.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | What is a Transformer block, how do its sublayers interact, and where do logits come from? |
| Beginner outcome | Follow embeddings and positional information through repeated blocks to logits; distinguish cross-position attention from position-wise MLP transformation and from downstream decoding. |
| Experienced-reader value already present | The page distinguishes attention sublayer, block and complete GPT; explains residual stream, pre-LN layout, parallel training versus sequential generation, depth versus width, and the difference between `d_model`, `d_head` and `d_ff`. |
| Bilingual check | FR/EN conceptual sequence and diagrams align. The practice hubs test the same five architectural distinctions. |
| Gap found | The explanation said that without normalization activations and gradients become unstable and training a deep stack fails. This was too categorical: the stability effect depends strongly on normalization placement and the surrounding architecture/training setup. |
| Change made | Replaced the categorical claim in both lessons and both exercise answer sets. The revised text says normalization helps control activation scale and gradient flow, then cites Xiong et al. (2020): the original Post-LN design can have large gradients near the output at initialization, whereas the studied Pre-LN variant has better-behaved gradients. It no longer implies that every deep architecture must fail without one particular arrangement. |
| Best-source contribution | Xiong et al., *On Layer Normalization in the Transformer Architecture* (ICML 2020, PMLR 119): https://proceedings.mlr.press/v119/xiong20b.html. The paper analyzes how the placement of LayerNorm affects gradient behavior and warm-up requirements. |
| Depth placement | Keep the page's pre-LN equations and model-family variants; avoid a full survey of normalization strategies. The linked paper supplies the deeper theoretical and empirical analysis. |
| Validation | Updated FR/EN main pages and FR/EN exercise answers in parallel. Source text was checked for matching assumptions and terminology. No rendered-site, visual browser, learner or CI validation is claimed. |

## Why this correction matters

A reader should not leave with the rule “no LayerNorm means a deep Transformer cannot train.” The evidence cited here supports a more precise lesson: where normalization sits in the residual block affects gradient magnitudes and optimization stability. The original Post-LN arrangement and Pre-LN variants can behave differently even though both use normalization. The revision preserves the useful beginner intuition that normalization supports stable optimization while removing the unsupported universal failure claim.

## Double-audience test

- **Beginner:** can say that normalization helps keep deep computation trainable, without memorizing the Post-LN/Pre-LN derivation.
- **Experienced reader:** can identify normalization placement as an architectural and optimization choice, and connect it to gradient behavior at initialization.
- **Remaining opportunity:** a controlled experiment could compare gradient norms across depth for Post-LN and Pre-LN on the same small Transformer. It should be implemented as a reproducible experiment rather than added as a long derivation to this overview lesson.


---

# Addendum — second-wave audit 5/6: `queries-keys-values`

**Status:** French and English lessons and their exercise hubs reviewed. No content change is warranted in this pass; source-level review only.

## Page identity and role

- FR: `site/fr/queries-keys-values.qmd`; EN: `site/en/queries-keys-values.qmd`
- Practice: `site/fr/exercises/queries-keys-values.qmd` and `site/en/exercises/queries-keys-values.qmd`
- Role: introduce the three learned projections from a shared input and explain why Q/K determine attention weights while V supplies the content being aggregated.
- Boundary: score scaling, masking, softmax and weighted aggregation are derived in the scaled-dot-product-attention lesson; causal visibility belongs to causal masking; detailed geometry and multi-head variants are deferred to the advanced Q/K/V page and practice collection.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | Why does self-attention need three learned projections from one representation stream? |
| Beginner outcome | Distinguish the query, key and value roles and explain the two paths: compatibility/routing (Q and K) and content aggregation (V). |
| Experienced-reader value already present | The lesson states the shared-input parameterization, distinct learned matrices, dimensions `d_k` and `d_v`, and the distinction from cross-attention where Q and K/V originate from different streams. It avoids anthropomorphic claims and does not treat attention weights as universal semantic relevance. |
| Bilingual check | FR/EN definitions, equations, dimensions, examples and self-checks align. Exercise hubs add a useful nuance: changing V with Q/K fixed leaves weights unchanged, but the aggregate need not change if weighted differences cancel. |
| Gap found | No critical conceptual gap found. The page's deliberate decision not to perform matrix calculations is appropriate for its core role; the deeper exercises carry those operations and transfer to cross-attention and GQA/MQA. |
| Change made | None. The lesson already contains the distinctive routing-versus-content insight and the exercise hub tests it without duplicating the full derivation. |
| Depth placement | Keep the core page conceptual; leave dot-product scaling, causal constraints and the output weighted sum to their canonical pages. |
| Validation | Reviewed both lessons and both exercise hubs. No rendered browser or learner validation is claimed. |

## Double-audience test

- **Beginner:** can explain Q/K as determining where information is weighted and V as supplying what is combined.
- **Experienced reader:** can reason about independent changes to Q, K and V, distinguish self-attention from cross-attention, and recognize that weights are not semantic labels.

---

# Addendum — second-wave audit 6/6: `causal-masking`

**Status:** French and English lessons and exercise hubs reviewed, with a source-level cross-check of the reference implementation and tests. No content change is warranted in this pass.

## Page identity and role

- FR: `site/fr/causal-masking.qmd`; EN: `site/en/causal-masking.qmd`
- Practice: `site/fr/exercises/causal-masking.qmd` and `site/en/exercises/causal-masking.qmd`
- Implementation: `src/llm_lab/foundations/attention.py`; tests: `tests/unit/test_attention.py`
- Role: express the autoregressive information constraint as a lower-triangular attention mask and explain why it must be applied before softmax.
- Boundary: Q/K/V projections belong to the preceding lesson; score computation and weighted aggregation belong to scaled dot-product attention; target shifting and loss masking are distinct training-data/objective concerns.

## Page-level value record

| Field | Finding |
|---|---|
| Learner question | How can all training positions be computed in parallel without allowing a position to use future tokens? |
| Beginner outcome | Read the rule `j ≤ i`, understand why the diagonal is allowed when predicting the next token, and distinguish causal masking from padding and loss masks. |
| Experienced-reader value already present | The page treats masking as an information-flow constraint, not a visual convention; explains boolean-mask polarity differences between PyTorch APIs; handles fully masked rows explicitly; and states the prefix-invariance property needed to detect future leakage beyond inspecting the mask matrix. |
| Bilingual check | FR/EN equations, mask conventions, API warning, misconception checks and exercise hub align. The documentation-version note is explicit rather than silently assuming boolean-mask polarity is universal. |
| Implementation check | The reference `causal_mask` returns a lower-triangular additive mask with 0 on allowed positions and `-inf` on future positions. The attention primitive accepts an additive mask of exact shape `(T_q, T_k)`, rejects invalid entries and handles fully masked rows with zero weights and output. Unit tests verify mask structure, fully masked-row behaviour, zero future weights and prefix invariance when a future key/value is changed. The page correctly warns that this is a primitive-level test, not a complete-GPT test. |
| Gap found | No critical gap found. The implementation note is accurately scoped and does not overclaim that testing the mask alone proves the complete model is free of leakage. |
| Change made | None. The lesson is already unusually precise about API conventions, numerical edge cases and the difference between an attention primitive and a full model. |
| Depth placement | Preserve the main explanation and the advanced API/code note. Future extension should test a complete model's prefix invariance, but that is a separate implementation milestone, not a reason to expand this concept page. |
| Validation | Reviewed both lessons, both exercise hubs, `attention.py` and `test_attention.py`. Source-level cross-check only; tests were read, not executed in this pass. No full model test or browser validation is claimed. |

## Double-audience test

- **Beginner:** can explain why future tokens must be blocked before softmax and why the current position remains visible when predicting the next token.
- **Experienced reader:** can distinguish boolean-mask API polarity, handle fully masked rows, and understand why prefix-invariance tests are stronger than checking the triangular matrix alone.
- **Remaining opportunity:** add an end-to-end causal-invariance test for a complete small GPT once the implementation milestone exists; retain the current primitive-level test as a lower-level invariant.
