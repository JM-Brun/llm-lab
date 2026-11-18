# Triage raisonné des sources sans extraction — 18 novembre 2026

**Périmètre :** inventaire de `data/sources.yml` et des fichiers `data/extractions/`, complété par les titres, types, tags, pages associées et statuts de catalogue. Ce document est un **triage éditorial de métadonnées**, pas une attestation de lecture intégrale du nombre de ressources restant à auditer.

## 1. Réconciliation de l'inventaire

- Catalogue : **139 sources**.
- Fichiers d'extraction : **93**.
- Cinq fichiers portent un nom différent de l'identifiant du catalogue, mais leur champ `source_id` renvoie bien à une source existante : Chanin, Cunningham, Neuronpedia, Shu et Wayland. Ils ne doivent pas être comptés comme cinq sources non extraites. La convention du dépôt demande néanmoins un nom de fichier égal à l'identifiant canonique ; cette anomalie de nommage mérite un correctif séparé.
- Sennrich et al. (2016), #1311, a été fusionnée dans `main` le 18 novembre 2026 ; son extraction est incluse dans les 93 fichiers.
- Gage (1994), #1314, a depuis également été fusionnée dans `main`.
- Le décompte de **44 sources** du présent triage est donc obsolète. Il doit être recalculé par comparaison ensembliste des `source_id` du catalogue et des extractions du head courant ; ne pas le réutiliser comme état actuel. Les cinq fichiers non canoniques restent des extractions existantes, pas cinq sources manquantes.

Ce décompte est un état de dépôt, pas un KPI de qualité ni une mesure de couverture documentaire. Il ne dit rien de la valeur des sources ni de leur inspection effective.

## 2. Règles de décision

Une extraction est justifiée seulement si elle capture une contribution atomique réutilisable et non déjà couverte. Les décisions possibles dans ce triage sont :

- **Référence / lien :** conserver la source dans la bibliographie et les pages, sans extraction dédiée.
- **Audit ciblé :** inspecter un passage, une API ou un chemin de code et n'extraire que les éléments utiles.
- **Audit pédagogique de projet :** reconstruire le parcours, les prérequis, les activités et les visualisations ; ne pas transformer automatiquement le projet en longue extraction de claims.
- **À différer / inaccessible :** ne pas produire d'extraction tant que l'accès ou l'identité ne permet pas un audit fiable.
- **À dédupliquer :** rapprocher d'une source ou extraction voisine avant toute nouvelle extraction.

Les recommandations ci-dessous sont provisoires et fondées sur les métadonnées. Une décision d'extraction exige ensuite une inspection réelle, des localisateurs précis et une comparaison avec les pages canoniques.

## 3. Sources de tokenisation et embeddings

