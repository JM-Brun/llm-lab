# Audit ciblé du parcours principal : couverture des sources et longueur des pages

**Date :** 2026-11-26  
**Périmètre :** pages françaises du parcours principal défini dans `data/guided-route.yml`  
**Nature :** audit documentaire et éditorial ; aucune page pédagogique ni métadonnée n'a été modifiée dans le cadre de cet audit.

## 1. Objectif et méthode

L'audit répond à deux questions distinctes :

1. Quelle page du parcours principal possède le moins de sources reliées dans le catalogue canonique ?
2. Quelle page est la plus courte, et mérite-t-elle pour autant davantage de contenu ?

La sélection des pages doit provenir de `data/guided-route.yml`, et non d'une recherche approximative dans tous les fichiers du site. Les pages optionnelles, d'approfondissement, d'exercices et de navigation sont exclues.

Trois indicateurs doivent rester distincts :

- **Sources du catalogue** : entrées de `data/sources.yml` dont `related.pages` contient la page.
- **Références visibles** : références bibliographiques ou liens externes effectivement présents dans le contenu de la page.
- **Longueur éditoriale** : volume de texte pédagogique, sans front matter, commentaires de métadonnées, blocs de code ou blocs mathématiques.

Le comptage de mots est heuristique : les shortcodes, composants Quarto, tableaux et éléments HTML peuvent rendre le résultat légèrement différent du texte effectivement perçu par le lecteur. Il sert à classer les candidates, pas à fixer une norme de longueur.

## 2. Pages candidates

### 2.1 Plus faible couverture du catalogue : Logits

