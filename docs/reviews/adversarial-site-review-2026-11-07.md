# Revue adversariale du site LLM Lab — 2026-11-07

**Périmètre :** revue critique de l'expérience publiée et de son architecture pédagogique, confrontée à l'état actuel de `main` et au backlog GitHub.  
**Nature :** audit source et de cohérence ; ce document ne constitue ni une certification exhaustive du rendu publié ni une étude d'efficacité pédagogique.

## 1. Conclusion exécutive

LLM Lab dispose désormais d'une architecture conceptuelle nettement plus cohérente que ne le laissait penser une première lecture isolée. Le graphe computationnel canonique, le graphe de concepts, le parcours guidé et le parcours Build ont des responsabilités distinctes. La colonne vertébrale computationnelle partagée entre génération, scoring, évaluation et apprentissage est intégrée.

La revue ne justifie donc **ni une nouvelle refonte générale, ni un nouveau registre, ni un nouveau système de navigation, ni une issue par page ou par notion**. La priorité est de terminer les validations ciblées déjà ouvertes, de vérifier quelques transitions pédagogiques et de confronter le dispositif à des lecteurs indépendants.

La faiblesse la plus importante n'est plus l'absence d'une architecture conceptuelle partagée. C'est l'écart restant entre :
- la cohérence démontrée par les sources et les tests ;
- la qualité réelle du rendu et de l'usage dans les situations non encore vérifiées ;
- la compréhension effective d'un lecteur indépendant.

Un build vert, une validation de schéma, un audit Axe ou une revue de code ne constituent pas, isolément, une preuve d'apprentissage.

## 2. Méthode et niveaux de preuve

Cette revue distingue :
1. **Source** : lecture des pages Quarto, registres YAML, documents d'architecture et de gouvernance.
2. **Automatisation** : tests Python, contrôles de liens, rendu Quarto, tests DOM/Chromium et Axe.
3. **Rendu observé** : inspection visuelle des captures et du comportement réel sur des viewports définis.
4. **Usage humain** : navigation et raisonnement d'un lecteur indépendant, sans guidage.

Une conclusion n'est considérée comme établie qu'au niveau de preuve effectivement disponible. Les contrôles automatisés ne sont pas présentés comme une inspection visuelle ou une étude utilisateur.

Fichiers confrontés : `site/index.qmd`, `data/guided-route.yml`, `docs/canonical-computational-spine.md`, `docs/learning-path.md`, `docs/page-audit-inventory.md`, pages FR de génération, Q/K/V et architectures Transformer, et `docs/learner-validation-pilot.md`.

## 3. Acquis à préserver

### 3.1 Une colonne vertébrale computationnelle commune

Le modèle central est désormais explicite :

`context → forward pass → logits → conditional distribution`

Cette distribution conditionnelle alimente plusieurs usages frères, et non une succession unique :
- **Génération** : politique de décodage, token généré, réinjection dans le contexte ; paramètres fixes.
- **Scoring** : probabilité d'une cible observée, puis log-probabilité et vraisemblance de séquence.
- **Évaluation** : scoring sur données tenues à l'écart, métriques adaptées, sans mise à jour des paramètres.
- **Apprentissage** : NLL/cross-entropy, agrégation selon les masques et la réduction, gradients et mise à jour des paramètres.

Le défaut initial qui consistait à représenter l'évaluation comme une branche « données → métriques » sans montrer le scoring du modèle est **corrigé au niveau architectural et documentaire** (notamment PR #589, #598 et #604). Ne pas rouvrir ce point comme lacune générale.

### 3.2 Q/K/V dans le bon niveau de calcul

Q/K/V sont projetés depuis les états d'entrée de chaque bloc Transformer. Ils participent à la construction des états contextualisés suivants ; ils ne viennent pas après des représentations contextualisées finales déjà calculées.

La page Q/K/V actuelle conserve une séparation pédagogique saine :
- Q/K/V : rôles et projections ;
- attention à produit scalaire : scores, softmax et agrégation ;
- masque causal : contrainte d'accès ;
- walkthrough/build : implémentation ;
- historique : contexte historique.

Ne pas fusionner ces pages au nom d'une simplification artificielle.

### 3.3 Prefill, decode, KV cache et teacher forcing

