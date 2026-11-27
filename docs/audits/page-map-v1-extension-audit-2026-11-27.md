# Audit du contrat PAGE-MAP v1 et de ses consommateurs

**Date :** 2026-11-27  
**Périmètre :** contrat des métadonnées de page, index partagé, validation, génération de la learning map et affichage.  
**Objectif :** décider si une métadonnée facultative de durée estimée peut être ajoutée sans casser PAGE-MAP v1.

## 1. Décision

**Conserver le marqueur `LLM-LAB-PAGE-MAP v1` et autoriser les extensions additives facultatives, sous validation explicite de chaque champ consommé.**

Le contrat en place est extensible de fait :

- le validateur `site/tools/check_page_metadata.py` exige un ensemble de champs structurels, mais ne rejette pas les clés supplémentaires ;
- `site/tools/page_index.py` conserve le mapping PAGE-MAP complet dans `PublishedPage.metadata` ;
- les consommateurs de projection lisent explicitement les champs dont ils ont besoin ;
- aucun modèle Pydantic fermé (`extra="forbid"`) n'est appliqué au mapping PAGE-MAP lui-même.

L'ajout d'un champ facultatif ne justifie donc pas une nouvelle version tant qu'il ne modifie ni la sémantique ni la structure des champs existants. Cette décision ne transforme pas PAGE-MAP en schéma libre : tout nouveau champ doit être documenté, validé et testé dans le ou les consommateurs concernés.

## 2. Contrat actuel vérifié

Le bloc caché est identifié par le marqueur exact `LLM-LAB-PAGE-MAP v1`, placé immédiatement après le front matter Quarto. Le validateur vérifie notamment :

- l'unicité et l'emplacement du bloc ;
- la validité YAML et la présence des champs structurels `id`, `scope`, `purpose`, `suggested_route`, `hierarchy`, `related` et `tags` ;
- les identifiants, relations, cycles, tags contrôlés et correspondances `keywords` ;
- la parité FR/EN des dimensions éditoriales et des relations.

`summary` est déjà documenté comme facultatif. Il n'est pas dans la liste des champs obligatoires du validateur.

## 3. Consommateurs vérifiés

| Composant | Responsabilité observée | Conséquence pour une extension |
|---|---|---|
| `site/tools/page_index.py` | Parse le bloc et conserve le mapping complet dans `PublishedPage.metadata` | Un champ additionnel reste disponible sans adaptation de l'index |
| `site/tools/check_page_metadata.py` | Valide la structure, les relations, les tags et la parité | Ajouter une validation typée pour tout nouveau champ ; ne pas rendre les extensions silencieusement invalides |
| `site/tools/build_learning_map.py` | Projette explicitement les métadonnées utiles dans les enregistrements JSON | Un champ n'est pas publié dans la learning map tant qu'il n'est pas ajouté explicitement à cette projection |
| `site/tools/learning_map_renderers.py` | Utilise `summary` dans la recherche, les cartes et le panneau de détail ; utilise aussi `purpose` dans le détail | Aucun affichage d'une nouvelle métadonnée n'est automatique |
| `site/tools/audit_page_metadata.py` | Compare notamment les recouvrements lexicaux de `scope` et `purpose` | La durée n'a pas à entrer dans l'audit des frontières éditoriales |
| `data/guided-route.yml` et son générateur | Utilisent les pages et les contrats de leçon pour construire le parcours et ses contextes | La durée ne doit pas être confondue avec un prérequis, un objectif ou une étape de parcours |
| `site/_quarto.yml` | Définit les pages effectivement rendues, base de couverture du validateur | La sélection des pages principales reste pilotée par le parcours, pas par la seule présence d'une durée |

Les artefacts JSON et fragments bilingues de la learning map sont des projections générées. Ils ne doivent pas devenir des sources d'édition concurrentes.

## 4. Cas particulier de `summary` : durcissement recommandé

Le contrat éditorial dit que `summary` est facultatif, en une ou deux phrases, et décrit le contenu trouvé sur la page. Le validateur actuel ne contrôle pas son type. Dans `build_learning_map.py`, la valeur est convertie avec `str(metadata.get("summary", ""))`.

Cette conversion peut masquer une erreur de saisie : une liste, un nombre ou un booléen deviendrait une chaîne au lieu d'être rejeté.

**Correction recommandée avant ou avec l'ajout de la durée :**

- si `summary` est absent, accepter l'absence ;
- s'il est présent, exiger une chaîne non vide ;
- ne pas convertir implicitement une valeur de mauvais type ;
- conserver le repli d'affichage `summary || purpose` déjà introduit dans la learning map.

