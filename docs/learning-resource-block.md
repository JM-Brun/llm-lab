# Supplementary resource block

## Purpose

The learning path should read as one coherent explanation. Optional destinations—hands-on explorations, further reading, and dedicated exercise collections—belong together in one quiet, collapsed-by-default block at the end of the lesson.

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

</div>
</details>
```

Use only the categories that have content. Do not add empty headings or filler links. Keep descriptions concise and make each link's purpose clear.

## Editorial boundaries

- **Main flow:** definitions, explanations, caveats, figures, links needed to understand the current argument, and short comprehension checks.
- **Explore in practice:** optional interactive demonstrations, notebooks, controlled experiments, and hands-on workshops.
- **Further reading:** optional papers, references, advanced companion pages, and implementation resources.
- **Exercises:** links to a separate exercise collection or dedicated practice page.
- **Self-check:** remains in the main lesson when it provides immediate formative feedback; its answer key may remain independently collapsed.

The disclosure is not a dumping ground. A link should remain beside the relevant explanation when it is necessary to follow that explanation.

## Accessibility and compatibility

- Keep `<details>` closed by default: never add the `open` attribute.
- Use the native `<summary>` as the only disclosure control; do not recreate it with a custom button.
- Keep a visible focus indicator and readable summary text.
- Preserve existing fragment IDs when moving headings. If a fragment targets content inside the disclosure, the global enhancement opens the containing block before navigation.
- Test keyboard activation, narrow viewports, direct fragment URLs, and both language versions.

## Rollout checklist

1. Inventory existing end-of-page optional sections in the learning path.
2. Move only optional destinations into the disclosure; preserve main-flow teaching and self-checks.
3. Reuse the same class names and category order in French and English.
4. Preserve all public fragment IDs and check incoming links.
5. Render both language versions and verify the block is closed on initial load.
