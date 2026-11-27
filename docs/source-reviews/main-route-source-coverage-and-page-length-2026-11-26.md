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

Le premier comptage brut plaçait cette page au bas du classement. Le relevé affiné distingue environ 1 118 mots sur l'ensemble de la page et 785 mots dans le tronc visible après retrait des callouts repliés, des ressources HTML et du code. La lecture textuelle seule se situe donc autour de 5 à 7 minutes ; les exemples, le schéma et les formules doivent être pris en compte avant de conclure que la leçon passe sous le seuil de 7 minutes.

La page est déjà structurée autour de :
- la définition de l'ICL et les configurations zero-shot / one-shot / few-shot ;
- la distinction entre ICL, préentraînement, fine-tuning et RAG ;
- les informations fournies par le prompt ;
- les limites de généralisation et la sensibilité aux exemples ;
- des approfondissements séparés sur les hypothèses mécanistes et les protocoles expérimentaux.

Sa bibliographie visible contient quatre références : Brown et al. (2020), Olsson et al. (2022), Xie et al. (2022) et Min et al. (2022). Le catalogue relie actuellement une source à cette page, la vidéo générale d'Andrej Karpathy *Deep Dive into LLMs like ChatGPT* ; les quatre articles cités ne disposent pas encore de liaisons canoniques dédiées à cette leçon.

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

Pour Logits et Gradients — audit pédagogique et mathématique effectué dans la PR #1757 :
- les dérivations des logits, de la cross-entropie one-hot, du gradient `p-y`, de la moyenne sur positions valides et de la règle de chaîne ont été vérifiées ;
- les trois références PyTorch déjà liées aux pages sont maintenant cataloguées : CrossEntropyLoss, Autograd mechanics et gradcheck ;
- les trois notices disposent d'extractions atomiques et de relations vers les pages FR/EN et concepts existants ;
- les pages explicitent désormais `p = softmax(z)` et les conditions de précision/validité de `gradcheck` ;
- l'entrée `jay-alammar-illustrated-gpt2` a été réexaminée : sa section *Model Output* est pertinente mais redondante avec l'exemple autonome actuel et spécifique à GPT-2 ; aucune intégration ni reprise de figure n'est retenue.

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

Le comptage distingue :

- **Texte total** : volume lexical approximatif de la page, y compris le contenu replié.
- **Tronc de prose** : texte visible après retrait du front matter, des commentaires HTML, des directives d'inclusion Quarto, des blocs de code clôturés, des callouts explicitement `collapse="true"`, des éléments HTML `details`, des URLs et des expressions mathématiques délimitées.
- **Code, mathématiques et figures** : exclus du comptage lexical et à estimer séparément, car leur lecture demande un effort qui n'est pas proportionnel au nombre de mots.

La fourchette ci-dessous est une **base de lecture textuelle** calculée à 130–150 mots/minute et arrondie. Elle ne représente pas encore la durée de leçon à afficher : elle n'inclut pas le temps d'interprétation des équations, de lecture des figures, d'exécution du code ni les exercices. La durée pédagogique réelle sera donc généralement supérieure, mais l'ampleur de cet écart doit être estimée par type de contenu et validée sur quelques leçons.

| Leçon (FR) | Prose du tronc approx. | Sources catalogue reliées | Base textuelle indicative |
|---|---:|---:|---:|
| Vue d'ensemble | 1 997 | 1 | 13–16 min |
| Du texte aux tokens | 1 620 | 1 | 11–13 min |
| Espace des embeddings | 1 058 | 2 | 7–9 min |
| Encodage positionnel | 1 050 | 1 | 7–9 min |
| Représentations contextualisées | 1 372 | 4 | 9–11 min |
| Transformer | 1 597 | 3 | 11–13 min |
| Queries, Keys, Values | 1 265 | 4 | 8–10 min |
| Attention à produit scalaire | 1 077 | 4 | 7–9 min |
| Masquage causal | 1 190 | 1 | 8–10 min |
| Logits | 804 | 0 | 5–7 min |
| Probabilités de sortie | 855 | 1 | 6–7 min |
| Entropie | 1 093 | 0 | 7–9 min |
| Génération | 1 978 | 2 | 13–16 min |
| Apprentissage en contexte (ICL) | 785 | 1 | 5–7 min |
| Ingénierie du contexte | 1 192 | 0 | 8–10 min |
| Vraisemblance | 978 | 1 | 7–8 min |
| Cross-entropy | 1 727 | 0 | 12–14 min |
| Loss | 1 128 | 0 | 8–9 min |
| Gradients | 771 | 0 | 5–6 min |
| Training loop | 1 997 | 0 | 13–16 min |