Ce durcissement ne change pas la sémantique de PAGE-MAP v1.

## 5. Contrat proposé pour la durée

Ajouter, après calibration, un champ facultatif dans le même bloc :

```yaml
estimated_reading_minutes: 15
```

Règles :

1. Valeur entière strictement positive ; booléen, chaîne, flottant, zéro et valeur négative refusés.
2. Champ facultatif : son absence est normale tant que la méthode n'est pas calibrée ou que la page n'a pas été revue.
3. Estimation éditoriale du tronc principal visible ; exercices et approfondissements facultatifs exclus.
4. Calcul indépendant pour chaque version linguistique : aucune règle d'égalité FR/EN.
5. Valeur arrondie à la minute, sans décimales ni fausse précision.
6. Le rapport calcule une estimation indépendante et signale les écarts ; il n'écrase jamais la valeur éditoriale.
7. Aucune durée ne doit être ajoutée aux pages avant la fin des décisions éditoriales, de la réconciliation des sources et de la calibration.

La valeur ne doit pas être incluse dans les champs de parité bilingue actuellement comparés par `check_page_metadata.py`. La cohérence attendue porte sur la méthode et le sens éditorial, pas sur l'égalité des minutes.

## 6. Consommation et affichage : séparation nécessaire

Le stockage de la durée dans PAGE-MAP et son affichage sont deux décisions différentes.

- Le validateur doit contrôler le type et le domaine de valeur.
- Le générateur peut exposer la durée dans un artefact ou un fragment lorsqu'un consommateur en a besoin.
- Un mécanisme partagé doit produire le libellé localisé sur les pages concernées.
- Les pages ne doivent pas recopier manuellement la durée dans leur corps.
- Les pages hors périmètre ne doivent pas afficher une durée par simple héritage de leur statut publié.

Le point d'injection exact dans le rendu Quarto reste à décider après inspection des mécanismes communs de mise en page. Il ne faut pas détourner le panneau de détails de la learning map pour en faire le mécanisme d'affichage des leçons.

## 7. Tests de validation

### Validation PAGE-MAP

- absence de `estimated_reading_minutes` acceptée ;
- entier positif accepté ;
- chaîne, flottant, booléen, zéro, entier négatif et collection refusés ;
- valeur conservée dans l'index de pages ;
- absence de comparaison d'égalité entre les durées FR et EN ;
- champ inconnu non consommé sans effet sur les champs existants.

### Projection et affichage

- le générateur ne publie le champ que si le consommateur le requiert ;
- le libellé est localisé FR/EN ;
- absence de durée : aucun espace ou libellé vide ;
- présence d'une durée : une seule occurrence visible par page ;
- les pages d'exercices et d'approfondissement ne récupèrent pas par erreur la durée du tronc principal ;
- les artefacts générés restent déterministes et à jour.

## Follow-up implementation — PR #1759

The validation gap identified above is addressed in the follow-up implementation:

- `summary` remains optional; absence is accepted.
- When present, it must be a non-empty string. Null, booleans, numbers, collections, empty strings and whitespace-only strings are rejected.
- The shared published-page index and the full PAGE-MAP validator use the same validation helper.
- The learning-map projection no longer coerces the value with `str()`.
- Tests cover absent, valid and invalid values through both consumers.

The implementation preserves PAGE-MAP v1 and the existing `summary || purpose` discovery fallback. PR #1759 carries the code, tests and schema wording. Its test suite, Python quality/domain checks, and full Quarto render with browser audit have passed.

## 8. Conclusion et travail restant

**Choix technique validé : extension additive facultative de PAGE-MAP v1, sans changement de marqueur.**

Cette décision autorise le futur champ `estimated_reading_minutes`, mais n'autorise pas encore à renseigner les pages ni à activer l'affichage.

Ordre de suite :

1. terminer la revue et la validation CI de PR #1759, qui implémente le contrôle de type de `summary` et ses tests ;
2. ajouter la validation facultative de `estimated_reading_minutes` et ses tests, lorsque l'estimateur sera prêt ;
3. inspecter les conventions de rendu Quarto et choisir le point d'injection commun ;
4. construire le rapport et calibrer l'estimateur avant toute population des pages.

L'audit initial ne modifiait aucune page de leçon, durée, source, relation, route ou workflow CI. Le suivi PR #1759 ajoute uniquement la validation de type de `summary`, ses tests et la documentation du contrat.
