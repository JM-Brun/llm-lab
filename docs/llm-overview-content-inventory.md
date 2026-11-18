# Inventaire de conservation — refonte du panorama LLM

> État : inventaire éditorial avant déplacement de contenu. Sources FR/EN consultées sur `main` le 18 novembre 2026. Les lignes sont des repères de lecture, non des ancres stables. Les versions anglaises ont été contrôlées : elles suivent la même architecture, sans imposer un fil narratif identique au français.
>
> Règle : aucun bloc n'est supprimé tant que son contenu distinctif, ses figures, références, exercices, liens et réserves n'ont pas un propriétaire vérifié dans les deux langues.

## 1. Gouvernance du parcours

- `data/guided-route.yml` conserve neuf étapes. `context-use` garde ICL et Context engineering comme pages principales et `rag-memory-boundaries` comme approfondissement facultatif.
- Aucun nouveau stage, prérequis, ordre entre pages Deepen ou parcours parallèle n'est introduit.
- La topologie et la propriété des concepts restent définies par `docs/learning-path.md` et `docs/content-section-mapping.md`.
- Les fils narratifs FR (Otis) et EN (Monty Python) restent propres à chaque langue.

## 2. Matrice de conservation — RAG et récupération documentaire

| Source FR (EN : section miroir) | Contenu distinctif | Destination | Action / garde-fou |
|---|---|---|---|
| `rag-memory-boundaries.qmd` §1, l. 28–37 | Six états : disponible, stocké/préparé, indexé, récupéré, transmis, exploité ; aucun ne garantit le suivant | Page RAG conservée | Garder comme modèle d'ensemble, éventuellement resserré. Ne pas dupliquer intégralement dans la nouvelle page. |
| §2, l. 43–55 | Définition de retrieval et frontière retrouver/transmettre | Nouvelle page Deepen sœur `document-retrieval.qmd` | Déplacer l'explication détaillée ; garder dans RAG une transition et un lien. |
| §2.1, l. 57–74 | Tableau BM25, bi-encoder dense, SPLADE, ColBERT, cross-encoder ; usages et compromis | `document-retrieval.qmd` | Conserver le tableau et l'idée centrale : familles alternatives/composables, pas une échelle de maturité. |
| §2.2, l. 76–108 | ColPali, pipeline OCR vs page visuelle, diagramme Mermaid, résultats ViDoRe, coûts, limites, références ICLR 2025 et Daily Dose | `document-retrieval.qmd` | Déplacer en bloc avec diagramme, chiffres contextualisés, liens et réserves. Ne pas transformer le résultat benchmark en classement universel. |
| §3, l. 110–133 | Définition RAG, diagramme, préparation amont vs exécution à la question, distinction avec adaptation des poids | Page RAG conservée | Garder. Réduire les détails des retrievers et renvoyer vers `document-retrieval`. Préserver le lien Post-training. |
| §3.1, l. 134–145 | Causes d'échec du RAG ; évaluer séparément récupération et réponse conditionnée | Page RAG + exercices | Garder la taxonomie ; les protocoles détaillés de métriques restent dans la page d'évaluation canonique. |
| §§4–5, l. 147–180 | Types fonctionnels de mémoire, cycle écrire/entretenir/lire, provenance, temporalité, comparaison des finalités RAG/mémoire | Page RAG conservée | Garder. Dans Context engineering, remplacer la reprise détaillée par une synthèse et un lien. Ne pas présenter les types comme universels. |
| §6, l. 182–194 | ICL : faits, exemples, mémoire et instructions ; aucune mise à jour persistante des paramètres | `in-context-learning.qmd` | Le propriétaire ICL couvre déjà zero/one/few-shot, adaptation et limites. Garder dans RAG un rappel d'une phrase et un lien. |
| §7, l. 195–215 | Expérience Orion/Delta, conditions A–G, stockage/indexation/récupération/transmission/ICL, facteurs et mesures | Page RAG conservée + exercices | Garder comme expérience intégratrice de bout en bout ; ne pas la réduire à retrieval seul. |
| §8, l. 217–221 | Injection indirecte, séparation instructions/données, permissions, provenance, fraîcheur, effacement multi-couches | Page RAG conservée | Garder. Context engineering peut rappeler les contrôles sans recopier le développement. |
| §9, l. 223–232 | Quatre questions diagnostiques : où l'information existe, comment elle est retrouvée, transmise, exploitée | Page RAG conservée | Garder comme synthèse et grille de diagnostic. |
| Exemple FAISS, l. 234–240 | Tutoriel Hugging Face, embeddings, index de voisins ; limites de la recherche vectorielle seule | `document-retrieval.qmd` | Déplacer avec la référence et la précision : ce n'est pas un RAG complet. |
| Ressources reranking, l. 241–247 | Bi-encoder/cross-encoder, trois références, compromis et accès partiellement payant | `document-retrieval.qmd` | Déplacer ; vérifier les liens et ne pas présenter le cross-encoder comme obligatoire. |
| Limites, pratique, inclusion, l. 249–262 | Limites de portée, exercices RAG, include généré, sélecteur de langue | Page RAG conservée | Garder les exercices intégrateurs. Ne jamais éditer manuellement l'include généré. Un exercice retrieval séparé exige un objectif non couvert démontré. |

