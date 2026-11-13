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
