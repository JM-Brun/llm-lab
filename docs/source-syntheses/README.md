# Dossiers de synthèse des sources

Ce répertoire contient des comparaisons concises et durables de plusieurs sources qui contribuent à une même question d'apprentissage.

Créer un dossier lorsque les sources apportent des angles explicatifs complémentaires, des exemples ou séquences pédagogiques matériellement différents, des affirmations contradictoires, ou lorsqu'un sujet nécessite une synthèse suivie. Ne pas créer un dossier pour chaque source ni pour chaque simple recouvrement.

Suivre la [méthode de synthèse des sources](../source-synthesis-method.md). Conserver l'identité des sources et les preuves atomiques dans data/sources.yml et data/extractions/ ; le présent répertoire documente la comparaison éditoriale et les décisions d'intégration. Il ne constitue ni une seconde bibliographie, ni un catalogue, ni un graphe de concepts, ni une copie du contenu des leçons.

## Dossiers

- [LLMs and compression algorithms](llms-and-compression-algorithms-2026-11.md) — analogie entre modélisation du langage et compression statistique ; synthèse critique, garde-fous théoriques et proposition d'expérience.
- [Compression des LLM](model-compression-2026-11.md) — pruning, quantification et distillation ; distinction entre taille du checkpoint, mémoire d'exécution et accélération réelle.
- [Deux sens de la compression appliqués aux LLM](compression-two-meanings-2026-11.md) — comparaison de la compression prédictive/statistique et de la compression du modèle, avec métriques distinctes et protocole expérimental commun.
- [Cross-entropy, compression et distillation](cross-entropy-compression-distillation-2026-11.md) — coût d'un code mal adapté, entraînement des LLM, justification de la log-loss, distillation et divergence KL.
- [Pilote #1739 — contributions intellectuelles de la leçon Entropie croisée](cross-entropy-intellectual-contributions-pilot-2026-11.md) — inventaire page-centré FR/EN, vérification des destinations réelles et séparation entre leçon fondamentale et approfondissement mathématique.
- [Pilote #1739 — contributions intellectuelles de la leçon Espace des embeddings](embedding-space-intellectual-contributions-pilot-2026-11.md) — audit de la valeur distinctive, correction de l'invariance par renumérotation cohérente des IDs et vérification de l'alignement purpose–leçon–Practice.
- [Audit #1739 — leçons de représentation dans Understand](understand-representations-intellectual-contributions-audit-2026-11.md) — audit page par page de l'encodage positionnel et des représentations contextualisées, avec provenance, décisions de placement et limites de preuve.
- [Encodage positionnel — synthèse multi-source](positional-encoding-source-synthesis-2026-11-26.md) — comparaison des mécanismes absolus et relatifs, de leurs points d'insertion computationnels, de RoPE, du masque causal et de NoPE ; AiEdge reste une source partiellement inspectée.
- [Audit #1739 — génération, scoring et apprentissage](understand-generation-scoring-training-contributions-audit-2026-11.md) — contributions distinctives des trois usages de la distribution prédictive, des préfixes de référence, des masques et de la mise à jour des paramètres.
- [Audit #1739 — apprentissage en contexte et ingénierie du contexte](understand-context-use-intellectual-contributions-audit-2026-11.md) — distinction entre ICL et conception système, trois niveaux de contexte, généralisation, provenance et sécurité.
- [Audit #1739 — panorama et entrée texte](understand-overview-text-input-intellectual-contributions-audit-2026-11.md) — modèle mental global, trois usages de la prédiction, contrat tokenizer–poids et limites du comptage de tokens.
- [Matrice consolidée #1739 — parcours Understand](understand-route-intellectual-contributions-index-2026-11.md) — couverture page par page des leçons canoniques, preuves, contrat de modélisation et validations restantes.
- [Théorie de l'information et LLM](information-theory-and-llms-2026-11.md) — entropie, cross-entropy, attention/MI, Landauer, compression et V-information.
- [Compression, information et efficacité de l'inférence](compression-intelligence-and-inference-efficiency-2026-11.md) — MDL en deux parties, prédiction séquentielle, coût de mise à jour du modèle et cadres agentifs (AIXI/active inference), avec expérience contrôlée forward/reverse.
- [Compression et intelligence — synthèse transversale](compression-intelligence-cross-source-2026-11.md) — comparaison des sources sur compression prédictive, MDL, représentations, généralisation, adaptation et action ; distingue résultats établis, hypothèses et décisions pédagogiques.
- [Complexité de Kolmogorov, prédiction universelle et AIXI](kolmogorov-aixi-computability-2026-11.md) — distinction entre K, semi-mesure de Solomonoff, décision active, limites de calculabilité d'AIXI et construction AIXI(t,l), à partir des sources primaires.
- [Pilote pédagogique — attention à produit scalaire](scaled-dot-product-attention-learning-page-pilot-2026-11.md) — deuxième test du workflow de production sur une page mathématique et computationnelle, avec distinction des axes, des intermédiaires et des ressources Practice.
- [Pilote source-to-code — Transformer Block Walkthrough](transformer-block-walkthrough-source-audit-2026-11.md) — troisième archétype, centré sur la traçabilité entre publications, implémentation NumPy et tests ; reconnaissance initiale, ingestion des six sources encore ouverte.

## Structure suggérée

1. **Question et périmètre** — pages canoniques, prérequis et position dans le parcours.
2. **Couverture actuelle** — ce que la leçon explique déjà, avec les sections exactes.
3. **Carte des contributions** — source, identifiant d'extraction, angle explicatif, forme pédagogique, valeur distinctive, limites et qualité des preuves.
4. **Synthèse** — perspectives complémentaires, convergences, désaccords et dépendances.
5. **Décisions d'intégration** — socle, approfondissement optionnel, études de cas, expériences, références ou liens ; éléments différés/rejetés et raisons.
6. **Lacunes et suites** — affirmations non résolues, perspectives manquantes, vérifications de provenance/droits et déclencheurs de révision.

Préférer les liens vers les extractions et sections de pages aux duplications de texte. Mettre à jour le dossier lorsque les évaluations de sources ou les intégrations publiées changent.

## Fiche de révision et expérience

- [Fiche de révision bilingue sur la compression](../../site/fr/compression-revision.qmd) — carte mentale, formules, distinctions et auto-évaluation.
- [Expérience de codage prédictif exact](../../experiments/predictive-compression/README.fr.md) — codage arithmétique rationnel, comparaison à une référence uniforme et reconstruction sans perte sur un alphabet synthétique.
- [Expérience entropie / zlib](../../experiments/sequence-compression/README.fr.md) — comparaison reproductible de l'entropie marginale, de l'entropie conditionnelle et de la taille réelle d'un flux compressé.

## Transfer validation

The tokenization/embeddings collection includes a retrospective assessment of whether the Q/K/V-calibrated source-to-knowledge method transfers to a heterogeneous source family: [method transfer validation](tokenization-embeddings-method-transfer-validation-2026-11.md). This is a method assessment, not another source catalogue or a replacement for the collection dossier.