### Frontière des deux pages Deepen

**Document retrieval** possède la recherche/indexation documentaire : représentations, familles de retrievers, recherche visuelle, classement/reranking, qualité de récupération, exemple FAISS et références associées.

**RAG, mémoire et transmission au contexte** possède le cycle de vie de l'information externe : RAG, mémoire applicative, différence entre stockage/récupération/transmission/exploitation, sécurité/provenance, diagnostic et expérience intégratrice.

Les deux pages seraient des ressources sœurs facultatives de `context-use`, sans `suggested_route.previous/next` entre elles. La page RAG actuelle garde son identifiant et son rôle, pour ne pas casser les relations existantes.

## 3. Déduplication — Context engineering

La page `context-engineering.qmd` (FR l. 31–163 ; EN structure miroir) doit conserver :
- la définition du contexte système et les opérations de sélection, structuration, actualisation et sécurisation ;
- les trois niveaux : contexte système, séquence/fenêtre de contexte, contexte accessible à une position ;
- la distinction capacité maximale / longueur active / visibilité selon le masque causal ;
- les frontières entre prompt engineering, ICL, context engineering, RAG, mémoire, tool use, ingénierie agentique et fine-tuning ;
- l'exemple de conception, les limites et l'évaluation du contexte.

Les sections « De la conception du contexte aux architectures de récupération et de mémoire », « De la récupération documentaire à une information exploitable » et « Mémoire persistante : stocker n'est pas transmettre » (FR l. 92–128 ; EN sections miroirs) reprennent une grande partie du pipeline RAG et de la frontière retrouvé/transmis. Elles doivent être remplacées par une explication courte de la responsabilité propre du context engineering : choisir, ordonner, compresser, actualiser et contrôler les éléments effectivement transmis. Les explications de pipeline, de retrieval et de mémoire restent dans la page RAG. Toute information unique de ces sections doit être absorbée dans cette synthèse avant retrait.

## 4. Autres pages propriétaires — décisions préalables

| Pages / blocs | Constat | Décision de conservation |
|---|---|---|
| `generation.qmd` §§ boucle, notation, prefill/decode, sélection, limites (FR l. 74–230 ; EN miroir) | Noyau conceptuel nécessaire à Understand | Garder boucle, sélection et explication minimale prefill/decode dans Generation. |
| Callout Generation latence/serving (FR l. 145–181 ; EN l. 140–177) | Mélange latence, ordonnancement multi-requêtes et cache | Déplacer les explications coût/mémoire/KV-cache vers `llm-computational-complexity.qmd`. Vérifier un propriétaire existant pour scheduling/serving avant de déplacer ce sous-bloc ; ne pas charger la page de complexité de tout le sujet. Garder un repère et un lien dans Generation. |
| `llm-computational-complexity.qmd` §4 et §9 (FR l. 91–116, 159–169 ; EN miroir) | Compare entraînement, prefill, decode, travail, dépendances et mémoire | Étendre si nécessaire avec le mécanisme du cache KV et ses coûts, sans refaire le tutoriel de génération. Distinguer coûts théoriques et politiques de serving. |
| `training-loop.qmd` (FR l. 61–170 ; EN miroir) | Le pas d'entraînement, l'exemple jouet, la validation et le pré-entraînement forment une progression intégrée | Garder la boucle, l'exemple, la validation, le code et le lien Build. Raccourcir les rappels mathématiques avec liens vers Loss et Gradients. |
| `loss.qmd` (FR l. 59–115 ; EN miroir) | Propriétaire de l'agrégation de loss, des cibles décalées, du masquage et du teacher forcing | Ne pas recopier les dérivations dans Training loop ; garder une synthèse et un lien. |
| `gradients.qmd` (gradient des logits, règle de chaîne, exemple de projection ; EN miroir) | Propriétaire du gradient et de la rétropropagation | Training loop ne garde que le rôle du gradient dans la boucle et renvoie vers la dérivation. |
| `llm-evolution.qmd`, `transformer-history.qmd`, `llm-limits.qmd` | Synthèse multi-axes, histoire et limites sont des questions autonomes | Pas de micro-découpage. Réduire les redites avec le panorama sans supprimer les analyses spécifiques. |

