# Supplementary resource block

## Purpose

The learning path should read as one coherent explanation. Optional destinations—hands-on explorations, further reading, and dedicated exercise collections—belong together in one quiet, collapsed-by-default block at the very end of the lesson. The block also contains the page's short **self-check** so that practice and assessment material share one predictable place.

The shared presentation uses native HTML `<details>` and `<summary>`, styled by `.learning-resources` in `site/styles.scss`. It requires no JavaScript for ordinary opening and closing. The small global enhancement in `site/includes/accessibility-fixes.html` opens the block when a deep link targets content inside it.

## Canonical template

Use this structure in Quarto pages, translating labels and descriptions naturally:

```html
<details class="learning-resources">
<summary>
  <span class="learning-resources__title">Ressources complémentaires</span>
  <span class="learning-resources__description">Expérimenter, approfondir et s'exercer sur les notions de cette leçon.</span>
</summary>
<div class="learning-resources__content" markdown="1">

### Explorer en pratique

Une phrase qui explique l'intérêt de la ressource, puis son [lien explicite](...).

### Pour approfondir

Lectures, références ou implémentations réellement complémentaires.

### Exercices

Accès à la [page d'exercices dédiée](...).

::: {.self-check}
## Vérifier sa compréhension

Une ou plusieurs questions courtes pour vérifier les idées essentielles.

<details>
<summary>Afficher les réponses</summary>

Réponses ou raisonnement, lorsque cela aide l'apprentissage.

</details>
:::

</div>
</details>
```

Use only the categories that have content. Do not add empty headings or filler links. The block can grow incrementally as exercises, experiments, and further resources are created. Keep descriptions concise and make each link's purpose clear.

## Editorial boundaries

- **Main flow:** definitions, explanations, caveats, figures, links needed to understand the current argument, and short explanations that are essential to follow the lesson.
- **Explore in practice:** optional interactive demonstrations, notebooks, controlled experiments, and hands-on workshops.
- **Further reading:** optional papers, references, advanced companion pages, and implementation resources.
- **Exercises:** links to a separate exercise collection or dedicated practice page, plus exercise material intended as optional follow-up.
- **Self-check:** the page's short comprehension questions, exercise links attached to those questions, and any answer key or reasoning. Keep answers independently collapsed when useful.

The disclosure is not a dumping ground. A link should remain beside the relevant explanation when it is necessary to follow that explanation. Do not move worked examples, essential caveats, or required reasoning into the block.

## Placement and accessibility

- Place the complete `.learning-resources` block at the very end of the page, after the visible language switch and any essential learning-path navigation.
- Keep `<details>` closed by default: never add the `open` attribute.
- Use the native `<summary>` as the only disclosure control; do not recreate it with a custom button.
- Keep a visible focus indicator and readable summary text.
- Preserve existing fragment IDs when moving headings. If a fragment targets content inside the disclosure, the global enhancement opens the containing block before navigation.
- Test keyboard activation, narrow viewports, direct fragment URLs, and both language versions.

## Rollout checklist

1. Inventory existing end-of-page optional sections in the learning path.
2. Move optional destinations and the page's self-check into the disclosure; preserve essential teaching content in the main flow.
3. Reuse the same class names and category order in French and English.
4. Preserve all public fragment IDs and check incoming links.
5. Render both language versions and verify the block is closed on initial load.

## Build-path application

The Build path uses the same disclosure, but its editorial boundary needs extra care:

- Keep worked examples, executable code, and explanations needed to understand the current implementation step in the main lesson.
- Move the separate exercise-page link and the page's short self-check into the disclosure. Keep answer keys independently collapsed when useful.
- Keep explicit previous/next links that define a guided sequence visible in the main flow under a concise **Connections** section. They are essential progression controls, not optional resources.
- Move other navigation collections (related concept pages, source files, and test files) into **Further reading** when they are optional orientation rather than required steps in the explanation.
- Move curated external references and companion material into **Further reading**; keep a link inline when the current explanation depends on it.
- In pages with a revision sheet or recap, keep it in the main flow: it consolidates the lesson rather than pointing to another destination.

This distinction is particularly important in implementation walkthroughs: an inline worked example teaches the implementation, while the dedicated self-check and a link to a separate exercise page are supplementary practice.