Page : [Logits : les scores avant normalisation](https://jm-brun.github.io/llm-lab/fr/logits.html)

Constat vérifié dans le registre consulté :

- aucune entrée de `data/sources.yml` ne relie actuellement cette page via `related.pages` ;
- la page contient néanmoins un lien direct vers la documentation PyTorch `CrossEntropyLoss` ;
- la page explique déjà la projection de sortie, la dimension du vocabulaire, les scores, le classement et la distinction entre logits et probabilités ;
- les concepts canoniques `output-projection` et `logits` référencent tous deux cette page dans `data/concepts.yml`.

**Interprétation :** le zéro du catalogue n'indique pas que la page est dépourvue de références ou de contenu. Il révèle surtout une lacune de traçabilité entre les références de la page et le catalogue central.

#### Source complémentaire examinée : The Illustrated GPT-2

Jay Alammar, [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/).

Cette ressource propose une représentation visuelle de la sortie du modèle et de la projection vers le vocabulaire. Elle peut aider à relier l'état final du Transformer à la liste des scores candidats.

Le registre contient déjà `jay-alammar-illustrated-gpt2`, mais cette entrée est actuellement marquée `integration_status: deferred`, n'associe pas la page Logits dans `related.pages` et ne relie pas les concepts `logits` / `output-projection` dans sa classification. L'inspection précédemment consignée porte sur le texte de l'article, pas sur une nouvelle vérification des droits de réutilisation de ses illustrations.

La documentation GPT-2 de Hugging Face constitue un complément technique utile pour vérifier les formes de tenseurs et les conventions propres à cette architecture : [GPT-2 documentation](https://huggingface.co/docs/transformers/model_doc/gpt2). La documentation PyTorch déjà citée sur la page reste la référence directe pour l'interface de loss qui reçoit des logits non normalisés.

#### Décision éditoriale

Ne pas ajouter une longue section à la page principale. La page couvre déjà le mécanisme attendu.

Un complément court peut être pertinent pour distinguer :

- **projection de sortie liée (*weight tying*)** : partage des poids entre table d'embeddings d'entrée et projection de sortie ;
- **projection indépendante (*untied*)** : matrice de sortie distincte.

Cette distinction doit être présentée comme une variante de paramétrisation, et non comme une propriété universelle des LLM. Le GPT pédagogique de LLM Lab utilise actuellement une tête de sortie indépendante ; cette observation est vérifiable dans [`src/llm_lab/foundations/gpt.py`](https://github.com/JM-Brun/llm-lab/blob/main/src/llm_lab/foundations/gpt.py).

**Destination recommandée :** encadré facultatif ou ressource complémentaire. Les détails d'implémentation et les variantes de modèles restent dans Build / Deepen.

### 2.2 Page la plus courte : Apprentissage en contexte (ICL)

Page : [Apprentissage en contexte](https://jm-brun.github.io/llm-lab/fr/in-context-learning.html).

Le comptage heuristique effectué sur les pages candidates place cette page au bas du classement, autour de 950 mots de contenu. Ce chiffre est un ordre de grandeur, pas une métrique éditoriale normative.

La page est déjà structurée autour de :
- la définition de l'ICL et les configurations zero-shot / one-shot / few-shot ;
- la distinction entre ICL, préentraînement, fine-tuning et RAG ;
- les informations fournies par le prompt ;
- les limites de généralisation et la sensibilité aux exemples ;
- des approfondissements séparés sur les hypothèses mécanistes et les protocoles expérimentaux.

Sa bibliographie visible contient quatre références : Brown et al. (2020), Olsson et al. (2022), Xie et al. (2022) et Min et al. (2022). Aucune de ces références n'était reliée à la page dans `data/sources.yml` lors de l'audit.

**Interprétation :** la page est courte mais n'est pas sous-documentée dans son contenu visible. Son potentiel d'amélioration vient d'une nuance empirique importante, pas d'un besoin d'allonger la définition.

#### Source complémentaire principale : Min et al. (2022)

Sewon Min et al., [Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?](https://aclanthology.org/2022.emnlp-main.759/), EMNLP 2022.

Les auteurs rapportent, sur un ensemble de tâches de classification et de choix multiple et douze modèles, que remplacer aléatoirement les labels des démonstrations peut n'entraîner qu'une faible dégradation dans leurs configurations expérimentales. Ils identifient notamment comme contributions des démonstrations l'information sur l'espace des labels, la distribution des textes d'entrée et le format global de la séquence.

Cette source est déjà citée sur la page : l'apport consiste à mieux exploiter et nuancer ce résultat, pas à ajouter une référence redondante.

#### Contrepoint indispensable : Yoo et al. (2022)

Kang Min Yoo et al., [Ground-Truth Labels Matter: A Deeper Look into Input-Label Demonstrations](https://aclanthology.org/2022.emnlp-main.155/), EMNLP 2022.

Les auteurs réexaminent l'importance des correspondances entrée-label. Ils montrent que l'effet des labels corrects varie selon la configuration expérimentale, et mettent notamment en évidence le rôle de la verbosité des templates et de la taille du modèle dans la robustesse au bruit.

Ce travail empêche de transformer le résultat de Min et al. en affirmation générale selon laquelle les labels corrects seraient inutiles. Les deux études doivent être présentées comme des résultats empiriques dépendants du protocole, non comme deux vérités contradictoires à départager abstraitement.

#### Source à réserver à l'approfondissement : Xiang et al. (2024)

Yanzheng Xiang et al., [Addressing Order Sensitivity of In-Context Demonstration Examples in Causal Language Models](https://aclanthology.org/2024.findings-acl.386/), Findings of ACL 2024.

Cette étude rapporte une sensibilité à l'ordre des démonstrations plus forte pour les modèles causaux que pour les modèles PrefixLM dans les expériences considérées. Les auteurs relient ce phénomène aux masques d'attention autorégressifs et aux champs réceptifs différents selon les positions.

Le lien avec le masque causal est intéressant, mais son explication détaillée mobilise les représentations par position et les mécanismes d'attention. Ce niveau de détail dépasse le besoin de la page d'introduction.

**Destination recommandée :** Deepen, avec éventuellement un lien depuis la phrase existante sur la sensibilité à l'ordre. Ne pas introduire cette explication mécaniste dans le corps principal.

#### Proposition d'intégration dans la page principale

Ajouter un seul paragraphe dans « Ce que l'ICL permet — et ses limites », après la présentation des facteurs dont dépendent les résultats :

> Les démonstrations ne servent pas uniquement à montrer au modèle les bonnes réponses. Dans certaines expériences, Min et al. (2022) observent que remplacer les labels des exemples par des valeurs aléatoires dégrade relativement peu les performances : les démonstrations fournissent aussi des indications sur l'espace des labels, la distribution des entrées et le format attendu. Ce résultat n'est toutefois pas universel. Yoo et al. (2022) montrent que l'effet des labels corrects varie selon la configuration expérimentale, notamment selon la verbosité du template et la taille du modèle. Une démonstration fournit donc plusieurs types d'information, dont l'importance dépend de la tâche et du protocole.

Cet ajout apporte une intuition empirique et une limite explicite, sans créer une nouvelle notion ni une nouvelle section. Il doit rester compact et être intégré dans les versions française et anglaise.

## 3. Décisions de modélisation documentaire

### 3.1 Pages et concepts

Aucun nouveau concept canonique n'est requis.

- Logits : réutiliser `logits` et `output-projection`.
- ICL : réutiliser `in-context-learning`.
- Ne pas créer de concepts dédiés uniquement à « label correctness sensitivity », « demonstration order » ou « induction heads » dans le cadre de cet enrichissement.

Les relations de concepts existantes doivent être conservées. L'ajout d'une source ne justifie pas à lui seul une modification du graphe de connaissances.

### 3.2 Registre des sources

Pour Logits :
- réexaminer l'entrée existante `jay-alammar-illustrated-gpt2` ;
- si l'apport est retenu, ajouter `fr/logits` et `en/logits` à `related.pages` ;
- ajouter `logits` et `output-projection` aux concepts pertinents de la classification ;
- ne pas déclarer la source entièrement intégrée tant que son statut de scan, les limites d'inspection et la décision d'intégration ne sont pas cohérents ;
- ne pas réutiliser ses figures sans vérification spécifique de provenance et de droits.

Pour ICL :
- créer ou réconcilier les entrées canoniques des références Brown, Olsson, Xie et Min déjà présentes dans la bibliographie ;
- créer l'entrée de Yoo et al. (2022) après vérification bibliographique ;
- relier les sources retenues à `fr/in-context-learning` et `en/in-context-learning` dans `related.pages` ;
- associer le concept existant `in-context-learning` ;
- distinguer le statut de consultation de celui d'intégration effective ;
- conserver Xiang et al. comme source d'approfondissement si la page principale ne reprend pas son mécanisme.

Ne pas supposer qu'une référence visible est une source ingérée, ni qu'une source cataloguée est automatiquement intégrée à une page.

### 3.3 Métadonnées de page

Les pages disposent déjà de leur classification de leçon principale et de leur destination `understand`. Les concepts canoniques et les ressources sont déjà reliés.

Aucun changement de tags `type`, `destination`, `topic` ou `level` n'est justifié par cet audit. L'enrichissement proposé ne change ni le niveau pédagogique ni la destination des pages.

Les éventuelles références vers Deepen doivent être portées par les liens de ressources et les relations de page appropriées, pas par la création artificielle d'un nouveau concept.

## 4. Automatisation à documenter

Le dépôt dispose déjà de :
- `site/tools/report_source_coverage.py` pour les indicateurs sources / extractions / concepts / destinations ;
- `site/tools/audit_page_metadata.py` pour les relations de pages et la topologie du parcours.

Il est préférable d'étendre ces rapports ou d'ajouter un mode de rapport ciblé, plutôt que de créer un workflow GitHub Actions par page ou par concept.

Le rapport de classement souhaité devrait :

1. lire les pages principales depuis `data/guided-route.yml` ;
2. exclure les `optional_pages` ;
3. dédupliquer les pages et calculer séparément FR et EN ;
4. compter les sources cataloguées par identifiant source unique via `related.pages` ;
5. compter séparément les références bibliographiques visibles ;
6. calculer une longueur éditoriale avec une méthode explicitée et testée ;
7. signaler les liens bibliographiques présents sur une page mais absents du catalogue ;
8. présenter les classements comme des alertes de revue, jamais comme des défauts automatiques ;
9. garder le résultat déterministe et exploitable en local, sans ajouter une action CI dédiée.

Les tests doivent couvrir au minimum : exclusion des pages optionnelles, déduplication, liens multiples vers une même source, référence visible non cataloguée, blocs de code et mathématiques, commentaires de métadonnées, pages bilingues et page sans bibliographie.

## 5. Plan d'action proposé

| Priorité | Action | Critère d'acceptation |
|---|---|---|
| P0 | Réconcilier les références ICL existantes avec `data/sources.yml` | Chaque référence bibliographique retenue possède une entrée canonique et une liaison à la page |
| P0 | Cataloguer Yoo et al. (2022) | Métadonnées bibliographiques vérifiées, source et extraction qualifiées |
| P1 | Ajouter le paragraphe Min / Yoo dans ICL FR et EN | Même nuance scientifique dans les deux langues, sans allongement disproportionné |
| P1 | Classer Xiang et al. en approfondissement | Lien facultatif depuis la discussion sur l'ordre, sans explication mécaniste dans le tronc principal |
| P1 | Réexaminer Jay Alammar pour Logits | Décision d'intégration explicite, liaison aux concepts et pages si retenue |
| P2 | Étendre le rapport de couverture | Classements sources / références / longueur reproductibles depuis le parcours principal |
| P2 | Ajouter les tests du rapport | Les cas limites listés ci-dessus sont vérifiés |

## 6. Limites de cet audit

- Les nombres de mots sont des estimations issues d'un comptage heuristique et doivent être recalculés par un outil versionné avant toute comparaison future.
- Le nombre de sources du catalogue mesure la traçabilité documentaire, pas la qualité d'une page.
- L'inspection des articles et les résultats empiriques cités ne permettent pas de généraliser au-delà des tâches, modèles et protocoles étudiés par les auteurs.
- Aucune modification de page, de registre de sources, de concept ou de graphe n'est incluse dans ce document.
- La vérification des licences et des droits de réutilisation des figures doit être effectuée séparément avant toute reprise d'illustration.

## 7. Sources de l'audit

- Min et al. (2022), [Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?](https://aclanthology.org/2022.emnlp-main.759/).
- Yoo et al. (2022), [Ground-Truth Labels Matter: A Deeper Look into Input-Label Demonstrations](https://aclanthology.org/2022.emnlp-main.155/).
- Xiang et al. (2024), [Addressing Order Sensitivity of In-Context Demonstration Examples in Causal Language Models](https://aclanthology.org/2024.findings-acl.386/).
- Alammar, [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/).
- Hugging Face, [GPT-2 model documentation](https://huggingface.co/docs/transformers/model_doc/gpt2).
- PyTorch, [CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).


## 8. Critère éditorial : durée cible et équilibre des leçons

La longueur ne doit pas être optimisée indépendamment de l'objectif pédagogique. La cible éditoriale du parcours principal est désormais :

- **environ 15 minutes** pour une leçon standard ;
- **7 minutes** comme seuil inférieur de vigilance ;
- **20 minutes** comme seuil supérieur de vigilance.

Ces bornes sont des repères de conception, pas des seuils automatiques de validation. Une leçon de 8 ou 10 minutes peut être parfaitement équilibrée si elle traite une unité conceptuelle cohérente. Une leçon de 18 minutes n'a pas à être raccourcie si chaque partie est nécessaire. Il ne faut ni ajouter du contenu pour atteindre 15 minutes, ni supprimer des explications utiles pour passer sous 20 minutes.

### 8.1 Décider du bon périmètre avant de modifier la longueur

Pour une leçon sous 7 minutes, examiner dans cet ordre :

1. son objectif constitue-t-il une unité d'apprentissage autonome ?
2. lui manque-t-il une explication, un exemple travaillé, une représentation ou une transition nécessaire à la compréhension ?
3. une notion préalable ou complémentaire a-t-elle été artificiellement séparée alors qu'elle forme avec elle une même progression ?
4. la page est-elle plutôt une fiche de référence, une étape de parcours ou une véritable leçon ?

Pour une leçon au-dessus de 20 minutes :

1. identifier les objectifs pédagogiques distincts ;
2. repérer les changements de question, d'objet étudié ou de niveau d'abstraction ;
3. déterminer si une partie peut devenir une leçon autonome avec prérequis et transition explicites ;
4. déplacer les variantes, démonstrations avancées et détails d'implémentation vers Deepen ou Build lorsqu'ils ne sont pas nécessaires à l'objectif principal.

Le découpage doit suivre les dépendances conceptuelles et la progression du raisonnement, pas un quota de mots. Ne pas scinder une explication au milieu d'une chaîne causale simplement pour obtenir deux durées proches.

### 8.2 Durée de lecture : une estimation explicite et reproductible

Chaque leçon du parcours devrait afficher une durée approximative, idéalement calculée à partir d'une métadonnée structurée et rendue automatiquement dans l'interface. Cette durée doit représenter le temps nécessaire pour lire et comprendre le contenu principal, et non seulement un nombre de mots divisé par une vitesse de lecture.

Le calcul devrait distinguer au minimum :

- prose explicative ;
- tableaux et listes denses ;
- équations et notations à interpréter ;
- exemples travaillés et blocs de code à lire ;
- schémas et diagrammes à parcourir ;
- contenu facultatif de type Deepen, qui ne doit pas être confondu avec le temps du tronc principal ;
- exercices, comptabilisés séparément puisqu'ils disposent de pages dédiées.

La méthode doit être documentée, versionnée et appliquée de la même manière en français et en anglais. Il faut afficher une **estimation arrondie** (par exemple « ≈ 15 min »), pas une précision artificielle à la minute près si la méthode ne la justifie pas. La durée doit être révisée après toute modification substantielle du contenu.

### 8.3 Métadonnée et affichage proposés

Conserver une valeur structurée, lisible par les outils, dans le bloc de métadonnées de la page (PAGE-MAP ou schéma de métadonnées canonique retenu par le dépôt), par exemple :

```yaml
estimated_reading_minutes: 15
```

Ce champ est une estimation éditoriale maintenue et vérifiée par le rapport, pas une valeur que le rapport doit écraser automatiquement. Le rapport peut calculer une estimation indépendante, signaler un écart et demander une revue.

Les sources doivent rester canoniques dans `data/sources.yml`, avec leurs identifiants et leurs relations `related.pages`. La page doit continuer à présenter au lecteur ses références et ressources pertinentes. Le rapport doit pouvoir confronter les références visibles, le catalogue et les sources réellement mobilisées dans le contenu ; il ne doit pas confondre ces trois notions.

À terme, la page peut afficher ensemble, de façon discrète, la durée approximative et ses références principales. Les références complémentaires et approfondissements restent séparés des sources qui soutiennent directement le tronc principal. Éviter de recopier dans une métadonnée de page une seconde liste de sources qui divergerait du catalogue canonique.

### 8.4 Critères d'équilibre à auditer

La revue d'une leçon doit donc combiner :

| Dimension | Question de contrôle |
|---|---|
| Objectif | La leçon répond-elle à une question pédagogique précise et identifiable ? |
| Prérequis | Les connaissances nécessaires sont-elles introduites ou reliées explicitement ? |
| Progression | Les explications, exemples et représentations s'enchaînent-ils sans saut ? |
| Profondeur | Le tronc principal contient-il le nécessaire, sans absorber les développements de Build / Deepen ? |
| Sources | Les affirmations importantes sont-elles soutenues par des sources identifiables et pertinentes ? |
| Durée | La durée estimée est-elle proche de 15 min et comprise idéalement entre 7 et 20 min ? |
| Autonomie | La leçon a-t-elle une conclusion, des références et une transition vers la suite ? |

Une durée hors intervalle déclenche une revue éditoriale, jamais une correction mécanique. Une durée dans l'intervalle ne prouve pas à elle seule que la leçon est bien construite.

### 8.5 Conséquence pour les deux pages de cet audit

- **ICL** : ne pas l'allonger uniquement parce qu'elle est la plus courte. L'ajout Min / Yoo ne se justifie que par la nuance empirique qu'il apporte. Réestimer ensuite la durée réelle ; si elle reste sous 7 minutes, revoir le périmètre et les éventuelles notions manquantes avant de décider d'un enrichissement ou d'un regroupement.
- **Logits** : ne pas ajouter une section sur le *weight tying* uniquement pour augmenter la durée ou le nombre de sources. Ne l'intégrer au tronc que si cette distinction est nécessaire pour comprendre la projection de sortie ; sinon, conserver une ressource facultative / Build / Deepen.

Le classement initial par nombre de mots reste un signal exploratoire. Il doit être remplacé, pour le suivi régulier, par une estimation de durée tenant compte des différents types de contenu et accompagnée d'une validation éditoriale.


## 9. Première cartographie de longueur du parcours principal

Un relevé complémentaire a été effectué sur les 20 pages françaises déclarées dans les champs `pages.fr` des étapes de `data/guided-route.yml`. Les pages de `optional_pages`, les pages d'exercices et les pages de transition non présentes dans les étapes n'ont pas été comptées comme leçons principales.

### 9.1 Mesure exploratoire

Le comptage ci-dessous porte sur le texte de la page après retrait du front matter, des commentaires HTML, des directives d'inclusion Quarto et des blocs de code clôturés. Il reste un comptage lexical approximatif : les composants, tableaux, contenus repliés et ressources peuvent encore être comptés même s'ils ne font pas partie de la lecture centrale. Les blocs de code sont indiqués séparément lorsqu'ils ont été relevés.

La fourchette de lecture indicative est calculée à 130–150 mots/minute, arrondie à la minute. Elle **n'est pas encore une durée de leçon validée** : elle ne mesure pas correctement l'interprétation des équations, des schémas ou des exemples, et ne distingue pas systématiquement le tronc principal du contenu facultatif. Elle sert uniquement à repérer les pages à examiner en premier.

| Leçon (FR) | Mots approx. | Sources catalogue reliées | Lecture brute indicative |
|---|---:|---:|---:|
| Vue d'ensemble | 2 367 | 1 | 16–18 min |
| Du texte aux tokens | 1 913 | 1 | 13–15 min |
| Espace des embeddings | 1 453 | 2 | 10–11 min |
| Encodage positionnel | 1 689 | 1 | 11–13 min |
| Représentations contextualisées | 1 746 | 4 | 12–13 min |
| Transformer | 1 934 | 3 | 13–15 min |
| Queries, Keys, Values | 1 762 | 4 | 12–14 min |
| Attention à produit scalaire | 2 321 | 4 | 16–18 min |
| Masquage causal | 1 983 | 1 | 13–15 min |
| Logits | 1 282 | 0 | 9–10 min |
| Probabilités de sortie | 1 235 | 1 | 8–10 min |
| Entropie | 1 527 | 0 | 10–12 min |
| Génération | 3 245 | 2 | 22–25 min |
| Apprentissage en contexte (ICL) | 1 118 | 1 | 7–9 min |
| Ingénierie du contexte | 1 654 | 0 | 11–13 min |
| Vraisemblance | 1 254 | 1 | 8–10 min |
| Cross-entropy | 2 404 | 0 | 16–19 min |
| Loss | 1 617 | 0 | 11–12 min |
| Gradients | 1 741 | 0 | 12–13 min |
| Training loop | 3 012 | 0 | 20–23 min |

**Important :** le nombre de sources est celui des identifiants canoniques dont `related.pages` référence la page dans `data/sources.yml`. Ce n'est ni le nombre de références bibliographiques visibles ni le nombre de sources effectivement mobilisées. Par exemple, l'unique source reliée à ICL dans le catalogue est actuellement la vidéo générale d'Andrej Karpathy ; la page cite aussi quatre articles scientifiques visibles. La couverture catalogue ne doit donc pas être lue comme une mesure de qualité ou de profondeur bibliographique.

### 9.2 Première lecture des déséquilibres

**Pages à examiner en priorité pour un possible découpage ou déplacement de contenu :**

- **Génération (3 245 mots)** : la page réunit la boucle autorégressive, la sélection du prochain token, le prefill/decode et des éléments de latence, d'ordonnancement et de cache pour le service de plusieurs requêtes. Le fil principal doit conserver la boucle de génération et le couple prefill/decode. Les détails de serving, d'ordonnancement et d'optimisation du cache sont des candidats naturels pour Build / Deepen, à condition de préserver les liens explicatifs utiles.
- **Training loop (3 012 mots)** : le corps précédant la section « Approfondissements » représente environ 1 979 mots dans le même comptage. La page semble donc déjà proche de la cible dans son tronc principal ; il faut éviter de la raccourcir sur la base du volume total sans distinguer les sections facultatives. Les comparaisons d'optimiseurs, workflows et détails d'implémentation doivent rester clairement hors du tronc principal.
- **Cross-entropy (2 404 mots)** : le texte avant « Cibles souples et divergence KL » représente environ 1 348 mots ; avant les sections d'implémentation, environ 1 424 mots. Le contenu sur labels souples / KL et les implémentations NumPy/PyTorch / stabilité numérique doit être évalué comme approfondissement ou Build, plutôt que d'être nécessairement imposé dans le parcours principal. Le noyau doit garder le lien entre cible observée, probabilité, perte par token, agrégation sur les positions, masques et perplexité si ces éléments sont nécessaires à la transition vers l'entraînement.
- **Vue d'ensemble (2 367 mots)** et **Attention à produit scalaire (2 321 mots)** : leur longueur brute mérite une lecture éditoriale, mais aucun découpage ne doit être décidé sans vérifier la fonction de synthèse de la première et le fil de calcul de la seconde.

**Pages courtes à examiner sans présumer qu'elles sont insuffisantes :**

- **ICL (1 118 mots)**, **Logits (1 282)**, **Probabilités (1 235)** et **Vraisemblance (1 254)**. Ces pages peuvent être des unités conceptuelles volontairement resserrées. Leur durée réelle doit intégrer la lecture des exemples et des formules. Pour ICL, l'ajout Min / Yoo ne se justifie que par la nuance scientifique ; il ne doit pas être utilisé comme remplissage.
- **Logits** n'a aucune source catalogue reliée à ce jour, mais contient une référence PyTorch visible. Il faut réconcilier cette référence avant de conclure à un défaut de sources.
- **ICL** a une source catalogue reliée (vidéo générale Karpathy), mais ses quatre articles visibles ne sont pas encore représentés comme des entrées dédiées dans le registre. La priorité est la traçabilité bibliographique, non l'augmentation du volume de texte.

### 9.3 Conséquences éditoriales provisoires

1. Ne pas appliquer une règle « toute page sous 15 min doit grossir ». Une durée de 8–12 min peut convenir à une notion étroite si la leçon est autonome et correctement reliée à ses prérequis et à la suivante.
2. Ne pas appliquer une règle « toute page au-dessus de 20 min doit être scindée ». Vérifier d'abord si le dépassement vient du contenu facultatif ou d'une unité pédagogique réellement trop large.
3. Distinguer explicitement, dans les estimations futures, le **temps du tronc principal**, le **temps des approfondissements facultatifs** et le **temps des exercices**.
4. Pour les pages bilingues, utiliser la même méthode mais calculer les durées FR et EN indépendamment ; ne pas recopier une durée d'une langue à l'autre.
5. Ne pas remplir `estimated_reading_minutes` avec les fourchettes lexicales ci-dessus. Ce champ ne doit être renseigné qu'après mise en place d'une méthode qui distingue le contenu principal des ressources repliées et qui prend en compte équations, figures et exemples.

### 9.4 Ordre recommandé de la revue éditoriale

1. Génération : décider précisément de la frontière entre compréhension de l'inférence et optimisation du serving.
2. Cross-entropy : séparer le noyau conceptuel des variantes soft-target / KL et des implémentations.
3. Training loop : vérifier que le corps principal, hors approfondissements, forme une leçon cohérente et proche de la cible.
4. Vue d'ensemble et attention : vérifier les répétitions et les objectifs distincts avant tout déplacement.
5. Leçons courtes : examiner l'autonomie, les exemples, les transitions et les sources ; ne pas ajouter de contenu par quota.
6. Après ces décisions, établir la méthode de durée et renseigner les métadonnées FR/EN.
