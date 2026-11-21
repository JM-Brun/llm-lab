# Évaluation avec des apprenants du parcours principal / Learner evaluation of the main path

> **Statut / Status:** protocole prêt à piloter / protocol ready for a pilot. **Aucune session n'a encore été menée et aucun résultat utilisateur n'est revendiqué.** / **No sessions have been run and no learner results are claimed.**

Ce protocole prend le relais de l'audit éditorial des 18 leçons. Il vise à vérifier la compréhension, la progression et la valeur ajoutée pour deux publics, sans confondre qualité du texte, facilité de navigation et apprentissage réel.

This protocol follows the editorial audit of the 18 lessons. It tests comprehension, progression, and added value for two audiences without conflating writing quality, navigation usability, and actual learning.

---

## 1. Questions de recherche / Research questions

1. **Compréhension débutante / Beginner comprehension:** après lecture, les participants peuvent-ils expliquer le mécanisme avec leurs propres mots et résoudre un cas nouveau ?
2. **Progression / Progression:** les prérequis sont-ils disponibles au moment où une leçon les mobilise ? Les transitions entre pages sont-elles comprises ?
3. **Transfert / Transfer:** les participants peuvent-ils réutiliser une idée dans un contexte légèrement différent, plutôt que répéter une phrase du cours ?
4. **Valeur expérimentée / Experienced-reader value:** les lecteurs déjà familiers des LLM découvrent-ils une distinction, une limite, un compromis ou un lien systémique utile ?
5. **Navigation / Navigation:** les participants savent-ils où aller ensuite et distinguent-ils Understand, Practice et Build ?
6. **Charge cognitive / Cognitive load:** quels passages provoquent surcharge, retour en arrière, abandon ou confiance injustifiée ?

## 2. Participants et portée / Participants and scope

### Cohorte débutante / Beginner cohort

Recruter **4 à 6 personnes** qui n'ont pas construit de Transformer ni suivi un cours avancé de modélisation du langage. Une familiarité d'usage avec ChatGPT est acceptable. Noter séparément les connaissances en Python, algèbre linéaire, probabilités et machine learning ; ne pas exclure automatiquement les personnes qui ont une de ces bases.

Recruit **4–6 people** who have not built a Transformer or taken an advanced language-modeling course. Familiarity with ChatGPT is acceptable. Record Python, linear algebra, probability, and machine-learning background separately; do not automatically exclude people with one of these foundations.

### Cohorte expérimentée / Experienced cohort

Recruter **3 à 5 personnes** ayant déjà étudié ou implémenté au moins une partie d'un Transformer/LLM. Relever leur expérience réelle (lecture, entraînement, fine-tuning, inférence, recherche) plutôt que leur seul intitulé de poste.

Recruit **3–5 people** who have previously studied or implemented at least part of a Transformer/LLM. Record their actual experience (reading, training, fine-tuning, inference, research), not job title alone.

### Interprétation / Interpretation

Il s'agit d'une **étude formative exploratoire**, pas d'un échantillon représentatif ni d'un test statistique d'efficacité. Avec ces effectifs, rechercher des problèmes récurrents et des mécanismes explicatifs ; ne pas publier de pourcentages comme s'ils estimaient une population.

This is a **formative exploratory study**, not a representative sample or a statistical effectiveness trial. With these sample sizes, look for recurring problems and explanatory mechanisms; do not report percentages as population estimates.

## 3. Préparation / Preparation

- Utiliser la version publiée du site et noter la date, la langue, l'appareil et la largeur d'écran.
- Préparer un environnement vierge, sans historique de navigation ni aide du facilitateur.
- Demander aux participants de penser à voix haute, sans leur enseigner la réponse pendant les tâches.
- Enregistrer uniquement les notes nécessaires. Audio/vidéo seulement avec consentement explicite ; pseudonymiser les notes et supprimer les données brutes selon une durée annoncée.
- Avant la session, recueillir le niveau de confiance initial (1–5) et les prérequis déclarés. Ne pas faire de quiz éliminatoire.

- Use the published site and record its date, language, device, and viewport width.
- Prepare a clean environment, without browsing history or facilitator help.
- Ask participants to think aloud; do not teach the answer during tasks.
- Record only necessary notes. Audio/video only with explicit consent; pseudonymize notes and delete raw data according to a stated retention period.
- Before the session, collect initial confidence (1–5) and self-reported prerequisites. Do not use a screening quiz.