| Source ID | Type / rôle probable | Décision provisoire | Motif et prochain contrôle |
|---|---|---|---|
| `sebastian-raschka-llms-from-scratch-ch02` | Chapitre de livre pédagogique | À dédupliquer puis audit ciblé | Comparer au contenu déjà couvert par les ressources Raschka et les exemples BPE existants ; n'extraire que les explications ou exercices distinctifs. |
| `huggingface-course-tokenizers-chapter6` | Leçon de cours | À dédupliquer puis audit pédagogique ciblé | Rapprocher du cours Hugging Face déjà présent ; déterminer si le chapitre apporte une séquence d'apprentissage ou des démonstrations non couvertes. |
| `catherine-arnett-tokenizer-fertility` | Article secondaire sur la fertilité des tokenizers | Audit ciblé, claims à corroborer | Potentiellement utile pour les coûts multilingues ; séparer définitions, mesures et recommandations, puis vérifier les résultats contre les études primaires. |
| `sentence-transformers-similarity-documentation` | Documentation officielle d'API | Référence technique ; extraction sélective si utilisée | Conserver les contrats précis des API de similarité/encodage, sans extraire la documentation entière. |
| `openai-tiktoken-educational-bpe` | Module pédagogique / code | Audit de code ciblé | Vérifier pré-tokenisation, fusion, vocabulaire, tokens spéciaux et décodage ; comparer au dépôt tiktoken et à minbpe. |
| `karpathy-minbpe` | Implémentation minimale | Audit de code ciblé | Source utile pour illustrer entraînement et encodage BPE ; ne pas confondre le code pédagogique avec une spécification universelle. |
| `huggingface-tokenizers-pipeline-docs` | Documentation technique officielle | Extraction ciblée | Extraire les responsabilités réelles des étapes normalizer, pre-tokenizer, model, post-processor et decoder, avec version/API. |
| `google-sentencepiece-documentation` | Documentation technique officielle | Extraction ciblée | Distinguer normalisation, unités de base, BPE/Unigram et traitement des espaces ; garder les comportements dépendants de version explicites. |
| `huggingface-tokenizer-algorithms-summary` | Documentation de synthèse | Référence / déduplication | Comparer à la documentation de pipeline ; ne pas dupliquer les mêmes descriptions d'algorithmes. |
| `pytorch-embedding-api` | Documentation officielle d'API | Référence technique ; extraction ciblée si affirmation de page | Ne retenir que les garanties API effectivement utilisées : lookup par indices, forme, padding et options pertinentes. |
| `openai-tiktoken-repository` | Implémentation | Audit de code ciblé | Identifier les chemins d'encodage/décodage et les fichiers de vocabulaire ; auditer une version ou un commit précis. |
| `huggingface-tokenizers-repository` | Implémentation | Audit de code ciblé | Sélectionner les chemins de code qui corroborent les étapes du pipeline ; ne pas faire une extraction exhaustive du dépôt. |
| `google-sentencepiece-repository` | Implémentation | Audit de code ciblé | Relier documentation, algorithmes et code à une version ; comparer uniquement les comportements utiles à la leçon. |
| `sauravp97-hf-bpe-visualizer-article` | Article explicatif et visualisation | Audit pédagogique de projet / déduplication | Examiner la valeur explicative du visuel et les étapes rendues visibles ; rapprocher de son dépôt compagnon. |
| `sauravp97-hf-bpe-visualizer-repository` | Dépôt du visualiseur | Audit technique ciblé, lié à l'article | Vérifier les interactions et la fidélité au tokenizer réellement représenté ; ne pas dupliquer l'article en extraction séparée. |
| `rushang-chauhan-embeddings-bridge-tokens-context` | Article pédagogique secondaire | Référence, extraction seulement si apport distinct | Comparer les analogies et explications aux pages embeddings/contextualisation ; ne pas traiter une analogie comme preuve technique. |
| `poloclub-transformer-explainer-paper-2026` | Article de recherche sur un outil pédagogique | Audit pédagogique de projet | Examiner objectifs, conception d'interaction et protocole d'évaluation ; ne pas inférer l'efficacité d'apprentissage de la seule existence de l'outil. |
| `poloclub-transformer-explainer-repository` | Implémentation de l'outil pédagogique | Audit de projet/code ciblé | Relier les interactions aux mécanismes réellement calculés ; garder le dépôt distinct de l'article, mais dans un même dossier de projet. |
| `raschka-bpe-from-scratch-2025` | Tutoriel / implémentation pédagogique | Référence ou audit pédagogique ciblé | Comparer à minbpe et à l'explication canonique ; extraire seulement les choix didactiques ou pièges d'implémentation nouveaux. |
| `philip-mueller-bpe-explainer` | Visualisation interactive | Ressource pédagogique, pas extraction automatique | Vérifier ce que l'utilisateur peut manipuler, les hypothèses de segmentation et les limites du modèle illustré. |
| `cornell-byte-pair-visualizer` | Visualiseur pédagogique | Différé tant que l'accès et la valeur ajoutée ne sont pas confirmés | Conserver la référence ; ne pas créer d'extraction sur la seule base du titre. |
| `bytebytego-how-llms-learn-from-internet-2025` | Article secondaire de vulgarisation | Référence contextuelle | Les affirmations sur collecte/préparation de corpus doivent être corroborées par sources primaires ou techniques ; pas d'extraction de claims génériques. |
| `bytebytego-how-llms-see-world-2025` | Article secondaire de vulgarisation | Référence contextuelle | Comparer aux explications canoniques de tokens, embeddings et représentations ; éviter une seconde synthèse redondante. |
| `vizuara-tokenization-from-scratch-bpe` | Cours / leçon pédagogique | Audit pédagogique ciblé si le cours est retenu | Reconstruire le modèle local, les étapes et les exercices avant toute intégration ; pas d'extraction si le contenu répète l'existant. |
| `vizuara-llms-from-30000-feet` | Cours d'introduction | Audit pédagogique de projet, priorité basse | Évaluer la progression globale et les prérequis ; le simple recouvrement de thèmes ne justifie pas une extraction par chapitre. |
| `mike-x-cohen-llm-breakdown-tokenization-2025` | Article / leçon pédagogique | Audit ciblé | Examiner les exemples et démonstrations ; conserver seulement les explications qui résolvent un obstacle distinct. |
| `rohan-paul-vocabulary-size-tradeoffs-2025` | Analyse secondaire des compromis de vocabulaire | Claims ciblés à corroborer | Séparer hypothèses, mesures et recommandations ; relier les chiffres à leurs études et modèles d'origine. |
| `yael-gomez-tokenization-overview-2025` | Vue d'ensemble secondaire | Référence contextuelle / déduplication | Ne pas créer une extraction de résumé si elle n'ajoute ni preuve, ni modèle pédagogique, ni exemple distinctif. |

