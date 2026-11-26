# Modèles pédagogiques et dossiers de sources — portes 01 à 03

**Édition :** calendrier scientifique 2026  
**État :** modèle de travail pour les trois premières portes  
**Règle :** ce document décrit les modèles des pages et les reconstructions des ressources déjà ingérées. Il ne constitue ni une nouvelle ontologie parallèle ni un nouveau parcours obligatoire.

## Contrat commun

Chaque porte possède quatre objets distincts :

1. **Modèle de la page** : question, intention, unités de connaissance, progression argumentative, résultat attendu et frontières.
2. **Modèles des sources** : reconstruction de l'argument de chaque ressource, avec son niveau de complétude et ses limites d'inspection.
3. **Comparaison page–sources** : apports repris, apports complémentaires, divergences, éléments volontairement écartés et lacunes.
4. **Suivi** : une issue ouverte portant les défauts observés, les tâches ordonnées et la route de validation.

Le modèle de la page est une représentation éditoriale dérivée de son contenu ; il ne doit pas être présenté comme un modèle formel écrit par l'auteur de la ressource. Les modèles sources restent ceux des extractions canoniques `data/extractions/<source-id>.yml`. Les résumés ci-dessous sont des vues de synthèse, pas des copies des extractions.

Les exercices, questions de compréhension, calculs à réaliser et expériences guidées restent dans **S'exercer et expérimenter**. Une page du calendrier peut contenir un exemple démonstratif travaillé et une seule invitation discrète vers la page de pratique ; elle ne doit pas héberger une banque d'exercices.

---

# Porte 01 — Pourquoi le mot « je » revient-il si souvent ?

