# Décisions sur les sources intégrées sans extraction — 2026-11-19

**Périmètre :** contrôle des sources de `data/sources.yml` dont `integration_status: integrated` et pour lesquelles aucun fichier `data/extractions/<source_id>.yml` n'existe sur `main`.
**Méthode :** rapprochement exact des 139 identifiants du catalogue avec les 95 fichiers YAML du répertoire d'extractions, puis examen des audits et synthèses déjà présents. Ce document ne constitue pas une nouvelle lecture intégrale des 23 sources.
**Règle :** « déjà couvert » signifie qu'une preuve de couverture identifiable existe dans le dépôt ; la simple présence d'une source dans la bibliographie ou dans le catalogue ne suffit pas. « Différer » n'est pas une validation scientifique ni une décision de rejet.

## 1. Décisions explicites — 23 sources marquées intégrées

| Source ID | Décision | Motif et preuve / condition |
|---|---|---|
| `sebastian-raschka-llms-from-scratch-ch02` | Déjà couvert avec preuve | Audit antérieur #96 et matrice de migration `tokenization-embeddings-source-migration-map-2026-11.md`; le parcours texte → token IDs → embeddings et les notebooks BPE sont déjà traités. Conserver la limite entre entraînement simplifié caractère/chaîne et chargement GPT-2 pré-entraîné. |
| `huggingface-course-tokenizers-chapter6` | Déjà couvert avec preuve | Audit #114 / PR #173 et pages bilingues de stratégies de tokenisation : BPE, WordPiece, Unigram et pipeline. La couverture est bornée au chapitre et aux sections inspectées, pas au cours entier. |
| `catherine-arnett-tokenizer-fertility` | Différer | L'entrée est enregistrée comme ressource sur le tokenizer recycling, mais aucun fichier d'extraction dédié ni preuve de couverture atomique localisée n'a été identifié dans le contrôle présent. Reprendre l'audit primaire et déterminer précisément les affirmations originales avant extraction ; ne pas déduire que les autres travaux d'Arnett couvrent cet article. |
| `sentence-transformers-similarity-documentation` | Différer | Documentation vivante d'API ; le dossier de collection traite déjà similarité et géométrie, mais ne prouve pas une couverture versionnée de toutes les API. Reprendre uniquement avec une version/documentation datée et des localisateurs API utiles au code du projet. |
| `openai-tiktoken-educational-bpe` | Déjà couvert avec preuve | Audit comparatif `tokenization-implementations-huggingface-tiktoken-minbpe-2026-11.md` : module éducatif distingué du cœur natif `CoreBPE`, avec limites d'usage explicites. |
| `karpathy-minbpe` | Déjà couvert avec preuve | Même audit comparatif : variantes Basic, Regex et GPT4, chemins de code et limites de fidélité décrits. La licence du dépôt est vérifiée dans le catalogue ; cela ne vaut pas autorisation de réutiliser des éléments tiers. |
| `huggingface-tokenizers-pipeline-docs` | Déjà couvert avec preuve | Audit comparatif du 18–19 novembre, complété par PR #1326 : pipeline versionné v0.23.3 distingué de la documentation non versionnée et de l'avertissement rc0. Pas de revendication de test d'exécution ou de compatibilité. |
| `google-sentencepiece-documentation` | Déjà couvert avec preuve | Synthèse de collection et pages bilingues de stratégies de tokenisation ; SentencePiece est distingué comme bibliothèque/pipeline et non assimilé à une implémentation BPE générique. Revoir seulement si une API/version précise devient nécessaire. |
| `huggingface-tokenizer-algorithms-summary` | Déjà couvert avec preuve | Les familles BPE, WordPiece et Unigram sont comparées dans les pages de tokenisation et dans l'audit du cours HF (#114 / PR #173). La page récapitulative ne justifie pas une seconde extraction des mêmes définitions. |
| `pytorch-embedding-api` | Différer | La notion d'indexation/lookup d'embedding est déjà couverte dans le graphe et les pages d'embeddings ; la documentation API n'a pas été reliée ici à une version PyTorch et à un chemin de code précis. Reprendre si un exemple exécutable du projet dépend d'un comportement d'API déterminé. |
| `openai-tiktoken-repository` | Déjà couvert avec preuve | Audit comparatif des implémentations : commit inspecté, `Encoding`, pré-découpage, rangs, tokens spéciaux et délégation au cœur natif explicités. La distinction production/pédagogie est maintenue. |
| `huggingface-tokenizers-repository` | Déjà couvert avec preuve | Audit comparatif et PR #1326 : architecture des composants et limites de version documentées. La documentation du pipeline n'est pas présentée comme un audit exhaustif de toutes les API du dépôt. |
| `google-sentencepiece-repository` | Déjà couvert avec preuve | Dossier de collection tokenization/embeddings et pages bilingues ; le dépôt sert de référence d'implémentation complémentaire. Aucun claim de compatibilité ou de benchmark n'est ajouté. |
| `sauravp97-hf-bpe-visualizer-article` | Différer | La matrice de migration et l'audit #114 documentent le visualiseur et ses limites. Ne pas extraire une seconde fois les explications générales BPE ; différer une extraction propre à l'article jusqu'à preuve de claims distincts et de localisateurs exacts. |
| `sauravp97-hf-bpe-visualizer-repository` | Déjà couvert avec preuve | Matrice de migration : dépôt inspecté au commit `1a802315afc0e17dddf3a64972cf25dddda8bbfe`, limites de pré-tokenisation/byte-level et absence de validation d'exécution enregistrées. Un fichier d'extraction supplémentaire du dépôt n'apporterait pas de claims distincts à ce stade. |
| `rushang-chauhan-embeddings-bridge-tokens-context` | Différer | Le sujet général tokens → embeddings → contexte est déjà enseigné ; la provenance des visuels et leurs droits restent à traiter séparément. Ne pas transformer l'article pédagogique en preuve scientifique d'un mécanisme sans claims et localisateurs propres identifiés. |
| `poloclub-transformer-explainer-paper-2026` | Extraire | Article de recherche CHI 2026 distinct du dépôt logiciel : ses questions de recherche, méthode d'évaluation, population/tâches et résultats doivent être extraits avec localisateurs propres. L'audit pédagogique existant est un point de départ, pas un substitut à une extraction atomique. |
| `poloclub-transformer-explainer-repository` | Déjà couvert avec preuve | Audit comparatif pédagogique : README, licence MIT et composants Svelte sélectionnés sont inspectés. Garder le dépôt comme artefact logiciel lié au papier ; ne pas confondre licence logicielle et droits des figures/données du papier. |
| `philip-mueller-bpe-explainer` | Différer | Le dossier de collection et la matrice de migration couvrent déjà les explications BPE et les ressources visuelles. Une extraction n'est justifiée que si l'inspection identifie un mécanisme ou une explication distincte, avec preuve et localisateur. |
| `bytebytego-how-llms-learn-from-internet-2025` | Différer | Ressource pédagogique déjà répertoriée dans le dossier de collection ; aucun élément vérifié ici ne justifie une extraction scientifique indépendante. Conserver les limites de couverture de l'article et ne pas extrapoler à l'ensemble du site ByteByteGo. |
| `bytebytego-how-llms-see-world-2025` | Différer | Même traitement : ressource de vulgarisation, non équivalente à une source primaire. Réexaminer seulement si une affirmation précise apporte une contribution distincte, vérifiable et utile aux pages existantes. |
| `sebastian-raschka-full-to-hybrid-attention-companion-2026` | Déjà couvert avec preuve | Le dossier `raschka-full-to-hybrid-attention-2026.md` examine le post et l'article compagnon, distingue les catégories d'architecture et qualifie l'échantillon/les pourcentages. L'extraction existante du post ne doit pas être dupliquée ; conserver les deux identités et leurs rôles dans le dossier. |
| `apple-embedding-atlas` | Déjà couvert avec preuve | Revue `embedding-atlas-neuronpedia-integration-2026-11.md` et intégration bilingue : fonctions, activité pédagogique, limites des projections, paramètres de reproductibilité et séparation entre licence du logiciel et droits des figures/données sont explicités. |