## 5. Exercices, médias et dépendances

- Les exercices `exercises/rag-memory-boundaries.qmd` (FR/EN, 126 lignes chacun) couvrent sept objectifs : frontière de transmission, diagnostic RAG, distinction RAG/mémoire/ICL, expérience contrôlée, qualité retrieval vs exploitation, gouvernance mémoire, connaissances paramétriques vs informations fournies. Ils restent intégrateurs tant qu'une analyse question par question ne justifie pas un exercice retrieval autonome.
- Le bloc ColPali contient un diagramme Mermaid, des références primaires et secondaires, des chiffres de benchmark et des réserves : déplacer les quatre ensemble dans les deux langues.
- Generation et Overview ont des figures bilingues et des variantes mobile/desktop. Aucun déplacement n'est proposé ici ; leurs IDs, alt text, légendes, variantes et références devront figurer dans l'inventaire détaillé du lot Overview.
- Les includes `generated-guided-context-*`, page maps et fragments générés ne sont pas des sources éditables manuellement. Les métadonnées et projections doivent être régénérées par leur pipeline.
- Vérifier les liens internes, ancres, références et exercices dans les deux langues au même lot logique.

## 6. Séquence d'exécution sûre

1. Auditer les exercices RAG question par question, les références externes et les propriétaires existants de serving/scheduling.
2. Créer la page retrieval FR/EN avec le contenu copié à l'identique au premier passage, ses métadonnées Deepen et ses liens ; vérifier l'index Deepen généré.
3. Réduire ensuite les blocs correspondants de la page RAG en les remplaçant par transitions/liens ; préserver RAG, mémoire, expérience, sécurité et exercices intégrateurs.
4. Réduire les sections redondantes de Context engineering en gardant les décisions propres de construction du contexte.
5. Traiter séparément Generation/complexity puis Training loop/Loss/Gradients.
6. Vérifier parité FR/EN, métadonnées, liens, ancres, citations, figures, alt text, exercices, durée rendue et navigation. Distinguer CI, rendu Quarto et revue humaine.

## 7. État des preuves

- Vérifié sur les sources FR/EN : titres et ordre des sections RAG, Context engineering, Generation, complexity, Training loop et ICL.
- Vérifié : exercices RAG FR/EN et leurs sept familles de questions.
- Vérifié : Loss et Gradients possèdent déjà les explications mathématiques que Training loop doit rappeler sans recopier.
- Vérifié : `data/guided-route.yml` a neuf étapes et une seule entrée facultative `rag-memory-boundaries` sous `context-use`.
- Réalisé depuis cet inventaire : création des pages retrieval FR/EN, transfert vérifié des sections et ressources correspondantes, réduction des pages RAG et Context engineering, intégration dans le registre de route optionnelle, la carte Deepen, la configuration Quarto et le test de membership.
- En attente : génération locale du graphe/projections, rendu Quarto final, CI sur le dernier commit, revue rendue/accessibilité et test avec apprenant.

## Synthèse opérationnelle

La séparation retrieval / RAG-mémoire est justifiée par deux objectifs autonomes déjà présents. La nouvelle page optionnelle possède les familles de retrievers, la recherche visuelle, le reranking et l'exemple FAISS ; la page RAG conserve le cycle d'information externe, l'expérience intégratrice, la mémoire et la sécurité. Context engineering reste propriétaire de la conception du contexte et ne perd que les explications qui appartiennent au propriétaire RAG. Les lots Generation/complexity et Training loop/Loss/Gradients restent distincts et seront traités après vérification de leurs dépendances.


## 8. Audit détaillé des exercices et de l'index Deepen

### Exercices RAG existants : répartition des objectifs

Les sept exercices FR/EN ont été lus intégralement. Ils couvrent les objectifs suivants :

