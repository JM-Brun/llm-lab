from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXTRACTIONS = ROOT / "data" / "extractions"


def _load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    assert isinstance(value, dict)
    return value


def _corpus():
    sources_doc = _load(ROOT / "data" / "sources.yml")
    concepts_doc = _load(ROOT / "data" / "concepts.yml")
    sources = {source["id"]: source for source in sources_doc["sources"]}
    extractions = {
        record["source_id"]: record
        for path in sorted(EXTRACTIONS.glob("*.yml"))
        if (record := _load(path)).get("source_id")
    }
    return sources, extractions, concepts_doc


def test_historical_scan_blocks_pair_with_source_history_without_lossy_assumptions() -> None:
    sources, extractions, _ = _corpus()
    scan_records = {
        source_id: record for source_id, record in extractions.items() if "scan" in record
    }

    assert len(scan_records) == 36
    expected_scan_keys = {
        "accessed_at",
        "author_text",
        "code_data",
        "comments",
        "figures_media",
        "linked_resources",
        "metadata",
        "retrieval_method",
        "rights",
        "unresolved_questions",
    }

    for source_id, record in scan_records.items():
        assert source_id in sources
        scan = record["scan"]
        assert isinstance(scan, dict)
        assert set(scan) == expected_scan_keys

        history = sources[source_id].get("scan_history", [])
        history_dates = {str(event["accessed_at"]) for event in history}
        assert str(scan["accessed_at"]) in history_dates


def test_historical_scan_newer_source_events_remain_distinguishable() -> None:
    sources, extractions, _ = _corpus()
    expected = {
        "andrej-karpathy-gpt-tokenizer-video": ("2026-10-30", "2026-11-19"),
        "maarten-grootendorst-visual-guide-multimodal-generation": (
            "2026-11-07",
            "2026-11-15",
        ),
        "marek-ryabinin-score-centering-off-policy-rl-2026": (
            "2026-11-09",
            "2026-11-19",
        ),
    }

    for source_id, (extraction_date, latest_source_date) in expected.items():
        assert extractions[source_id]["scan"]["accessed_at"] == extraction_date
        history = sources[source_id]["scan_history"]
        assert max(str(event["accessed_at"]) for event in history) == latest_source_date


def test_aiedge_scan_preserves_facet_detail_beyond_the_source_event_summary() -> None:
    sources, extractions, _ = _corpus()
    source_id = "aiedge-how-cuda-graphs-speed-up-llm-inference"
    scan = extractions[source_id]["scan"]
    event = next(
        event
        for event in sources[source_id]["scan_history"]
        if str(event["accessed_at"]) == str(scan["accessed_at"])
    )

    assert scan["author_text"]["status"] == "partial"
    assert scan["figures_media"]["status"] == "not-inspected"
    assert scan["code_data"]["status"] == "not-inspected"
    assert scan["rights"]["status"] == "unknown"
    assert len(scan["unresolved_questions"]) == 3
    assert len(event["inspected_scope"]) == 3
    assert len(event["limitations"]) == 5
    assert "unresolved_questions" not in event
    assert "rights" not in event


def test_all_canonical_mapping_blocks_are_preserved_and_classified_by_shape() -> None:
    _, extractions, concepts = _corpus()
    mappings = {
        source_id: record["canonical_mapping"]
        for source_id, record in extractions.items()
        if "canonical_mapping" in record
    }

    assert len(mappings) == 28
    assert all(isinstance(mapping, dict) for mapping in mappings.values())
    assert all(
        {"proposed_relations", "route_implications", "decision_summary"} <= set(mapping)
        for mapping in mappings.values()
    )
    assert sum("proposed_concepts" in mapping for mapping in mappings.values()) == 27
    assert sum("integrated_concepts" in mapping for mapping in mappings.values()) == 1

    non_empty_relations = {
        source_id: mapping["proposed_relations"]
        for source_id, mapping in mappings.items()
        if mapping["proposed_relations"]
    }
    assert set(non_empty_relations) == {
        "aiedge-how-cuda-graphs-speed-up-llm-inference",
        "marek-ryabinin-score-centering-off-policy-rl-2026",
    }

    marek = mappings["marek-ryabinin-score-centering-off-policy-rl-2026"]
    assert len(marek["integrated_concepts"]) == 6
    canonical_concept_ids = {concept["id"] for concept in concepts["concepts"]}
    assert {item["id"] for item in marek["integrated_concepts"]} <= canonical_concept_ids


