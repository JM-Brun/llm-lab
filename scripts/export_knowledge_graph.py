#!/usr/bin/env python3
"""Export the canonical LLM Lab knowledge model as deterministic JSON-LD 1.1.

YAML remains the authoring source. This export is an interoperability projection,
not a second source of truth and not a replacement for the interactive map.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONCEPTS = ROOT / "data" / "concepts.yml"
DOMAINS = ROOT / "data" / "domains.yml"
BASE = "https://jm-brun.github.io/llm-lab"
LLMLAB = f"{BASE}/vocab/"
CONCEPT_SCHEME = f"{BASE}/id/scheme/concepts"
DOMAIN_SCHEME = f"{BASE}/id/scheme/domains"
RELATION_TYPES = {
    "prerequisite",
    "part-of",
    "generalizes",
    "contrasts-with",
    "analogy",
    "implemented-by",
    "applies-to",
    "constrains",
    "produces",
    "normalized-by",
    "evaluated-by",
    "represented-by",
    "contributes-to",
    "mapped-by",
}


def _page_records() -> dict[str, dict[str, Any]]:
    """Read published page metadata without inferring concepts from headings."""
    records: dict[str, dict[str, Any]] = {}
    for path in sorted(SITE.rglob("*.qmd")):
        source = path.read_text(encoding="utf-8")
        front_match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", source, re.DOTALL)
        match = re.search(
            r"<!--\s*\nLLM-LAB-PAGE-MAP v1\n(.*?)\n-->",
            source,
            re.DOTALL,
        )
        if match is None or front_match is None:
            continue
        front = yaml.safe_load(front_match.group(1))
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict):
            continue
        tags = {
            key: value
            for item in metadata.get("tags", [])
            if isinstance(item, str) and ":" in item
            for key, value in [item.split(":", maxsplit=1)]
        }
        if tags.get("status") != "published":
            continue
        page_id = metadata.get("id")
        language = tags.get("language")
        if not isinstance(page_id, str) or language not in {"fr", "en"}:
            continue
        if "/" not in page_id:
            continue
        _, slug = page_id.split("/", maxsplit=1)
        href = f"{BASE}/{language}/" if slug == "index" else f"{BASE}/{language}/{slug}.html"
        records[page_id] = {
            "id": page_id,
            "url": href,
            "language": language,
            "title": str(front.get("title", slug)),
            "scope": str(metadata.get("scope", "")),
            "purpose": str(metadata.get("purpose", "")),
            "type": tags.get("type", "concept-lesson"),
            "level": tags.get("level", "core"),
        }
    return records


def _jsonld_literal(value: str, language: str) -> dict[str, str]:
    return {"@value": value, "@language": language}


def relation_predicate(kind: str) -> str:
    """Return the SKOS or project predicate for a typed concept relation."""
    if kind not in RELATION_TYPES:
        raise ValueError(f"Unsupported relation type: {kind}")
    if kind == "generalizes":
        return "skos:narrower"
    return "llmlab:" + re.sub(r"-(.)", lambda match: match.group(1).upper(), kind)


def build_graph() -> dict[str, Any]:
    """Build a stable JSON-LD graph from canonical YAML and published pages."""
    concepts_data = yaml.safe_load(CONCEPTS.read_text(encoding="utf-8"))
    domains_data = yaml.safe_load(DOMAINS.read_text(encoding="utf-8"))
    pages = _page_records()

    graph: list[dict[str, Any]] = [
        {
            "@id": CONCEPT_SCHEME,
            "@type": "skos:ConceptScheme",
            "skos:prefLabel": [
                _jsonld_literal("Concepts LLM Lab", "fr"),
                _jsonld_literal("LLM Lab concepts", "en"),
            ],
        },
        {
            "@id": DOMAIN_SCHEME,
            "@type": "skos:ConceptScheme",
            "skos:prefLabel": [
                _jsonld_literal("Domaines de connaissance LLM Lab", "fr"),
                _jsonld_literal("LLM Lab knowledge domains", "en"),
            ],
        },
    ]

    for domain in domains_data["domains"]:
        node: dict[str, Any] = {
            "@id": f"{BASE}/id/domain/{domain['id']}",
            "@type": "skos:Concept",
            "skos:inScheme": {"@id": DOMAIN_SCHEME},
            "skos:prefLabel": [
                _jsonld_literal(domain["labels"][lang], lang) for lang in ("fr", "en")
            ],
            "skos:definition": [
                _jsonld_literal(domain["descriptions"][lang], lang) for lang in ("fr", "en")
            ],
        }
        graph.append(node)

    for concept in concepts_data["concepts"]:
        node = {
            "@id": f"{BASE}/id/concept/{concept['id']}",
            "@type": "skos:Concept",
            "skos:inScheme": {"@id": CONCEPT_SCHEME},
            "skos:prefLabel": [
                _jsonld_literal(concept["labels"][lang], lang) for lang in ("fr", "en")
            ],
            "skos:definition": [
                _jsonld_literal(concept["definitions"][lang], lang) for lang in ("fr", "en")
            ],
            "dcterms:subject": [
                {"@id": f"{BASE}/id/domain/{domain_id}"} for domain_id in concept["domains"]
            ],
        }
        graph.append(node)

    for concept in concepts_data["concepts"]:
        concept_uri = f"{BASE}/id/concept/{concept['id']}"
        for page_id in concept["resources"]:
            page = pages.get(page_id)
            if page is None:
                continue
            graph.append(
                {
                    "@id": page["url"],
                    "@type": ["schema:WebPage", "schema:LearningResource"],
                    "schema:name": page["title"],
                    "schema:inLanguage": page["language"],
                    "schema:description": page["scope"],
                    "schema:abstract": page["purpose"],
                    "schema:learningResourceType": page["type"],
                    "llmlab:editorialLevel": page["level"],
                    "schema:about": {"@id": concept_uri},
                }
            )

    # Only genuine taxonomy/generalization edges map to SKOS hierarchy.
    # Other edge meanings are preserved as project-specific predicates.
    for relation in concepts_data["relations"]:
        source = f"{BASE}/id/concept/{relation['from']}"
        target = f"{BASE}/id/concept/{relation['to']}"
        kind = relation["type"]
        predicate = relation_predicate(kind)
        graph.append({"@id": source, predicate: {"@id": target}})

    # Provenance is intentionally limited to the generated export and its
    # canonical source artifacts; it does not assert claim-level evidence.
    export_uri = f"{BASE}/knowledge-graph.jsonld"
    activity_uri = f"{BASE}/id/activity/knowledge-graph-export"
    source_uris = [
        f"{BASE}/source/data/concepts.yml",
        f"{BASE}/source/data/domains.yml",
        f"{BASE}/source/site-page-metadata",
    ]
    graph.append(
        {
            "@id": export_uri,
            "@type": "prov:Entity",
            "dcterms:format": "application/ld+json",
            "prov:wasGeneratedBy": {"@id": activity_uri},
            "prov:wasDerivedFrom": [{"@id": uri} for uri in source_uris],
        }
    )
    graph.append(
        {
            "@id": activity_uri,
            "@type": "prov:Activity",
            "prov:used": [{"@id": uri} for uri in source_uris],
        }
    )
    for uri in source_uris:
        graph.append({"@id": uri, "@type": "prov:Entity"})

    return {
        "@context": {
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "dcterms": "http://purl.org/dc/terms/",
            "schema": "https://schema.org/",
            "prov": "http://www.w3.org/ns/prov#",
            "llmlab": LLMLAB,
        },
        "@graph": graph,
    }


def write_export(output: Path = SITE / "knowledge-graph.jsonld") -> Path:
    """Write the deterministic JSON-LD projection and return its path."""
    payload = build_graph()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "site" / "knowledge-graph.jsonld",
        help="Output JSON-LD path (default: site/knowledge-graph.jsonld)",
    )
    args = parser.parse_args()
    output = write_export(args.output)
    sys.stdout.write(f"Exported JSON-LD knowledge graph to {output}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
