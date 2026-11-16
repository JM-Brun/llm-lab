# Dossiers de synthèse des sources

Ce répertoire contient des comparaisons concises et durables de plusieurs sources qui contribuent à une même question d'apprentissage.

Créer un dossier lorsque les sources apportent des angles explicatifs complémentaires, des exemples ou séquences pédagogiques matériellement différents, des affirmations contradictoires, ou lorsqu'un sujet nécessite une synthèse suivie. Ne pas créer un dossier pour chaque source ni pour chaque simple recouvrement.

Suivre la [méthode de synthèse des sources](../source-synthesis-method.md). Conserver l'identité des sources et les preuves atomiques dans data/sources.yml et data/extractions/ ; le présent répertoire documente la comparaison éditoriale et les décisions d'intégration. Il ne constitue ni une seconde bibliographie, ni un catalogue, ni un graphe de concepts, ni une copie du contenu des leçons.

## Dossiers

- [LLMs and compression algorithms](llms-and-compression-algorithms-2026-11.md) — analogie entre modélisation du langage et compression statistique ; synthèse critique, garde-fous théoriques et proposition d'expérience.
- [Compression des LLM](model-compression-2026-11.md) — pruning, quantification et distillation ; distinction entre taille du checkpoint, mémoire d'exécution et accélération réelle.
- [Deux sens de la compression appliqués aux LLM](compression-two-meanings-2026-11.md) — comparaison de la compression prédictive/statistique et de la compression du modèle, avec métriques distinctes et protocole expérimental commun.\n- [Théorie de l'information et LLM](information-theory-and-llms-2026-11.md) — entropie, cross-entropy, attention/MI, Landauer, compression et V-information.

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

## Transfer validation

The tokenization/embeddings collection includes a retrospective assessment of whether the Q/K/V-calibrated source-to-knowledge method transfers to a heterogeneous source family: [method transfer validation](tokenization-embeddings-method-transfer-validation-2026-11.md). This is a method assessment, not another source catalogue or a replacement for the collection dossier.
