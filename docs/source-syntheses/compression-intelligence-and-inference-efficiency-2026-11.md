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