Les pages Logits, Probabilités, ICL et Gradients ont une base textuelle sous ou proche de 7 minutes. Ce n'est pas encore une conclusion : Logits et Probabilités contiennent des exemples et des formules ; ICL comporte un schéma et un exemple ; Gradients contient plusieurs équations. La durée réelle doit inclure cet effort de lecture avant de décider si une leçon est sous le seuil.

**Important :** le nombre de sources est celui des identifiants canoniques dont `related.pages` référence la page dans `data/sources.yml`. Ce n'est ni le nombre de références bibliographiques visibles ni le nombre de sources effectivement mobilisées. Par exemple, l'unique source reliée à ICL dans le catalogue est actuellement la vidéo générale d'Andrej Karpathy ; la page cite aussi quatre articles scientifiques visibles. La couverture catalogue ne doit donc pas être lue comme une mesure de qualité ou de profondeur bibliographique.

### 9.2 Première lecture des déséquilibres

**Leçons proches de la cible :**

- **Génération (1 978 mots de prose visibles, base textuelle 13–16 min)** : le contenu de base est proche de la cible. Les développements sur TTFT / ITL, le service multi-requêtes, le continuous batching et le prefix caching sont dans un callout replié. La page de complexité traite déjà prefill, decode et mémoire du cache KV. Ne pas scinder la leçon sur la base du volume total ; conserver le caractère facultatif des optimisations de serving et vérifier les liens avec la page de complexité.
- **Training loop (1 997 mots, 13–16 min)** : le tronc principal est proche de la cible. Les comparaisons d'optimiseurs, workflows et détails d'implémentation sont dans la partie approfondissement. Ne pas raccourcir le noyau ; vérifier seulement que la frontière entre explication conceptuelle et implémentation est visible.
- **Cross-entropy (1 727 mots, 12–14 min)** : sa base textuelle est déjà proche de la cible. Les exemples de formes, de décalage causal, de masques, de perplexité et le lien au gradient donnent une progression cohérente. Les cibles souples / KL et les implémentations méritent une revue de niveau (Understand vs Build / Deepen), mais il n'y a pas de justification à les déplacer sur le seul critère de durée.
- **Vue d'ensemble (1 997 mots, 13–16 min)** : cohérente avec la cible ; contrôler les recouvrements avec les leçons détaillées plutôt que la raccourcir automatiquement.

**Leçons courtes ou proches du seuil à examiner :**

- **ICL (785 mots de prose visible, base 5–7 min)** : candidate la plus nette à une revue sous le seuil. La page contient déjà un exemple, un schéma et deux approfondissements repliés. Avant d'ajouter du texte, vérifier si l'exemple permet réellement de comparer zero-shot, one-shot et few-shot et d'identifier les différentes informations apportées par les démonstrations. Un exemple travaillé comparant ces configurations pourrait apporter de la valeur ; le paragraphe Min / Yoo ne doit pas servir de remplissage. La version anglaise compte environ 664 mots de prose visible ; la parité de durée doit être vérifiée indépendamment, sans imposer un nombre de mots identique entre les langues.
- **Logits (804 mots, base 5–7 min)** : le fil est précis et les exemples numériques et visuels ajoutent un effort de lecture non compté. Vérifier le temps réel avant toute extension ; ne pas ajouter une section uniquement pour la durée.
- **Probabilités (855 mots, base 6–7 min)** : la softmax, la température et l'interprétation de la distribution doivent être comprises à partir des exemples et des formules. Vérifier la durée réelle avec ces éléments.
- **Gradients (771 mots, base 5–6 min)** : le comptage textuel est bas, mais la page contient plusieurs équations et des explications mathématiques. C'est la priorité pour une estimation incluant la lecture mathématique ; si elle reste sous 7 minutes, revoir si un exemple numérique de calcul et d'interprétation du gradient manque au tronc.
- **Attention à produit scalaire (1 077 mots, base 7–9 min)** et **Masquage causal (1 190, base 8–10 min)** : les callouts repliés sont volumineux. Vérifier que le tronc visible donne un exemple complet et une compréhension suffisante, mais conserver les approfondissements repliés hors de la durée principale.
- **Encodage positionnel (1 050 mots), Espace des embeddings (1 058 mots), Vraisemblance (978 mots)** : leur base textuelle se situe autour de 7–9 minutes. Les exemples, figures et équations doivent être pris en compte avant de décider d'un enrichissement.

