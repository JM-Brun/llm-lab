# Loi de Zipf — collection de sources et extraction comparative

**Date de la passe :** 2026-11-24  
**Phase :** A — identification, inspection partielle et extraction atomique  
**Collection :** `zipf-law`  
**Dossier pédagogique existant :** [Day 01 — dossier de sources](../advent-calendar-pilots/day-01-source-dossier.md)

## 1. Point de départ : ne pas recréer la leçon

Le dépôt contient déjà une leçon bilingue publiée :

- `site/fr/advent-calendar-story-day-01.qmd`
- `site/en/advent-calendar-story-day-01.qmd`

et des pages de pratique distinctes :

- `site/fr/exercises/zipf-law.qmd`
- `site/en/exercises/zipf-law.qmd`

Les PR #1592, #1593 et #1594 ont établi cette structure et intégré la leçon dans les rubriques Deepen. La présente collection ne crée donc ni nouvelle leçon, ni nouvelle page d'exercices, ni nouveau nœud conceptuel. Elle documente les sources qui étayent ou peuvent enrichir le travail déjà publié.

**Question pédagogique centrale :** comment décrire la distribution très inégale des fréquences lexicales, comment évaluer cette description et que peut-on réellement en déduire ?

La leçon existante traite le cas lexical écrit, la relation rang–fréquence, l'échelle log-log, les biais de représentation et une conséquence limitée pour les corpus d'entraînement. La collection étend l'analyse vers les méthodes d'estimation, les mécanismes proposés et les autres unités de communication.

## 2. Inventaire des sources enregistrées

Les sources sont inscrites dans `data/sources.yml`, leurs contributions atomiques dans `data/extractions/<source-id>.yml`. Les statuts distinguent inspection, extraction et intégration : une source partiellement inspectée peut fournir des éléments extraits, mais cela ne rend pas sa numérisation complète.

| Source | Rôle dans la collection | Inspection |
|---|---|---|
| Piantadosi (2014) | Revue critique centrale : formule, résidus, erreur de rang et limites des explications | Partielle ; texte PDF ciblé, figures non inspectées |
| Lestrade (2017) | Modèle syntaxe–sémantique proposé | Partielle ; texte HTML ciblé, suppléments/code non inspectés |
| Pilgrim & Hills (2021) | Biais des estimateurs et distinction rang empirique / rang probabiliste | Partielle ; texte ciblé, code et supplément non inspectés |
| Linders & Louwerse (2023) | Extension au dialogue oral et à plusieurs unités linguistiques | Partielle ; méthodes et résultats principaux ciblés, données/supplément non inspectés |
| Roda (2024), Wolfram Demonstrations | Inspiration pour un laboratoire interactif de fréquences lexicales | Partielle ; page descriptive seulement, notebook non exécuté |
| Zipf (1949), *Human Behavior and the Principle of Least Effort* | Référence historique | Découverte bibliographique seulement ; contenu du livre non inspecté |

### Statuts de source

- **5 sources partiellement inspectées et extraites** : Piantadosi, Lestrade, Pilgrim & Hills, Linders & Louwerse, Wolfram Demonstrations.
- **1 référence historique découverte** : Zipf (1949). Les métadonnées et le sommaire bibliographique ont été vérifiés, pas le texte.
- **Aucune source n'est déclarée entièrement scannée.**
- **Aucun fichier source, figure, notebook ou jeu de données externe n'est recopié dans le dépôt.**

## 3. Ce que chaque source apporte réellement

### 3.1 Piantadosi (2014) — le socle critique

