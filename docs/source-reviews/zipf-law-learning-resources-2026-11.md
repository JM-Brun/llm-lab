# Loi de Zipf — collection de sources et extraction comparative

**Date de la passe :** 2026-11-24  
**Phase :** A — identification, inspection partielle et extraction atomique  
**Collection :** \`zipf-law\`  
**Dossier pédagogique existant :** [Day 01 — dossier de sources](../advent-calendar-pilots/day-01-source-dossier.md)

## 1. Point de départ : ne pas recréer la leçon

Le dépôt contient déjà une leçon bilingue publiée :

- \`site/fr/advent-calendar-story-day-01.qmd\`
- \`site/en/advent-calendar-story-day-01.qmd\`

et des pages de pratique distinctes :

- \`site/fr/exercises/zipf-law.qmd\`
- \`site/en/exercises/zipf-law.qmd\`

Les PR #1592, #1593 et #1594 ont établi cette structure et intégré la leçon dans les rubriques Deepen. La présente collection ne crée donc ni nouvelle leçon, ni nouvelle page d'exercices, ni nouveau nœud conceptuel. Elle documente les sources qui étayent ou peuvent enrichir le travail déjà publié.

**Question pédagogique centrale :** comment décrire la distribution très inégale des fréquences lexicales, comment évaluer cette description et que peut-on réellement en déduire ?

La leçon existante traite le cas lexical écrit, la relation rang–fréquence, l'échelle log-log, les biais de représentation et une conséquence limitée pour les corpus d'entraînement. La collection étend l'analyse vers les méthodes d'estimation, les mécanismes proposés et les autres unités de communication.

## 2. Inventaire des sources enregistrées

Les sources sont inscrites dans \`data/sources.yml\`, leurs contributions atomiques dans \`data/extractions/<source-id>.yml\`. Les statuts distinguent inspection, extraction et intégration : une source partiellement inspectée peut fournir des éléments extraits, mais cela ne rend pas sa numérisation complète.

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

**Disposition actuelle :** piste historique, pas source extraite. Une lecture ciblée du chapitre consacré aux mots est nécessaire avant toute intégration historique.

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

## 6. Position dans le modèle de connaissances

- **Domaine principal conservé :** \`probabilistic-foundations-training\`, cohérent avec le classement actuel de la leçon Day 01 dans le registre des pages.
- **Domaine secondaire des sources :** \`text-tokenization\` lorsque la distinction entre formes lexicales et tokens de tokenizer est matériellement traitée.
- **Aucun concept canonique Zipf n'est créé en Phase A.** Les sources sont reliées à la leçon et à ses exercices par leurs destinations candidates ; les tags servent à la recherche, pas à créer des nœuds du graphe.
- Les identifiants de concept candidats ne sont pas inventés. Un concept durable « loi de Zipf » pourra être envisagé en Phase B seulement si le graphe et plusieurs ressources l'exigent réellement.
- Le parcours principal ne doit pas être réordonné : cette notion est un approfondissement des propriétés statistiques des corpus, pas une étape du forward pass ou du calcul d'attention.

## 7. Limites et tâches de vérification

- [ ] Inspection visuelle des figures de Piantadosi, Lestrade, Pilgrim & Hills et Linders & Louwerse.
- [ ] Inspection des suppléments de Lestrade, Pilgrim & Hills et Linders & Louwerse.
- [ ] Audit du dépôt de code et des données de Pilgrim & Hills ; aucune reproduction n'a été effectuée.
- [ ] Audit des scripts, données et modèles alternatifs de Lestrade ; aucune reproduction n'a été effectuée.
- [ ] Lecture ciblée de Zipf (1949), notamment “On the Economy of Words”.
- [ ] Ouverture et exécution du notebook Wolfram ; vérification de sa licence exacte et de son ergonomie.
- [ ] Phase B : comparer chaque item extrait aux sections exactes de la leçon et des exercices, puis décider des intégrations sans perte de contenu.
- [ ] Validation bilingue, rendu Quarto, liens, accessibilité et revue par lecteur non spécialiste après toute modification de page.

## 8. Références

- Piantadosi, S. T. (2014). [DOI](https://doi.org/10.3758/s13423-014-0585-6) · [PDF auteur](https://colala.berkeley.edu/papers/piantadosi2014zipfs.pdf)
- Lestrade, S. (2017). [DOI](https://doi.org/10.1371/journal.pone.0181987) · [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0181987)
- Pilgrim, C., & Hills, T. T. (2021). [DOI](https://doi.org/10.1038/s41598-021-96214-w) · [Scientific Reports](https://www.nature.com/articles/s41598-021-96214-w)
- Linders, G. M., & Louwerse, M. M. (2023). [DOI](https://doi.org/10.3758/s13423-022-02142-9) · [Publisher](https://link.springer.com/article/10.3758/s13423-022-02142-9)
- Roda, G. (2024). [Wolfram Demonstrations](https://demonstrations.wolfram.com/ZipfsLawForNaturalLanguages/)
- Zipf, G. K. (1949). [Google Books](https://books.google.com/books?id=1tx9AAAAIAAJ)
