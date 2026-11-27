# Fil rouge narratif et clin d'œil culturel — contrat éditorial et audit

**État :** audit source-level initial, recommandations à appliquer de façon incrémentale  
**Date :** 2026-11-26  
**Périmètre :** parcours Theory / Understand, cohérence FR/EN, exemples de génération, scoring et apprentissage  
**Références :** [noyau computationnel canonique](canonical-computational-spine.md), [parcours principal et travail restant](curriculum-main-route-remaining-work.md), [route bilingue](../data/guided-route.yml), [issue #575](https://github.com/JM-Brun/llm-lab/issues/575), [intégration Build différée #924](https://github.com/JM-Brun/llm-lab/issues/924).

Ce document consigne l'audit du fil rouge narratif (dont le clin d'œil culturel) dans le parcours. Il ne définit ni un nouveau parcours, ni un registre de concepts, ni un second graphe computationnel. Il complète les sources canoniques existantes par un contrat éditorial et un relevé de travail.

## 1. Décision éditoriale

Le fil rouge doit être un **support récurrent de raisonnement**, pas une citation décorative répétée dans toutes les pages.

Il sert à faire suivre au lecteur une situation reconnaissable à travers plusieurs opérations : texte fourni, tokenisation, représentations, calcul de la distribution, génération, scoring d'une continuation observée, loss et mise à jour des paramètres.

Le clin d'œil culturel est une porte d'entrée facultative. Il ne doit jamais être nécessaire pour comprendre une définition, une équation, un algorithme ou un résultat. Chaque réapparition doit apporter une fonction pédagogique nouvelle ou rendre explicite une relation déjà étudiée.

Le parcours français et le parcours anglais peuvent employer des références narratives localisées différentes. La parité attendue est **conceptuelle et computationnelle**, pas une identité littérale des textes. Chaque langue doit toutefois conserver une chaîne d'exemple stable à l'intérieur de ses propres pages.

## 2. Contrat de cohérence

### 2.1 Invariants

1. **Préfixe et continuation sont distincts.** Le préfixe est le contexte fourni au modèle ; la continuation est produite ou observée après ce préfixe.
2. **Ne pas confondre scène culturelle et trace de calcul.** Si une scène met en jeu plusieurs interlocuteurs, préciser qu'elle sert d'accroche et introduire une continuation illustrative à un seul locuteur pour les calculs autorégressifs.
3. **Une chaîne stable par langue.** Les pages d'une même langue réutilisent le même préfixe canonique et la même continuation de référence, sauf si une variante est annoncée et justifiée.
4. **Les variantes sont typées.** Distinguer explicitement : continuation générée (sortie possible), continuation de référence (cible observée), branche contrefactuelle (autre cible possible) et exemple indépendant (illustration locale sans prétention de continuité).
5. **Les nombres sont cohérents ou leur changement est expliqué.** Une distribution jouet doit garder les mêmes candidats, ordre, probabilités et cible lorsqu'elle est réutilisée pour entropie, surprisal, scoring, cross-entropy et gradient. Une nouvelle distribution après ajout d'un token correspond à un nouveau préfixe et doit être présentée comme telle.
6. **Les tokens ne sont pas déduits de la typographie.** Toute trace qui dépend du découpage exact doit annoncer le tokenizer et sa configuration, ou déclarer explicitement une convention jouet. Ne pas laisser entendre que « Vous », « savez » ou une ponctuation sont universellement un token chacun.
11. **Le fil rouge est l'exemple principal de tokenisation.** La leçon part du préfixe canonique de sa langue ; elle ne lui substitue pas un exemple sans lien comme `hello world`. Les mots visibles (« situation », « scribe », « Romans ») servent à observer le découpage réel, mais ne sont jamais déclarés tokens isolés sans vérification. Toute comparaison entre tokenizers réencode le même préfixe, afin de ne faire varier que le tokenizer.
7. **Les paramètres restent fixes hors entraînement.** Génération, ICL, context engineering et scoring modifient le contexte ou la cible, pas les poids. Seule la branche d'apprentissage applique gradients et optimiseur.
8. **Le fil rouge reste subordonné à l'objectif de la page.** Une page de théorie peut l'omettre si son ajout n'améliore ni intuition, ni démonstration, ni transfert.
9. **La traduction n'est pas une substitution mécanique.** Une localisation peut changer les noms et la référence culturelle, mais elle doit préserver les rôles formels, les transitions, les hypothèses, les résultats numériques et les distinctions conceptuelles.
10. **La provenance et le statut éditorial sont maîtrisés.** Les informations internes sur l'origine du clin d'œil ne doivent pas fuiter dans les métadonnées publiques si le choix éditorial est de le laisser non attribué. Les références de travail restent dans les dossiers internes appropriés.