### Résultat de cette première tranche

- 12 décisions « déjà couvert avec preuve » ;
- 1 décision « extraire » (papier Polo Club) ;
- 10 décisions « différer » ;
- 0 rejet à ce stade : aucune source n'a été rejetée sans examen de son identité, de sa provenance et de son apport.

Les décisions « déjà couvert » ne signifient pas que toutes les composantes d'une source (commentaires, figures, code, données, licence, versions) ont été auditées. Les limites décrites dans les dossiers existants restent applicables.

## 2. Réconciliation des dénominateurs et métadonnées

Contrôle effectué sur `main` après fusion de PR #1326 :

- 139 entrées dans `data/sources.yml` ;
- 95 fichiers YAML dans `data/extractions/` ;
- 44 identifiants sans fichier d'extraction correspondant ;
- parmi ces 44, 23 ont `integration_status: integrated` (traités dans le tableau ci-dessus).

Le rapprochement des statuts de licence ne reproduit pas le nombre de 128 statuts `unknown` communiqué dans le suivi antérieur :

| Valeur dans le catalogue | Nombre |
|---|---:|
| `unknown` | 126 |
| statut absent | 4 |
| `known` | 1 |
| `verified` | 8 |
| **Total** | **139** |

Il y a donc 130 enregistrements sans statut de licence exploitable si l'on regroupe `unknown` et les champs absents ; il ne faut pas les présenter comme 130 valeurs `unknown`. Le décompte précédent de 128 doit être réconcilié avec un instantané daté ou une règle de comptage différente avant toute correction en masse.

Pour les dates de publication, 44 valeurs sont explicitement `null`. Une date absente, une date non retrouvée et une date non applicable doivent rester distinguées lors du futur audit ; aucune date ne doit être inférée à partir du nom du fichier, d'une date d'accès ou d'une date de mise à jour.

## 3. Suite nécessaire

1. Produire l'extraction atomique du papier Polo Club à partir du texte intégral et de localisateurs vérifiables ; ne pas copier de figures ou de données sans droits établis.
2. Exécuter les dix décisions différées seulement si leur condition de reprise est satisfaite ; sinon conserver le motif de différé.
3. Traiter les 21 autres sources sans extraction (celles qui ne sont pas marquées `integrated`) avec la même grille de décision.
4. Réconcilier les 128 statuts de licence antérieurs avec l'état courant (126 `unknown` + 4 absents) avant toute modification de métadonnées.
5. Auditer les 44 dates `null` indépendamment des licences.
6. Définir les règles de comptage, l'unité d'analyse et les dénominateurs avant toute publication de KPI. Aucun taux de couverture scientifique n'est produit ici.

## 4. Limites

Cette décision tranche la nécessité d'une extraction au regard des preuves déjà présentes dans le dépôt ; elle ne certifie pas la vérité de chaque affirmation source. Les audits existants ont des périmètres différents et parfois partiels. Les 95 fichiers d'extraction ne sont pas assimilés à 95 sources intégrées, et les 139 enregistrements du catalogue ne constituent pas un dénominateur de couverture scientifique.