| Exercice | Compétence testée | Propriétaire après découpage |
|---|---|---|
| 1. Frontière de transmission | Distinguer disponibilité, récupération, injection au contexte et retour d'outil au tour suivant | Page RAG : synthèse de bout en bout |
| 2. Diagnostic d'un RAG défaillant | Parcourir source, parsing, chunking, requête, ranking, assemblage, troncature et usage par le modèle | Page RAG : diagnostic intégré ; renvoi vers retrieval pour les étapes recherche/classement |
| 3. RAG, mémoire et ICL | Affecter des finalités différentes à documentation, continuité de projet et format d'exemple | Page RAG + liens vers Memory/ICL |
| 4. Expérience contrôlée | Séparer stockage, indexation, récupération et transmission, puis contrôler les variables | Page RAG : expérience intégratrice |
| 5. Qualité de retrieval vs exploitation | Interpréter rappel de récupération et fidélité de réponse conditionnelle | Pont entre les deux pages ; le détail des mesures de retrieval peut être lié depuis la page retrieval |
| 6. Gouvernance mémoire | Gérer contradictions, fraîcheur, provenance, remplacement et propagation des suppressions | Page RAG : mémoire et gouvernance |
| 7. Connaissance paramétrique vs information fournie | Distinguer pré-entraînement, fine-tuning, RAG et contexte ponctuel | Page RAG : synthèse d'ensemble |

**Décision : ne pas scinder le hub d'exercices à ce stade.** Aucun exercice n'est exclusivement consacré aux architectures de retrievers ; l'exercice 2 et l'exercice 5 les touchent, mais au sein d'un diagnostic de bout en bout. Un exercice retrieval autonome ferait doublon tant qu'un objectif d'apprentissage spécifique (par exemple choisir un retriever selon une distribution de requêtes et interpréter nDCG/Recall@k) n'est pas ajouté au contenu et étayé par un protocole. La nouvelle page pourra renvoyer au hub existant, avec un libellé indiquant qu'il s'agit d'une pratique intégratrice RAG/mémoire, et non d'un atelier spécialisé de ranking.

### Placement de la future page retrieval : implications constatées

Le hub `site/fr/deepen.qmd` est une carte éditoriale manuelle, organisée par six questions. La page RAG actuelle figure explicitement sous **Inférence et efficacité**. L'ajout d'une page retrieval exige donc une mise à jour coordonnée de la carte FR et EN, pas seulement un changement de page map.

Pour rester cohérent avec les contrats existants, la future page devra au minimum avoir :
- un `LLM-LAB-PAGE-MAP` propre avec un identifiant stable `fr/document-retrieval` / `en/document-retrieval` ;
- `domain: inference-efficiency`, `type:deep-dive`, `destination:deepen`, `level:advanced`, et un topic distinct `document-retrieval` ;
- `hierarchy.parents: ["fr/deepen"]` / `["en/deepen"]`, sans parent RAG : ce n'est pas un sous-chapitre de RAG mais une page sœur ;
- `suggested_route.previous: null` et `next: null` ; aucun lien d'ordre entre les deux approfondissements ;
- des relations `related` réciproques avec RAG et Context engineering si elles expriment une pertinence réelle ;
- une entrée dans `data/guided-route.yml` sous `optional_pages` de `context-use`, uniquement si les tests confirment que ce champ représente bien une appartenance facultative sans ordre ;
- une entrée explicite dans la carte Deepen FR/EN, dans la liste `hierarchy.children` du hub si cette liste sert de projection, et dans les éventuels index/sidebar/render lists pilotés manuellement ;
- une page d'exercices distincte seulement si le contenu produit un objectif de pratique non couvert par le hub RAG existant.

Le champ `hierarchy.children` de `deepen.qmd` n'est pas à compléter aveuglément : il ne répertorie actuellement qu'un sous-ensemble des entrées visibles dans la carte. Avant édition, il faut identifier le consommateur de ce champ et vérifier s'il s'agit d'une hiérarchie volontairement partielle ou d'un inventaire incomplet. Ne pas transformer ce champ en inventaire parallèle.

### Conséquence sur les durées

Le découpage ne doit pas être justifié par la seule longueur de la page source. Il sépare deux questions autonomes : « comment retrouver et classer des documents ? » et « comment une information externe traverse-t-elle stockage, récupération, contexte et usage ? ». Après déplacement, mesurer les durées sur le rendu final FR/EN. Si la page RAG reste au-dessus de 15 minutes, examiner d'abord la densité réelle et les répétitions restantes ; ne pas couper automatiquement les sections sécurité, gouvernance ou expérience intégratrice.

