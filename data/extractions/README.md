# Structured source extractions

Store one YAML file per source in this directory, named with its stable source ID.

The canonical source identity and scan history live in data/sources.yml.
Extraction records contain atomic, evidence-linked items; they are not a second source catalogue or concept registry.

## Top-level shape

    schema_version: 1
    source_id: example-source
    items:
      - id: example-source:attention-definition
        kind: definition
        summary: "A concise paraphrase of the extracted idea."
        locator:
          type: section
          value: "2.1"
          label: "Scaled dot-product attention"
        evidence:
          kind: formal-definition
          confidence: high
          scope: "The paper's mathematical formulation."
          assumptions: []
          limitations: []
        classification:
          primary_theme: architectures-mechanisms
          secondary_themes:
            - mathematical-tools-geometry
          tags:
            - topic:attention
            - method:scaled-dot-product
          concept_ids:
            - self-attention
        candidate_destinations:
          pages:
            - en/scaled-dot-product-attention
          concepts:
            - self-attention
        disposition: pending

## Record rules

- source_id must resolve to exactly one record in data/sources.yml.
- Item IDs are stable and unique; do not derive them from translated labels.
- kind must use data/source-taxonomy.yml.
- A locator must identify the actual inspected location (page, section, PDF page, figure, code path, commit, timestamp, or dataset field).
- Evidence and confidence describe the extracted item, not the reputation of the source.
- If an item comes from a reader comment or another voice embedded in a source, add `provenance` with its voice, speaker (only if explicit), parent source ID, exact comment locator and capture date. Add `verification` separately when checking the claim against independent evidence; never merge the comment and verifier's interpretation into one attributed statement.
- Item-level classification may refine the source classification; it must not silently rewrite it.
- concept_ids refer only to existing canonical concepts in data/concepts.yml. Candidate concepts are proposals, not IDs to insert pre-emptively.
- Candidate page IDs are proposals and must resolve before integration.
- disposition: pending is an extraction hand-off state, not a publication status.
- Keep full text, copied figures, datasets, and code out of these records unless rights permit it. Prefer concise paraphrases and links to source locations.

The exact schema and validation contract is specified in docs/source-catalogue-schema.md.