## 4. Déroulé d'une session / Session outline

Durée cible : **50 à 60 minutes**.

| Étape | Durée | Action |
|---|---:|---|
| Accueil et consentement | 5 min | Expliquer qu'on teste le parcours, pas la personne. |
| Profil initial | 5 min | Expérience, prérequis, confiance initiale. |
| Tâches guidées par objectif | 30–35 min | Quatre tâches ci-dessous, sans indiquer la page à ouvrir. |
| Retour réflexif | 5–10 min | Difficultés, surprises, valeur perçue, prochaine étape. |
| Vérification différée courte | 5 min | Une question de transfert sans consulter le site, si le temps le permet. |

Target duration: **50–60 minutes**.

| Step | Duration | Action |
|---|---:|---|
| Welcome and consent | 5 min | Explain that the path is being tested, not the participant. |
| Initial profile | 5 min | Experience, prerequisites, initial confidence. |
| Goal-based tasks | 30–35 min | Four tasks below, without naming the page to open. |
| Reflection | 5–10 min | Difficulties, surprises, perceived value, next step. |
| Short delayed check | 5 min | One transfer question without the site, if time allows. |

## 5. Tâches et questions / Tasks and prompts

Les tâches sont identiques dans leur intention pour les deux cohortes. Adapter seulement le vocabulaire si nécessaire ; ne pas donner d'indice conceptuel.

Tasks have the same intent for both cohorts. Adapt vocabulary only when necessary; do not provide conceptual hints.

### Tâche A — Du texte à la représentation / From text to representation

**Consigne :** « Expliquez le trajet d'un texte saisi jusqu'à la représentation utilisée par le Transformer. Qu'est-ce qui change si la même phrase est tokenisée en davantage de morceaux ? »

**Transfert :** « À fenêtre de contexte fixe, pourquoi deux langues ou deux formulations peuvent-elles laisser une quantité différente de texte exploitable ? »

**À observer :** distinction texte/tokens/IDs/vecteurs ; ordre des opérations ; lien entre fragmentation, budget de contexte et coût ; absence d'assimilation entre ID et sens.

**Prompt:** “Explain the path from entered text to the representation used by the Transformer. What changes if the same sentence is split into more pieces?”

**Transfer:** “With a fixed context window, why might two languages or phrasings leave different amounts of usable text?”

**Observe:** distinction between text/tokens/IDs/vectors; operation order; link between fragmentation, context budget, and cost; no conflation of token ID with meaning.

### Tâche B — Des scores à l'incertitude / From scores to uncertainty

**Consigne :** « Un modèle produit les logits (2, 1). Que peut-on en conclure, et que ne peut-on pas en conclure ? Que change l'ajout de 100 à chaque logit ? »

**Transfert :** « Deux distributions ont la même prédiction la plus probable, mais des répartitions différentes. Comment expliquer cette différence sans confondre probabilité, certitude et vérité ? »

**À observer :** logits non assimilés à des probabilités ; invariance de softmax à un décalage commun ; distinction argmax/distribution ; interprétation prudente de l'entropie et de la confiance.

**Prompt:** “A model produces logits (2, 1). What can and cannot be concluded? What changes if 100 is added to every logit?”

**Transfer:** “Two distributions have the same most likely prediction but different spreads. Explain the difference without conflating probability, certainty, and truth.”

**Observe:** logits are not treated as probabilities; softmax invariance to a common shift; distinction between argmax and distribution; careful interpretation of entropy and confidence.

### Tâche C — Attention et masque causal / Attention and causal masking

**Consigne :** « Expliquez comment une position peut utiliser l'information d'autres positions. Pourquoi une visualisation de poids d'attention ne suffit-elle pas à prouver qu'un token est important ou qu'un raisonnement a eu lieu ? »

**Transfert :** « Que doit empêcher le masque causal pendant la prédiction du token suivant ? Est-ce une affirmation sur la causalité dans le monde ? »

**À observer :** rôles de Q/K/V et des valeurs ; mélange d'information ; poids ≠ contribution complète ni explication ; causalité computationnelle distinguée de causalité du monde.

**Prompt:** “Explain how one position can use information from other positions. Why does an attention-weight visualization not prove that a token is important or that reasoning occurred?”

**Transfer:** “What must causal masking prevent during next-token prediction? Is this a claim about causality in the world?”