**Traçabilité des sources :**

- **Logits** n'a aucune source catalogue reliée à ce jour, mais contient une référence PyTorch visible. Il faut réconcilier cette référence avant de conclure à un défaut de sources.
- **ICL** a une source catalogue reliée (vidéo générale Karpathy), mais ses quatre articles visibles ne sont pas encore représentés comme des entrées dédiées dans le registre.
- Les autres pages à zéro source catalogue ont aussi des références visibles (voir la section 10) : la priorité est la réconciliation bibliographique, non l'ajout de contenu.

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


## 10. Vérification ciblée des références visibles sur les pages sans source catalogue

Une seconde vérification des sections de ressources et de références confirme que plusieurs zéros du tableau précédent sont des défauts de liaison au catalogue, et non des pages sans références.

| Leçon | Sources reliées dans le catalogue | Références visibles repérées lors de la vérification |
|---|---:|---|
| Logits | 0 | 1 : PyTorch `CrossEntropyLoss` |
| Entropie | 0 | 3 : Shannon, Cover & Thomas, 3Blue1Brown |
| Ingénierie du contexte | 0 | 3 : Anthropic, Liu et al. (*Lost in the Middle*), OWASP |
| Cross-entropy | 0 | 5 : PyTorch `CrossEntropyLoss`, PyTorch `LogSoftmax`, Shannon, Cover & Thomas, 3Blue1Brown |
| Loss | 0 | 1 : PyTorch `CrossEntropyLoss` |
| Gradients | 0 | 2 : PyTorch autograd, PyTorch `gradcheck` |
| Training loop | 0 | 9 références / ressources documentaires, dont Adam, AdamW, Deep Learning (Goodfellow et al.), Karpathy et plusieurs ressources Hugging Face |

Pour ICL, le catalogue compte actuellement une source reliée, mais il s'agit de la vidéo générale *Deep Dive into LLMs like ChatGPT* d'Andrej Karpathy ; la page comporte quatre références d'articles scientifiques (Brown, Olsson, Xie et Min). La source générale ne remplace pas quatre notices bibliographiques dédiées.

Ces vérifications sont une lecture des sections de ressources des pages concernées ; elles ne constituent pas encore une extraction automatique exhaustive de toutes les URLs de toutes les pages du parcours.

### Décision documentaire

- Ne pas ajouter une notice catalogue par simple copie de chaque URL sans vérifier l'identité bibliographique, la qualité, le statut de consultation et l'apport de la source.
- Réconcilier les notices canoniques existantes quand elles existent déjà, puis compléter les entrées manquantes.
- Lier une source à une page seulement si elle soutient effectivement une notion ou une explication de cette leçon. Les ressources d'implémentation et d'approfondissement doivent garder leur rôle explicite.
- Conserver les références visibles dans les leçons : le catalogue central les complète et les rend interrogeables, il ne doit pas rendre la bibliographie visible inutilement opaque.
- Ajouter un contrôle de cohérence qui compare les références visibles et les sources cataloguées, mais présente les différences comme une file de revue, car les formats de citation, les liens internes et les ressources facultatives ne se prêtent pas tous à une correspondance automatique.


## 11. Architecture de la durée estimée et travail restant

Cette section transforme les constats précédents en plan d'implémentation. Elle ne constitue pas encore une décision de renseigner les durées dans les pages.

### 11.1 État technique vérifié

Le dépôt possède déjà un format de métadonnées de page versionné (LLM-LAB-PAGE-MAP v1) et un validateur central dans site/tools/check_page_metadata.py.

