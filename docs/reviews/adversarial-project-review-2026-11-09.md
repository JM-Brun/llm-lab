# Revue adversariale du projet LLM Lab — 2026-11-09

**Périmètre :** le projet dans son ensemble — site publié, code de référence, documentation et processus — confronté à `main` au commit `a77b09e` (#792) et au site en ligne le même jour.

**Nature :** revue stratégique et critique. Elle ne certifie ni le rendu exhaustif, ni l'accessibilité, ni la parité FR/EN, ni l'efficacité pédagogique. Elle ne modifie aucune étiquette de priorité ni l'ordre d'exécution : ses propositions attendent une décision du mainteneur (§ 7).

**Relation avec les revues précédentes :** complète la [revue adversariale du 2026-11-07](adversarial-site-review-2026-11-07.md) et la [revue du 2026-10-30](../high-level-adversarial-site-review-2026-10-30.md). Elle s'en écarte sur un point explicite (§ 4). Pour la navigation, l'[audit de navigation et d'ergonomie du même jour](navigation-ergonomics-audit-2026-11-09.md) fait référence ; cette revue n'en reprend que les points de C5 et C8.

## 1. Conclusion

Le contenu est rigoureux et le code de référence est propre. Mais le projet investit davantage dans sa propre cohérence interne que dans ce qu'un lecteur peut faire : le « Lab » n'a pas de modèle qui produit du texte, pas d'exécution dans le navigateur et pas encore de lecteur indépendant.

Le levier principal n'est pas une couche de validation supplémentaire. C'est de faire produire du texte au modèle que le lecteur a lu — ce qui est possible sans lever le gate G8 (§ 4) —, puis de lui faire apprendre quelque chose une fois ce gate levé.

## 2. Méthode et niveaux de preuve

- **Source** : mesures sur `main` (`a77b09e`), lecture du code de `src/llm_lab/foundations/`, de la feuille de route, de la [passation du 2026-11-09](../next-work-handoff-2026-11-09.md) et des revues et audits récents.
- **Site publié** : lecture de l'accueil et des pages Construire, attention à produit scalaire, carte, Exercices, lois d'échelle, RoPE et architectures hybrides (FR), sur desktop et en viewport mobile 375 px.
- **Non couvert** : parité EN, audit d'accessibilité, lecture exhaustive des 109 pages, observation d'un lecteur.

Les décomptes de mots utilisent `wc -w` sur les sources (front matter et code compris) ; ils comparent des ordres de grandeur, pas une densité éditoriale.

## 3. Contexte de gouvernance

Trois règles du projet encadrent les recommandations de cette revue :

- **Budget** : le temps d'apprentissage du mainteneur est plafonné à cinq heures par semaine ([feuille de route](../roadmap.md)).
- **Gates de connaissance** : une implémentation n'avance qu'après validation des connaissances minimales requises. G8 (rétropropagation, optimiseur, boucle d'entraînement) est bloqué par le gate privé de [#656](https://github.com/JM-Brun/llm-lab/issues/656).
- **Une tranche active à la fois**, au plus trois candidats suivants ; pas de nouveau registre, workflow ou système parallèle sans limite démontrée ([passation, § 5](../next-work-handoff-2026-11-09.md#5-operating-rules)).

Cette revue respecte ces règles. Elle conteste en revanche la façon dont le budget est dépensé (C1) et propose un ordre différent à l'intérieur des gates existants (§ 4).

## 4. Désaccord avec la revue du 2026-11-07

La revue du 2026-11-07 classe « La page Build promet trop » comme traité : l'accueil dit que l'entraînement manque, et le statut est honnête.

Position de cette revue : **l'honnêteté sur l'écart ne le comble pas.** Un lecteur qui suit tout le parcours Construire ne voit jamais le modèle produire un mot : les poids sont aléatoires et la sortie est une liste d'identifiants d'un vocabulaire synthétique. Pour un site dont l'objet est de comprendre les LLM, c'est le défaut prioritaire, pas une limite à documenter.

Ce défaut peut être réduit **sans contourner le gate G8** : charger des poids pré-entraînés dans le forward déjà implémenté et testé ne demande ni rétropropagation, ni optimiseur, ni boucle d'entraînement. C'est le jalon G9 (comparaison à une référence compatible), que la feuille de route place après le pré-entraînement (P5, étape 2) alors que ses prérequis sont déjà remplis.

Accord avec R3 (badge « Concept vérifié »), R4 (pas de nouveau registre) et R5 (expérience humaine non établie) ; cette revue va plus loin sur R4 (recommandation 5).

## 5. Constats

### C1 — La méta-documentation dépasse le produit

| Mesure sur `main` (`a77b09e`) | Valeur |
|---|---|
| `docs/` : fichiers Markdown | 117 fichiers, 296 327 mots |
| dont notes de recherche (`source-reviews/`, `source-syntheses/`) | 30 fichiers, 61 077 mots |
| dont planification, gouvernance, audits et workflows | ≈ 235 000 mots |
| Pages du site (`site/fr`, `site/en`) | 100 585 mots FR, 88 946 mots EN |
| Code de référence (`src/`) | 1 294 lignes Python |
| Outillage du site (`site/tools/`) | 6 371 lignes Python |
| Commits depuis le 2026-10-20 | 600, dont 13 touchent `src/` |
| Issues | 120, toutes ouvertes par le mainteneur |

La documentation de pilotage représente environ 2,4 fois le contenu publié dans une langue, et dépasse les deux langues réunies. Quel que soit l'outil qui la produit, sa relecture puise dans le même budget de cinq heures par semaine que l'apprentissage et le code. L'audit du jour sur l'annexe D de Raschka (warmup, décroissance cosinus, clipping) analyse les améliorations d'une boucle d'entraînement qui n'existe pas encore dans le code.

### C2 — La promesse « Construire » n'est pas tenue

- La page Construire indique : « Les visites ne demandent pas d'écrire un GPT complet depuis zéro ». C'est une visite guidée de code existant.
- Le modèle n'est jamais entraîné ni chargé avec des poids appris : pas d'optimiseur, pas de boucle d'entraînement (`losses.py` calcule la perte et son gradient, sans mise à jour). Cette absence est voulue tant que le gate G8 n'est pas levé ; l'absence de poids appris ne l'est pas (§ 4).
- Le lecteur n'écrit pas de code : aucun squelette à compléter n'est fourni.

### C3 — Un « Lab » sans exécution dans le navigateur

Aucune page n'utilise Pyodide, quarto-live, OJS ou JupyterLite. Les badges indiquent « Python · à exécuter localement ». Lancer l'exemple demande uv, un clone du dépôt et deux fichiers de dépendances supplémentaires. L'issue [#268](https://github.com/JM-Brun/llm-lab/issues/268) existe mais reste différée en P3 tant qu'un besoin lecteur concret n'est pas établi ([passation, § 2](../next-work-handoff-2026-11-09.md#p3--deliberately-deferred)) ; cette friction d'installation est ce besoin.

### C4 — Les mises en garde sont si nombreuses qu'elles perdent leur effet

- Page attention à produit scalaire : « pertinence sémantique » apparaît 4 fois, toujours pour dire que les poids ne la mesurent pas.
- Page Construire : 4 formules du type « ne prouve pas », « n'établit ni ».
- Le badge « Concept vérifié » désigne une formalisation, pas une vérification (point déjà relevé en R3 du 2026-11-07).

Quand chaque phrase est nuancée, le lecteur ne distingue plus la limite importante de la précaution de style.

### C5 — Le vocabulaire interne remonte jusqu'au lecteur

- Sous-titre de la carte : « Huit étapes, territoires, rubriques, pages et notions canoniques ».
- Le filtre de la carte expose les types de relations du graphe (« est projeté par », « contraint », « est normalisé par »).
- L'accueil FR renvoie vers `docs/full-curriculum-plan.md`, document de gouvernance en anglais de plus de 100 KB.
- Trois numérotations cohabitent côté lecteur : étapes du parcours 01–08, jalons G0–G9 (plus G1b et E1), étapes 0–8 du tableau Construire.

### C6 — Couverture déséquilibrée

- Pas de page dédiée à l'optimiseur (SGD, Adam, taux d'apprentissage), à la rétropropagation dans un bloc, au fine-tuning et à LoRA, ni au post-entraînement (SFT, DPO, RL). Le cache KV est expliqué dans les pages d'inférence mais pas implémenté.
- La page Exercices contient des sections Préentraînement, Fine-tuning et Efficacité sans leçons correspondantes.
- En parallèle, des approfondissements traitent un cas fournisseur précis (Nemotron 3), l'émergence et l'histoire.
- La page sur les lois d'échelle s'arrête à Kaplan (2020) et Hoffmann/Chinchilla (2022) : rien sur l'entraînement au-delà de l'optimum Chinchilla, le régime à données limitées ou le calcul au moment de l'inférence.

### C7 — Aucun lecteur indépendant

Le protocole du pilote existe ; l'issue [#447](https://github.com/JM-Brun/llm-lab/issues/447) est ouverte, en attente du prérequis [#483](https://github.com/JM-Brun/llm-lab/issues/483), et aucun participant n'a été observé. Il n'existe pas de canal de retour sur les pages, hormis l'ouverture d'une issue GitHub. Tous les signaux de qualité sont internes : tests, validateurs, audits.

### C8 — Défauts concrets

| Défaut | État |
|---|---|
| 24 liens 404 dans les docstrings de `src/llm_lab/foundations/` (`/fr/slug/` au lieu de `slug.html`) | Corrigé dans [#789](https://github.com/JM-Brun/llm-lab/pull/789), avec un test |
| Fil d'Ariane « Construire un petit GPT > Construire un petit GPT » | Corrigé dans #789 |
| `<meta name="description">` absente sur 99 pages | Corrigé dans #789 (filtre Lua depuis le sous-titre) |
| Pages de navigation plus longues que les leçons : carte 9 364 mots, Exercices 12 011 mots | Ouvert (§ 7) |

Leçon de #789 pour le pilote de groupes cliquables proposé par l'[audit de navigation](navigation-ergonomics-audit-2026-11-09.md#pilote-recommandé) : Quarto relie un groupe du menu à sa première page, et un groupe portant le même titre que sa page d'entrée produit un fil d'Ariane doublé. Le pilote doit donc garder des titres distincts. Le générateur de carte résout déjà les entrées `{text, href}` ; une `section` munie d'un `href` n'y est pas traitée comme une page, ce que le pilote doit vérifier dans la carte générée.

## 6. Recommandations

Classées par rapport valeur pour le lecteur / effort.

1. **Charger les poids GPT-2 small dans le GPT NumPy existant (G9).** L'architecture est déjà compatible : pre-LN, positions apprises, GELU tanh, biais, LayerNorm à `eps = 1e-5`, `linear` en `(out, in)`. Un chargeur suffit : découper `c_attn` en Q/K/V, transposer les poids `Conv1D`, copier `wte` dans la tête de sortie avec un biais nul, tokenizer via `tiktoken`. Résultat : du vrai texte produit par le code que le lecteur a lu, et le test de parité G9 contre les logits de Hugging Face. Prévoir une option float32 (124 M paramètres en float64 ≈ 1 GB).
   *Critère :* les logits NumPy et HF concordent à une tolérance explicite sur un prompt fixé ; un exemple génère du texte lisible.
2. **Entraînement minimal (G8), après levée du gate #656.** Modèle au niveau caractère sur un texte français du domaine public ; reprise du forward en PyTorch (l'extra `ml` existe) avec test de parité NumPy ↔ PyTorch ; quelques minutes sur CPU. Une page « échantillons aux étapes 0, 100 et 1000, plus la courbe de perte ».
   *Critère :* la perte de validation baisse nettement sous la baseline unigramme ; les échantillons sont joints au rapport.
3. **Rendre « Construire » réel.** Fournir des squelettes `raise NotImplementedError` que le lecteur complète, validés par les tests de référence existants — d'abord pour les composants d'inférence, hors gate.
4. **Exécution dans le navigateur.** quarto-live (Pyodide, NumPy supporté) sur les pages attention, softmax avec température et masque causal ; badge Colab sur chaque visite guidée.
5. **Gel de la méta-documentation pendant 4 à 6 semaines.** Pas de nouvel audit ni de nouveau validateur ; chaque PR modifie une page lue par le lecteur ou `src/`. Archiver les audits datés dans `docs/archive/`.
6. **Un seul encadré « Limites » par page.** Supprimer les répétitions dans le texte ; renommer le badge « Concept vérifié » en « Définition formelle ».
7. **Retirer le jargon des pages lecteur.** Masquer ou renommer le filtre des relations, retirer les liens vers les documents de gouvernance, garder une seule numérotation (01–08).
8. **Combler le cycle de vie avant les sujets avancés.** Optimiseur, rétropropagation, cache KV implémenté (prolongement de `generate.py`), LoRA, post-entraînement ; mettre à jour la page sur les lois d'échelle.
9. **Valider avec de vrais lecteurs.** Exécuter #447 dès que #483 est satisfait ; ajouter un canal de retour léger (par exemple Giscus) ; mesurer le temps jusqu'à la première exécution et l'endroit où le lecteur abandonne.

## 7. Intégration au backlog — aucune priorité modifiée

Chaque recommandation est rattachée à un propriétaire existant, conformément à la règle « un propriétaire canonique par sujet ». Aucune issue n'est créée et aucune étiquette n'est changée par ce document.

| Recommandation | Propriétaire existant | État actuel | Proposition soumise au mainteneur |
|---|---|---|---|
| 1. Poids GPT-2 (G9) | [#78](https://github.com/JM-Brun/llm-lab/issues/78) | Feuille de route P5 : comparaison de référence après le pré-entraînement | Avancer G9 avant G8 ; ouvrir une issue enfant de #78 si accepté |
| 2. Entraînement minimal (G8) | [#656](https://github.com/JM-Brun/llm-lab/issues/656) | P1, bloqué par le gate privé | Garder le gate ; faire de sa levée la prochaine tranche P1 d'apprentissage, avant de nouveaux audits de sources sur l'entraînement |
| 3. Squelettes à compléter | #78 | — | Commencer par les composants d'inférence déjà testés |
| 4. Exécution dans le navigateur | [#268](https://github.com/JM-Brun/llm-lab/issues/268) | P3, différé | Passer en P2 (besoin documenté en C3) |
| 5. Gel de la méta-documentation | [#130](https://github.com/JM-Brun/llm-lab/issues/130) ; passation § 5 | Règle existante : pas de nouveau registre ni workflow | Étendre la règle aux audits et validateurs pendant 4 à 6 semaines |
| 6. Limites et badge | #130 | Relevé en R3 le 2026-11-07 | Un encadré « Limites » par page ; badge « Définition formelle » |
| 7. Jargon côté lecteur | [#416](https://github.com/JM-Brun/llm-lab/issues/416), [#337](https://github.com/JM-Brun/llm-lab/issues/337) | P2 | Masquer le filtre des relations ; une seule numérotation |
| 8. Couverture du cycle de vie | #78 ; audits fine-tuning/LoRA (P3) ; page lois d'échelle sans propriétaire | — | Prioriser le cycle de vie sur les approfondissements ; rattacher la mise à jour des lois d'échelle à #130 |
| 9. Lecteurs indépendants | [#447](https://github.com/JM-Brun/llm-lab/issues/447) après [#483](https://github.com/JM-Brun/llm-lab/issues/483) | P2, gate #483 | Garder le gate ; ajouter un canal de retour léger sous #130 |
| C8 restant : pages de navigation trop longues | #337 (carte) ; #130 (Exercices) | P2 | Découper Exercices par collection ; alléger l'introduction de la carte |

## 8. À préserver

- La distinction génération / scoring / apprentissage et la colonne vertébrale computationnelle.
- Les tests d'invariance causale et la qualité des commentaires du code de référence.
- Le bilinguisme.
- L'exactitude des exemples : l'exemple numérique de la page attention (sortie ≈ (6,7 ; 6,6)) et l'exercice associé ont été recalculés sans écart.

## 9. Limites de cette revue

- Lecture d'environ huit pages FR ; pas de comparaison FR/EN.
- Pas d'audit d'accessibilité ni d'observation d'utilisateur.
- Le filtre des relations de la carte est rempli en JavaScript ; son contenu a été observé dans le DOM rendu, pas dans le HTML statique.
- Le gate privé de #656 n'a pas été examiné : cette revue ne se prononce pas sur l'état des connaissances qu'il vérifie.