**Observe:** roles of Q/K/V and values; information mixing; weights are not the full contribution or an explanation; computational causality distinguished from real-world causality.

### Tâche D — De la prédiction à l'apprentissage / From prediction to learning

**Consigne :** « Reliez probabilité attribuée au token observé, vraisemblance, NLL/cross-entropy, gradient et mise à jour des paramètres. Vous pouvez expliquer sans refaire toutes les dérivations. »

**Transfert :** « Pourquoi une perplexité n'est-elle pas une mesure directe de la vérité ou de la qualité générale d'une réponse ? Quelles conditions rendent deux valeurs comparables ? »

**À observer :** chaîne conceptuelle correcte ; somme vs moyenne et positions évaluées ; gradient comme sensibilité locale ; distinction rétropropagation/optimiseur ; dépendance de la perplexité au tokenizer et au protocole d'évaluation.

**Prompt:** “Connect the probability assigned to the observed token, likelihood, NLL/cross-entropy, gradient, and parameter update. You may explain without reproducing every derivation.”

**Transfer:** “Why is perplexity not a direct measure of truth or overall answer quality? What conditions make two values comparable?”

**Observe:** correct conceptual chain; sum vs mean and evaluated positions; gradient as local sensitivity; backpropagation distinguished from optimizer; perplexity depends on tokenizer and evaluation protocol.

## 6. Rubrique de notation / Scoring rubric

Noter chaque dimension de 0 à 2, avec une preuve verbatim ou une observation concrète. **Ne pas noter l'aisance orale, l'accent ou la vitesse comme compréhension.**

Score each dimension from 0 to 2, with verbatim evidence or a concrete observation. **Do not score speaking fluency, accent, or speed as comprehension.**

| Score | Définition |
|---:|---|
| 0 | Absent, incorrect ou contredit par la réponse. |
| 1 | Partiellement correct, mais incomplet, fragile ou obtenu après une relance neutre. |
| 2 | Correct, autonome et transféré au cas nouveau. |

| Score | Definition |
|---:|---|
| 0 | Missing, incorrect, or contradicted by the response. |
| 1 | Partly correct, but incomplete, fragile, or achieved after a neutral prompt. |
| 2 | Correct, independent, and transferred to the new case. |

Pour chaque tâche, noter séparément : **exactitude conceptuelle**, **explication du mécanisme**, **transfert**, **confiance calibrée** et **navigation**. La confiance est bien calibrée lorsque le participant sait signaler ce qu'il ignore ; une confiance élevée avec une réponse erronée est un signal de risque pédagogique.

For each task, score separately: **conceptual accuracy**, **mechanism explanation**, **transfer**, **calibrated confidence**, and **navigation**. Confidence is calibrated when the participant can identify what they do not know; high confidence with an incorrect answer is a pedagogical risk signal.

Pour la cohorte expérimentée, ajouter une note qualitative distincte : **valeur nouvelle** (aucune / faible / nette), avec citation ou description précise de l'idée nouvellement apprise. Ne pas la déduire de la seule appréciation « j'ai aimé ».

For the experienced cohort, add a separate qualitative note: **new value** (none / slight / clear), with a quote or precise description of the newly learned idea. Do not infer it from a general “I liked it”.

## 7. Journal d'observation / Observation log

Pour chaque tâche, consigner :

- page(s) consultée(s) et ordre de navigation ;
- temps approximatif, retours en arrière et abandons ;
- réponse initiale, relances neutres et réponse finale ;
- concept exact mal compris ou confondu ;
- prérequis manquant, s'il est démontré ;
- niveau de confiance avant/après ;
- citation courte anonymisée ;
- gravité : **bloquant**, **important**, **mineur**, **préférence**.

For each task, record:

- page(s) visited and navigation order;
- approximate time, backtracking, and abandonment;
- initial answer, neutral prompts, and final answer;
- exact misunderstood or conflated concept;
- missing prerequisite, if evidenced;
- confidence before/after;
- short anonymized quote;
- severity: **blocking**, **major**, **minor**, **preference**.

## 8. Règles de décision / Decision rules