Le validateur :
- extrait un unique bloc PAGE-MAP placé immédiatement après le front matter ;
- exige actuellement les champs structurels id, scope, purpose, suggested_route, hierarchy, related et tags ;
- vérifie notamment les relations, les identifiants, les tags contrôlés et la parité FR/EN ;
- n'expose pas encore de contrat dédié pour une durée de lecture.

Le rapport site/tools/audit_page_metadata.py charge ces métadonnées et audite le graphe documentaire. Il n'est pas aujourd'hui un estimateur de durée. Le nouveau besoin doit donc s'intégrer à l'architecture existante sans détourner le sens de ces outils.

### 11.2 Contrat de données recommandé

Retenir une métadonnée facultative et numérique, par exemple :

    estimated_reading_minutes: 15

Principes :
- la valeur décrit le tronc principal visible de la leçon, hors exercices et approfondissements explicitement facultatifs ;
- elle est calculée indépendamment pour chaque langue ;
- elle est entière et arrondie, sans décimale ni fausse précision ;
- elle reste une estimation éditoriale, pas une mesure instrumentée du temps réel ;
- elle ne doit pas être déduite automatiquement d'une simple division du nombre de mots ;
- son absence est autorisée tant que la méthode n'est pas calibrée.

Le PAGE-MAP v1 ne doit pas être modifié implicitement. Avant d'ajouter le champ, vérifier la compatibilité du parseur, les éventuels consommateurs externes et les conventions de versionnement. Si le schéma est volontairement extensible, documenter et tester cette extensibilité ; sinon, introduire une version de schéma explicite ou un mécanisme d'extension contrôlé. Ne pas changer la version pour un champ facultatif sans vérifier les implications sur les pages existantes.

L'affichage doit être produit par un mécanisme commun aux pages de leçon, avec une formulation localisée (« Durée estimée : ≈ 15 min » / « Estimated time: ≈ 15 min »). Ne pas dupliquer manuellement cette information dans le corps des 40 pages. L'emplacement exact (composant Quarto, include partagé ou mécanisme déjà utilisé par le site) reste à choisir après inspection du rendu et des conventions existantes.

### 11.3 Méthode d'estimation à calibrer

Le premier comptage lexical de la section 9 est un indicateur de triage. Il ne doit pas être converti mécaniquement en durée officielle.

La méthode versionnée devra séparer les composantes suivantes :
1. prose courante du tronc principal ;
2. tableaux, listes et légendes denses ;
3. équations et notations nécessitant une interprétation ;
4. exemples travaillés et calculs guidés ;
5. code à lire, distinct du code simplement fourni comme référence ;
6. figures et schémas qui portent une partie de l'explication ;
7. contenu facultatif (callouts repliés, détails Deepen) ;
8. exercices, hors durée de la leçon principale.

Éviter d'attribuer un coefficient arbitraire à chaque élément dès la première version. Commencer par une mesure reproductible des contenus, puis calibrer les pondérations sur quelques leçons représentatives avec une lecture réelle chronométrée ou une estimation éditoriale argumentée. Conserver les composantes brutes dans le rapport pour rendre les résultats auditables.

Échantillon de calibration minimal :
- une leçon surtout textuelle ;
- une leçon mathématique avec équations et figures (priorité : Gradients) ;
- une leçon avec code ou exemples techniques ;
- une leçon riche en callouts facultatifs (Génération ou ICL).

Comparer le temps estimé au temps observé, documenter les écarts et ajuster la méthode avant de calculer les 40 pages. La vitesse de lecture 130–150 mots/minute peut rester un point de départ pour la prose, pas une constante universelle appliquée à tout le contenu.

### 11.4 Architecture du rapport

Étendre de préférence un outil de rapport existant ou ajouter un script local unique, plutôt que créer une action CI ou un workflow par page.

Le rapport devrait prendre data/guided-route.yml comme source d'autorité pour le parcours :
- inclure les pages des étapes principales ;
- exclure optional_pages, les pages d'exercices et les ressources de navigation ;
- dédupliquer les identifiants ;
- résoudre les fichiers FR et EN séparément ;
- compter les notices canoniques uniques via data/sources.yml et related.pages ;
- extraire séparément les références visibles et signaler les écarts à examiner ;
- produire les composantes de longueur et la durée estimée ;
- signaler les valeurs manquantes ou atypiques comme alertes de revue, sans faire échouer le build.

