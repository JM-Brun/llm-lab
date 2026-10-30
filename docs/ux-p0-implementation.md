# P0 UX implementation — homepage and navigation

## Scope

This change applies the first structural pass from the high-level UX review. It is limited to the bilingual landing pages and the Quarto sidebar; it does not introduce new model implementations or claim that planned features are available.

## Navigation decision

The sidebar groups three related but distinct stages under one parent:

- Prepare text and data
- Represent text
- Compute with the Transformer

The three stages remain separately named and numbered. They are nested under **Data pipelines & representations / Pipelines de données & représentations** to reduce top-level visual density without erasing the conceptual boundaries between preprocessing, representation, and computation.

The same hierarchy is used in French and English. Prediction, learning objective, evaluation, practice, and deep dives remain top-level because they represent different learner tasks.

## Homepage decision

The existing seven-step route and three-process diagram already provide complementary orientation:

- the process diagram distinguishes inference, training, and evaluation;
- the seven-step route describes conceptual dependencies;
- the hero actions provide immediate entry points.

Adding another profile chooser or a second curriculum diagram would duplicate these structures. The homepage therefore introduces a visible fil rouge: a small decoder-only GPT trained from random initialization, with a French-language corpus only after provenance and licence are selected.

The project is a learning target, not a claim that the implementation exists. No interactive demo is added until it can reuse tested Python code and expose verifiable outputs.

## Status and evidence policy

Do not add generic “complete” badges until each page has a maintained status record separating:

1. conceptual coverage;
2. implementation availability;
3. test/CI evidence;
4. rendered desktop/mobile review.

A page's presence is not evidence that its code is implemented or validated.

## Deferred items

- Cmd/Ctrl+K search hint: confirm the actual Quarto search shortcut and keyboard behavior before advertising it.
- Adaptive profile selector: reconsider only if user research shows that the existing entry points are insufficient.
- Interactive tensor/attention demo: implement only against canonical Python code and tests.
- Curriculum DAG and quizzes: separate work; preserve the sequential route as an accessible fallback.
- Dark mode and typography: require a dedicated visual regression pass rather than a broad unreviewed palette change.

## Validation still required

- Quarto build.
- Local-link and bilingual-parity checks.
- Desktop and mobile rendered inspection.
- Keyboard navigation and focus-state review.