- **Bloquant :** au moins deux participants d'une même cohorte échouent sur le même concept central, ou une seule erreur révèle un défaut scientifique sérieux. Corriger avant d'ajouter du contenu.
- **Important :** difficulté répétée, transfert impossible, prérequis non annoncé ou confiance erronée ; retravailler explication, exemple, transition ou exercice.
- **Mineur :** hésitation isolée ou formulation ambiguë sans conséquence durable ; corriger si le coût est faible.
- **Préférence :** préférence stylistique isolée sans effet observable sur compréhension ou navigation ; ne pas déclencher automatiquement une réécriture.

- **Blocking:** at least two participants in one cohort fail on the same central concept, or one error reveals a serious scientific flaw. Fix before adding content.
- **Major:** repeated difficulty, failed transfer, unstated prerequisite, or miscalibrated confidence; revise explanation, example, transition, or exercise.
- **Minor:** isolated hesitation or ambiguous wording without lasting consequence; fix when low-cost.
- **Preference:** isolated stylistic preference with no observable effect on comprehension or navigation; do not automatically trigger a rewrite.

Une correction doit être suivie d'un nouveau test ciblé avec une personne qui n'a pas vu la version précédente. Les résultats doivent distinguer les deux cohortes et les langues ; ne pas fusionner des difficultés qui ont des causes différentes.

After a change, run a targeted retest with someone who has not seen the previous version. Report results separately by cohort and language; do not merge difficulties with different causes.

## 9. Synthèse et restitution / Synthesis and reporting

Après le pilote :

1. regrouper les observations par concept et par page, non par préférence générale ;
2. distinguer problème de contenu, de prérequis, de navigation, de rendu et de facilitation ;
3. chercher les contre-exemples et les participants qui réussissent, pas seulement les échecs ;
4. décider pour chaque constat : corriger, tester davantage, documenter comme compromis ou ne rien changer ;
5. publier un compte rendu anonymisé avec méthode, effectifs réels, limites et changements décidés.

After the pilot:

1. group observations by concept and page, not general preference;
2. distinguish content, prerequisite, navigation, rendering, and facilitation problems;
3. look for counterexamples and successful participants, not only failures;
4. decide for each finding: fix, test further, document as a trade-off, or make no change;
5. publish an anonymized report with method, actual sample sizes, limitations, and decisions.

## 10. Limites / Limitations

- Quatre tâches ne couvrent pas les 18 leçons ; elles échantillonnent les principaux enchaînements conceptuels.
- Une session immédiate mesure surtout la compréhension à court terme ; le rappel différé demande une seconde mesure.
- Les participants volontaires peuvent être plus motivés que le lectorat réel.
- Les résultats qualitatifs guident des améliorations ; ils ne démontrent pas à eux seuls un gain causal d'apprentissage.
- Les parcours Practice et Build nécessitent ensuite des tâches dédiées : manipulation d'exercices, lecture/écriture de code, tests et débogage.

- Four tasks do not cover all 18 lessons; they sample the main conceptual chains.
- An immediate session mainly measures short-term understanding; delayed retention requires a second measurement.
- Volunteers may be more motivated than the actual readership.
- Qualitative findings guide improvements; they do not by themselves demonstrate a causal learning gain.
- Practice and Build need dedicated tasks later: exercise manipulation, code reading/writing, testing, and debugging.

---

## Annexe — fiche rapide de session / Appendix — session sheet

- Identifiant pseudonyme / Pseudonymous ID:
- Cohorte / Cohort: débutante / beginner · expérimentée / experienced
- Langue / Language:
- Date et version du site / Date and site version:
- Appareil / Device:
- Prérequis déclarés / Self-reported prerequisites:
- Tâches réalisées / Tasks completed: A · B · C · D
- Difficultés bloquantes / Blocking issues:
- Citations anonymisées / Anonymized quotes:
- Valeur nouvelle pour lecteur expérimenté / New value for experienced reader:
- Changements suggérés / Suggested changes:
- Limites et biais / Limitations and bias:

<a id="prediction-use-pilot"></a>

## Annexe — Pilote des usages de la prédiction / Prediction-use pilot

Complément court à la tâche D. Les deux formes évaluent le choix du préfixe et l’usage de la prédiction. Le cas inédit vérifie ensuite la lecture d’une loss de validation. Les données ci-dessous sont fictives. Le protocole attend une première session indépendante.

Short extension to Task D. The two forms probe which prefix is used and what happens to the prediction. A separate, unseen case then checks interpretation of validation loss. All data below are synthetic. The protocol is ready for a first independent session.

### Déroulé / Session sequence

