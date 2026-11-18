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
