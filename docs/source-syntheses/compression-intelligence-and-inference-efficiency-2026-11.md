# Compression, information and inference efficiency — synthesis of three complementary articles

**Périmètre :** synthèse critique et différentielle de trois billets de vulgarisation, pas une revue systématique :
- Karthik Shashidhar, [LLMs and compression algorithms](https://artofdatascience.substack.com/p/llms-and-compression-algorithms), 27 août 2024.
- Wayland Zhang, [Information Theory Is All You Need (to Understand LLMs)](https://waylandz.com/blog/information-theory-and-llm/), rewrite dated 17 février 2026.
- Sourav Mukherjee, [Compression Is Intelligence: The Information Theory Behind LLMs](https://medium.com/bongquisitive-tech/compression-is-intelligence-the-information-theory-behind-llms-70022356dad8), 20 juillet 2026.

## 1. Conclusion exécutive

Les trois articles racontent une histoire voisine : apprendre des régularités améliore la prédiction ; de bonnes probabilités peuvent réduire le coût idéal d'encodage ; et les mêmes idées d'information peuvent éclairer les compromis d'efficacité.

Le nouvel article de Mukherjee n'apporte pas une nouvelle théorie de l'entropie ni une nouvelle définition de la compression prédictive. Son apport distinct est de mettre en avant l'usage de signaux dérivés de l'entropie dans l'optimisation de l'inférence, notamment l'allocation du cache KV et la sélection de calculs à conserver ou à recalculer. Cette contribution doit être présentée avec des distinctions précises entre les méthodes.

## 2. Carte des recouvrements et nouveautés

| Sujet | Déjà acquis dans LLM Lab | Apport différentiel du nouvel article | Décision |
|---|---|---|---|
| Prédiction → surprisal → longueur de code | Dérivation et codage arithmétique exact | Métaphore plus accessible et prix Hutter | Réutiliser ; nuancer le slogan |
| Entropie / cross-entropy | Leçons canoniques et expérience jouet | Rappel du lien avec le coût moyen | Ne pas dupliquer ; clarifier bits/nats |
| Compression du modèle | Quantification, pruning, distillation | Aucun nouveau mécanisme central | Conserver la séparation |
| Mémoire d'exécution | Cache KV et budgets mémoire | Signaux d'entropie pour allouer/évincer/recalculer | Nouvel approfondissement avancé |
| Chaînes de raisonnement | Pas de résultat projet établissant une suppression sûre par entropie | Hypothèse de redondance des tokens intermédiaires | Expérience réelle à concevoir, aucun résultat à revendiquer |
| Hallucinations | Limites, calibration et ancrage externe | Analogie avec compression avec perte | Ajouter comme intuition limitée, pas comme explication complète |

## 3. Quatre quantités à ne pas confondre

Pour un contexte (c) et une distribution prédictive (q(\cdot\mid c)) :

1. **Entropie prédictive du modèle** : (H(q)=-\sum_x q(x\mid c)\log q(x\mid c)). Elle décrit l'incertitude du modèle sur son prochain symbole.
2. **Surprisal réalisé** : (-\log q(x_t\mid c)). Il mesure le coût attribué au symbole effectivement observé.
3. **Entropie des poids d'attention** : entropie de la distribution d'attention sur des positions. Elle décrit la dispersion de ces poids, pas l'incertitude du prochain token ni une information mutuelle entre tokens.
4. **Dérive du cache KV** : différence entre états mis en cache et états qui seraient recalculés. C'est une quantité d'erreur/instabilité propre à un protocole de cache.

Aucune de ces quantités n'est à elle seule une mesure de l'utilité sémantique d'un token. Faible entropie ou faible surprisal ne signifie pas « supprimable sans risque ».

La cross-entropy moyenne est encore une autre quantité : elle moyenne le négatif du logarithme de la probabilité attribuée aux cibles observées sous une distribution d'évaluation. Les unités dépendent de la base du logarithme : nats avec le logarithme naturel, bits avec log₂.

## 4. Ce que la recherche sur le cache ajoute réellement

Deux exemples consultés illustrent des signaux différents :

- Kim & Jung (2025), [Entropy-Guided KV Caching for Efficient LLM Inference](https://www.mdpi.com/2227-7390/13/15/2366), utilisent l'entropie des poids d'attention par tête, agrégée par couche, pour répartir un budget de cache et sélectionner des tokens.
- Cheong et al. (2026), [EntropyCache](https://arxiv.org/abs/2603.18489), utilisent l'entropie des distributions de tokens nouvellement décodés comme indicateur de dérive du cache KV dans des modèles de langage par diffusion. Il s'agit d'une décision de saut/recalcul, pas d'une règle générale de suppression des tokens de raisonnement dans les modèles autorégressifs.

Ces travaux montrent que l'entropie peut être un signal utile dans un système d'inférence défini. Ils ne valident pas une règle universelle « faible entropie = token inutile ». Les résultats doivent rester attachés au modèle, à la distribution mesurée, au budget, au workload et aux métriques de qualité de chaque étude.

## 5. Compression et hallucinations : formulation prudente

La compression prédictive peut favoriser les régularités fréquentes et réutilisables. Une analogie avec la compression avec perte aide à comprendre pourquoi un système peut reproduire une structure plausible tout en échouant sur un détail exact.

Mais il ne faut pas conclure que les faits rares sont toujours perdus, que la haute entropie signifie faible fiabilité, ni que toutes les hallucinations sont des artefacts de compression. La génération optimise une distribution apprise, pas une vérification factuelle. Les données contradictoires, le décalage de distribution, la calibration, l'ambiguïté, le décodage et l'absence de sources externes interviennent aussi.

La réponse opérationnelle consiste à externaliser les opérations qui exigent exactitude et vérifiabilité (calcul, base de données, recherche documentaire), avec contrôle de provenance, de date et de cohérence.

## 6. Programme expérimental

### Expérience A — Entropie contre surprisal (jouet, reproductible)

Construire une distribution binaire très déséquilibrée, par exemple (P(A)=0.99), (P(B)=0.01). L'entropie est faible (environ 0,081 bit par tirage), mais l'événement rare (B) porte environ 6,644 bits de surprisal lorsqu'il survient. Cela suffit à réfuter l'identification entre entropie moyenne et surprise d'un événement.

Cette expérience est mathématique et ne démontre rien sur l'utilité des tokens d'un LLM.

### Expérience B — Utilité réelle des tokens (à réaliser sur modèle)

Comparer, à budget de suppression identique :
- aucun pruning ;
- pruning par entropie prédictive ;
- pruning par surprisal réalisé ;
- pruning aléatoire ;
- baseline de récence ou d'attention.

Mesurer exactitude, exact match, robustesse des étapes intermédiaires, longueur, latence, débit, pic mémoire et coût de sélection. Utiliser des tâches faciles et difficiles, plusieurs prompts et plusieurs seeds. Publier les erreurs et les intervalles d'incertitude. Un résultat ne peut être annoncé qu'après exécution et vérification.

### Expérience C — Cache KV (étude distincte)

Comparer cache complet, fenêtre récente, méthode attention-entropy et méthode de recomputation entropy-guided sous le même modèle, contexte, budget mémoire et backend. Rapporter la qualité, le coût de sélection, le temps de préremplissage, le temps de décodage et le pic mémoire. Ne pas fusionner les méthodes autoregressives et diffusion sans expliciter leurs architectures.

## 7. Décisions pédagogiques

- Garder les leçons canoniques d'entropie et cross-entropy comme seules définitions de référence.
- Garder la fiche de révision « Compression et LLM » comme synthèse des budgets : données, checkpoint, mémoire d'exécution.
- Ajouter un encadré sur les quatre signaux (entropie prédictive, surprisal, entropie d'attention, dérive KV).
- Lier les méthodes de cache comme approfondissement avancé, sans créer une nouvelle étape obligatoire du parcours.
- Traiter l'élagage de chaîne de raisonnement comme une question de recherche et non comme une optimisation déjà démontrée.
- Conserver l'analogie JPEG uniquement avec ses limites et les autres causes possibles d'hallucination.

## 8. Synthèse à mémoriser

**La prédiction explique le coût idéal du codage ; l'entropie peut aussi guider certaines décisions d'inférence, mais uniquement si le signal, la cible et le protocole sont spécifiés.**

L'entropie mesure une incertitude de distribution, le surprisal une observation, l'entropie d'attention la dispersion des poids d'attention, et la dérive KV une erreur de cache. Aucun de ces nombres ne remplace une mesure directe de l'utilité, de la qualité ou de la véracité.

## Références complémentaires

- [Hutter Prize — official rules](https://prize.hutter1.net/).
- Kim & Jung (2025), [Entropy-Guided KV Caching for Efficient LLM Inference](https://www.mdpi.com/2227-7390/13/15/2366).
- Cheong et al. (2026), [EntropyCache](https://arxiv.org/abs/2603.18489).
- Wang et al. (2025), [SAGE-KV: LLMs Know What to Drop](https://arxiv.org/abs/2503.08879).


## 9. Lewis — model cost, causal order and agent-level theories (2025)

[“Intelligence and compression”](https://lewish.io/posts/intelligence-and-compression) adds a distinct perspective to the collection. It should not be conflated with the similarly titled articles by Sourav Mukherjee, David Chen or Mingdi Fan.

### 9.1 What this source adds

- **Two-part description length:** the data cost conditional on a model and the description cost of the model itself, a direct bridge to MDL. This is a more complete framing than treating a predictor's parameters as free.
- **Expertise as chunking:** the musician analogy illustrates how prior knowledge changes the units and patterns an observer can recognize. Keep it as an analogy about domain-specific schemas, not a quantitative account of human memory.
- **Causal/temporal order:** the article distinguishes sequential prediction from order-free batch compression and reports a forward/reverse enwik8 comparison. This is a useful experimental prompt, not a verified general law: compressor versions, options and preprocessing are not fully specified.
- **Adaptation cost:** the Chollet connection broadens the discussion from static model fit to the efficiency of acquiring skills and updating a model.
- **Agent frameworks:** AIXI places reward maximization on top of universal prediction; active inference offers a different perception/action perspective. These are advanced theoretical connections, not evidence that compression alone defines intelligence.

### 9.2 Qualifications to preserve

The total MDL objective is commonly represented as \\(L(M)+L(D\\mid M)\\), relative to a chosen model class and coding scheme. It is not simply “choose the smallest model”; nor does it guarantee truth or generalization. Practical MDL, Kolmogorov complexity and Solomonoff induction must remain distinct.

Predictive probabilities can be converted into code lengths, but a practical compressor must account for the coding protocol, shared model/side information and decoder. The article's short variable-length example is illustrative, not an optimal coding construction. The logarithm base determines bits versus nats.

The reported forward/reverse differences are small and source-reported. They do not by themselves establish causality or a universal forward-order advantage. A controlled experiment should compare known causal and non-causal synthetic generators, with fixed compressor versions/options and reproducible preprocessing.

Finally, the article's FEP section is explicitly a lay interpretation. Surprisal, variational free energy, prediction error, reward and preferred outcomes are not synonyms. The proposed compression-based unification of intelligence remains a hypothesis/perspective.

### 9.3 Collection-level decision

Integrate the two-part MDL framing and the model-update/agent comparison into this dossier. Keep the musician analogy as optional complementary pedagogy. Defer any canonical page or graph changes until primary references and learner benefit are verified. Do not create a duplicate entropy, compression or intelligence concept solely to mirror this source's vocabulary.

Source review: [Lewis, “Intelligence and compression”](../source-reviews/lewish-intelligence-and-compression-2025.md). Structured provenance and atomic dispositions: [source extraction](../../data/extractions/lewish-intelligence-and-compression-2025.yml).


## 10. Précision complémentaire — AIXI et dépendance au langage de référence

La formulation d'AIXI comme agent universellement optimal doit toujours être rapportée à son cadre formel. La distribution universelle dépend du choix de la machine de Turing universelle (UTM) qui définit les descriptions des environnements. Le travail ultérieur de Leike et Hutter, [“On the Computability of AIXI” / analyse des universal priors](https://www.hutter1.net/publ/saixicplex.pdf), documente des cas où un choix malheureux ou adversarial de l'UTM peut modifier fortement le comportement ; il invite donc à ne pas lire les garanties comme une mesure absolue et indépendante de toute représentation. AIXI reste en outre incomputable dans sa forme idéale. Cette dépendance ne réfute pas le cadre, mais précise la portée de ses garanties : elles sont relatives à la classe d'environnements, à la distribution universelle et à la machine de référence choisies.