1. Poser les quatre questions avec une forme avant lecture. Relever les préfixes écrits, les résultats, le raisonnement et la confiance (1–5). Garder le corrigé pour la fin.
2. Demander de retrouver dans le [plan FR](../../site/fr/review-path.qmd#compare-prediction-uses) ou [EN](../../site/en/review-path.qmd#compare-prediction-uses) les passages qui expliquent la génération, le contexte, le scoring et l’entraînement. Noter les pages réellement consultées et les hésitations.
3. Reposer les mêmes questions avec l’autre forme, plan fermé. Alterner l’ordre A→B et B→A entre sessions lorsque c’est possible. La symétrie des consignes rend la comparaison lisible. La difficulté relative des formes reste à observer.
4. Proposer le cas inédit, puis revenir sur les explications et les obstacles de navigation. Compter environ 20 à 25 minutes pour les quatre temps, à ajuster après la première session.

1. Ask the four questions using one form before reading. Record the written prefixes, results, reasoning, and confidence (1–5). Keep the answer key until the end.
2. Ask the participant to find the parts that explain generation, context, scoring, and training in the [FR](../../site/fr/review-path.qmd#compare-prediction-uses) or [EN](../../site/en/review-path.qmd#compare-prediction-uses) plan. Record which pages they actually use and where they hesitate.
3. Ask the same questions with the other form, with the plan closed. Alternate A→B and B→A across sessions where possible. The symmetric prompts make comparison straightforward. Relative form difficulty still needs to be observed.
4. Offer the unseen case, then discuss the explanations and navigation obstacles. Allow about 20–25 minutes for the four parts and revise the estimate after the first session.

### Support commun A/B / Common A/B handout

Un scribe doit produire deux tokens. Le vocabulaire jouet contient deux tokens, `X` et `Y`. Le contexte initial est `c`. Pour un nouvel appel, l’application peut ajouter un exemple à `c`, donnant `c'`. Le tableau donne les probabilités de sortie du même checkpoint pour ces préfixes. La continuation de référence est donnée avec chaque forme.

A scribe must produce two tokens. The toy vocabulary contains two tokens, `X` and `Y`. The initial context is `c`. For another call, the application can add a demonstration to `c`, yielding `c'`. The table gives the same checkpoint’s output probabilities for these prefixes. Each form supplies its own reference continuation.

| Préfixe / Prefix | Forme A / Form A (`p_X,p_Y`) | Forme B / Form B (`p_X,p_Y`) |
|---|---:|---:|
| `c` | (0.70, 0.30) | (0.40, 0.60) |
| `c+[X]` | (0.80, 0.20) | (0.35, 0.65) |
| `c+[Y]` | (0.60, 0.40) | (0.25, 0.75) |
| `c'` | (0.20, 0.80) | (0.65, 0.35) |

Continuation de référence / Reference continuation

- A · `[Y, X]`
- B · `[X, Y]`

Paramètre scalaire pour la question 4 / Scalar parameter for question 4

| Forme / Form | Valeur courante / Current value θ | Gradient `g` | Taux / Rate η |
|---|---:|---:|---:|
| A | 1 | −2 | 0.1 |
| B | 2 | 2 | 0.1 |

| Question | Français | English |
|---|---|---|
| 1 · Générer / Generate | On retient le token le plus probable à chaque tour. Quels deux tokens sortent et quel préfixe est utilisé au deuxième tour ? | Select the most probable token each round. Which two tokens are emitted, and which prefix is used in round two? |
| 2 · Scorer / Score | Quelle probabilité le checkpoint attribue-t-il à la continuation de référence sous `c` ? Donnez les deux lignes et le calcul. | What probability does the checkpoint assign to the reference continuation given `c`? Give the two rows and the calculation. |
| 3 · Préparer l’entrée / Prepare the input | Comparez le premier token glouton avec `c` et `c'`. Quel résultat attendre si l’exemple est stocké mais que le modèle reçoit exactement `c`, dans les mêmes conditions ? | Compare the first greedy token under `c` and `c'`. What should happen if the demonstration is stored but the model receives exactly `c` under the same conditions? |
| 4 · Entraîner / Train | Le gradient du tableau a été calculé sur un lot d’entraînement. Donnez θ après le calcul du gradient, après un pas θ ← θ − ηg, puis après une passe de validation. | The table’s gradient was computed on a training batch. Give θ after computing the gradient, after a θ ← θ − ηg step, and after a validation pass. |

### Cas inédit après la lecture / Unseen post-reading case

Deux checkpoints `P` et `Q` sont évalués sur les mêmes cibles de validation. Tokenizer et positions valides sont identiques. Le tableau donne les sommes de NLL en nats. Quel checkpoint obtient la plus faible NLL **par cible valide** ? Un collègue moyenne les deux moyennes de lot à poids égal. Expliquez la divergence éventuelle et dites ce que changerait un autre regroupement des mêmes cibles et des mêmes prédictions.

Two checkpoints `P` and `Q` are evaluated on the same validation targets. The tokenizer and valid positions are identical. The table gives NLL sums in nats. Which checkpoint gets the lowest NLL **per valid target**? A colleague gives the two batch means equal weight. Explain any disagreement and say what would happen if the same targets and predictions were grouped differently.

| Lot / Batch | Cibles valides / Valid targets | NLL `P` | NLL `Q` |
|---|---:|---:|---:|
| 1 | 3 | 9 | 3 |
| 2 | 9 | 6 | 15 |

### Corrigé facilitateur / Facilitator key

| Dimension | Réponse attendue / Expected answer |
|---|---|
| 1 · Préfixe généré / Generated prefix | A produit `[X, X]` en prolongeant `c` par `X`. B produit `[Y, Y]` en le prolongeant par `Y`. / A produces `[X, X]` by extending `c` with `X`. B produces `[Y, Y]` by extending it with `Y`. |
| 2 · Préfixe observé / Observed prefix | A lit `Y` sous `c`, puis `X` sous `c+[Y]`. La probabilité vaut 0.30 × 0.60 = 0.18. B lit `X` sous `c`, puis `Y` sous `c+[X]`, soit 0.40 × 0.65 = 0.26. / A reads `Y` under `c`, then `X` under `c+[Y]` for 0.18. B reads `X` under `c`, then `Y` under `c+[X]` for 0.26. |
| 3 · Entrée effective / Effective input | Transmettre `c'` fait passer le choix de `X` à `Y` en A et de `Y` à `X` en B. Un exemple seulement stocké laisse le choix initial si l’entrée effective et les conditions sont les mêmes. Le checkpoint est fixe. / Sending `c'` changes the choice from `X` to `Y` in A and from `Y` to `X` in B. A stored-only demonstration leaves the original choice in place when the effective input and conditions match. The checkpoint stays fixed. |
| 4 · Mesure et pas / Measurement and step | A donne 1 → 1.2 → 1.2, B donne 2 → 1.8 → 1.8. Le calcul du gradient laisse la valeur initiale. Seul le pas d’optimisation la modifie. / A gives 1 → 1.2 → 1.2, B gives 2 → 1.8 → 1.8. Computing the gradient leaves the initial value in place. The optimizer step changes it. |
| Transfert · Dénominateur / Transfer · Denominator | Par cible, `P=15/12=1.25` et `Q=18/12=1.5`. À poids égal par lot, `P=11/6` et `Q=4/3`, donc le classement s’inverse. Regrouper les mêmes couples prédiction–cible laisse la moyenne par cible inchangée. / Per target, `P=1.25` and `Q=1.5`. With equal batch weights, `P=11/6` and `Q=4/3`, reversing the ranking. Regrouping the same prediction–target pairs preserves the per-target mean. |

Relever pour chaque réponse le mécanisme invoqué et le résultat. Appliquer 0 si le mécanisme manque ou contredit la réponse, 1 si une partie seulement est correcte, 2 si le calcul et le mécanisme sont corrects. Consigner à part une erreur arithmétique lorsque le préfixe et l’opération sont corrects. Comparer chaque dimension A/B avec le même barème. Consigner le transfert à part et distinguer un mauvais calcul, une confusion de vocabulaire et l’impossibilité de trouver la leçon. Les premiers écarts servent à améliorer les consignes et les pages.

Record the reasoning and result for each response. Use 0 when the reasoning is absent or contradicts the answer, 1 when only part is correct, and 2 when both the calculation and the mechanism are correct. Record an arithmetic slip separately when the prefix and operation are right. Use the same rubric in each form and compare per dimension. Record the novel transfer case separately and distinguish calculation errors, terminology confusion, and difficulty finding the lesson. Use the first observations to improve the prompts and pages.