Steven T. Piantadosi, “Zipf’s word frequency law in natural language: A critical review and future directions”, *Psychonomic Bulletin & Review*, 21, 1112–1130. [DOI](https://doi.org/10.3758/s13423-014-0585-6) · [PDF auteur](https://colala.berkeley.edu/papers/piantadosi2014zipfs.pdf).

La revue formalise la relation rang–fréquence et sa variante de Zipf–Mandelbrot, mais insiste surtout sur la complexité qui reste visible au-delà de l'ajustement. Son apport méthodologique le plus important pour la pédagogie est l'erreur de mesure corrélée : lorsque rang et fréquence sont estimés sur le même échantillon, les deux coordonnées d'un point ne sont pas indépendantes. La revue propose une séparation des échantillons pour réduire ce problème et montre une structure résiduelle au-delà de la courbe ajustée.

Elle souligne également que plusieurs familles de modèles peuvent produire une régularité proche de Zipf. Reproduire la courbe ne suffit donc pas à valider un mécanisme psychologique ou linguistique : une explication doit aussi rendre compte d'autres phénomènes et produire des prédictions indépendantes.

**Contribution à préserver :** expliquer le mécanisme statistique qui rend un graphique rang–fréquence potentiellement trompeur, puis distinguer qualité d'ajustement et explication causale.

**Limite d'inspection :** texte PDF et passages empiriques ciblés consultés ; les figures originales n'ont pas été récupérées comme fichiers ni visuellement auditées.

### 3.2 Lestrade (2017) — une hypothèse mécaniste concrète

Sander Lestrade, “Unzipping Zipf’s law”, *PLOS ONE* 12(8), e0181987. [DOI](https://doi.org/10.1371/journal.pone.0181987) · [Article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0181987).

L'article propose une interaction entre :
- **syntaxe** : les classes grammaticales ont des tailles lexicales très différentes, alors que leur fréquence agrégée peut être comparable ;
- **sémantique** : un terme doit être assez spécifique pour distinguer un référent, mais assez général pour rester réutilisable.

Dans le modèle étudié, la taille des classes syntaxiques seule ne suffit pas ; le volet sémantique seul ne suffit pas non plus. Leur interaction produit une distribution proche de Zipf. L'auteur rappelle néanmoins que les origines de la loi restent difficiles à établir.

**Contribution à préserver :** un cas d'étude qui transforme une régularité descriptive en hypothèse computationnelle testable, sans la présenter comme consensus.

**Limite d'inspection :** les sections centrales, la conclusion et l'inventaire des suppléments ont été examinés ; scripts R, données, modèles alternatifs, dérivation supplémentaire et figures originales restent à inspecter.

### 3.3 Pilgrim & Hills (2021) — pourquoi l'estimation de l'exposant est délicate

Charlie Pilgrim & Thomas T. Hills, “Bias in Zipf’s law estimators”, *Scientific Reports* 11, 17309. [DOI](https://doi.org/10.1038/s41598-021-96214-w) · [Article](https://www.nature.com/articles/s41598-021-96214-w).

Cette source affine la mise en garde de Piantadosi. Elle distingue le **rang empirique** obtenu en triant les fréquences observées du **rang probabiliste** associé aux probabilités sous-jacentes inconnues. Dans un échantillon fini, ces rangs peuvent différer. Les estimateurs de maximum de vraisemblance usuels peuvent alors être biaisés, car leur hypothèse d'ordre a priori ne correspond pas au rang construit à partir des données.

Les auteurs étudient une vraisemblance tenant compte des permutations possibles, mais son calcul exact devient rapidement impraticable. L'approximate Bayesian computation réduit le biais sur des données synthétiques issues de lois idéalisées ; les résultats restent toutefois dépendants du modèle génératif supposé lorsqu'on traite des textes naturels.

**Contribution à préserver :** ne pas enseigner l'estimation de \(\alpha\) comme une simple régression linéaire sur un graphique log-log. Il faut distinguer bruit d'échantillonnage, incertitude sur les rangs, biais d'estimateur et inadéquation du modèle.

**Limite d'inspection :** sections méthodologiques et résultats principaux consultés ; le supplément et le dépôt de code lié n'ont pas été audités ou exécutés.

### 3.4 Linders & Louwerse (2023) — ne pas réduire le langage au texte écrit

Guido M. Linders & Max M. Louwerse, “Zipf’s law revisited: Spoken dialog, linguistic units, parameters, and the principle of least effort”, *Psychonomic Bulletin & Review*, 30, 77–101. [DOI](https://doi.org/10.3758/s13423-022-02142-9) · [Article](https://link.springer.com/article/10.3758/s13423-022-02142-9).

L'étude étend l'analyse à des dialogues oraux et à des unités autres que les mots isolés : bigrammes, unités syntaxiques, énoncés, actes de dialogue et comportements non verbaux. Elle rapporte des ajustements souvent bons, mais des exposants qui varient selon les unités et les corpus. Un \(R^2\) élevé ne signifie donc pas que le même exposant ou le même mécanisme est présent partout.

Les auteurs opérationnalisent aussi une hypothèse d'effort cognitif : une charge extralinguistique plus forte pourrait conduire les locuteurs à économiser leurs contributions linguistiques, ce qui se traduirait par un exposant plus élevé. Il s'agit d'une hypothèse étudiée dans des conditions déterminées, pas d'une loi universelle.

**Contribution à préserver :** rendre explicite que le résultat dépend de l'unité linguistique, du mode de communication et du protocole de corpus.

**Limite d'inspection :** principaux choix de corpus, d'échantillonnage, unités et résultats qualitatifs consultés ; les tableaux détaillés, le supplément et les données disponibles sur demande ne sont pas reproduits.

### 3.5 Roda (2024) — une inspiration pour l'expérimentation

Giovanna Roda, “Zipf’s Law for Natural Languages”, Wolfram Demonstrations Project. [Démonstration](https://demonstrations.wolfram.com/ZipfsLawForNaturalLanguages/).

La page décrit une exploration où l'on choisit un texte d'exemple, une borne de rang et un graphique log-log. Le survol des points permet de retrouver le terme et ses valeurs. C'est un bon modèle d'activité : relier les points d'une courbe aux mots réellement comptés.

**Contribution à préserver :** une expérience interactive centrée sur les données, en complément de la figure statique synthétique de la leçon.

**Limite d'inspection :** notebook et code non ouverts ni exécutés ; démonstration annoncée comme optimisée pour ordinateur ; licence affichée CC BY-NC-SA sans version établie. Ne pas recopier le notebook ou ses médias.

### 3.6 Zipf (1949) — source historique à examiner ultérieurement

George Kingsley Zipf, *Human Behavior and the Principle of Least Effort: An Introduction to Human Ecology*, Addison-Wesley Press, 1949. [Notice Google Books](https://books.google.com/books?id=1tx9AAAAIAAJ).

Les notices bibliographiques confirment l'édition de 1949 et un chapitre intitulé “On the Economy of Words”. Le texte du livre n'a pas été lu dans cette passe. Il ne faut donc pas lui attribuer ici une démonstration précise ni une interprétation détaillée du principe du moindre effort.

**Disposition actuelle :** `scan_status: discovered`, `integration_status: deferred` ; piste historique, pas source extraite. Les notices bibliographiques et le sommaire ne permettent pas d'attribuer un argument précis au livre. Une lecture ciblée du chapitre consacré aux mots est nécessaire avant toute intégration historique.

## 4. Comparaison transversale : les contributions complémentaires

Les sources ne sont pas interchangeables. Elles occupent des niveaux différents :

| Niveau de compréhension | Contribution | Source |
|---|---|---|
| Décrire | Relation rang–fréquence et variante de Mandelbrot | Piantadosi |
| Observer les limites | Résidus structurés et erreurs de coordonnées corrélées | Piantadosi |
| Estimer | Rang empirique différent du rang probabiliste ; biais des estimateurs | Pilgrim & Hills |
| Expliquer | Interaction proposée entre classes syntaxiques et spécificité sémantique | Lestrade |
| Généraliser avec prudence | Dialogue oral, unités multiples, variation de l'exposant | Linders & Louwerse |
| Expérimenter | Explorer un texte, ses fréquences et ses rangs | Wolfram Demonstrations |
| Historiser | Principe du moindre effort dans l'œuvre de Zipf | Zipf (à lire) |

### Convergences

- La relation rang–fréquence est une régularité descriptive utile, mais les distributions réelles sont plus complexes qu'une formule unique.
- L'unité observée et la procédure d'estimation influencent l'interprétation.
- Une courbe bien ajustée n'identifie pas, à elle seule, le mécanisme qui a produit les données.

### Différences à conserver

- Piantadosi critique les explications insuffisamment testées et montre des structures empiriques au-delà de la courbe.
- Lestrade propose un mécanisme syntaxe–sémantique particulier.
- Linders & Louwerse étudient une hypothèse cognitive dans le dialogue et sur plusieurs unités.
- Pilgrim & Hills traitent d'abord la validité statistique des estimateurs, pas de l'origine linguistique de la loi.

Ne pas fusionner ces propositions en une explication composite : elles ont des objets, des hypothèses et des statuts de preuve distincts.

## 5. Conséquences pédagogiques proposées pour la suite

Leçon actuelle : conserver la progression courte et la distinction entre fréquence lexicale et token de tokenizer. Elle n'a pas besoin d'absorber toute la théorie des mécanismes.

La suite devrait enrichir progressivement les pages d'exercices déjà créées :

1. **Comptage et rang** : reconstruire un classement à partir d'occurrences et expliciter les conventions de normalisation.
2. **Lecture log-log** : retrouver la pente et l'exposant, puis expliquer pourquoi la linéarité visuelle ne suffit pas.
3. **Erreur de rang** : simuler un échantillonnage où le rang empirique change d'un échantillon à l'autre.
4. **Modèle versus mécanisme** : distinguer la loi observée, le modèle ajusté et l'hypothèse causale.
5. **Transfert d'unité** : comparer mots, bigrammes ou tokens d'un tokenizer sans confondre les distributions.
6. **Comparaison de corpus** : interpréter séparément qualité d'ajustement et stabilité de l'exposant.

Pour un laboratoire reproductible, privilégier un notebook écrit dans le projet avec un corpus redistribuable et une politique de comptage documentée. La démonstration Wolfram est une référence d'interaction, pas une dépendance à intégrer.

**Candidat de corpus retenu pour le pilote : ELTeC (European Literary Text Collection).** Les collections [ELTeC-fra](https://github.com/COST-ELTeC/ELTeC-fra) et [ELTeC-eng](https://github.com/COST-ELTeC/ELTeC-eng) proposent chacune 100 romans européens, principalement publiés entre 1840 et 1920. Les deux dépôts annoncent les textes dans le domaine public. Attention à ne pas homogénéiser leurs mentions de droits : ELTeC-fra indique ne revendiquer aucun droit sur la composition du corpus, les métadonnées, la transcription ou l'encodage ; ELTeC-eng précise que son balisage textuel est sous CC BY 4.0. Les versions archivées sont identifiables par DOI : [ELTeC-fra v1.0.1](https://doi.org/10.5281/zenodo.4662433) et [ELTeC-eng v1.0.1](https://doi.org/10.5281/zenodo.4662490). Cette paire est préférable à un corpus non documenté ou à une collection dont la licence est NC pour un laboratoire susceptible d'être réutilisé hors du projet.

Ce choix reste un **corpus littéraire historique**, pas un échantillon représentatif du français ou de l'anglais contemporains. Le laboratoire devra donc :
- épingler les versions et les DOI, sélectionner explicitement les documents et conserver leurs métadonnées ;
- extraire le texte des éléments TEI sans compter les balises, notes éditoriales ou métadonnées comme des mots ;
- expliciter la normalisation (Unicode, casse, apostrophes, ponctuation, mots composés) et conserver une variante de comptage sensible à la casse pour mesurer son effet ;
- comparer les fréquences de formes lexicales et celles d'un tokenizer donné, sans assimiler les deux unités ;
- tracer la courbe rang–fréquence et son équivalent log-log, en affichant les comptes et les rangs plutôt qu'une droite ajustée seule ;
- séparer l'ajustement descriptif de l'estimation de l'exposant, puis mesurer la stabilité par rééchantillonnage de documents ;
- comparer les résultats français et anglais séparément avant toute interprétation interlinguistique.

Le premier jalon doit rester modeste : quelques romans par langue, un pipeline déterministe et des sorties vérifiables. L'extension aux 100 textes et l'analyse de robustesse viendront après validation du nettoyage et des conventions de comptage.

## 6. Position dans le modèle de connaissances

- **Domaine principal conservé :** `probabilistic-foundations-training`, cohérent avec le classement de la leçon Day 01.
- **Domaine secondaire :** `text-tokenization` lorsque la distinction entre formes lexicales et tokens de tokenizer est matériellement traitée.
- **Décision de Phase B :** deux concepts canoniques sont créés dans `data/concepts.yml` :
  - `word-frequency-distribution` — distribution empirique des occurrences de formes lexicales dans un corpus défini ;
  - `zipf-law` — approximation rang–fréquence appliquée à cette distribution.
- **Relations typées :**
  - `zipf-law` `approximates` `word-frequency-distribution` : la loi est une approximation empirique, pas une identité ni une explication générative ;
  - `word-frequency-distribution` `contrasts-with` `conditional-distribution` : fréquence marginale observée dans un corpus et probabilité conditionnelle du prochain token sont deux objets différents.
- Les deux concepts sont classés `supporting`, rattachés aux domaines probabiliste et texte/tokenisation, et reliés aux pages bilingues de leçon et d'exercices. Les sources et items extraits pointent désormais vers ces identifiants canoniques.
- Aucun concept distinct `frequency-rank` n'est créé : le rang est défini dans la notion de loi et les exercices, sans justifier ici une carte autonome.
- Ces relations appartiennent au graphe de connaissances (`data/concepts.yml`) : elles ne décrivent pas une dépendance de calcul et ne créent aucune arête dans le graphe computationnel canonique.
- Le parcours principal n'est pas réordonné : Zipf reste un approfondissement des propriétés statistiques des corpus, pas une étape du forward pass ou du calcul d'attention.
## 7. Travail restant — état au 2026-11-24

Le travail restant est séparé en trois niveaux : clôture technique de la PR, compléments d'inspection des sources, puis laboratoire expérimental. Les éléments reportés ne doivent pas être interprétés comme des lacunes bloquant la validité des contenus déjà intégrés.

### 7.1 Clôture de la PR #1601

- [x] Suite de tests CI : réussie sur le commit `7b01334d18bbca5f6b51498b2553915004186c1a`.
- [x] Contrôles de qualité Python et contrôles de domaine : réussis.
- [x] Rendu complet Quarto et audit navigateur : réussis.
- [x] Secret scanning : réussi.
- [x] Vérification des discussions de revue : aucune review ni thread de revue ouvert n'a été retourné lors du contrôle du 2026-11-24.
- [ ] **Synchroniser la branche avec `main` avant fusion.** Au contrôle du 2026-11-24, la branche était en avance de 32 commits et en retard d'un commit (`main` : `9c18169568b5b139963362e1656d8ae4f9877f47`, base commune : `64007c9b256ca5f4caac2cbfae0d59a280f86fb9`). GitHub signalait alors la PR comme non fusionnable. Intégrer le commit manquant de `main`, résoudre d'éventuels conflits sans écraser les changements de la PR, puis vérifier le diff final.
- [ ] Relancer et attendre les workflows sur le nouveau SHA après synchronisation. Les succès du SHA précédent ne valident pas un commit ultérieur.
- [ ] Vérifier une dernière fois le diff, l'état mergeable et les checks requis, puis fusionner la PR.

**Décision :** les validations automatiques du contenu actuel sont réussies ; la fusion reste suspendue à la synchronisation de branche et à la validation du nouveau commit. Les compléments de recherche listés ci-dessous ne sont pas des prérequis à la fusion de cette PR.

### 7.2 Inspection scientifique et bibliographique différée

- [ ] Inspecter visuellement les figures originales de Piantadosi, Lestrade, Pilgrim & Hills et Linders & Louwerse ; noter ce qu'elles apportent au-delà des descriptions textuelles déjà extraites.
- [ ] Examiner les suppléments de Lestrade, Pilgrim & Hills et Linders & Louwerse ; mettre à jour les limites d'inspection item par item.
- [ ] Auditer le dépôt de code et les données de Pilgrim & Hills sans supposer que les résultats sont directement reproductibles.
- [ ] Auditer les scripts, données et modèles alternatifs de Lestrade ; ne pas transformer une reproduction partielle en validation indépendante.
- [ ] Lire de manière ciblée Zipf (1949), en particulier le chapitre “On the Economy of Words”, avant toute affirmation historique plus précise.
- [ ] Ouvrir et exécuter le notebook Wolfram ; vérifier le comportement réel, les dépendances, l'ergonomie et la licence affichée. Ne pas le recopier dans le dépôt.

### 7.3 Laboratoire de corpus — issue dédiée

Le laboratoire ne doit pas être développé dans la PR d'ingestion et ne doit pas alourdir la leçon Day 01. Son cadrage détaillé et ses critères d'acceptation sont suivis dans [l'issue #1605 — laboratoire reproductible sur corpus Zipf](https://github.com/JM-Brun/llm-lab/issues/1605).

Ordre recommandé :

1. **Ressources et droits** : épingler les versions ELTeC-fra et ELTeC-eng, examiner séparément les droits des textes, transcriptions, métadonnées et encodages, puis sélectionner quelques romans par langue.
2. **Extraction TEI** : définir une extraction déterministe excluant balises, métadonnées et notes éditoriales ; conserver un manifeste des documents et des journaux de nettoyage.
3. **Comptage** : tester les choix de normalisation (Unicode, casse, apostrophes, ponctuation, mots composés), distinguer occurrences, formes lexicales, types et tokens d'un tokenizer.
4. **Rang et visualisation** : définir le traitement des ex æquo, produire tableaux de fréquences, rangs, courbes linéaires et log-log, et rendre les observations inspectables.
5. **Estimation et robustesse** : séparer ajustement descriptif et estimation de l'exposant ; étudier résidus, incertitude, taille d'échantillon et rééchantillonnage par document. Une pente OLS en log-log ne doit pas être présentée comme une estimation robuste à elle seule.
6. **Comparaison** : analyser français et anglais séparément ; expliciter les limites d'un corpus littéraire historique et de toute interprétation interlinguistique.
7. **Pédagogie** : publier le laboratoire dans “S'exercer et expérimenter”, avec une page d'entrée courte, des questions de transfert et des corrigés/critères d'interprétation. La leçon principale reste concise.

### 7.4 Sources pédagogiques candidates non encore ingérées

Ces ressources ont été repérées mais **ne sont pas encore enregistrées comme sources extraites dans le catalogue** :

- **Webis, notes de cours “Corpus Linguistics”** ([PDF](https://downloads.webis.de/lecturenotes/natural-language-processing/unit-en-corpora.pdf)) : candidate pour la sparsité des corpus, les hapax, la queue longue, Zipf–Mandelbrot, les écarts tête/queue et les implications pour le lissage. À examiner avec les pages et passages exacts avant toute intégration.
- **UMBC, NLP Assignment 1 (2018)** ([PDF](https://courses.cs.umbc.edu/undergraduate/473/f18/content/materials/a1.pdf)) : candidate pour la séquence pratique comptage token/type → rang-fréquence → visualisation → comparaison de langues. Son ajustement log-log par OLS doit être contextualisé comme simplification pédagogique exploratoire, et non repris comme méthode statistique de référence.

Pour chacune : enregistrer la référence, inspecter les sections pertinentes, produire des extractions atomiques avec localisateurs, comparer aux pages/exercices existants, puis attribuer à chaque contribution une disposition motivée (`integrate`, `already-covered` ou `defer`). Ne créer une page ou un concept que si un apport distinct le justifie.

### 7.5 Validation pédagogique à mener après réalisation

- [ ] Faire relire la séquence et le laboratoire par une personne non spécialiste : compréhension des rangs, de l'exposant, des limites d'un ajustement et distinction entre description et causalité.
- [ ] Vérifier les consignes, corrigés, liens, navigation clavier, rendu mobile et fonctionnement sans exécution du notebook.
- [ ] Recueillir des difficultés observées et réviser les exercices ; ne revendiquer aucune efficacité pédagogique tant qu'aucune évaluation n'a été conduite.

## 8. Références

- Piantadosi, S. T. (2014). [DOI](https://doi.org/10.3758/s13423-014-0585-6) · [PDF auteur](https://colala.berkeley.edu/papers/piantadosi2014zipfs.pdf)
- Lestrade, S. (2017). [DOI](https://doi.org/10.1371/journal.pone.0181987) · [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0181987)
- Pilgrim, C., & Hills, T. T. (2021). [DOI](https://doi.org/10.1038/s41598-021-96214-w) · [Scientific Reports](https://www.nature.com/articles/s41598-021-96214-w)
- Linders, G. M., & Louwerse, M. M. (2023). [DOI](https://doi.org/10.3758/s13423-022-02142-9) · [Publisher](https://link.springer.com/article/10.3758/s13423-022-02142-9)
- Roda, G. (2024). [Wolfram Demonstrations](https://demonstrations.wolfram.com/ZipfsLawForNaturalLanguages/)
- Schöch, C., & Burnard, L. (eds.). (2021). [French Novel Corpus (ELTeC-fra), v1.0.1](https://doi.org/10.5281/zenodo.4662433).
- Burnard, L. (ed.). (2021). [English Novel Corpus (ELTeC-eng), v1.0.1](https://doi.org/10.5281/zenodo.4662490).
- Zipf, G. K. (1949). [Google Books](https://books.google.com/books?id=1tx9AAAAIAAJ)

## 9. Index des extractions atomiques

Le catalogue relie chaque source à un fichier d'extraction unique. Les identifiants d'items permettent de retrouver une contribution sans dépendre de son titre ni de son ordre dans le document.

| Fichier | Items extraits |
|---|---|
| `data/extractions/piantadosi-zipf-word-frequency-2014.yml` | `rank-frequency-form`, `zipf-mandelbrot-variant`, `correlated-rank-frequency-errors`, `structure-beyond-simple-law`, `theory-underdetermination` |
| `data/extractions/lestrade-unzipping-zipfs-law-2017.yml` | `syntax-class-size`, `semantic-specificity-reusability`, `joint-model-and-non-consensus` |
| `data/extractions/pilgrim-hills-bias-zipf-estimators-2021.yml` | `empirical-rank-vs-probability-rank`, `maximum-likelihood-bias`, `abc-not-a-universal-fix` |
| `data/extractions/linders-louwerse-zipf-spoken-dialog-2023.yml` | `unit-generalization`, `fit-vs-exponent`, `cognitive-effort-hypothesis` |
| `data/extractions/roda-wolfram-zipf-natural-languages-2024.yml` | `interactive-rank-frequency-workbench` |

Les items sont paraphrasés, localisés et bornés par leur niveau d'inspection. Leur disposition (`integrate`, `already-covered` ou `defer`) et sa justification sont enregistrées dans chaque extraction. Ces décisions éditoriales ne valent ni validation scientifique indépendante ni preuve d'efficacité pédagogique ; les vérifications restantes sont listées à la section 7.


## 10. Suivi éditorial complémentaire — 2026-11-25

Le dossier de sources et le laboratoire ne couvrent pas à eux seuls tous les travaux éditoriaux de la leçon. Le suivi transversal de la leçon Day 01 et de ses prolongements est centralisé dans [l'issue #1653 — clarification de la leçon Zipf et organisation des approfondissements](https://github.com/JM-Brun/llm-lab/issues/1653).

La répartition des responsabilités est la suivante :

- **PR #1639** : première révision bilingue remplaçant le texte culturel par un texte original ; fusionnée.
- **PR #1648** : choix éditorial ultérieur, fusionné : le texte français fourni est conservé comme easter egg non attribué dans la page publique ; les informations de provenance restent dans le dossier. Le corpus anglais demeure indépendant.
- **PR #1615** : intégration des sources et des exercices approfondis ; fusionnée. **PR #1628** complète la leçon bilingue et ses usages ; **PR #1631** termine l'audit des relations conceptuelles. **PR #1608** est fermée sans fusion et ne constitue pas l'état intégré.
- **PR #1654** : lien entre ce dossier et l'issue de suivi #1653 ; fusionnée.
- **Issue #1653** : cohérence FR/EN, définitions des unités, intuition des paramètres, visualisations, usages concrets, lien rigoureux aux LLM, ramifications Deepen et validation novice.
- **Issue #1605** : laboratoire reproductible sur corpus (ELTeC, extraction TEI, comptages, rangs, estimation et robustesse). Ne pas dupliquer ce périmètre dans #1653.

L'architecture éditoriale retenue comporte trois espaces : une leçon principale concise et autonome ; des approfondissements Deepen facultatifs, créés progressivement lorsqu'une notion mérite une page autonome ; une pratique séparée, accessible depuis la leçon par un lien discret. Le graphe conceptuel, le graphe computationnel et le parcours pédagogique restent trois représentations distinctes.

Les candidates de prolongement (Zipf–Mandelbrot, loi de Heaps, hapax, diversité lexicale, comparaisons de corpus et lien aux distributions de tokens des LLM) ne sont pas des pages promises ni des concepts à enregistrer automatiquement. Leur création dépend d'un apport pédagogique autonome, de sources suffisantes et d'une modélisation cohérente. Les expériences comparatives, notamment entre langues ou discours politiques, relèvent des pages de pratique et doivent contrôler genre, période, taille, normalisation et unité de comptage.

**Important :** l'issue #1653 est un plan de travail, pas une preuve que les points sont déjà corrigés. Les statuts d'implémentation, de validation technique et de validation pédagogique doivent rester distincts.