### 2.2 Trois usages de la même distribution

Pour un préfixe c, le modèle calcule pθ(· | c). À partir de cette distribution :

- **Générer :** une politique de décodage sélectionne un token ; ce token est ajouté au contexte avant le tour suivant.
- **Scorer :** une cible observée y est évaluée par pθ(y | c) ; le préfixe suivant est celui de la séquence de référence, pas celui d'un token librement choisi.
- **Entraîner :** les pénalités des cibles observées sont agrégées dans un objectif, puis différentiées ; l'optimiseur met à jour les paramètres.

Ne pas représenter ces usages comme une seule boucle d'exécution. Cette distinction est déjà définie dans le document architectural canonique et reste la référence.

## 3. État observé dans les pages

L'audit ci-dessous est une inspection des sources Quarto du dépôt au 2026-11-26. Il ne constitue pas une validation du rendu publié ni une étude auprès d'apprenants.

### 3.1 Français

Le scénario principal est le préfixe :

> « C'est une bonne situation, ça, scribe ? »

Les pages suivantes le réutilisent de manière identifiable :

| Zone du parcours | État observé | Fonction pédagogique |
|---|---|---|
| Panorama | Le préfixe introduit la prédiction du prochain token et la distinction contexte / continuation. | Donner une question concrète au mécanisme central. |
| Logits et probabilités | Le préfixe est associé à un vocabulaire jouet ; « Vous » reçoit 0,6, « Je » 0,2, puis deux autres candidats complètent la distribution. | Relier la projection de sortie, les logits et la softmax. |
| Entropie | La distribution (0,6 ; 0,2 ; 0,1 ; 0,1) est réutilisée. | Calculer la dispersion avant observation et distinguer entropie et surprisal. |
| Génération | Le premier choix « Vous » est ajouté au préfixe ; une nouvelle distribution est calculée au tour suivant. | Montrer la boucle autorégressive, le changement de contexte et le maintien des paramètres. |
| Vraisemblance | La continuation observée « Vous savez , » est scorée avec les probabilités conditionnelles annoncées. | Distinguer une cible de référence d'un token sélectionné en génération. |
| Loss | Les probabilités illustratives 0,6, 0,5 et 0,8 sont reprises pour construire les pénalités locales et la NLL de séquence. | Passer du score d'une cible à l'agrégation de la loss. |
| Gradients et boucle d'entraînement | La première cible « Vous » et la distribution initiale sont réutilisées pour calculer le gradient, puis illustrer une mise à jour SGD. | Relier le calcul local à la modification des paramètres. |
| Représentations contextualisées | Le mot « situation » est mobilisé dans deux contextes de sens différents. | Donner un exemple linguistique du rôle du contexte sur les représentations. |