def test_aiedge_relation_proposals_are_not_canonical_edges_or_declared_relations() -> None:
    _, extractions, concepts = _corpus()
    mapping = extractions["aiedge-how-cuda-graphs-speed-up-llm-inference"]["canonical_mapping"]
    concept_ids = {concept["id"] for concept in concepts["concepts"]}
    relation_types = set(concepts["relation_types"])
    canonical_edges = {(edge["from"], edge["type"], edge["to"]) for edge in concepts["relations"]}

    assert mapping["proposed_concepts"][0]["id"] == "cuda-graphs"
    assert "cuda-graphs" not in concept_ids
    assert {"decode-step", "kv-cache"} <= concept_ids

    proposals = mapping["proposed_relations"]
    assert {(item["type"]) for item in proposals} == {"optimizes", "complements"}
    assert all(item["type"] not in relation_types for item in proposals)
    assert all(
        (item["from"], item["type"], item["to"]) not in canonical_edges for item in proposals
    )


def test_marek_prose_relations_are_not_silently_promoted_to_edges() -> None:
    _, extractions, concepts = _corpus()
    mapping = extractions["marek-ryabinin-score-centering-off-policy-rl-2026"]["canonical_mapping"]
    proposals = mapping["proposed_relations"]

    assert len(proposals) == 6
    assert all(isinstance(proposal, str) for proposal in proposals)
    assert all("from" not in proposal and "type" not in proposal for proposal in proposals)

    canonical_edges = {(edge["from"], edge["type"], edge["to"]) for edge in concepts["relations"]}
    assert (
        "score-function",
        "part-of",
        "policy-gradient",
    ) in canonical_edges
    assert (
        "training-inference-mismatch",
        "constrains",
        "policy-gradient",
    ) in canonical_edges
    assert (
        "score-centering",
        "applies-to",
        "off-policy-reinforcement-learning",
    ) in canonical_edges
    assert (
        "importance-sampling",
        "applies-to",
        "off-policy-reinforcement-learning",
    ) in canonical_edges
    assert (
        "importance-sampling",
        "contrasts-with",
        "score-centering",
    ) in canonical_edges

def test_marek_concepts_have_bilingual_pages_and_documentary_evidence() -> None:
    sources, extractions, concepts = _corpus()
    source_id = "marek-ryabinin-score-centering-off-policy-rl-2026"
    extraction = extractions[source_id]
    mapping = extraction["canonical_mapping"]
    integrated_ids = {item["id"] for item in mapping["integrated_concepts"]}
    expected_ids = {
        "policy-gradient",
        "score-function",
        "off-policy-reinforcement-learning",
        "training-inference-mismatch",
        "score-centering",
        "importance-sampling",
    }
    assert integrated_ids == expected_ids

    concept_by_id = {concept["id"]: concept for concept in concepts["concepts"]}
    for concept_id in expected_ids:
        concept = concept_by_id[concept_id]
        assert set(concept["labels"]) >= {"fr", "en"}
        assert set(concept["definitions"]) >= {"fr", "en"}
        assert {"fr/score-centering", "en/score-centering"} <= set(concept["resources"])

    fr_page = ROOT / "site" / "fr" / "score-centering.qmd"
    en_page = ROOT / "site" / "en" / "score-centering.qmd"
    assert fr_page.is_file()
    assert en_page.is_file()
    fr_text = fr_page.read_text(encoding="utf-8")
    en_text = en_page.read_text(encoding="utf-8")
    for phrase in (
        "gradient de politique",
        "fonction score",
        "hors politique",
        "décalage entraînement",
        "centrage du score",
        "échantillonnage par importance",
    ):
        assert phrase in fr_text.lower()
    for phrase in (
        "policy-gradient",
        "score function",
        "off-policy",
        "training–inference mismatch",
        "score centering",
        "importance sampling",
    ):
        assert phrase in en_text.lower()

    source = sources[source_id]
    assert {"fr/score-centering", "en/score-centering"} <= set(source["related"]["pages"])
    assert expected_ids <= set(source["related"]["concepts"])
    verification_event = next(
        event for event in source["scan_history"] if event["accessed_at"] == "2026-11-19"
    )
    assert any("Canonical arXiv v1 PDF" in item for item in verification_event["inspected_scope"])
    assert any("tests/test_loss.py" in item for item in verification_event["inspected_scope"])

    review = ROOT / "docs" / "source-reviews" / "score-centering-2026-11.md"
    assert "Verification update — 2026-11-19" in review.read_text(encoding="utf-8")
    assert all("locator" in item and "evidence" in item for item in extraction["items"])


def test_marek_bilingual_pages_do_not_retain_superseded_audit_warning() -> None:
    fr_page = (ROOT / "site" / "fr" / "score-centering.qmd").read_text(encoding="utf-8")
    en_page = (ROOT / "site" / "en" / "score-centering.qmd").read_text(encoding="utf-8")

    assert "les tests officiels n'ont pas été exécutés" not in fr_page
    assert "official tests have not been executed" not in en_page
    assert "jax>=0.11.1" in fr_page
    assert "jax>=0.11.1" in en_page