Les pages et le parcours distinguent maintenant :
- prefill du prompt ;
- decode incrémental ;
- politique de décodage ;
- cache KV comme optimisation facultative ;
- teacher forcing dans la branche apprentissage, et non comme prérequis de l'inférence.

Ces notions doivent rester reliées, mais non confondues :
- prefill/decode décrivent des phases d'exécution de l'inférence ;
- teacher forcing décrit l'utilisation des préfixes observés dans l'apprentissage autorégressif ;
- KV cache est une optimisation d'exécution, pas une condition mathématique de génération.

PR #601 et #604 ont déjà intégré des corrections importantes. Ne pas créer de nouvelles pages ou issues pour ces notions sans lacune précise démontrée.

### 3.4 Représentations et calcul du Transformer

Le document canonique sépare texte/tokens/IDs/lookup/information positionnelle, états initiaux, calcul interne de chaque bloc, états contextualisés successifs et projection finale vers les logits. Il qualifie aussi le placement des résidus et de la normalisation selon les variantes architecturales (Pre-LN/Post-LN), au lieu de présenter un ordre unique comme universel.

Le parcours peut introduire les représentations contextualisées avant le détail de leur production si cela est clairement un **aperçu pédagogique**, et non une affirmation sur l'ordre causal du calcul. Le parcours n'est pas un graphe d'exécution.

### 3.5 Périmètre Build honnête

La page d'accueil indique explicitement que l'inférence de référence est testée et que l'entraînement complet reste à réaliser. La feuille de route Build (#78) reste propriétaire de la progression concept-vers-code et des lacunes d'implémentation : pipeline tokenizer/corpus, entraînement complet, checkpoints et évaluation de bout en bout. Conserver l'ambition finale sans laisser entendre que ces capacités sont déjà disponibles.

## 4. Réexamen des constats initiaux

| Constat initial | État après confrontation à `main` | Décision |
|---|---|---|
| L'évaluation ne montre pas le scoring des cibles | Corrigé dans la colonne vertébrale et le crosswalk | Ne pas rouvrir ; conserver les limites de scoring |
| Q/K/V apparaissent après les représentations contextualisées | Corrigé dans le modèle computationnel canonique | Préserver les relations actuelles |
| Prefill et teacher forcing sont peu visibles | Intégrés dans les pages et la structure du parcours | Vérifier les transitions restantes dans #584 |
| Le cache KV semble obligatoire | Classé comme optimisation facultative | Pas de nouvelle issue |
| La génération apparaît deux fois dans le parcours | Une page canonique a une appartenance de prévisualisation et une appartenance d'approfondissement en inférence | Vérifier que les deux contextes indiquent clairement leur objectif ; ne pas dupliquer la page |
| Les représentations contextualisées précèdent le détail du calcul des blocs | Choix pédagogique acceptable si présenté comme aperçu | Contrôle de transition dans #584, pas refonte de l'ordre |
| La page Build promet trop | L'accueil indique que l'entraînement complet manque ; #78 suit les dépendances réelles | Maintenir statut et code synchronisés |
| Trop de registres et graphes | Responsabilités explicites ; #584 interdit un registre parallèle | Ne pas ajouter de couche ou workflow |
| La carte confond parcours et inventaire | Les sources distinguent les deux ; l'UX rendue reste à vérifier | Utiliser #337 et #415 |
| Parité FR/EN non démontrée | Audits sources et rendus partiels acquis, mais pas certification universelle | Réutiliser l'inventaire #584 |
| Accessibilité non vérifiée | Contrôles automatisés et Chromium acquis sur plusieurs périmètres ; tests humains restent ouverts | Terminer #584, #341, #191 selon leur périmètre |
| Aucun apprentissage indépendant démontré | Protocole disponible, aucun participant indépendant observé | Exécuter #447 après son prérequis #483 |

## 5. Risques et questions réellement ouverts

### R1 — Intention des appartenances multiples de la page génération

La page génération apparaît dans l'étape d'orientation et dans l'étape d'inférence. Cette réutilisation est acceptable : première vue boîte noire, puis retour mécanistique. Elle devient confuse si le lecteur ne voit pas ce qui est attendu à chaque passage.

À vérifier dans #584 :
- l'étape d'orientation annonce une lecture de survol ;
- l'étape d'inférence pointe vers prefill/decode et la boucle détaillée ;
- les indications contextuelles ne donnent pas l'impression qu'il faut relire la page sans nouvel objectif.

