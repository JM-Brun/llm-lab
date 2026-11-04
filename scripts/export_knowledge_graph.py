#!/usr/bin/env python3
"""Export the canonical LLM Lab knowledge model as deterministic JSON-LD 1.1.

YAML remains the authoring source. This export is an interoperability projection,
not a second source of truth and not a replacement for the interactive map.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONCEPTS = ROOT / "data" / "concepts.yml"
DOMAINS = ROOT / "data" / "domains.yml"
RESOURCES = ROOT / "data" / "resources.yml"
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
            "source_uri": (
                "https://github.com/JM-Brun/llm-lab/blob/main/site/"
                f"{path.relative_to(SITE).as_posix()}"
            ),
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
    resources_data = yaml.safe_load(RESOURCES.read_text(encoding="utf-8"))
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

    # Build each page node once, even when several concepts or code resources
    # refer to it. Existing concept.resources remain published page IDs.
    page_concepts: dict[str, set[str]] = {}
    for concept in concepts_data["concepts"]:
        for page_id in concept["resources"]:
            if page_id in pages:
                page_concepts.setdefault(page_id, set()).add(concept["id"])
    active_resources = [
        item
        for item in resources_data["resources"]
        if item["status"] in {"published", "deprecated"}
    ]
    resource_page_ids = {page_id for item in active_resources for page_id in item["referenced_by"]}
    for page_id in sorted(set(page_concepts) | resource_page_ids):
        page = pages.get(page_id)
        if page is None:
            continue
        node: dict[str, Any] = {
            "@id": page["url"],
            "@type": ["schema:WebPage", "schema:LearningResource"],
            "schema:name": page["title"],
            "schema:inLanguage": page["language"],
            "schema:description": page["scope"],
            "schema:abstract": page["purpose"],
            "schema:learningResourceType": page["type"],
            "llmlab:editorialLevel": page["level"],
        }
        concept_uris = sorted(
            f"{BASE}/id/concept/{concept_id}" for concept_id in page_concepts.get(page_id, set())
        )
        if concept_uris:
            node["schema:about"] = [{"@id": uri} for uri in concept_uris]
        graph.append(node)

    # First-class non-page resources have their own stable IDs. Local file
    # locations are links, not resource identifiers; repository metadata is
    # deliberately not copied onto each source file as schema:codeRepository.
    for resource in active_resources:
        location = resource["location"]
        location_url = (
            f"https://github.com/JM-Brun/llm-lab/blob/main/{location['path']}"
            if location["type"] == "local"
            else location["url"]
        )
        node = {
            "@id": f"{BASE}/id/resource/{resource['id']}",
            "@type": "schema:SoftwareSourceCode",
            "schema:name": [
                _jsonld_literal(resource["labels"][lang], lang) for lang in ("fr", "en")
            ],
            "schema:description": [
                _jsonld_literal(resource["descriptions"][lang], lang) for lang in ("fr", "en")
            ],
            "schema:inLanguage": resource["language"],
            "schema:url": location_url,
            "llmlab:resourceKind": resource["kind"],
            "llmlab:lifecycleStatus": resource["status"],
            "schema:subjectOf": [
                {"@id": pages[page_id]["url"]}
                for page_id in sorted(resource["referenced_by"])
                if page_id in pages
            ],
        }
        if resource.get("programming_language"):
            node["schema:programmingLanguage"] = resource["programming_language"]
        if resource["concepts"]:
            node["schema:about"] = [
                {"@id": f"{BASE}/id/concept/{concept_id}"}
                for concept_id in sorted(resource["concepts"])
            ]
        provenance = resource.get("provenance", {})
        if "creator" in provenance:
            node["dcterms:creator"] = provenance["creator"]
        if "publisher" in provenance:
            node["dcterms:publisher"] = provenance["publisher"]
        if "source_url" in provenance:
            node["dcterms:source"] = {"@id": provenance["source_url"]}
        if "license" in provenance:
            node["dcterms:license"] = provenance["license"]
        graph.append(node)

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
    referenced_page_ids = {
        page_id for concept in concepts_data["concepts"] for page_id in concept["resources"]
    } | resource_page_ids
    page_source_uris = sorted(
        {pages[page_id]["source_uri"] for page_id in referenced_page_ids if page_id in pages}
    )
    resource_source_uris = [
        f"https://github.com/JM-Brun/llm-lab/blob/main/{item['location']['path']}"
        for item in active_resources
        if item["location"]["type"] == "local"
    ]
    declared_source_uris = [
        item["provenance"]["source_url"]
        for item in active_resources
        if item.get("provenance", {}).get("source_url")
    ]
    source_uris = sorted(
        {
            "https://github.com/JM-Brun/llm-lab/blob/main/data/concepts.yml",
            "https://github.com/JM-Brun/llm-lab/blob/main/data/domains.yml",
            "https://github.com/JM-Brun/llm-lab/blob/main/data/resources.yml",
            *page_source_uris,
            *resource_source_uris,
            *declared_source_uris,
        }
    )
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
