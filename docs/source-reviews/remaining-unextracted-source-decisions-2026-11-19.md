# Décisions sur les 21 autres sources sans extraction — 2026-11-19

**Périmètre :** seconde tranche du contrôle des sources sans fichier `data/extractions/<source_id>.yml`, après la première décision des 23 sources marquées `integration_status: integrated` et après l'extraction dédiée du papier CHI 2026 Transformer Explainer.
**Instantané de référence :** catalogue `data/sources.yml` sur `main` au 19 novembre 2026. Les décisions ci-dessous ne modifient pas les statuts du catalogue.
**Principe :** « déjà couvert avec preuve » désigne une couverture bornée et localisable dans un audit ou une page existante ; cela ne signifie pas que l'intégralité de la source, ses figures, son code ou ses droits ont été audités. « Différer » conserve explicitement une condition de reprise. « Rejeter » concerne l'usage de la référence comme preuve exploitable, pas la suppression de sa trace de provenance.

## Décisions individuelles

| Source ID | Décision | Preuve / motif et limite |
|---|---|---|
| `raschka-bpe-from-scratch-2025` | Déjà couvert avec preuve | L'audit de tokenisation et la matrice de migration traitent l'explication BPE, l'entraînement/encodage et les liens d'implémentation ; destinations bilingues `tokenization-strategies`. La source reste une explication secondaire et aucun code n'est déclaré exécuté dans cet audit. |
| `cornell-byte-pair-visualizer` | Différer | Le contrôle antérieur a observé `Frequency: undefined` dans l'interface. La comparaison BPE/WordPiece est déjà expliquée dans les pages bilingues, mais le comportement du démonstrateur n'est pas assez fiable pour être recommandé sans nouveau test manuel. Reprise : vérifier les états d'interaction et la valeur affichée. |
| `vizuara-tokenization-from-scratch-bpe` | Différer | L'audit #147 et la matrice de migration n'ont inspecté que la page de présentation, les ressources annoncées et la structure du cours ; les leçons/notebooks complets peuvent être protégés. Reprise uniquement avec accès au contenu intégral et contribution pédagogique distincte de l'explication BPE existante. |
| `vizuara-llms-from-30000-feet` | Différer | Le contrôle porte sur la description du micro-cours et ses thèmes, pas sur l'intégralité des leçons. Les pages `text-data` et `tokenization-strategies` couvrent déjà les notions annoncées ; aucune extraction atomique n'est justifiée sans accès aux contenus complets et à un apport distinct. |
| `mike-x-cohen-llm-breakdown-tokenization-2025` | Déjà couvert avec preuve | L'audit de source compare explicitement ses explications de tokenisation et son notebook aux traitements canoniques du projet ; les pages bilingues `text-data` et `tokenization-strategies` portent les notions retenues. Les formulations « optimal chunking » et compression ratio sont qualifiées ; figures et notebook ne sont pas réutilisés. |
| `rohan-paul-vocabulary-size-tradeoffs-2025` | Différer | L'article a été examiné sur la taille du vocabulaire, la longueur des séquences et les coûts des matrices d'embedding/sortie. Les affirmations chiffrées sont secondaires et dépendantes du modèle/protocole ; les pages existantes couvrent déjà les compromis conceptuels. Reprise seulement après corroboration primaire des chiffres qui apporteraient une information non redondante. |
| `yael-gomez-tokenization-overview-2025` | Déjà couvert avec preuve | L'audit compare ses exemples débutants, espaces blancs et discussion BPE aux explications techniques canoniques ; les pages bilingues `text-data` et `tokenization-strategies` couvrent les notions utiles. Les métaphores restent des aides pédagogiques et les affirmations de complexité sont limitées au terme quadratique de l'attention dense standard. |
| `aiedge-how-llm-distillation-trains-smaller-models` | Différer | L'article est inaccessible (cache miss) ; auteur, date, contenu, figures et références n'ont pas pu être vérifiés. Les publications voisines ne sont pas des substituts. Reprise : récupérer le texte primaire ou une version archivée vérifiable, sinon conserver l'état inaccessible. |
| `cameron-wolfe-score-centering-substack` | Différé au 19 novembre, traité le 21 novembre | Le corps était indisponible lors de cette revue. Le [nouvel audit](score-centering-2026-11.md#12-secondary-article-review--2026-11-21) et l'[extraction dédiée](../../data/extractions/cameron-wolfe-score-centering-substack.yml) documentent la lecture secondaire et les limites d'accès. Le papier et son implémentation restent des sources distinctes. |
| `jay-alammar-illustrated-gpt2` | Déjà couvert avec preuve | L'audit pédagogique #756/#758 a inspecté le texte intégral et documenté Q/K/V, masque causal, agrégation des valeurs, projection de sortie et distinction entraînement/inférence ; les pages bilingues `generation`, `queries-keys-values` et `scaled-dot-product-attention` sont liées. Les dimensions et intuitions GPT-2 ne sont pas généralisées à toutes les architectures. |
| `jay-alammar-how-transformer-llms-work-2025` | Différer | Seuls le plan officiel du cours, les objectifs, l'annonce et les liens de code ont été examinés ; vidéos, quiz et exemples n'ont pas été audités. Les pages actuelles couvrent déjà une partie du parcours. Reprise si l'accès aux leçons révèle un contenu avancé distinct (GQA, MLA, MoE, etc.) avec localisateurs et version. |
| `3blue1brown-attention-transformers-step-by-step-2024` | Déjà couvert avec preuve | L'audit #756/#759 a inspecté l'adaptation textuelle, les questions intégrées, les timestamps et le code source public des scènes ; les pages bilingues Q/K/V, attention à produit scalaire, masque causal et représentations sont liées. La vidéo rendue n'a pas été regardée indépendamment ; aucune animation n'est copiée. |
| `3blue1brown-but-what-is-a-gpt-2024` | Déjà couvert avec preuve | L'audit pédagogique a inspecté l'adaptation textuelle, la structure de la leçon et les scripts d'animation publics ; les destinations bilingues couvrent texte, embeddings, représentations contextualisées, génération et probabilités. Les exemples GloVe ne sont pas assimilés aux embeddings de tokens GPT et les explications d'entraînement restent introductives. |
| `youtube-jepa-platonic-representation-j0o8a6ducw` | Rejeter | L'identité du contenu n'est pas vérifiable : titre, créateur, date, durée, transcription et propos restent inconnus malgré les tentatives de récupération. La référence est rejetée comme preuve et comme ressource pédagogique exploitable. Conserver la notice de provenance jusqu'à décision distincte de nettoyage du catalogue ; ne rien lui attribuer. |
| `brij-pandey-inference-generation-linkedin-2026` | Déjà couvert avec preuve | L'audit dédié a inspecté le texte visible et le diagramme sur tokenisation, prefill, décodage, KV cache, streaming, TTFT/ITL et speculative decoding ; les pages bilingues `generation` portent les mécanismes retenus. La source est secondaire, aucun benchmark n'est inféré et le diagramme n'est pas reproduit. |
| `bbycroft-llm-visualization` | Différer | L'audit des ressources visuelles n'a vu que la description et des captures indexées ; le parcours interactif complet et sa révision ne sont pas épinglés. La ressource peut compléter l'aperçu des tenseurs/Transformer, mais ses dimensions et proportions propres au modèle ne doivent pas être généralisées. Reprise après inspection manuelle complète et versionnement. |
| `tensorflow-playground` | Différer | La page officielle et le README ont été examinés. L'outil porte sur un petit réseau feed-forward, pas sur un Transformer ou un LLM ; il peut servir de prérequis facultatif pour gradients, loss et surapprentissage. Ne pas créer d'extraction scientifique LLM ; reprendre seulement si un exercice de formation générale nécessite un test d'interaction et une licence clarifiée. |
| `raschka-visual-attention-variants` | Déjà couvert avec preuve | La revue des ressources visuelles et l'extension bilingue comparent MHA/MQA/GQA/MLA, fenêtres glissantes et attention sparse. Les distinctions entre nombre de têtes KV, taille du cache, connectivité, calcul et latence sont conservées ; les exemples de modèles et performances restent à vérifier sur sources primaires et benchmarks comparables. |
| `grootendorst-visual-guide-moe` | Déjà couvert avec preuve | La revue des ressources visuelles a inspecté le plan et les sections accessibles sur experts, routage, capacité et équilibrage ; un exercice déterministe top-2 a été ajouté au parcours bilingue. Les équations complètes, références primaires et exemples de routage n'ont pas été reproduits ; la source reste un support pédagogique, non une preuve primaire. |
| `modular-llm-inference-handbook` | Déjà couvert avec preuve | La revue a inspecté la page d'accueil, le README public et l'inventaire des outils ; les pages bilingues de génération ont été étendues sur TPOT, continuous batching, prefix caching et chunked prefill. Les chapitres individuels, calculateurs, benchmarks et révisions du handbook ne sont pas couverts ; les affirmations matérielles restent datées et dépendantes du workload. |
| `dailydose-visual-guide-bi-cross-colbert-2025` | Déjà couvert avec preuve | La revue dédiée et les extensions bilingues cosine/RAG documentent bi-encodeur, cross-encodeur, late interaction/ColBERT, BM25, SPLADE, hybrid retrieval et limites du reranking. Les sections paywall et l'image intégrée non récupérée restent hors périmètre ; les affirmations techniques sont corroborées par les papiers primaires listés dans le dossier, pas par le tutoriel seul. |

## Synthèse des décisions

| Décision | Nombre |
|---|---:|
| Déjà couvert avec preuve (couverture bornée) | 11 |
| Extraire | 0 |
| Différer | 9 |
| Rejeter | 1 |
| **Total** | **21** |

Aucune extraction supplémentaire n'est déclenchée dans cette tranche : les sources jugées couvertes ont déjà une preuve documentaire bornée et les sources différées ne satisfont pas encore leurs conditions de reprise. Le rejet porte uniquement sur une vidéo dont l'identité et le contenu sont invérifiables.

## Conditions de reprise

1. Cornell : revalider le défaut d'interface et la cohérence BPE/WordPiece.
2. Vizuara : obtenir et inspecter le contenu intégral des cours.
3. Rohan Paul : vérifier les chiffres contre les sources primaires.
4. AI Edge : retrouver le texte exact avant toute attribution. Pour Cameron Wolfe, voir la décision du 21 novembre ci-dessus.
5. DeepLearning.AI : auditer les vidéos, le quiz et les exemples avant d'intégrer des contenus spécifiques.
6. Bbycroft et TensorFlow Playground : exécuter un parcours interactif versionné si leur usage pédagogique est retenu.
7. Ne pas réouvrir les sources déjà couvertes sauf changement de version, nouvelle affirmation ou lacune précisément localisée.

## Limites de cette décision

Cette tranche s'appuie sur les audits et dossiers existants, dont plusieurs sont explicitement partiels. Elle n'est ni une nouvelle lecture intégrale de 21 ressources ni une validation indépendante de chaque affirmation technique. Aucun droit de réutilisation de figure, de vidéo, de code ou de données n'est déduit de l'accessibilité publique. Aucun KPI de couverture scientifique n'est calculé.