Ne créer une seconde page « aperçu de génération » que si un test lecteur démontre que les ancres et le guidage contextuel ne suffisent pas.

### R2 — Information positionnelle : ne pas universaliser l'addition d'embeddings

Le regroupement « embeddings et information positionnelle » est pédagogiquement utile, mais ne doit pas suggérer que toutes les architectures ajoutent un vecteur positionnel aux embeddings de tokens.

Maintenir la distinction entre :
- embeddings positionnels absolus ajoutés aux représentations d'entrée dans certaines architectures ;
- RoPE appliqué aux requêtes et clés dans les mécanismes concernés ;
- autres méthodes positionnelles possibles, sans prétendre les couvrir exhaustivement.

Le travail source/rendu sur positional encoding, RoPE et tenseurs a été traité dans #643/#646. Réutiliser les preuves et l'inventaire existants ; ne pas recommencer l'audit. Vérifier seulement qu'aucune projection ne réintroduit une lecture linéaire trompeuse.

### R3 — Marqueurs épistémiques : précision du vocabulaire

La page d'accueil utilise « Concept vérifié » pour des définitions formelles, équations et hypothèses explicites. « Vérifié » peut être interprété comme une validation expérimentale alors que la description couvre aussi la formalisation mathématique.

À examiner dans #130 et #61 :
- distinguer définition/formalisation, propriété dérivée, test logiciel et résultat expérimental ;
- ne pas multiplier les badges ;
- conserver les marqueurs uniquement s'ils aident à comprendre la nature de la preuve ;
- ne pas laisser entendre qu'un test de code valide une affirmation scientifique générale.

C'est une question de précision éditoriale, pas une erreur scientifique déjà démontrée.

### R4 — Complexité de maintenance

Le système est maintenant suffisamment riche. Le risque résiduel est la duplication entre registres, pages et projections, non l'absence d'une nouvelle abstraction.

Garde-fous :
- `data/computational-graph.yml` reste la source du graphe computationnel ;
- `data/concepts.yml` reste la source du graphe conceptuel ;
- `data/guided-route.yml` reste la source du parcours guidé ;
- le parcours Build garde son objectif et ses dépendances d'implémentation ;
- les projections générées ne deviennent pas des sources éditoriales concurrentes.

Toute validation nouvelle doit être mutualisée dans les outils existants. Pas d'action GitHub par notion, pas de moteur de diagrammes parallèle, pas de registre supplémentaire.

### R5 — Expérience humaine non établie

Les validations de rendu, d'accessibilité automatisée et de structure ne démontrent pas que le lecteur sait raisonner sur les mécanismes.

Le pilote #447 doit rester explicite. Il teste notamment la navigation texte→attention, la distinction lookup/état contextualisé, les rôles Q/K/V et le transfert du masque causal. Une observation qualitative unique peut révéler des défauts, mais ne prouve pas l'efficacité générale du dispositif.

## 6. Intégration au backlog existant — aucune roadmap parallèle