Le rapport doit distinguer au minimum :
- nombre de notices canoniques reliées ;
- nombre de références bibliographiques visibles détectées ;
- nombre de références visibles non réconciliées ;
- volume de prose du tronc ;
- contenu mathématique, code, figures et éléments facultatifs détectés ;
- durée estimée du tronc ;
- durée indicative des approfondissements, si elle est calculée ;
- statut de calibration de la méthode.

### 11.5 Tests et critères d'acceptation

Les tests doivent vérifier :
- sélection des seules pages du parcours principal depuis guided-route.yml ;
- exclusion des pages optionnelles et des pages d'exercices ;
- déduplication des pages et des sources ;
- absence de double comptage d'une même source liée plusieurs fois ;
- distinction entre bibliographie visible et catalogue canonique ;
- exclusion du front matter, du PAGE-MAP, des commentaires et des URLs ;
- traitement explicite des blocs de code, mathématiques, tableaux, callouts repliés et HTML details ;
- calcul indépendant FR / EN ;
- stabilité des résultats sur des fixtures représentatives ;
- absence de seuil bloquant basé sur la durée ;
- cohérence entre métadonnée, rapport et affichage localisé.

Critère final : une modification de contenu substantielle doit pouvoir entraîner une mise à jour reproductible de l'estimation, et un contributeur doit pouvoir comprendre pourquoi une page est évaluée à cette durée.

### 11.6 Plan de travail restant

| Ordre | Travail | Livrable / critère de sortie |
|---|---|---|
| P0 | Vérifier le schéma PAGE-MAP et ses consommateurs | Décision documentée sur compatibilité, extensibilité et versionnement |
| P0 | Réconcilier les sources des pages signalées en section 10 | Notices canoniques vérifiées et liens related.pages justifiés, sans doublons |
| P1 | Finaliser le contenu ICL FR/EN (nuance Min/Yoo) | Paragraphe concis, symétrique sur le fond, bibliographie/catalogue réconciliés |
| P1 | Revoir l'exemple pédagogique ICL | Comparaison zero-shot / one-shot / few-shot réellement exploitable ; aucune extension de remplissage |
| P1 | Revoir Logits | Décision sur la source Jay Alammar et sur la courte note weight tying / untied ; aucun ajout d'illustration sans vérification de provenance |
| P1 | Revoir Gradients | Évaluer un exemple numérique guidé et la durée réelle de lecture des équations |
| P1 | Vérifier les frontières de niveau | Génération, Cross-entropy et Training loop : tronc Understand distinct de Build / Deepen |
| P2 | Implémenter le rapport local | Rapport déterministe basé sur le parcours, sans action CI dédiée |
| P2 | Ajouter les tests automatisés | Cas de sélection, extraction, bilinguisme, sources et contenus mixtes couverts |
| P2 | Calibrer la méthode sur l'échantillon | Écarts estimé / observé documentés et méthode stabilisée |
| P3 | Ajouter la métadonnée aux leçons FR/EN | Valeurs distinctes et justifiées, aucune valeur copiée automatiquement entre langues |
| P3 | Ajouter l'affichage commun localisé | Durée visible une seule fois, sans bruit de métadonnées |
| P3 | Recalculer et relire les 40 pages | Rapport final, anomalies revues manuellement, durées cohérentes |
| P3 | Documenter la maintenance | Règle simple : quand recalculer, comment valider, comment interpréter les alertes |

### 11.7 Ordre d'exécution recommandé

Ne pas commencer par modifier les 40 pages. L'ordre le moins risqué est :

1. stabiliser les décisions éditoriales prioritaires (ICL, Logits, Gradients et frontières Understand / Build / Deepen) ;
2. réconcilier les références bibliographiques et le catalogue ;
3. vérifier le contrat PAGE-MAP et choisir le point d'intégration de l'affichage ;
4. construire le rapport local et ses tests ;
5. calibrer l'estimateur sur quatre profils de leçons ;
6. calculer les durées FR/EN et les soumettre à une revue humaine ;
7. seulement ensuite renseigner les métadonnées et activer l'affichage commun.

Cette séquence évite de figer des durées provisoires, de propager des valeurs erronées dans les deux langues ou de créer un outil trop complexe avant d'avoir validé son utilité.