- **Page FR :** `site/fr/advent-calendar-story-day-01.qmd`
- **Page EN :** `site/en/advent-calendar-story-day-01.qmd`
- **Issue :** [#1653](https://github.com/JM-Brun/llm-lab/issues/1653)
- **Pratique :** [exercices Zipf](https://jm-brun.github.io/llm-lab/fr/exercises/zipf-law.html)
- **Dossier source :** [day-01-source-dossier.md](day-01-source-dossier.md)

## 1. Modèle conceptuel et progression de la page

**Question directrice.** Pourquoi certaines formes lexicales apparaissent-elles beaucoup plus souvent que d'autres, et que permet réellement de conclure une distribution rang–fréquence ?

**Intention pédagogique.** Partir d'un texte concret pour construire une description statistique de l'inégalité des fréquences, puis confronter cette description à la littérature et en borner les interprétations. Le texte de démonstration sert d'accroche et de corpus jouet ; il n'est pas un échantillon représentatif.

| Étape | Idées / notions | Fonction dans le raisonnement |
|---|---|---|
| 1. Accroche empirique | texte, corpus, question sur « je » / « I » | Donner une raison d'observer avant de définir |
| 2. Opérationnalisation | normalisation, type lexical, occurrence lexicale, token de tokenizer | Définir précisément l'unité comptée |
| 3. Distribution | fréquence, rang, classement, longue traîne, hapax | Transformer un texte en distribution rang–fréquence |
| 4. Modèle | loi de Zipf, (f(r) \approx C/r^\alpha) | Décrire la décroissance sans la déclarer exacte |
| 5. Paramètres | échelle (C), exposant \(\alpha\), extension Zipf–Mandelbrot \(\beta\) | Lire l'effet de chaque paramètre sur la courbe |
| 6. Lecture statistique | axes log–log, pente, résidus, estimation, erreur de rang | Distinguer apparence graphique et preuve statistique |
| 7. Confrontation | corpus réels, variation interlinguistique, unités et genres | Montrer la portée et la dépendance au corpus |
| 8. Lien LLM | fréquence lexicale marginale, fréquence après tokenisation, exposition d'entraînement, probabilité conditionnelle | Relier prudemment les fréquences aux données d'apprentissage |
| 9. Limites et retour | explications proposées, diversité lexicale, causalité, représentativité | Répondre à la question initiale sans surinterpréter |

**Relations principales :**

- un corpus et une convention de segmentation déterminent les occurrences observées ;
- les occurrences déterminent les fréquences ; le tri des fréquences détermine les rangs ;
- le modèle de Zipf décrit approximativement la relation entre rang et fréquence ;
- Zipf–Mandelbrot ajoute un décalage des rangs, sans être automatiquement un meilleur modèle ;
- la fréquence marginale d'une unité dans un corpus n'est pas la probabilité conditionnelle du prochain token calculée par un LLM ;
- le tokenizer transforme les unités textuelles en unités de modèle : les deux distributions ne sont donc pas interchangeables.

**Résultat attendu.** Le lecteur sait lire une distribution rang–fréquence, expliquer ce que représentent ses paramètres, identifier les biais d'estimation et formuler une connexion LLM qui ne confond pas statistique de corpus et mécanisme prédictif.

**Frontières éditoriales.** Les comparaisons contrôlées de corpus, l'estimation, les rééchantillonnages et les analyses de discours sont de la pratique. Les développements autonomes sur Zipf–Mandelbrot, Heaps, hapax et diversité lexicale peuvent devenir des approfondissements facultatifs. Ne pas insérer Zipf dans le graphe computationnel du Transformer.

## 2. Ressources ingérées et leur modèle

| Ressource | Modèle reconstruit / contribution propre | État d'inspection connu |
|---|---|---|
| Piantadosi (2014), [critical review](https://doi.org/10.3758/S13423-014-0585-6) — `piantadosi-zipf-word-frequency-2014` | Revue critique : relation rang–fréquence, distributions plus complexes que la loi simple, corrélation des erreurs lorsque rang et fréquence sont estimés sur le même échantillon, intérêt des découpages indépendants. | Texte inspecté de façon ciblée ; figures originales, code et données non inspectés. |
| Lestrade (2017), [Unzipping Zipf's law](https://doi.org/10.1371/journal.pone.0181987) — `lestrade-unzipping-zipfs-law-2017` | Proposition d'un mécanisme combinant classes syntaxiques et spécificité/réutilisabilité sémantique ; une hypothèse explicative parmi d'autres, non un consensus. | Texte ciblé ; figures et suppléments non inspectés intégralement, code non exécuté. |
| Pilgrim & Hills (2021), [Bias in Zipf's law estimators](https://doi.org/10.1038/s41598-021-96214-w) — `pilgrim-hills-bias-zipf-estimators-2021` | Problème d'estimation des rangs empiriques, biais des estimateurs et difficulté de la queue rare ; complète la critique méthodologique de Piantadosi. | Article et certaines figures inspectés ; code, données et supplément non audités/exécutés. |
| Linders & Louwerse (2023) — `linders-louwerse-zipf-spoken-dialog-2023` | Étend l'objet d'étude au dialogue oral et à plusieurs unités linguistiques ; évite de réduire toute régularité de fréquence au seul mot écrit. | Source recensée dans la collection ; couverture détaillée à reprendre dans le dossier avant toute affirmation plus fine. |
| Zipf (1949), [Human Behavior and the Principle of Least Effort](https://archive.org/details/humanbehaviorpri00zipf) | Source historique et cadre du principe de moindre effort ; ne fournit pas à lui seul une validation statistique contemporaine ni une explication causale universelle. | Référence historique ; inspection et droits des éventuels visuels à vérifier. |

## 3. Comparaison entre les ressources et la page

- **Socle repris :** Piantadosi fournit la formulation prudente et les pièges statistiques ; Pilgrim & Hills renforcent la critique des estimateurs ; Lestrade apporte une hypothèse explicative clairement étiquetée comme proposition.
- **Complémentarité :** Linders & Louwerse élargissent l'objet empirique au dialogue oral ; Zipf donne le contexte historique.
- **Choix éditorial de la page :** conserver une progression locale allant du texte de démonstration vers une loi statistique, plutôt qu'une revue de littérature. Le petit corpus motive le raisonnement mais ne valide pas Zipf.
- **Non-transfert :** ne pas importer dans la leçon les analyses d'estimation, bootstrap, corpus politiques ou linguistique quantitative avancée ; elles relèvent des exercices/labos.
- **Point de vigilance central :** une distribution de fréquences marginales n'est ni le softmax du modèle ni sa distribution conditionnelle du prochain token.

## 4. Route de progression

1. Terminer les corrections de fond et de visualisation déjà listées dans #1653.
2. Faire vérifier les comptes, les paramètres, les résidus et la distinction marginal/conditionnel dans les deux langues.
3. Faire une relecture non spécialiste réelle et consigner les incompréhensions, sans assimiler CI et acceptation pédagogique.
4. Créer les approfondissements seulement si une question autonome, des sources suffisantes et un contenu non redondant sont établis.
5. Garder les expériences quantitatives dans la page Practice dédiée et le laboratoire suivi séparément.

---

# Porte 02 — Combien de bits contient la surprise d'un événement ?

- **Page FR :** `site/fr/surprisal-information-content.qmd`
- **Page EN :** `site/en/surprisal-information-content.qmd`
- **Issue :** [#1666](https://github.com/JM-Brun/llm-lab/issues/1666)
- **Pratique :** [expérience de théorie de l'information](https://jm-brun.github.io/llm-lab/fr/experience-information-theory.html)

## 1. Modèle conceptuel et progression de la page

**Question directrice.** Comment quantifier la surprise d'un token observé, et pourquoi cette quantité diffère-t-elle de l'incertitude d'une distribution avant observation ?

**Intention pédagogique.** Faire calculer une quantité à partir d'une probabilité prédictive explicite, puis distinguer l'information d'une issue observée de l'espérance de cette information.

| Étape | Idées / notions | Fonction dans le raisonnement |
|---|---|---|
| 1. Situation prédictive | contexte (c), candidats, distribution (p(\cdot\mid c)) | Définir ce que le modèle croit possible avant l'observation |
| 2. Issue observée | cible (x), probabilité attribuée (p(x\mid c)) | Séparer la distribution de l'événement effectivement réalisé |
| 3. Information propre | (I(x\mid c)=-\log_b p(x\mid c)) | Quantifier le surprisal et introduire bits/nats |
| 4. Propriétés | monotonie, non-négativité, additivité | Justifier le logarithme à partir de ses propriétés |
| 5. Dépendance | probabilité conditionnelle, règle de chaîne | Passer d'événements indépendants à des séquences dépendantes |
| 6. Incertitude avant observation | entropie comme espérance du surprisal | Distinguer valeur observée et moyenne prédictive |
| 7. Séquences et LLM | somme des log-probabilités conditionnelles, score/NLL | Relier la théorie au score d'une séquence sans confondre les quantités |
| 8. Limites | dépendance au modèle/distribution, zéro-probabilité, sémantique | Éviter d'interpréter la surprise comme émotion, vérité ou importance |

**Relations principales :**

- le contexte détermine la distribution prédictive ;
- l'observation sélectionne une issue et sa probabilité ;
- le surprisal est une fonction de cette probabilité ;
- l'entropie est l'espérance du surprisal sur toutes les issues possibles ;
- la règle de chaîne décompose la probabilité d'une séquence en probabilités conditionnelles ;
- la somme des surprisals conditionnels donne l'information propre de la séquence ; sous un modèle de langage, elle correspond au score négatif associé aux tokens observés.

**Résultat attendu.** Le lecteur peut calculer le surprisal d'une cible, calculer/interpréter l'entropie de la distribution, expliquer leur différence et relier la règle de chaîne au score d'une séquence.

**Frontières éditoriales.** Ne pas confondre surprisal, entropie, entropie croisée, KL et loss d'entraînement. Ces notions sont liées mais ne sont pas synonymes. La page doit rester centrée sur surprisal observé et incertitude prédictive ; les dérivations avancées de codage, cross-entropy/KL ou compression ont leurs pages dédiées.

## 2. Ressources ingérées et leur modèle

| Ressource | Modèle reconstruit / contribution propre | État d'inspection connu |
|---|---|---|
| Shannon (1948), [A Mathematical Theory of Communication](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x) — `shannon-mathematical-theory-communication-1948` | Source primaire : entropie d'une source discrète et entropie conditionnelle ; théorème de codage sans bruit et limite asymptotique de débit. Les hypothèses de source et de codage doivent rester explicites. | Extraction atomique de définitions et théorème enregistrée ; conserver les hypothèses et ne pas assimiler entropie, cross-entropy et longueur finie exacte. |
| 3Blue1Brown, *Reinventing entropy* (part 1) — `3blue1brown-reinventing-entropy-compression-intelligence-part-1-2026` | Progression visuelle reconstruite : source de messages → code préfixe/arbre binaire → longueur idéale → information et entropie → taux d'entropie. | Transcription horodatée complète inspectée ; pas d'inspection audiovisuelle image par image. |
| 3Blue1Brown, *Cross entropy and compression* (part 2) — `3blue1brown-cross-entropy-compression-intelligence-part-2-2026` | Distingue distribution du code et distribution des données ; construit la cross-entropy, le coût excédentaire/KL, la log-loss de pré-entraînement et la distillation teacher–student. | Captions et sections de scripts Manim inspectées ; pas de reproduction indépendante ni d'inspection audiovisuelle complète. |
| Wayland & Zhang (2026), *Information Theory for LLMs* — `wayland-zhang-information-theory-llm-2026` | Vue large : information propre, entropie, cross-entropy/KL, attention/information mutuelle, Landauer, compression et V-information. Utile pour cartographier les prolongements, pas comme source unique de la définition de base. | Corps d'article complet disponible dans la récupération indexée ; inspection DOM, médias intégrés, notebook et validation externe non établis. |

## 3. Comparaison entre les ressources et la page

- **Socle repris :** Shannon fonde les définitions et propriétés ; 3Blue1Brown part 1 donne une progression visuelle vers l'entropie ; la page resserre l'entrée sur le surprisal d'une issue.
- **Complémentarité :** la partie 2 de 3Blue1Brown éclaire la frontière vers cross-entropy, KL, log-loss et distillation ; Wayland & Zhang cartographient les extensions informationnelles propres aux LLM.
- **Choix éditorial de la page :** l'exemple Paris/Lyon rend visible la différence entre cible observée (3,32 bits) et entropie prédictive (environ 1,02 bit) avant d'introduire la règle de chaîne.
- **À ne pas importer dans le récit principal :** développement complet de la compression optimale, KL, V-information, information mutuelle, Landauer ou distillation. Ces sujets sont des branches facultatives.
- **Lacune à vérifier :** la page doit s'assurer que l'entropie est bien introduite comme espérance, avec le même support et la même distribution que le calcul du surprisal ; l'exemple ne doit pas laisser croire qu'une seule cible suffit à calculer l'entropie.

## 4. Route de progression

1. Valider les calculs et unités, notamment l'exemple numérique et l'entropie de la distribution.
2. Revoir le passage surprisal → entropie → règle de chaîne, en explicitant à chaque fois la variable aléatoire et la distribution.
3. Vérifier les liens vers entropie, vraisemblance et cross-entropy pour éviter les répétitions.
4. Contrôler le rendu de la figure, les équations, les liens et l'équivalence FR/EN.
5. Obtenir une relecture non spécialiste ; garder les calculs supplémentaires dans la page d'expérience.

---

# Porte 03 — Le tokenizer, ingénieur de compression

- **Page FR actuellement référencée :** `site/fr/tokenizer-design-evaluation.qmd`
- **Page EN :** `site/en/tokenizer-design-evaluation.qmd`
- **Issue :** [#1667](https://github.com/JM-Brun/llm-lab/issues/1667)
- **Pratique / expérience :** à rattacher à une page dédiée existante ou à créer après audit ; aucune banque d'exercices ne doit être ajoutée à la page Deepen.

## 1. Modèle conceptuel et progression de la page

**Question directrice.** Quel compromis existe entre taille du vocabulaire et longueur des séquences, et dans quelles conditions peut-on parler de compression ?

**Intention pédagogique.** Partir d'un même texte et d'un même budget de données, comparer des segmentations reproductibles, puis montrer pourquoi la longueur en tokens est un indicateur utile mais insuffisant pour choisir un tokenizer.

| Étape | Idées / notions | Fonction dans le raisonnement |
|---|---|---|
| 1. Problème concret | texte, budget de contexte, coût de représentation | Faire apparaître le compromis à mesurer |
| 2. Représentation | Unicode, points de code, UTF-8, octets, alphabet de base | Comprendre ce que le tokenizer reçoit et les unités possibles |
| 3. Pipeline | normalisation, pré-tokenisation, modèle, post-traitement | Rendre visibles les décisions qui bornent la segmentation |
| 4. Construction | vocabulaire, fréquence de paires, fusions BPE, alternatives WordPiece/Unigram | Expliquer les mécanismes seulement lorsqu'ils éclairent le compromis |
| 5. Encodage | segmentation, séquence d'IDs, décodage | Relier le vocabulaire appris à la représentation du texte |
| 6. Mesure intrinsèque | nombre de tokens, taux de compression, taille de vocabulaire | Définir les unités de comparaison et les métriques |
| 7. Coûts système | matrice d'embedding/output, mémoire, calcul, budget de contexte | Montrer que moins de tokens n'est pas un gain gratuit |
| 8. Évaluation extrinsèque | qualité en aval, tâche, taille de modèle, budget d'entraînement | Séparer compression et performance |
| 9. Dimension multilingue | langue, script, normalisation, équité, coût par langue | Éviter une moyenne globale qui masque des écarts |
| 10. Décision | protocole contrôlé, limites et reproductibilité | Conclure qu'il n'existe pas de meilleur tokenizer indépendamment de l'objectif |

**Relations principales :**

- les choix de normalisation et de pré-tokenisation contraignent les unités disponibles ;
- l'algorithme d'apprentissage construit un vocabulaire et des règles/paramètres de segmentation ;
- l'encodage transforme un texte en séquence d'IDs ;
- la taille du vocabulaire et la longueur de séquence ont des effets distincts sur les coûts ;
- compression, mémoire, calcul et qualité en aval sont des axes de mesure distincts ;
- les résultats dépendent du corpus, de la langue, du tokenizer, du modèle, du budget et de la tâche.

**Résultat attendu.** Le lecteur peut concevoir une comparaison contrôlée de tokenizers, expliquer les différences de pipeline, mesurer la longueur et interpréter les compromis sans assimiler compression et qualité.

**Décision de réutilisation à prendre.** La page actuellement référencée est une leçon Deepen avancée et dense, centrée sur les mécanismes WordPiece/Unigramme, budgets, métriques et résultats. Son périmètre est pertinent, mais son architecture n'est pas encore une histoire de calendrier. #1667 doit décider si l'on peut la réorganiser sans perdre son contenu technique, ou s'il faut conserver cette page comme approfondissement avancé et faire de la porte 03 une leçon narrative canonique distincte, avec une frontière explicite et sans duplication.

## 2. Ressources ingérées et leur modèle

| Ressource | Modèle reconstruit / contribution propre | État d'inspection connu |
|---|---|---|
| Gage (1994), *A New Algorithm for Data Compression* — `philip-gage-byte-pair-compression-1994` | Algorithme historique de substitution par paires d'octets fréquentes, avec enregistrement des substitutions pour reconstruire la séquence. Source de l'idée historique BPE, mais pas une spécification de tokenizer subword moderne. | Extraction algorithmique ; distinguer compression byte-level et tokenisation moderne. |
| Karpathy, *Let's build the GPT Tokenizer* — `andrej-karpathy-gpt-tokenizer-video` | Progression pédagogique : Unicode → UTF-8 → octets → vocabulaire de base byte-level → comptage/fusions BPE → ordre des merges → encodage/décodage et conventions de tokenizer. | Transcription et chapitres partiellement inspectés ; visuels non examinés systématiquement, date/révision et liens incomplets. |
| Goldman et al. (2024), [Unpacking Tokenization](https://aclanthology.org/2024.findings-acl.134/) — `goldman-unpacking-tokenization-2024` | Évalue le lien entre support d'entraînement BPE, compression intrinsèque et performances aval ; observe des corrélations dans des conditions spécifiques, pas une loi universelle. | PDF et résultats principaux inspectés ; code, artefacts, données et reproduction non audités. |
| Schmidt et al. (2024), [Tokenization Is More Than Compression](https://aclanthology.org/2024.emnlp-main.40/) — `schmidt-tokenization-more-than-compression-2024` | Décompose l'analyse en pré-tokenisation, construction du vocabulaire et segmentation ; PathPiece traite la segmentation minimale pour vocabulaire fixe. Met en garde contre l'usage du seul nombre de tokens comme proxy de qualité. | PDF, figures principales et tableaux sélectionnés inspectés ; code, vocabulaires et données non audités/exécutés. |
| Ali et al. (2024), *The Impact of Tokenizer Choice on Language Model Training* — `ali-tokenizer-choice-llm-training-2024` | Compare critères intrinsèques/extrinsèques et coûts de calcul dans un protocole de choix de tokenizer ; apporte un cadre d'évaluation plus large que la compression seule. | PDF et tableaux/figure de calcul inspectés ; code, artefacts et données non audités ; variance multi-seed non établie. |
| Arnett et al. (2025), *Explaining and Mitigating Crosslingual Tokenizer Inequities* — `arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025` | Analyse les écarts d'efficacité de tokenisation entre langues et les effets de vocabulaire/pré-tokenisation ; apporte une dimension d'équité et de comparaison linguistique contrôlée. | PDF et certaines figures/annexes inspectés ; artefacts et données non exécutés, généralisation à ne pas extrapoler sans réserve. |
| Wegmann et al. (2025), *Tokenization and Language Variation* — `wegmann-tokenization-language-variation-2025` | Montre que l'effet de variation linguistique dépend de la tâche : certaines tâches doivent être robustes aux variations, d'autres doivent les préserver. Complément pour la définition des objectifs d'évaluation. | PDF et résultats principaux inspectés ; pas de reproduction ni audit complet du code/dataset. |
| Hugging Face Tokenizers, [pipeline](https://huggingface.co/docs/tokenizers/python/latest/pipeline.html), [BPE](https://huggingface.co/docs/tokenizers/python/latest/api/reference.html#models.BPE), [WordPiece](https://huggingface.co/docs/tokenizers/python/latest/api/reference.html#models.WordPiece), [Unigram](https://huggingface.co/docs/tokenizers/python/latest/api/reference.html#models.Unigram) | Modèle d'implémentation : normalisation → pré-tokenisation → modèle → post-traitement, avec comportements spécifiques aux implémentations. Sert à décrire les responsabilités du pipeline, pas une règle universelle. | Documentation inspectée dans l'audit ciblé ; les implémentations et versions doivent être fixées dans tout benchmark. |

## 3. Comparaison entre les ressources et la page

- **Socle mécanistique :** Gage documente l'origine byte-pair substitution ; Karpathy fournit une reconstruction pédagogique de BPE byte-level ; Hugging Face décrit un pipeline implémentable.
- **Socle expérimental :** Goldman teste une relation compression/performance dans des conditions déterminées ; Schmidt montre pourquoi le nombre de tokens seul ne suffit pas ; Ali élargit les critères aux coûts et résultats ; Arnett et Wegmann apportent des objectifs multilingues et dépendants des tâches.
- **Écart avec la page actuelle :** les sources soutiennent une histoire centrée sur un texte, des segmentations comparées et des critères de décision. La page existante présente aujourd'hui surtout une leçon avancée de conception/évaluation ; elle ne met pas encore assez en scène le problème concret et le même corpus passé dans plusieurs segmentations.
- **Risque de simplification :** « moins de tokens = meilleure compression = meilleur modèle » est faux comme conclusion générale. Les mesures et les résultats doivent garder leurs conditions expérimentales.
- **Lacune à traiter :** fixer une unité de référence, un corpus comparable, les versions et paramètres des tokenizers, les règles de normalisation, puis séparer longueur, taille de vocabulaire, coût système et qualité aval.

## 4. Route de progression

1. Auditer la page existante contre ce modèle et les pages canoniques de tokenisation de base ; établir une matrice de contenu à conserver/déplacer.
2. Prototyper une narration sur un même texte et plusieurs segmentations, avec un tableau mesuré et un visuel explicatif.
3. Prendre explicitement la décision de propriétaire : réorganiser la page existante ou la garder comme approfondissement avancé et créer une seule leçon narrative canonique.
4. Déplacer les détails algorithmiques qui interrompent le récit vers des approfondissements dédiés, sans perte d'information ni duplication.
5. Construire une expérience reproductible séparée ; documenter versions, normalisation, corpus, scripts/langues et limites.
6. Vérifier FR/EN, liens, accessibilité, rendu responsive et relecture non spécialiste.

---

## Relations entre les trois portes

Les portes sont indépendantes pour le lecteur et ne forment pas une chaîne de prérequis. Elles partagent néanmoins un thème de fond : la représentation statistique du langage.

- **Porte 01** observe la distribution des formes lexicales dans un corpus.
- **Porte 02** quantifie l'information associée à une issue selon une distribution probabiliste et distingue cette quantité de l'entropie.
- **Porte 03** étudie comment un système de tokenisation transforme le texte en unités discrètes et comment évaluer cette représentation.

Le lien conceptuel est donc une comparaison de niveaux, pas une dépendance directe : fréquence empirique des formes ≠ probabilité prédictive conditionnelle ; surprisal d'un token ≠ longueur en tokens ; compression d'une séquence tokenisée ≠ qualité du modèle.

Aucun de ces trois sujets ne doit être injecté artificiellement dans le forward pass du Transformer. Les relations sont conceptuelles et statistiques, non une succession d'opérations d'exécution.

## Contrôles transversaux avant clôture

- [ ] Les métamodèles restent synchronisés avec le contenu FR/EN et les pages canoniques réellement retenues.
- [ ] Chaque ressource citée existe dans le catalogue et son `source_id` correspond à une extraction vérifiable.
- [ ] La complétude d'une reconstruction et le niveau d'inspection de la source sont explicitement distingués.
- [ ] Chaque affirmation empirique reste dans le périmètre et les conditions de la source.
- [ ] Les pages du calendrier ne contiennent pas de banque d'exercices ; elles pointent vers Practice.
- [ ] Les branches d'approfondissement ne deviennent pas des prérequis cachés.
- [ ] Les validations techniques, visuelles et pédagogiques sont enregistrées séparément.