| Sujet | Issue propriétaire | Action retenue |
|---|---|---|
| Conception pédagogique et navigation transversales | [#130](https://github.com/JM-Brun/llm-lab/issues/130) | Utiliser cette revue comme synthèse critique et arbitrer les questions transversales |
| Colonne vertébrale, crosswalk et preuves restantes | [#584](https://github.com/JM-Brun/llm-lab/issues/584) | Continuer l'audit borné ; réutiliser `docs/page-audit-inventory.md` |
| Progression concept-vers-code et statut d'implémentation | [#78](https://github.com/JM-Brun/llm-lab/issues/78) | Synchroniser le statut Build avec code/tests ; respecter le gate de prérequis |
| Expérience et divulgation progressive des leçons | [#61](https://github.com/JM-Brun/llm-lab/issues/61) | Traiter la précision des marqueurs et les transitions au niveau des pages |
| Navigation/carte et correspondance avec le site rendu | [#337](https://github.com/JM-Brun/llm-lab/issues/337) | Vérifier parcours guidé / graphe exploratoire et points d'entrée |
| Carte et graphe conceptuel, sémantique des relations | [#415](https://github.com/JM-Brun/llm-lab/issues/415), [#416](https://github.com/JM-Brun/llm-lab/issues/416) | Ne pas confondre layout, relation conceptuelle et prérequis |
| Page d'accueil FR/EN | [#341](https://github.com/JM-Brun/llm-lab/issues/341) | Terminer la revue rendue spécifique à l'accueil |
| Design system, contrastes et composants | [#191](https://github.com/JM-Brun/llm-lab/issues/191) | Terminer les mesures et vérifications ciblées |
| Rendu Q/K/V et provenance média | [#483](https://github.com/JM-Brun/llm-lab/issues/483) | Terminer les contrôles de rendu et droits ; ne pas rouvrir l'intégration de contenu |
| Validation par lecteur indépendant | [#447](https://github.com/JM-Brun/llm-lab/issues/447) | Exécuter le protocole après le gate #483 |

### Ordre d'exécution recommandé

1. Terminer les PR et contrôles navigateur déjà en cours avant d'interpréter leurs résultats ou d'ouvrir des corrections.
2. Finir le lot partagé de #584 : audit source/rendu des pages restantes, puis vérifications manuelles de lecteur d'écran et breadcrumbs lorsqu'elles sont encore ouvertes. Ne pas répéter les audits déjà consignés dans `docs/page-audit-inventory.md`.
3. Traiter les revues rendues spécialisées : #341 (accueil), #337 (navigation/carte), #191 (composants/contrastes), #483 (Q/K/V). Chaque issue conserve son périmètre.
4. Exécuter #447 après satisfaction du prérequis #483. Consigner observations, réponses et limites sans prétendre mesurer une efficacité générale.
5. Réévaluer #130 à partir des résultats, puis fermer ou transférer explicitement les points résiduels.

## 7. Critères d'arbitrage des prochaines modifications

Une modification est justifiée si elle :
- corrige une erreur scientifique ou une relation conceptuelle trompeuse ;
- réduit une confusion observable dans le parcours ;
- rend une compétence attendue vérifiable ;
- améliore l'accessibilité ou l'usage sur une situation reproductible ;
- réduit réellement le coût de maintenance sans ajouter une abstraction disproportionnée.

Une modification n'est pas justifiée par le seul désir d'uniformiser les graphes, l'apparition de deux notions sur une page, la cooccurrence de concepts, l'ajout systématique d'un badge/page/workflow ou un score pédagogique non étayé.

## 8. Verdict

Le chantier prioritaire est passé de la **définition de l'architecture** à sa **validation et à son usage**. La colonne vertébrale computationnelle est intégrée ; les branches génération/scoring/évaluation/apprentissage sont distinguées ; les pages centrales ont déjà fait l'objet de plusieurs audits et corrections.

Le prochain gain substantiel viendra de la clôture rigoureuse des preuves restantes et du pilote lecteur, non de l'extension du système de métadonnées.

## 9. Références

- [#130 — coordination de la conception pédagogique](https://github.com/JM-Brun/llm-lab/issues/130)
- [#575 — colonne vertébrale computationnelle (close)](https://github.com/JM-Brun/llm-lab/issues/575)
- [#584 — intégration lecteur et crosswalk](https://github.com/JM-Brun/llm-lab/issues/584)
- [#78 — parcours concept-vers-code](https://github.com/JM-Brun/llm-lab/issues/78)
- [PR #577 — décision architecturale](https://github.com/JM-Brun/llm-lab/pull/577)
- [PR #578 — registre computationnel et graphe typé](https://github.com/JM-Brun/llm-lab/pull/578)
- [PR #589 — vues de la colonne vertébrale](https://github.com/JM-Brun/llm-lab/pull/589)
- [PR #594 — audit navigateur bilingue](https://github.com/JM-Brun/llm-lab/pull/594)
- [PR #598 — crosswalk Build](https://github.com/JM-Brun/llm-lab/pull/598)
- [PR #600 — audit G0–G9](https://github.com/JM-Brun/llm-lab/pull/600)
- [PR #601 — teacher forcing et prefill/decode](https://github.com/JM-Brun/llm-lab/pull/601)
- [PR #604 — scoring des préfixes observés](https://github.com/JM-Brun/llm-lab/pull/604)
- [PR #646 — positional encoding, RoPE et tenseurs](https://github.com/JM-Brun/llm-lab/pull/646)
- [Protocole de validation apprenant](../learner-validation-pilot.md)
- [Inventaire des audits de pages](../page-audit-inventory.md)