Pages de référence : [panorama FR](../site/fr/llm-overview.qmd), [logits](../site/fr/logits.qmd), [probabilités](../site/fr/probabilites.qmd), [entropie](../site/fr/entropy.qmd), [génération](../site/fr/generation.qmd), [vraisemblance](../site/fr/vraisemblance.qmd), [cross-entropy](../site/fr/cross-entropy.qmd), [loss](../site/fr/loss.qmd), [gradients](../site/fr/gradients.qmd), [boucle d'entraînement](../site/fr/training-loop.qmd), [représentations contextualisées](../site/fr/contextualized-representations.qmd).

**Constat :** le scénario traverse effectivement une grande partie du noyau Understand, jusqu'à l'apprentissage. La réutilisation numérique entre probabilités, entropie, scoring et gradients est un point fort. La page de vraisemblance emploie une continuation observée courte ; la convention selon laquelle les unités affichées sont traitées comme des tokens pour ce calcul doit rester explicitement jouet et ne pas être confondue avec le tokenizer réel.

### 3.2 Anglais

Le parcours anglais localise l'accroche autour de :

> “What have the Romans ever done for us?”

La page de panorama distingue explicitement la scène collective d'une continuation illustrative originale à un seul locuteur :

> “They built roads between distant towns.”

Les pages d'entropie, de probabilités, de cross-entropy, de loss, de gradients et de boucle d'entraînement reprennent la distribution jouet dont “They” reçoit 0.6 et “Aqueducts” 0.2. La page d'embeddings rappelle que la scène et la continuation calculatoire ont des rôles différents.

Pages de référence : [overview EN](../site/en/llm-overview.qmd), [embeddings](../site/en/embedding-space.qmd), [generation](../site/en/generation.qmd), [probabilities](../site/en/probabilities.qmd), [entropy](../site/en/entropy.qmd), [likelihood](../site/en/likelihood.qmd), [cross-entropy](../site/en/cross-entropy.qmd), [loss](../site/en/loss.qmd), [gradients](../site/en/gradients.qmd), [training loop](../site/en/training-loop.qmd).

**Constat :** l'anglais dispose lui aussi d'une chaîne cohérente de calculs, mais sa référence culturelle et son exemple de continuation sont localisés. La bonne exigence est de préserver la correspondance des rôles et des raisonnements, non de forcer la même citation dans les deux langues.

### 3.3 Différences et limites identifiées

- Les deux langues n'utilisent pas le même préfixe culturel ni les mêmes tokens-cibles. C'est acceptable si les correspondances formelles restent explicites.
- Les pages de contextualisation ne reproduisent pas exactement la même démonstration linguistique : le français exploite la polysémie de « situation » ; l'anglais compare notamment des occurrences de “Romans”. Ces exemples locaux sont complémentaires, pas des traductions ligne à ligne.
- La page ICL utilise actuellement un exemple indépendant de classification sentimentale. Elle explique correctement l'adaptation par le prompt à paramètres fixes, mais ne prolonge pas le fil rouge narratif.
- La page de context engineering utilise un scénario indépendant d'assistant répondant sur un dépôt logiciel. Il est pertinent pour la conception de contexte applicative ; le remplacer par le clin d'œil serait une régression de réalisme.
- Le parcours Build emploie des IDs et séquences synthétiques pour ses contrats de code et ses tests. C'est légitime : le fil rouge narratif ne doit pas imposer des IDs inventés ni se substituer aux fixtures testables.

## 4. Carte d'utilisation recommandée dans le parcours

| Étape Understand (source data/guided-route.yml) | Usage du fil rouge | Décision |
|---|---|---|
| Orientation | Accroche et aperçu de deux tours de prédiction. | Conserver ; expliciter préfixe et continuation. |
| Texte → tokens | Préfixe canonique de la langue, fragments et IDs calculés avec un tokenizer déterminé ; comparaison éventuelle sur ce même texte. | Exemple principal = fil rouge ; aucun exemple déconnecté ne le remplace. |
| Représentations | Lookup, position, contextualisation ; réutiliser une ambiguïté lexicale utile. | Conserver les exemples locaux pertinents ; ne pas répéter la citation entière. |
| Calcul du Transformer | Suivre une ou deux positions du même préfixe dans un bloc, si les dimensions et valeurs sont effectivement définies. | Optionnel ; priorité à la justesse des tenseurs et des opérations. |
| États → distribution | Réutiliser les candidats et la distribution jouet canonique de la langue. | Conserver la cohérence logits → softmax. |
| Génération | Sélection puis réinjection ; nouveau préfixe et nouvelle distribution. | Conserver ; distinguer distribution illustrative du résultat d'un modèle réellement entraîné. |
| Contexte / ICL | Comparer le prompt initial et un prompt enrichi à paramètres fixes. | Ajouter éventuellement une courte expérience de transfert ; ne pas remplacer les exemples spécialisés ICL/context engineering. |
| Scoring | Évaluer la continuation de référence avec les préfixes observés successifs. | Conserver ; aucune sélection de token. |
| Apprentissage | Cibles observées → NLL/cross-entropy → loss → gradients → update. | Conserver la chaîne numérique ; préciser ce qui est un calcul local jouet et ce qui relève de l'objectif agrégé. |

Le fil rouge n'a pas à apparaître dans toutes les pages d'approfondissement, dans chaque mécanisme d'attention, ni dans chaque exercice Build. La carte ci-dessus est une règle de pertinence, pas un quota de répétition.

## 5. Travail recommandé

### P0 — Cohérence des traces FR/EN

- [ ] Faire un tableau de correspondance explicite des préfixes, continuations, candidats, probabilités et cibles entre FR et EN ; confirmer les valeurs dans les pages sources et les calculs, pas uniquement dans les textes d'introduction.
- [x] Remplacer l'exemple principal `hello world` de la leçon de tokenisation par le préfixe localisé du fil rouge ; réutiliser ce même préfixe pour la comparaison GPT-2 / `cl100k_base` et pour le lookup synthétique de la trace.
- [ ] Vérifier que les distributions changent uniquement lorsqu'un nouveau préfixe est présenté, ou lorsque l'on introduit explicitement une branche contrefactuelle.
- [ ] Vérifier les formulations qui présentent une suite de mots comme une suite de tokens ; ajouter une convention jouet ou un tokenizer/configuration quand le découpage exact est important.
- [ ] Vérifier la cohérence des exemples entre panorama, génération, vraisemblance, loss, gradients et boucle d'entraînement après chaque évolution de contenu.

### P1 — Exploitation du contexte

- [ ] Ajouter dans la page ICL ou dans une courte expérience liée une comparaison contrôlée entre le prompt initial et un prompt enrichi, avec paramètres fixes et distributions illustratives clairement étiquetées. Conserver l'exemple de classification qui explique zero-shot / one-shot / few-shot.
- [ ] Dans context engineering, garder l'exemple applicatif du dépôt logiciel ; éventuellement ajouter un renvoi vers l'expérience du fil rouge comme illustration minimale de pθ(· | c) vs pθ(· | c').
- [ ] Ne pas prétendre qu'un changement de prompt produit un effet numérique déterminé sans logits ou sorties calculées ; si les distributions sont fictives, le dire.

### P1 — Rendu et parité

- [ ] Après les changements, contrôler le rendu FR/EN : équations, tableaux, citations, ponctuation, liens et alternatives textuelles.
- [ ] Vérifier les pages publiées après déploiement ; l'inspection des sources GitHub ne prouve pas que Pages sert déjà le même commit.
- [ ] Vérifier les métadonnées, cartes, extraits de recherche et navigation : le clin d'œil ne doit pas apparaître dans un champ interne/public non prévu par la décision éditoriale.

### P2 — Build (différé)

- [ ] Reprendre l'intégration du fil rouge dans Build selon [#924](https://github.com/JM-Brun/llm-lab/issues/924), après stabilisation des priorités de correction et de validation de la séquence G0–G9.
- [ ] Pour chaque jalon, décider si l'exemple est utile, facultatif ou volontairement absent ; ne pas le forcer dans les étapes où des IDs synthétiques ou fixtures sont plus rigoureux.
- [ ] Vérifier les IDs, formes, sorties attendues et tests depuis le code réellement exécuté ; aucune valeur de tokenisation ne doit être inventée à partir du texte.
- [ ] Maintenir Build autonome par rapport à Understand et ne pas dupliquer les explications canoniques.

## 6. Critères d'acceptation

- Une chaîne d'exemple identifiable existe dans chaque langue et reste cohérente à l'intérieur de cette langue.
- Les différences de localisation FR/EN sont intentionnelles, documentées et conceptuellement équivalentes.
- Préfixe, continuation générée, continuation observée et variantes contrefactuelles sont distingués.
- Les nombres réutilisés sont compatibles avec le préfixe, les candidats et la cible annoncés.
- Les conventions de tokenisation sont explicites dès qu'une conclusion dépend des frontières de tokens.
- L'exemple aide à distinguer génération, scoring, évaluation et apprentissage ; il ne les fusionne pas.
- Le clin d'œil reste facultatif et ne dégrade ni l'autonomie des leçons ni leur précision.
- Les contrôles source, rendu, accessibilité et compréhension des apprenants sont rapportés séparément.

## 7. Non-objectifs

- Uniformiser les références culturelles françaises et anglaises.
- Ajouter la citation dans chaque page ou chaque carte de connaissance.
- Transformer le fil rouge en prérequis du parcours Understand ou Build.
- Remplacer les exemples spécialisés (classification ICL, assistant logiciel, jeux de données, tenseurs synthétiques) lorsqu'ils répondent mieux à l'objectif local.
- Créer un registre, un graphe, un workflow ou une suite de tests parallèles.
- Déduire des IDs ou des frontières de tokens sans tokenizer effectif.

## 8. Synthèse

**Bilan :** le fil rouge est déjà utilisé de façon substantielle dans le parcours Understand, notamment pour relier la distribution prédictive, la génération, le scoring, la loss et les gradients. Sa localisation différente entre les langues est acceptable et même utile, à condition de préserver une chaîne interne stable par langue et la parité des raisonnements.

**Travail immédiat :** vérifier le rendu publié FR/EN après déploiement et poursuivre la consolidation des traces numériques FR/EN. La leçon de tokenisation utilise désormais le préfixe du fil rouge comme matériau principal, avec des IDs calculés par GPT-2 dans la trace reproductible.

**Travail ultérieur :** ajouter une petite expérience de contexte à paramètres fixes pour relier ICL/context engineering au noyau partagé, sans remplacer leurs exemples dédiés.

**Travail différé :** l'intégration Build reste explicitement portée par #924 ; elle ne doit pas être absorbée par cet audit ni bloquer les corrections prioritaires du parcours.

**Limite de preuve :** cet audit est fondé sur les sources Quarto consultées le 2026-11-26. Il ne prouve ni l'état du rendu Pages à cet instant, ni la compréhension réelle par des apprenants.