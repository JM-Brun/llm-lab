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
    }

    for source_id, (extraction_date, latest_source_date) in expected.items():
        assert extractions[source_id]["scan"]["accessed_at"] == extraction_date
        history = sources[source_id]["scan_history"]
        assert max(str(event["accessed_at"]) for event in history) == latest_source_date


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
        {"proposed_concepts", "proposed_relations", "route_implications", "decision_summary"}
        <= set(mapping)
        for mapping in mappings.values()
    )

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