## 4. Autres domaines

| Source ID | Type / rôle probable | Décision provisoire | Motif et prochain contrôle |
|---|---|---|---|
| `aiedge-how-llm-distillation-trains-smaller-models` | Article secondaire, marqué inaccessible | Inaccessible : aucune extraction | Retrouver une version stable ou conserver explicitement l'inaccessibilité ; ne pas reconstituer le contenu depuis le titre. |
| `cameron-wolfe-score-centering-substack` | Article technique secondaire sur score centering | Référence différée / vérification primaire | Identifier la proposition exacte et son domaine d'application ; vérifier contre les papiers et implémentations cités avant extraction. |
| `jay-alammar-illustrated-gpt2` | Article pédagogique illustré | Audit pédagogique de projet, actuellement différé | Les illustrations peuvent apporter un modèle mental distinctif ; examiner images, légendes et parcours avant extraction. |
| `jay-alammar-how-transformer-llms-work-2025` | Cours / série pédagogique | Audit pédagogique de projet, actuellement différé | Reconstruire le parcours et les activités par module ; ne pas assimiler une liste de sujets à un modèle pédagogique. |
| `3blue1brown-attention-transformers-step-by-step-2024` | Vidéo pédagogique | Audit média ciblé, actuellement différé | Capturer les séquences et timestamps réellement inspectés ; distinguer visualisation, affirmation technique et résultat d'apprentissage. |
| `3blue1brown-but-what-is-a-gpt-2024` | Vidéo pédagogique | Audit média ciblé, actuellement différé | Même règle : timestamps, figures et limites ; extraire les apports uniques sur génération et représentations seulement. |
| `youtube-jepa-platonic-representation-j0o8a6ducw` | Vidéo, titre/créateur non vérifiés | Inaccessible / identité à résoudre | Vérifier l'ID et les métadonnées avant toute attribution ou extraction. |
| `brij-pandey-inference-generation-linkedin-2026` | Publication sociale de praticien | Audit ciblé de provenance et corroboration | Séparer observation personnelle, affirmation générale et interprétation ; la portée d'un post ne suffit pas à établir un mécanisme d'inférence. |
| `sebastian-raschka-full-to-hybrid-attention-companion-2026` | Ressource compagnon sur les architectures hybrides | À dédupliquer avec les ressources Raschka proches | Vérifier si cette entrée est distincte de l'article principal et des extractions déjà existantes ; corriger les identités avant toute nouvelle extraction. |
| `bbycroft-llm-visualization` | Visualisation interactive de LLM | Audit de projet / ressource visuelle | Inspecter les contrôles, états et calculs représentés ; ne pas présenter la visualisation comme preuve empirique. |
| `tensorflow-playground` | Environnement interactif pédagogique | Audit de projet | Décrire les variables manipulables et les phénomènes effectivement observables ; extraction pédagogique uniquement si une activité est intégrée. |
| `raschka-visual-attention-variants` | Guide visuel d'attention | Audit pédagogique ciblé | Vérifier la fidélité des schémas aux variantes MHA/GQA/MLA et les hypothèses ; ne pas extraire les mêmes définitions déjà couvertes. |
| `grootendorst-visual-guide-moe` | Guide visuel MoE | Audit pédagogique ciblé | Extraire uniquement le modèle de routage, les visualisations ou les limites qui améliorent la page canonique. |
| `modular-llm-inference-handbook` | Documentation / handbook d'inférence | Audit technique ciblé | Vérifier version, périmètre et exactitude des descriptions prefill/decode/KV cache/serving ; retenir les contrats utiles plutôt qu'un résumé global. |
| `apple-embedding-atlas` | Outil de visualisation d'embeddings | Audit de projet et d'implémentation | Vérifier les opérations, méthodes de réduction/clustering et limites d'interprétation ; ne pas assimiler proximité 2D et similarité sémantique démontrée. |
| `dailydose-visual-guide-bi-cross-colbert-2025` | Guide pédagogique de recherche d'information | Audit pédagogique et technique ciblé | Distinguer bi-encoder, cross-encoder et late interaction ; vérifier les claims de performance et le rôle exact de ColBERT contre les papiers originaux. |

