# Refonte pédagogique du panorama LLM — décision éditoriale et plan de conservation

**Statut :** plan documentaire proposé dans PR #1209 ; exécution bilingue suivie par #1208 ; aucune suppression de contenu autorisée.  
**Date :** 2026-11-18  
**Périmètre :** `site/fr/llm-overview.qmd`, `site/en/llm-overview.qmd` et leurs destinations canoniques.  
**Coordination :** [#130](https://github.com/JM-Brun/llm-lab/issues/130) ; exécution : [#1208](https://github.com/JM-Brun/llm-lab/issues/1208) ; documentation proposée dans [PR #1209](https://github.com/JM-Brun/llm-lab/pull/1209).

## 1. Décision en bref

Le panorama doit être une **porte d'entrée conceptuelle** : donner une représentation mentale fiable de ce qu'est un LLM, de ce qu'il fait, du principe général de son fonctionnement, de son apprentissage et de ses limites. Il ne doit ni devenir un cours complet condensé ni remplacer les pages canoniques spécialisées.

La page actuelle contient une matière riche et scientifiquement nuancée, mais son périmètre excède une lecture d'orientation de 10–15 minutes. La solution n'est pas de couper des explications : **les contenus doivent être conservés, fusionnés avec leurs propriétaires canoniques, déplacés vers des approfondissements ou réorganisés en pages courtes qui se répondent.** Aucun contenu substantiel, exemple, réserve scientifique, référence, lien utile ou activité ne doit disparaître sans décision explicite et traçable.

Décisions :
1. Conserver une page d'orientation d'environ **8–10 minutes** (15 minutes maximum).
2. Réutiliser d'abord les pages canoniques et issues existantes ; ne créer aucune page avant l'audit des propriétaires.
3. Séparer les questions pédagogiques, pas les paragraphes arbitrairement.
4. Respecter Understand, Build, Deepen et Practice & experiment : deux parcours principaux indépendants, une destination d'approfondissement optionnelle et une pratique transversale.
5. Maintenir une explication canonique par concept ; les autres pages introduisent brièvement et renvoient.
6. Rendre explicite le pont entre prédiction du prochain token et capacités transférables, sans présenter une hypothèse comme un fait établi.
7. Introduire tôt les limites et la distinction modèle/système, sans tout développer dans le panorama.

## 2. Diagnostic du point de vue apprenant

### À conserver absolument

- L'accroche Astérix et la continuation : un exemple concret et réutilisable.
- La distinction assistant/application et modèle interrogé.
- Le prochain token, le contexte qui s'enrichit et les paramètres fixes à l'inférence.
- Le tableau de probabilités fictives, son statut illustratif et sa cohérence entre pages.
- Les définitions minimales de token, contexte et paramètres.
- « Une suite probable n'est pas une suite vraie ».
- La vue complète : texte, tokenisation, représentations, Transformer, logits/probabilités, sélection et boucle.
- Les trois usages du calcul : génération, scoring d'une cible observée et apprentissage, avec leurs différences.
- LLM / Transformer / GPT et les familles encodeur seul, encodeur-décodeur et décodeur seul.
- Les trois dimensions architecture / apprentissage / utilisation.
- Pré-entraînement, modèle de base, modèle de fondation, post-entraînement et adaptation.
- Connaissances paramétriques, fine-tuning, RAG, contexte, ICL, mémoire applicative et cache KV.
- Transfert et généralisation : réutiliser des régularités apprises dans des tâches différentes de l'objectif d'entraînement.
- Histoire du Transformer, contexte des changements et nuances historiques.
- Choix pratiques entre modèle généraliste, RAG et adaptation, avec les critères de décision.
- Distinction entre modèle et système conversationnel, rôle de l'application/runtime et exécution des outils.
- Réserves sur vérité, compréhension, émergence, généralisation, évaluation et limites des analogies.

### Frictions

- La lecture traverse trop de niveaux : orientation, mécanisme, mathématiques, histoire, adaptation, récupération, choix d'architecture et ingénierie système.
- *Prefill*, *decode*, vraisemblance, surprisal, loss, gradients, teacher forcing, KV-cache, RAG et ICL arrivent sans assez de balisage « essentiel maintenant / approfondir ensuite ».
- Le diagramme technique du Transformer arrive avant que le phénomène observable ait pleinement donné envie de comprendre ses composants.
- Le lien entre prédiction du prochain token et diversité des capacités reste trop peu explicite.
- La section « où se trouve l'information ? » est utile, mais trop développée pour un premier contact.
- La durée actuelle de 20–30 minutes confirme que la page réunit plusieurs leçons.

## 3. Architecture éditoriale cible

Le découpage ci-dessous répartit les responsabilités. Ce n'est pas une autorisation de créer toutes ces pages : vérifier d'abord les propriétaires canoniques et les issues. Viser 10 minutes par page, 15 minutes maximum ; si une destination dépasse ce budget, arbitrer un découpage conceptuel ou un approfondissement Deepen.

### A. Panorama — « Qu'est-ce qu'un LLM ? » (Understand, 8–10 min)

**Question :** quel est cet objet, que peut-il faire et quelle est la carte générale de son fonctionnement ?

Garder :
- définition intuitive et quelques usages concrets ;
- distinction modèle / assistant / application / outils ;
- exemple fil rouge, sans développer tous les calculs ;
- place des LLM dans IA / ML / deep learning / TAL, en cohérence avec #108 ;
- repère LLM / Transformer / GPT en quelques lignes et lien vers la comparaison canonique ;
- cycle de vie : données et pré-entraînement → éventuel post-entraînement/adaptation → inférence → évaluation ;
- principe autorégressif en une phrase et lien vers Generation ;
- carte des capacités et limites : utile, mais pas magique ; plausible n'est pas vrai ;
- carte des questions du parcours.

Ne pas y développer la tokenisation, les embeddings, l'attention, les logits, les dérivations mathématiques, l'histoire détaillée, les méthodes de post-entraînement ou le serving.

**Résultat attendu :** l'apprenant sait expliquer ce qu'est un LLM, le distinguer d'un assistant, nommer son principe général et identifier les grandes questions qui seront approfondies.

### B. Génération — réutiliser la page canonique existante (Understand, durée à vérifier)

Propriétaire : `generation.qmd` / EN, déjà lié au panorama et à la route.

Y conserver/fusionner :
- préfixe, continuation et boucle autorégressive ;
- distribution conditionnelle et exemple numérique fictif ;
- sélection, ajout au contexte, nouvel appel et arrêt ;
- distinction entre calcul des logits/probabilités et règle de décodage ;
- prefill/decode, cache KV et optimisations de serving au niveau approprié ;
- repère bref sur génération / scoring / apprentissage, avec renvois vers les propriétaires du scoring et de l'entraînement.

Les mathématiques de vraisemblance, surprisal, entropie, température et loss restent chez leurs propriétaires canoniques au-delà de l'intuition nécessaire.

### C. Pourquoi la prédiction permet-elle des capacités variées ? (arbitrage de propriété obligatoire)

**Question :** comment apprendre à prédire des continuations peut-il aider à traduire, résumer, expliquer, coder ou traiter une tâche nouvelle ?

Progression à expliquer :
1. Prédire exige d'exploiter des régularités présentes dans les données et le contexte.
2. L'entraînement ajuste des paramètres qui encodent des représentations distribuées, pas une table explicite de réponses.
3. Les régularités apprises peuvent être réutilisées dans des contextes et tâches différents.
4. Le transfert dépend des données, de l'objectif, de l'échelle, de la tâche et du protocole d'évaluation.
5. Une capacité observée ne prouve ni compréhension humaine ni généralisation universelle.

Avant de créer une page, examiner précisément `llm-limits.qmd`, `post-training.qmd`, `in-context-learning.qmd`, `scaling-laws.qmd`, `emergence.qmd` et `llm-evolution.qmd`. Enrichir un propriétaire existant si le propos y trouve naturellement sa place. Une page autonome n'est justifiée que si cette question reste sans propriétaire et qu'un pont de parcours est réellement nécessaire.

La perspective « intelligence et compression » peut fournir une intuition : apprendre des régularités peut produire des représentations plus compactes et des prédictions utiles. La présenter comme une perspective explicative, non comme une définition exhaustive de l'intelligence. Distinguer compression statistique, représentation, prédiction et intelligence ; renvoyer aux sources déjà ingérées et à leurs limites.

### D. Limites et évaluation — conserver le propriétaire canonique

Propriétaire : `llm-limits.qmd`, complété par la page d'évaluation expérimentale et les exercices existants.

Y conserver : probabilité vs vérité, plausibilité/hallucination, ce que l'objectif garantit ou non, critères opérationnels de « compréhension », capacités dites émergentes et dépendance aux métriques/protocoles, différence entre évaluer le modèle et le système assistant. Le panorama garde un avertissement synthétique et un lien.

### E. Apprentissage et adaptation — conserver les propriétaires existants

Propriétaires : `training-loop.qmd`, `post-training.qmd`, `loss.qmd`, `gradients.qmd` et exercices correspondants.

Y conserver : pré-entraînement auto-supervisé, base model vs foundation model, loss/gradients/optimisation/validation, SFT/instruction tuning et méthodes à préférences, paramètres modifiés vs contexte fixe. Le panorama donne seulement le cycle de vie et les termes utiles.

### F. Où se trouve l'information ? — approfondissement modulaire

Répartir selon les propriétaires :
- paramètres et connaissances apprises : pré-entraînement / post-entraînement ;
- contexte et ICL : `in-context-learning.qmd` ;
- construction du contexte : `context-engineering.qmd` ;
- recherche externe, RAG et mémoire : `rag-memory-boundaries.qmd` ;
- cache KV : `generation.qmd` et pages de serving.

Conserver la chaîne « source disponible → préparée/indexée → récupérée → transmise → éventuellement exploitée » dans la page RAG/context engineering. Garder explicitement la différence entre mémoire applicative persistante et cache KV temporaire.

### G. Histoire et évolution — Deepen / Reference

Propriétaires : `transformer-history.qmd` et `llm-evolution.qmd`. Le panorama garde un bref repère et des liens. Préserver jalons, compromis et nuances ; ne pas réduire l'histoire à « l'attention a tout changé » ni confondre parallélisme d'entraînement et génération autorégressive séquentielle.

### H. Choisir une approche et comprendre l'assistant comme système

Répartir entre les propriétaires post-training / context engineering / RAG et la page canonique de systèmes/outils à identifier avant édition. Préserver les critères qualité, erreurs, robustesse, coût, latence, confidentialité et maintenance. Préserver aussi la distinction entre requête structurée produite par le modèle et autorisation/exécution par le runtime.

## 4. Matrice de conservation — aucune information perdue

| Contenu actuel | Destination cible | Règle de conservation |
|---|---|---|
| Accroche Astérix, préfixe et continuation | Panorama + Generation | Garder le fil rouge et les valeurs fictives cohérentes ; éviter de dupliquer l'explication complète. |
| Modèle vs assistant/application | Panorama + page système | Repère immédiat ; détails runtime/outils chez le propriétaire système. |
| Définition LLM / GPT | Panorama | Définition courte ; ne pas assimiler tous les LLM aux GPT ni aux Transformers. |
| Token, contexte, paramètres | Text data / Generation / Glossary | Définitions canoniques et rappels minimaux. |
| Tableau 0,6 / 0,2 / 0,1 / 0,1 | Generation et exemples qui le réutilisent | Préserver valeurs, statut fictif et cohérence inter-pages. |
| Distribution conditionnelle | Probabilités / Generation | Garder l'ancrage : les candidats se partagent 1 pour un contexte donné. |
| Schéma en six étapes | Panorama simplifié + spine computationnel | Garder vue générale, figure détaillée ou destination et alternative textuelle. |
| Texte → tokens → embeddings → Transformer → logits → sélection | Guided route + pages canoniques | Ne pas recopier le cours des composants dans le panorama. |
| Génération / scoring / apprentissage | Spine + Generation / Likelihood / Training | Trois usages frères du calcul, pas trois étapes d'une exécution unique. |
| Prefill / decode | Generation | Conserver leur rôle de phases d'inférence. |
| Vraisemblance / surprisal / entropie / loss / gradients / teacher forcing | Pages mathématiques et entraînement | Déplacer les explications détaillées et garder les distinctions exactes. |
| LLM / Transformer / GPT et familles | Panorama + Transformer architectures | Résumé et renvoi dans le panorama ; comparaison complète chez le propriétaire. |
| Architecture / apprentissage / utilisation | Panorama | Conserver comme cadre mental central. |
| Pré-entraînement / base / foundation / SFT / préférences | Training loop / Post-training | Préserver définitions, ordre et paramètres modifiés. |
| Paramètres / fine-tuning / RAG / contexte | Post-training / ICL / Context engineering / RAG | Répartir par propriétaire, maintenir les frontières. |
| Mémoire applicative / cache KV | RAG-memory / Generation | Ne pas les présenter comme des mémoires équivalentes. |
| Transfert / généralisation | Propriétaire à arbitrer avec LLM limits et post-training | Ajouter explication explicite, sourcée et bornée. |
| Histoire des Transformers | Transformer history | Déplacer le développement, garder le lien. |
| Choisir modèle / RAG / adaptation | Pages d'adaptation et récupération | Garder tous les critères de décision. |
| Assistant, rôles, tool calling, runtime | Page système canonique à identifier | Préserver le fait que le runtime autorise/exécute et renvoie le résultat. |
| Références et liens | Propriétaires pertinents + références | Conserver provenance, liens et ancres utiles. |

**Contrôle de non-régression :** avant tout déplacement, inventorier titres, paragraphes, figures, légendes/alt, exemples, équations, liens, références et activités. Après déplacement, vérifier leur présence dans la destination ou leur fusion explicite avec conservation de l'information. Un doublon textuel peut disparaître uniquement si l'information et ses nuances restent accessibles dans un propriétaire canonique et que les renvois fonctionnent.

## 5. Articulation avec le parcours

Le registre canonique reste `data/guided-route.yml`. Ne créer ni route ni registre parallèle.

- **Understand :** le panorama reste l'orientation de la première étape et mène à Generation. La route conceptuelle garde ses étapes existantes : orientation → texte/tokens → représentations → calcul Transformer → prédiction → inférence → contexte/adaptation → scoring → apprentissage. Une éventuelle page sur les capacités/généralisation ne devient pas une nouvelle étape obligatoire ; elle est rattachée comme ressource optionnelle à l'étape la plus pertinente après vérification des sémantiques et projections.
- **Build :** reste indépendant. Les liens vers code/tests et G0–G9 sont des passerelles contextuelles, jamais des prérequis d'Understand.
- **Deepen :** histoire, dérivations, lois d'échelle, émergence, compression, architectures avancées et serving avancé restent facultatifs.
- **Practice & experiment :** relier les activités existantes avant d'en créer. Toute simulation précise si elle utilise des valeurs fictives, un petit modèle réel ou un modèle externe, et ce qu'elle ne prouve pas.

Expériences candidates à évaluer (pas à créer automatiquement) : varier le contexte et observer une distribution ; tracer une génération token par token ; comparer plausibilité et vérité ; observer une loss sur un petit modèle ; comparer mémorisation et généralisation sur un jeu contrôlé ; suivre la chaîne RAG de la source au contexte transmis.

## 6. Articulation avec les issues existantes

| Issue | Propriété actuelle | Conséquence |
|---|---|---|
| [#130](https://github.com/JM-Brun/llm-lab/issues/130) | Coordination learning-design/curriculum | Parent et coordination ; rattacher le présent plan. |
| [#108](https://github.com/JM-Brun/llm-lab/issues/108) | Panorama bilingue initial, livrée par PR #343 | Ne pas rouvrir/recréer son périmètre ; préserver ses critères et contenus intégrés. |
| [#971](https://github.com/JM-Brun/llm-lab/issues/971) | Retour apprenant et revue source du parcours | Réutiliser les observations et correctifs déjà traités ; ne pas répéter les audits. |
| [#1051](https://github.com/JM-Brun/llm-lab/issues/1051) | Intégration ciblée Microsoft Learn aux pages canoniques | Coordonner les enrichissements, sans chapitre concurrent ni copie de source. |
| [#1109](https://github.com/JM-Brun/llm-lab/issues/1109) | Fiches de synthèse bilingues | Réutiliser ses décisions ; le panorama n'est pas automatiquement une fiche infographique. |
| [#280](https://github.com/JM-Brun/llm-lab/issues/280) | Convergence du corpus et archétypes | Réutiliser inventaire/critères ; pas de nouvel audit général. |
| [#282](https://github.com/JM-Brun/llm-lab/issues/282) | Pilote borné de revue de pages/templates | Ne pas élargir rétroactivement ; réutiliser résultats et lots de rendu. |
| [#337](https://github.com/JM-Brun/llm-lab/issues/337) | Navigation/curriculum rendu FR/EN | Vérifier les nouvelles destinations/liens au moment de la validation. |
| [#368](https://github.com/JM-Brun/llm-lab/issues/368) | Contrat souple de pages, clôturé | Réutiliser l'anatomie existante ; pas de template rigide ni de durée obligatoire. |
| [#575](https://github.com/JM-Brun/llm-lab/issues/575) / [#584](https://github.com/JM-Brun/llm-lab/issues/584) | Colonne vertébrale computationnelle | Réutiliser génération/scoring/apprentissage et graphes canoniques ; pas de second graphe. |
| [#78](https://github.com/JM-Brun/llm-lab/issues/78) | Séquençage concept-vers-code / Build | Vérifier les passerelles, sans transformer Build en prérequis. |
| [#756](https://github.com/JM-Brun/llm-lab/issues/756) / [#764](https://github.com/JM-Brun/llm-lab/issues/764) | Audits de projets comparables / visuels | Réutiliser les conclusions vérifiées ; ne pas copier les actifs tiers. |

Toute proposition nouvelle doit être classée : (a) déjà couverte, (b) correction d'un propriétaire, (c) déplacement/fusion, (d) nouvelle page réellement nécessaire, ou (e) validation. Mettre à jour/lier l'issue propriétaire ; créer une issue seulement pour un lot distinct avec livrable et critères propres.

## 7. Plan d'exécution

### Lot 0 — Inventaire et arbitrage
- Comparer intégralement FR/EN.
- Inventorier chaque section, figure, tableau, exemple, formule, callout, lien, référence et activité.
- Estimer la durée de lecture par destination ; ne pas traiter la durée comme un quota.
- Comparer chaque bloc à son propriétaire et aux issues existantes.
- Produire la matrice exhaustive source → destination FR/EN → propriétaire → action (garder, fusionner, déplacer, remplacer par renvoi).
- Décider si le pont généralisation/capacités appartient à LLM limits, post-training, ou justifie une page autonome.

### Lot 1 — Panorama court FR/EN
- Réordonner le récit sans toucher aux explications spécialisées.
- Préserver fil rouge, modèle/application, cycle de vie, architecture/apprentissage/utilisation et limites de premier niveau.
- Simplifier la figure d'ouverture ; conserver la figure détaillée ou la déplacer avec texte alternatif.
- Ajouter objectifs/durée seulement s'ils sont spécifiques et crédibles.

### Lot 2 — Fusion/déplacement vers les propriétaires
- Déplacer les développements complets et fusionner avec l'existant.
- Si une page cible dépasse 15 minutes, revoir son périmètre ou placer le détail en Deepen.
- Corriger liens entrants/sortants, ancres, métadonnées et descriptions de périmètre.
- Régénérer les projections à partir des sources canoniques, jamais à la main.

### Lot 3 — Pont capacités/généralisation
- Expliquer et sourcer objectif → régularités → représentations → transfert → capacités observées.
- Distinguer faits empiriques, interprétations mécanistiques, hypothèses et analogies.
- Traiter la compression comme une perspective utile mais non exhaustive.

### Lot 4 — Navigation, pratique et validation
- Réconcilier guided-route, métadonnées, page map, sidebar et transitions.
- Vérifier parité FR/EN, ancres, liens, figures, alt text, glossaire et références.
- Exécuter tests documentaires, CI et Quarto ; rapporter séparément rendu navigateur et retour apprenant.
- Revue rendue desktop/mobile, clavier et accessibilité pertinente ; ne pas assimiler axe automatisé à une revue lecteur d'écran.
- Organiser une vraie lecture apprenant ; relever durée, confusions, retours arrière et réussite aux activités.

## 8. Critères d'acceptation

- [ ] Panorama FR/EN clair et cohérent en environ 8–10 min, 15 min maximum sans justification.
- [ ] Tout contenu hors budget possède une destination canonique identifiée ; aucune information substantielle perdue.
- [ ] Matrice exhaustive de conservation : source, destination, action, preuve.
- [ ] Chaque concept détaillé possède un propriétaire ; les autres pages rappellent et renvoient.
- [ ] Pont prédiction → régularités/représentations → transfert/capacités expliqué avec prudence scientifique.
- [ ] Distinctions architecture/apprentissage/utilisation et modèle/application/runtime conservées.
- [ ] Génération, scoring et entraînement restent des usages frères.
- [ ] Understand, Build, Deepen et Practice gardent leurs rôles ; aucune route parallèle.
- [ ] Issues existantes coordonnées ; pas de réouverture d'issues closes sans défaut nouveau.
- [ ] Parité sémantique, scientifique et navigation FR/EN.
- [ ] Liens, figures, alt, références, métadonnées et projections validés.
- [ ] CI/Quarto, rendu navigateur et retour apprenant rapportés comme preuves distinctes.

## 9. Garde-fous

Ne pas supprimer une section parce qu'elle est longue : lui trouver un propriétaire ou la fusionner. Ne pas transformer le panorama en catalogue de liens. Ne pas créer une page avant d'avoir vérifié les propriétaires existants. Ne pas confondre intuition et preuve. Ne pas affirmer que les LLM comprennent comme les humains, ni l'inverse sans critère. Ne pas présenter la compression comme définition complète de l'intelligence. Ne pas faire de Practice un parcours linéaire, ni de Build un prérequis d'Understand.

## 10. Synthèse

Le contenu actuel est précieux. La refonte doit **réduire la charge du premier contact en redistribuant la matière**, pas amputer les connaissances. Le panorama répond rapidement à « qu'est-ce qu'un LLM et quelle est la carte de son fonctionnement ? ». Generation explique la boucle ; les pages canoniques enseignent composants, apprentissage, adaptation, limites et systèmes ; Deepen accueille histoire, dérivations et débats ; Practice vérifie les intuitions.

Le principal enrichissement conceptuel est le passage de l'objectif de prédiction aux capacités transférables. Le principal garde-fou opérationnel est la matrice de conservation : chaque information déplacée a une destination vérifiée en français et en anglais avant que le texte source soit raccourci.


## 11. Lot 0 — premiers constats vérifiés sur les sources actuelles

Cette section complète le diagnostic initial à partir des deux fichiers Quarto et du registre canonique consultés sur la branche de travail le 2026-11-18. Elle ne vaut pas encore inventaire exhaustif paragraphe par paragraphe.

### Mesure de départ

| Indicateur | Français | English | Interprétation |
|---|---:|---:|---|
| Volume lexical brut du fichier Quarto | ~4 872 mots | ~4 476 mots | Comptage indicatif du source, qui inclut certains éléments techniques et textes alternatifs ; à recalculer sur le rendu lisible. |
| Durée à 180 mots/min | ~27 min | ~25 min | Confirme que les pages sont des mini-cours, pas encore des panoramas d'orientation de 8–10 min. |
| Sections de premier niveau | 8 | 8 | Les deux versions partagent la même ossature thématique. |
| Sections de second niveau dans le bloc historique/capacités | 3 | 3 | La partie histoire/transfert est déjà développée dans les deux langues. |

Le différentiel de volume FR/EN (~9 %) ne prouve pas à lui seul un défaut de parité, mais impose une comparaison sémantique et de densité lors de la refonte. Ne pas raccourcir mécaniquement la langue la plus longue : vérifier les exemples, nuances, réserves, références, exercices et renvois.

### Ce que les sources montrent déjà

- Les deux pages contiennent déjà le pont « prédiction du prochain token → régularités apprises → transfert vers d'autres tâches ». Il faut donc **auditer et améliorer ce contenu existant**, pas créer une nouvelle page ou une nouvelle étape pour combler un manque supposé.
- Les deux pages incluent déjà les sections sur la résidence de l'information, l'histoire et les changements apportés par les Transformers, le transfert, le choix entre modèle/RAG/adaptation, et le modèle versus le système conversationnel. Ce sont précisément les zones candidates à redistribuer vers les propriétaires canoniques.
- Le bloc « un calcul, trois usages » exprime correctement trois usages frères. Il ne doit pas devenir une progression pédagogique « génération puis scoring puis entraînement ».
- Les deux fichiers incluent des fragments générés : contexte guidé, route suggérée et couverture. Ils doivent rester des projections produites depuis leurs registres, pas des contenus à maintenir manuellement.
- Les métadonnées `suggested_route`, `hierarchy`, `covered_stages` et `related` ont des fonctions de navigation/classement distinctes. Elles ne doivent pas être transformées en un second séquencement d'apprentissage.

### Décision sur le pont capacités/transfert

Le contenu existant de « Pourquoi prédire le prochain token aide-t-il pour d'autres tâches ? » est le point de départ. Le travail doit :
1. vérifier ses affirmations et références, notamment le statut de « représentations distribuées » et les limites de l'explication par compression ;
2. conserver les trois voies distinctes : adaptation des paramètres, modification du contexte/ICL, apport d'information externe/RAG ;
3. faire la différence entre mécanisme établi, interprétation, hypothèse et analogie ;
4. déplacer le développement vers le propriétaire existant le plus cohérent après lecture de `llm-limits.qmd`, `post-training.qmd`, `in-context-learning.qmd`, `scaling-laws.qmd`, `emergence.qmd` et `llm-evolution.qmd` ;
5. ne pas créer de page autonome ni de nouvelle étape de parcours à ce stade.

## 12. Gouvernance stricte du parcours — aucune route parallèle

### Source de vérité

`data/guided-route.yml` est l'unique source de vérité pour l'ordre et les transitions du parcours Understand. Toute évolution de séquence, de prérequis ou de transition doit être faite dans ce fichier, puis propagée par les générateurs existants. La refonte du panorama ne modifie pas ce registre, sauf si un défaut réel du parcours est démontré et traité dans le périmètre de son propriétaire (#130 et issues de curriculum concernées).

### Rôle autorisé du panorama

Le panorama peut :
- dire en une phrase qu'il constitue le point d'orientation initial du parcours Understand ;
- renvoyer vers la vue canonique du parcours et vers l'étape suivante définie par le registre ;
- présenter une carte **non séquencée** des grandes questions auxquelles les pages du projet répondent ;
- distinguer les deux parcours principaux indépendants (Understand et Build), l'approfondissement facultatif (Deepen) et la pratique transversale (Practice & experiment) ;
- proposer des liens contextuels vers des pages utiles, sans les présenter comme prérequis.

Le panorama ne peut pas :
- recopier la liste des étapes Understand, même sous la forme d'une « feuille de route », d'un « itinéraire conseillé » ou d'une succession numérotée ;
- créer une nouvelle séquence locale, des prérequis, des étapes intermédiaires ou une route alternative ;
- présenter les liens « à lire ensuite » comme un ordre obligatoire lorsqu'il s'agit de ressources complémentaires ;
- transformer les trois usages (générer, scorer, apprendre) en étapes successives ;
- introduire un « parcours capacités/transfert » parallèle ou une nouvelle étape obligatoire issue du pont explicatif ;
- maintenir manuellement le contenu des fragments `generated-*`.

### Ne pas confondre les registres

| Élément | Fonction | Ce qu'il ne doit pas devenir |
|---|---|---|
| `data/guided-route.yml` | Ordre canonique, étapes, ressources et transitions Understand | Un catalogue exhaustif de toutes les pages |
| `learning-map.qmd` et ses projections | Explorer le corpus, ses territoires, pages et concepts ; afficher le parcours canonique | Un second parcours ou un graphe de prérequis implicites |
| Métadonnées `LLM-LAB-PAGE-MAP` | Décrire la portée, la hiérarchie éditoriale et les étapes couvertes pour les projections | Un ordre de lecture autonome |
| `suggested_route` | Navigation locale précédente/suivante d'une page | Une route concurrente du registre |
| `related` | Liens de proximité thématique | Une liste de prérequis |
| Build path | Parcours d'implémentation indépendant | La suite obligatoire d'Understand |
| Deepen | Ressources facultatives d'approfondissement | Une troisième route obligatoire |
| Practice & experiment | Activités mobilisables transversalement | Un cursus linéaire supplémentaire |

### Règles de mise en œuvre

1. Avant modification, relever tous les liens, inclusions, blocs et libellés de parcours dans les versions FR et EN.
2. Garder les inclusions générées lorsqu'elles affichent une projection utile du registre ; si elles produisent une répétition ou un encadré redondant, corriger leur source/générateur ou leur emplacement, jamais le fichier généré à la main.
3. Dans le panorama raccourci, remplacer toute liste d'étapes par un lien unique et explicite vers la vue canonique Understand ; conserver uniquement les liens contextuels nécessaires à la compréhension locale.
4. Ne pas modifier `data/guided-route.yml` pour satisfaire le budget de longueur du panorama.
5. Ne pas ajouter de nouvelle valeur `covered_stages` ni de page dans `optional_pages` sans vérifier les conventions de génération et l'impact sur les vues.
6. Pour chaque PR, contrôler qu'aucune nouvelle route, séquence numérotée, chaîne de prérequis ou projection maintenue manuellement n'a été introduite.
7. Vérifier le rendu FR et EN de la page et de la carte d'apprentissage ; le source seul ne suffit pas à valider l'absence de doublons visuels.

### Critères d'acceptation supplémentaires

- [ ] Le seul ordre Understand affiché provient de `data/guided-route.yml`.
- [ ] Le panorama ne contient aucune séquence locale concurrente, même non numérotée si elle implique un ordre obligatoire.
- [ ] Les liens thématiques sont clairement optionnels/contextuels.
- [ ] Build reste indépendant, Deepen facultatif et Practice transversal.
- [ ] Les inclusions et cartes générées restent des projections, jamais des sources éditoriales secondaires.
- [ ] Le pont transfert/capacités est intégré à un propriétaire existant ou, si une lacune est démontrée, proposé au propriétaire du curriculum avant toute création.


## 13. Capacité réelle des pages propriétaires — ne pas déplacer la surcharge

Le principe « déplacer vers le propriétaire canonique » ne signifie pas y transférer un bloc entier sans mesurer sa capacité. Un propriétaire déjà dense doit être allégé, redistribué dans ses sous-sections existantes ou faire l'objet d'un arbitrage de périmètre avant de recevoir de nouveaux développements.

Mesure indicative des fichiers actuels (comptage lexical brut, à confirmer sur rendu, estimation à 180 mots/min) :

| Propriétaire | FR | EN | Durée indicative FR / EN | Décision de capacité |
|---|---:|---:|---:|---|
| `generation.qmd` | ~3 186 | ~3 018 | 17,7 / 16,8 min | Déjà au-dessus de 15 min : conserver la boucle comme cœur, évaluer le déplacement des détails de serving/cache vers leur propriétaire existant ou Deepen. Ne pas y déverser le panorama. |
| `llm-limits.qmd` | ~1 596 | ~1 435 | 8,9 / 8,0 min | Bon candidat pour le pont objectif/limites/transfert si le contenu est bien de sa responsabilité ; vérifier la place des cas d'évaluation. |
| `post-training.qmd` | ~1 905 | ~1 701 | 10,6 / 9,5 min | Capacité limitée mais raisonnable ; n'y déplacer que les notions d'adaptation des paramètres. |
| `in-context-learning.qmd` | ~1 153 | ~1 040 | 6,4 / 5,8 min | Peut accueillir les explications ICL actuellement dispersées, sans répéter context engineering. |
| `context-engineering.qmd` | ~2 143 | ~1 919 | 11,9 / 10,7 min | Proche du plafond : ne pas lui transférer tout le bloc information/mémoire ; coordonner avec RAG boundaries. |
| `rag-memory-boundaries.qmd` | ~3 024 | ~2 626 | 16,8 / 14,6 min | FR dépasse déjà le plafond : répartir avec context engineering et approfondissements existants, sans créer un chapitre concurrent. |
| `transformer-history.qmd` | ~1 317 | ~1 172 | 7,3 / 6,5 min | Peut accueillir les jalons historiques, mais le panorama ne doit pas lui transférer le pont de capacités entier. |
| `llm-evolution.qmd` | ~2 676 | ~2 407 | 14,9 / 13,4 min | Très proche du plafond : ne pas y déplacer en bloc histoire, compression, transfert et outils. |
| `training-loop.qmd` | ~3 129 | ~2 795 | 17,4 / 15,5 min | Déjà trop dense : ne pas lui transférer la totalité des explications sur loss/gradients/teacher forcing ; conserver les propriétaires mathématiques. |

**Conséquence éditoriale :** la matrice de conservation doit être enrichie avec une colonne « capacité/durée de la destination avant et après déplacement ». Tout déplacement qui ferait dépasser 15 minutes à une page cible doit déclencher une redistribution entre propriétaires déjà établis, une clarification du périmètre ou un approfondissement optionnel. Ne pas créer une nouvelle page uniquement pour respecter un compteur de mots : une nouvelle page exige une question pédagogique autonome, un propriétaire explicite, un emplacement dans les destinations existantes et l'accord du propriétaire du curriculum.

Les durées ci-dessus sont des signaux de densité, pas des normes absolues. Les formules, figures, exercices et difficultés conceptuelles peuvent ralentir la lecture ; le test final reste le rendu et une lecture réelle.
