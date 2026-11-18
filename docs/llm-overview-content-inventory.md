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
- Non effectué : déplacement/suppression de contenu, création de page retrieval, modification de métadonnées, génération du graphe, rendu Quarto, CI, revue rendue ou test avec apprenant.

## Synthèse opérationnelle

La séparation retrieval / RAG-mémoire est justifiée par deux objectifs autonomes déjà présents. La nouvelle page optionnelle possède les familles de retrievers, la recherche visuelle, le reranking et l'exemple FAISS ; la page RAG conserve le cycle d'information externe, l'expérience intégratrice, la mémoire et la sécurité. Context engineering reste propriétaire de la conception du contexte et ne perd que les explications qui appartiennent au propriétaire RAG. Les lots Generation/complexity et Training loop/Loss/Gradients restent distincts et seront traités après vérification de leurs dépendances.