## 5. Priorisation recommandée

### Lot A — valeur technique élevée, audit ciblé
1. Hugging Face Tokenizers pipeline docs.
2. SentencePiece documentation.
3. PyTorch Embedding API.
4. tiktoken / minbpe : comparer les chemins d'implémentation utiles, sans extraction en double.
5. Sentence Transformers similarity API.

### Lot B — pédagogie et visualisations
1. Transformer Explainer (article + dépôt traités comme un projet lié).
2. BPE Explainer de Philip Müller.
3. Visualiseur Saurav (article + dépôt liés).
4. Ressources Raschka/Vizuara, après comparaison de redondance.

### Lot C — références secondaires et preuves à vérifier
Arnett, Rohan Paul, ByteByteGo, Yael Gomez, Rushang Chauhan, Mike X. Cohen. N'extraire que des claims nouveaux et vérifiés ou des dispositifs pédagogiques distinctifs.

### Lot D — accès, provenance ou périmètre incertains
AIEdge, vidéo JEPA non vérifiée, Cornell visualizer et publication LinkedIn. Résoudre l'accès et la provenance avant d'investir dans une extraction.

## 6. Garde-fous

- Ne pas créer d'extraction pour rendre les compteurs égaux.
- Ne pas transformer une documentation d'API en preuve d'une affirmation qui dépasse son contrat.
- Ne pas extraire un dépôt entier : sélectionner des chemins de code et une révision.
- Ne pas confondre visualisation, explication pédagogique et validation expérimentale.
- Ne pas créer de nouveaux concepts ou relations à partir de tags ou de titres.
- Pour toute source pédagogique effectivement extraite, construire le `pedagogical_model` requis (graphe local, outcomes, prérequis, route, forces/limites, comparaison).
- Pour chaque décision finale, conserver les localisateurs, la justification de disposition et la comparaison avec la page canonique.
- Sennrich et al. (#1311) et Gage (#1314) sont intégrés à `main`. Le décompte des sources restantes doit être recalculé sur les `source_id` du head courant.

## 7. Prochaine action

Commencer par le Lot A, en commençant par la documentation officielle Hugging Face et SentencePiece, puis l'API PyTorch. Pour chaque ressource, vérifier la version, inspecter les sections effectivement utilisées, identifier les affirmations des pages qui en dépendent, et ne créer une extraction que si un élément atomique nouveau ou une garantie technique précise est nécessaire.