## 9. Compléments de validation requis avant création des pages

- Inspecter les listes Quarto/sidebar, les contrôles de parité des pages bilingues, le générateur de page map et les tests qui consomment `hierarchy.children`, `related` et `optional_pages`.
- Vérifier si `deepen.qmd` est la seule carte éditoriale à modifier, ou si une liste d'entrées avancées est également maintenue dans une configuration.
- Auditer les liens de l'exercice RAG et les renvois depuis Context engineering pour éviter des liens qui pointent vers une section déplacée ou une ancre disparue.
- Vérifier les références ColPali, FAISS, bi-encoder/cross-encoder dans les deux langues et leur statut de liens externes.
- Après création, générer les projections de métadonnées et de graphe à partir des sources canoniques ; ne pas éditer les artefacts générés à la main.


## 10. Lot 1 exécuté — récupération documentaire et cycle RAG

### Pages créées et rôles stabilisés

- `site/fr/document-retrieval.qmd` et `site/en/document-retrieval.qmd` sont créées comme pages Deepen sœurs, avec le topic commun `document-retrieval`, le domaine `inference-efficiency`, un rôle avancé et aucun `suggested_route.previous/next`.
- Elles possèdent le pipeline d'ingestion/indexation/recherche/classement, les familles BM25/dense/SPLADE/ColBERT/cross-encoder, la recherche visuelle ColPali, le diagramme Mermaid, les résultats ViDoRe et leurs réserves, l'exemple FAISS et les ressources de reranking.
- Les blocs transférés ont été comparés au texte source avant réduction : le contenu de la section retrieval et des exemples FAISS/reranking est présent dans la nouvelle page dans les deux langues.
- `rag-memory-boundaries.qmd` conserve son identifiant et possède désormais le titre « RAG, mémoire et transmission au contexte ». Il garde les six états de l'information, le pipeline RAG et ses échecs, les types et la gouvernance de mémoire, la frontière ICL, l'expérience Orion/Delta, la sécurité et le diagnostic. Les blocs retrieval détaillés et l'exemple FAISS ne sont plus dupliqués.
- `context-engineering.qmd` conserve son rôle core. Les longs développements de pipeline retrieval/RAG/mémoire ont été remplacés par une synthèse locale qui garde les distinctions indispensables et renvoie vers les deux pages propriétaires.

### Intégration de navigation et du graphe

- Les deux nouvelles pages sont déclarées dans `data/guided-route.yml` comme membres **optionnels** de `context-use`, au même niveau que RAG. Aucune étape ni transition n'a été ajoutée.
- Le générateur existant projette directement les pages de `optional_pages` ; aucun nouveau mécanisme ni champ parallèle n'a été introduit.
- Les deux cartes Deepen et leurs relations hiérarchiques réciproques incluent la nouvelle page.
- `site/_quarto.yml` inclut les deux pages dans le rendu explicite et dans la navigation latérale FR/EN.
- Les liens context engineering ↔ retrieval/RAG et les relations page-map bilingues ont été mis à jour.
- Le test `test_guided_route_memberships.py` vérifie désormais que `document-retrieval` est optionnel dans `context-use`, et non une page core.

### Contrôles effectués et limites

- Comparaison de conservation automatisée sur les chaînes sources FR/EN : sections retrieval et exemples FAISS/reranking présents dans les nouvelles pages ; sections détaillées absentes des pages RAG après transfert.
- Contrôle structurel des pages : titres, topics, tags, relations, headings, diagramme Mermaid et liens de pratique.
- Le contrôle Python « Validate page metadata learning graph » a réussi sur un commit précédent de cette branche, après l'intégration des pages et de leurs métadonnées. Les commits de finition ultérieurs doivent encore repasser les contrôles.
- Les jobs Test suite et Quarto site & browser audit étaient encore en cours au dernier relevé ; ne pas les déclarer réussis avant lecture de leur conclusion sur le SHA courant.
- Pas de validation visuelle/accessibilité ni de test avec apprenant revendiqué.

### Synthèse du lot

Le découpage a été exécuté sans créer de route parallèle : retrieval est désormais une ressource Deepen facultative indépendante, tandis que RAG/mémoire garde le parcours de l'information externe jusqu'à son usage et Context engineering reste propriétaire de la conception du contexte. Les éléments déplacés sont préservés dans les deux langues ; les tests et le rendu sur le dernier commit restent les conditions de clôture du lot.
