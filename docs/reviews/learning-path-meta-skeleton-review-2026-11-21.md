# Squelette méta du parcours Understand — revue de cohérence

**Statut :** revue de documentation ; propositions seulement. Les décisions et priorités restent au [handoff courant](../next-work-handoff-2026-11-09.md) et aux issues [#1477](https://github.com/JM-Brun/llm-lab/issues/1477) et [#1478](https://github.com/JM-Brun/llm-lab/issues/1478).
**Date :** 2026-11-21
**Périmètre :** reconstruction du squelette méta du parcours Understand à partir des sources canoniques du dépôt, puis vérification de cohérence. Le présent document ne modifie ni `data/guided-route.yml`, ni `docs/learning-path.md`, ni les pages Quarto ; chaque constat propose une correction séparée.
**Méthode :** source-first, comme la [méthode éditoriale partagée](../reader-experience-and-editorial-method.md). Aucune phrase du squelette n'est avancée sans pointeur vers sa source canonique.

Le squelette méta est la question de départ de cette revue : peut-on décrire le parcours entier de façon très synthétique, globale (architecture du parcours) et locale (patron d'une leçon), sans créer une source de vérité concurrente ? La réponse est oui : **tout le squelette se reconstruit à partir des sources existantes**. Les constats qui suivent ne portent pas sur le squelette lui-même, mais sur les endroits où deux sources canoniques divergent.

## 1. Le squelette reconstruit des sources canoniques

### 1.1 Vue globale : un axiome, deux variables, trois-quatre usages

L'axiome affiché sur la [carte](../../site/fr/learning-map.qmd), pour un GPT autorégressif :

```text
p_θ(· | c) = softmax(f_θ(c))
```

(signé aussi `c \mapsto p_\theta(\cdot \mid c)` dans `data/guided-route.yml`, étape `orientation`). Deux variables portent tout le curriculum : le contexte `c` (ce qui est transmis) et les paramètres `θ` (ce qui est appris). Les usages du tableau comparatif de la carte se lisent sur ces deux variables : `c` s'allonge ou est assemblé, `θ` est fixé ou mis à jour. Le décompte exact des usages fait l'objet du constat C1.

### 1.2 Vue globale : la chaîne de signatures

Chaque étape du registre fournit une signature ; dans l'ordre des neuf étapes, elles se composent effectivement en l'axiome :

| Étape | Signature | Rôle dans la composition |
|---|---|---|
| `orientation` | `c ↦ p_θ( · | c)` | énoncé du tout, à ouvrir |
| `text-input` | `s →(tok) (i_1..i_T)` | définit `c` en entrée discrète |
| `representations` | `H^(0)_t = E_θ[i_t] + P_θ[t]` | des IDs aux états initiaux |
| `computation` | `H^(0) ↦ H^(L)` | contextualisation par les blocs |
| `prediction` | `z_t = W_θ h_t + b_θ ; p_t = softmax_vocab(z_t)` | ferme l'axiome (à `t = T`) |
| `inference` | `x_t ~ π( · | p_θ( · | c_t)) ; c_(t+1) = c_t ∥ x_t` | usage : générer, `θ` fixés |
| `context-use` | `c ↦ p_θ( · | c) ; c' ↦ p_θ( · | c')` | usage : concevoir le contexte, `θ` fixés |
| `scoring` | `log p_θ(x_(1:n) | c) = Σ_t log p_θ(x_t | c ∥ x_(<t))` | usage : scorer, `θ` fixés |
| `training` | `g = ∇_θ L(θ) ; θ' = θ − η g` | usage : entraîner, `θ` mis à jour |

Vérification : aucune variable n'apparaît sans définition en amont (`s`, `c`, `i_t`, `H`, `z`, `p`, `c'`, `x_t`, `θ`, `η`), et le critère de chaque étape énonce le comportement des paramètres. La chaîne compose ; aucun trou n'a été trouvé.

### 1.3 Vue locale : le patron d'une leçon

Chaque leçon cœur instancie le même patron, porté par trois registres :

```text
notions mobilisées  →  objet étudié  ·  acquis visé          (conceptual_focus)
question / résultat / signature / critère                    (overview)
contrat de leçon → fiche de révision + exercice de frontière  (lesson_contracts, boundaries)
```

Les preuves restent graduées (schéma, dérivation, test, expérience), conformément aux repères « concept vérifié / à exécuter localement / architecture-statut ».

## 2. Vérifications mécaniques (21 novembre 2026, sur `main` à `14d8c7eb`)

| Invariant attendu | Résultat |
|---|---|
| 9 étapes dans `data/guided-route.yml` | conforme (9) |
| 20 leçons cœur, symétrie FR/EN des listes `pages` et `optional_pages` | conforme (20 en FR, listes jumelées une à une en EN) |
| `conceptual_focus` couvre la leçon cœur de chaque étape | conforme, sauf cas `inference` : la clé `inference-generation` désigne la page `generation.qmd` (ID de page-map vs nom de fichier) ; voir le constat O1 |
| `prediction_use` sur les étapes d'usage, absent des étapes de calcul | conforme (4 étapes d'usage : `inference`, `context-use`, `scoring`, `training`) |
| 20 contrats de leçons avec fiche `revision-*` publiée | conforme (20 fiches présentes dans le sitemap) |
| 11 frontières avec exercice de transfert FR/EN | conforme |
| Signatures composables (tableau 1.2) | conforme |
| Cohérence des décomptes entre documents gouvernants | deux écarts : décompte des usages (C1) et décompte des étapes dans l'index IA (C3) |

## 3. Constats

### C1 — La topologie canonique des modules omet le module `context-use` [#1477](https://github.com/JM-Brun/llm-lab/issues/1477)

Dans `docs/learning-path.md` : la section route guidée parle de *four sibling uses*, la section topologie canonique de *three sibling operational uses*, et ni l'arbre hiérarchique ni le tableau des modules ne contiennent de module `context-use`. La projection lecteur (étape `context-use` de la route guidée, § 7 de l'ordre conceptuel) décrit donc un module que le contrat canonique n'enregistre pas. Proposition : ajouter le module (sibling de `inference`, phase « input ») et réconcilier le décompte. Impact documentaire seulement.

### C2 — Deux décomptes de mouvements dans la couche d'orientation [#1478](https://github.com/JM-Brun/llm-lab/issues/1478)

La note « Le parcours en bref » des cartes affiche cinq mouvements ; la [synthèse d'orientation](../understand-path-overview.md) en propose six (contexte séparé). La version à six mouvements est datée du 13 novembre et la page publiée montre toujours cinq. Décision à prendre, puis application FR/EN.

### C3 — L'index IA décrit une route à « eight canonical stages » [#1479](https://github.com/JM-Brun/llm-lab/issues/1479)

La ligne « Theory / Understand route » de l'inventaire système de `docs/information-architecture.md` (contrat IA, 2026-11-04) déclare « eight canonical stages », alors que le registre en compte neuf et que la carte affiche « trois questions, neuf étapes ». L'étape `context-use` est arrivée après la rédaction du contrat sans mise à jour de l'index. Proposition : mettre à jour la ligne de l'inventaire et vérifier l'absence d'autres occurrences de « eight stages ». Cette divergence appuie le constat C1 : `context-use` s'est ajouté à la projection sans être enregistré dans le contrat canonique ni dans l'index.

### O1 — Observation, sans action proposée

La clé `inference-generation` de `conceptual_focus` (étape `inference`) est la seule clé qui ne coïncide pas avec le slug de page FR ; le générateur valide les références, donc il s'agit vraisemblablement de l'ID de page-map. Consigné ici pour éviter qu'une future harmonisation des slugs ne casse la correspondance sans s'en apercevoir. De même, `transitions` ne porte que deux arêtes : c'est suffisant, chacune porte une distinction sœur (distribution → génération ; score → objectif) ; la complétude n'est pas un invariant à imposer.

## 4. Hors périmètre

Le parcours Build, `data/concepts.yml`, le graphe computationnel et les pages Quarto ne sont ni audités ni modifiés ici. Aucun nouveau registre, workflow ou tableau de suivi n'est créé (règle d'exploitation du handoff : pas de système parallèle sans limitation démontrée).

## 5. Suivi

| Constat | Issue | Action proposée |
|---|---|---|
| C1 | [#1477](https://github.com/JM-Brun/llm-lab/issues/1477) | ajout du module `context-use` + réconciliation du décompte dans `docs/learning-path.md` |
| C2 | [#1478](https://github.com/JM-Brun/llm-lab/issues/1478) | trancher 5 ou 6 mouvements, puis mettre au niveau les deux couches FR/EN |
| C3 | [#1479](https://github.com/JM-Brun/llm-lab/issues/1479) | mettre à jour « eight canonical stages » en « nine » dans `docs/information-architecture.md` |
| O1 | aucun | consigné, aucune action |
