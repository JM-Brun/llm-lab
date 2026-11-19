# Audit ciblé — Catherine Arnett, « Dangers of tokenizer recycling » — 19 novembre 2026

## Décision

**Référence contextuelle ; pas d'extraction dédiée.**

L'article est déjà cité dans les pages bilingues d'évaluation des tokenizers, avec une réserve explicite sur la portée de son illustration et sur le fait qu'il ne constitue pas une étude comparative universelle. Il contient des observations utiles sur la réutilisation des tokenizers et la pré-tokenisation, mais ses recommandations fortes et plusieurs liens causaux sont des retours d'expérience ou des hypothèses. Ils ne doivent pas devenir des claims du projet sans corroboration primaire.

## Source et périmètre

- ID catalogue : `catherine-arnett-tokenizer-fertility` (titre du catalogue : « Dangers of tokenizer recycling »).
- URL : https://huggingface.co/blog/catherinearnett/dangers-of-tokenizer-recycling
- Autrice : Catherine Arnett.
- Publication indiquée par la page : 27 septembre 2024.
- Type : article communautaire Hugging Face.
- Lecture : article public complet, sections sur données d'entraînement du tokenizer, pré-tokenisation, segmentation numérique et alternatives tokenizer-free ; liens de recherche associés ; pages FR/EN du projet.
- La source est un article communautaire ; aucune révision immuable n'a été identifiée.

## Contenu et niveau de preuve

L'article soutient notamment :
1. Le corpus utilisé pour entraîner un tokenizer influence la qualité de segmentation et la compression sur les domaines/langues concernés.
2. Réentraîner sur un échantillon représentatif peut améliorer la compression sur les données visées, selon les tests rapportés par l'autrice.
3. Des choix de pré-tokenisation (contractions anglaises, groupes de chiffres de longueur limitée) peuvent produire des effets indésirables hors anglais ou sur du code.
4. Des différences de segmentation numérique pourraient être liées à des performances de raisonnement arithmétique ; l'article formule lui-même cette relation comme une possibilité, pas comme une démonstration causale.
5. Compression et « sens linguistique » des tokens ne suffisent pas à eux seuls à évaluer un tokenizer ; l'article signale des résultats contradictoires et des travaux en cours.
6. Les approches byte/character-level allongent les séquences ; les coûts varient aussi selon les langues et les écritures.

**Niveau de preuve :** retour d'expérience et argumentation d'une praticienne, accompagnés de liens vers des travaux de recherche. Les observations de compression sont liées aux données et tokenizers testés par l'autrice. Les conjectures sur raisonnement numérique ou causalité entre pré-tokenisation et capacités du modèle ne sont pas établies par l'article.

## Corroboration et limites

- Le papier d'Ali et al. sur le choix du tokenizer en entraînement de LLM constitue une preuve expérimentale primaire plus appropriée pour discuter d'effets de choix de tokenizer sur certaines performances et coûts, dans les limites de son protocole.
- Les travaux de Wegmann et al. sur la variation linguistique examinent expérimentalement les effets du pré-tokenizer dans des tâches BERT-base précises ; ils ne valident pas toutes les hypothèses de l'article.
- Les travaux sur compression et performances (Goldman et al.) ainsi que les analyses soulignant que la compression n'est pas toute la qualité (Schmidt et al.) doivent être lus conjointement, sans en déduire une règle universelle.
- Les affirmations relatives à la prise en charge de tokenizers par vLLM et aux modèles récents sont temporelles : elles nécessiteraient une vérification sur une version précise avant d'être reprises.
- La relation entre pré-tokenisation numérique et raisonnement arithmétique est présentée comme une hypothèse. Aucune causalité ne doit être affirmée sur cette base.

## Couverture existante dans LLM Lab

Les pages `site/en/tokenizer-design-evaluation.qmd` et `site/fr/tokenizer-design-evaluation.qmd` :
- citent déjà l'article comme retour d'expérience sur le réemploi des tokenizers ;
- distinguent ses observations des résultats contrôlés ;
- présentent des dimensions distinctes d'évaluation (compression, tâches en aval, variation linguistique et reproductibilité) ;
- expliquent la dépendance des résultats au corpus, à la version, à la normalisation, aux langues et à la tâche ;
- citent des études primaires qui permettent de corroborer certains sujets sans attribuer à l'article une portée excessive.

L'article ne justifie donc pas une extraction autonome de ses conseils ou hypothèses.

## Illustration et droits

L'illustration de fertilité hébergée dans l'article est déjà intégrée par URL dans les pages du projet. Son droit de réutilisation pour cet actif précis demeure à vérifier dans l'issue #156. Cet audit n'a ni téléchargé, ni copié, ni modifié l'image. Le fait que l'article soit public ou que l'autrice soit créditée ne suffit pas à établir une autorisation de réutilisation.

## Disposition

**Conserver comme référence contextuelle ; aucune extraction.** Réouvrir uniquement si une affirmation précise de l'article devient nécessaire et peut être corroborée par une source primaire, ou si un protocole contrôlé du projet permet de tester directement une hypothèse de pré-tokenisation.

## Travaux non effectués

- Aucun entraînement ou benchmark de tokenizer n'a été reproduit.
- Aucun test de raisonnement numérique n'a été réalisé.
- Les versions actuelles de vLLM, Llama ou d'autres frameworks n'ont pas été vérifiées.
- Les droits de l'illustration restent ouverts dans #156.
- Aucun claim n'a été extrait dans `data/extractions/`.

## Sources internes croisées

- `site/en/tokenizer-design-evaluation.qmd`
- `site/fr/tokenizer-design-evaluation.qmd`
- `docs/source-reviews/tokenization-embeddings-source-collection.md`
- `data/sources.yml` — entrée `catherine-arnett-tokenizer-fertility`

## Suite opérationnelle

Maintenir l'article comme source contextuelle. Traiter séparément #156 pour l'actif visuel. Ne pas utiliser cet article seul pour justifier une recommandation de réentraînement de tokenizer ou une explication des capacités de raisonnement numérique.
