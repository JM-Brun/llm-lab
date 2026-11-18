#!/usr/bin/env python3
"""Benchmark concept-registry validation on deterministic synthetic growth fixtures.

Run from the repository root with the same Python environment as the site tools:
    uv run --no-project --with-requirements docs/requirements-history-validation.txt \
      --python 3.12 python site/tools/benchmark_concept_registry.py
"""

from __future__ import annotations

import argparse
import copy
import json
import platform
import statistics
import subprocess
import sys
import time
import tracemalloc
from itertools import pairwise
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "site" / "tools"
sys.path.insert(0, str(TOOLS))

from check_concept_registry import validate_registry  # noqa: E402
from page_index import load_published_pages  # noqa: E402


SHAPES = ("chain", "hub", "disconnected", "dense", "mixed")


def _build_synthetic_relations(
    identifiers: list[str],
    relation_types: dict[str, Any],
    shape: str,
    dense_degree: int,
    mixed_degree: int,
) -> list[dict[str, str]]:
    """Build deterministic valid relations for one controlled graph topology."""
    if shape not in SHAPES:
        raise ValueError(f"unsupported synthetic graph shape: {shape}")
    if shape == "chain":
        pairs = list(pairwise(identifiers))
        return [{"from": source, "type": "part-of", "to": target} for source, target in pairs]

    if shape == "hub":
        hub_count = min(2, len(identifiers))
        hubs = identifiers[-hub_count:] if hub_count else []
        leaves = identifiers[:-hub_count] if hub_count else []
        return [
            {"from": source, "type": "part-of", "to": hubs[index % len(hubs)]}
            for index, source in enumerate(leaves)
        ]

    if shape == "disconnected":
        relations: list[dict[str, str]] = []
        component_size = 10
        for start in range(0, len(identifiers), component_size):
            component = identifiers[start : start + component_size]
            relations.extend(
                {"from": source, "type": "part-of", "to": target}
                for source, target in pairwise(component)
            )
        return relations

    if shape == "dense":
        return [
            {"from": source, "type": "part-of", "to": target}
            for index, source in enumerate(identifiers)
            for target in identifiers[index + 1 : index + 1 + dense_degree]
        ]

    candidates = [
        kind
        for kind, definition in sorted(relation_types.items())
        if isinstance(definition, dict) and definition.get("learning_dependency") is not True
    ]
    if not candidates:
        raise ValueError("the baseline registry has no relation types for mixed workload")
    degree = min(mixed_degree, len(candidates))
    relations = []
    for index, source in enumerate(identifiers):
        for offset, target in enumerate(
            identifiers[index + 1 : index + 1 + degree]
        ):
            kind = candidates[(index + offset) % len(candidates)]
            definition = relation_types[kind]
            from_id, to_id = source, target
            if definition.get("direction") == "symmetric" and from_id >= to_id:
                from_id, to_id = to_id, from_id
            relations.append({"from": from_id, "type": kind, "to": to_id})
    return relations


def build_synthetic_registry(
    base: dict[str, Any],
    target_size: int,
    shape: str = "chain",
    dense_degree: int = 4,
    mixed_degree: int = 6,
) -> dict[str, Any]:
    """Extend the real registry with valid bilingual concepts and a chosen topology."""
    if target_size < len(base["concepts"]):
        raise ValueError(
            f"target size {target_size} is smaller than baseline {len(base['concepts'])}"
        )
    if dense_degree < 1 or mixed_degree < 1:
        raise ValueError("synthetic relation degrees must be at least 1")

    result = copy.deepcopy(base)
    concepts = result["concepts"]
    if not concepts:
        raise ValueError("the baseline registry must contain at least one concept")
    template = concepts[0]
    additions = target_size - len(concepts)
    synthetic_ids = [f"benchmark-concept-{index:05d}" for index in range(additions)]

    for index, identifier in enumerate(synthetic_ids):
        concept = copy.deepcopy(template)
        concept["id"] = identifier
        concept["labels"] = {
            "fr": f"Concept synthétique {index}",
            "en": f"Synthetic concept {index}",
        }
        concept["definitions"] = {
            "fr": f"Définition de test pour le concept synthétique {index}.",
            "en": f"Test definition for synthetic concept {index}.",
        }
        concepts.append(concept)

    result["relations"].extend(
        _build_synthetic_relations(
            synthetic_ids,
            result["relation_types"],
            shape,
            dense_degree,
            mixed_degree,
        )
    )
    return result

def benchmark(
    base: dict[str, Any],
    published_pages: set[str],
    domain_ids: set[str],
    sizes: list[int],
    repeats: int,
    shapes: list[str],
    dense_degree: int,
    mixed_degree: int,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    baseline_size = len(base["concepts"])
    mixed_relation_types = sorted(
        kind
        for kind, definition in base["relation_types"].items()
        if isinstance(definition, dict) and definition.get("learning_dependency") is not True
    )

    for shape in shapes:
        for size in sizes:
            build_durations: list[float] = []
            validation_durations: list[float] = []
            peak_bytes: list[int] = []
            error_counts: list[int] = []
            relation_count = 0
            for _ in range(repeats):
                started = time.perf_counter()
                fixture = build_synthetic_registry(
                    base, size, shape, dense_degree, mixed_degree
                )
                build_durations.append(time.perf_counter() - started)
                relation_count = len(fixture["relations"])

                tracemalloc.start()
                started = time.perf_counter()
                errors = validate_registry(fixture, published_pages, domain_ids)
                validation_durations.append(time.perf_counter() - started)
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                peak_bytes.append(peak)
                error_counts.append(len(errors))

            rows.append(
                {
                    "shape": shape,
                    "concepts": size,
                    "relations": relation_count,
                    "fixture_build_seconds_median": round(
                        statistics.median(build_durations), 6
                    ),
                    "validation_seconds_median": round(
                        statistics.median(validation_durations), 6
                    ),
                    "validation_seconds_min": round(min(validation_durations), 6),
                    "validation_seconds_max": round(max(validation_durations), 6),
                    "validation_peak_bytes_max": max(peak_bytes),
                    "validation_error_counts": error_counts,
                }
            )

    return {
        "benchmark": "concept-registry-validation",
        "method": {
            "repeats": repeats,
            "sizes": sizes,
            "shapes": shapes,
            "baseline_concepts": baseline_size,
            "baseline_relations": len(base["relations"]),
            "topology_parameters": {
                "hub_count": 2,
                "disconnected_component_size": 10,
                "dense_degree": dense_degree,
                "mixed_degree": mixed_degree,
                "mixed_relation_types": mixed_relation_types,
            },
            "timed_scope": (
                "in-memory validate_registry call; YAML loading, page discovery, "
                "fixture construction and interpreter startup are excluded"
            ),
            "memory_scope": "tracemalloc peak during validate_registry only",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "repository_root": str(ROOT),
            "commit_sha": _git_revision(),
        },
        "results": rows,
    }


def _git_revision() -> str | None:
    """Return the checked-out commit when the benchmark runs inside a Git worktree."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[500, 2000, 10000],
        help="target total concept counts (default: 500 2000 10000)",
    )
    parser.add_argument(
        "--shapes",
        nargs="+",
        choices=SHAPES,
        default=["chain"],
        help="synthetic graph topologies (default: chain)",
    )
    parser.add_argument("--dense-degree", type=int, default=4)
    parser.add_argument("--mixed-degree", type=int, default=6)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", type=Path, help="optional JSON output path")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be at least 1")
    if args.dense_degree < 1 or args.mixed_degree < 1:
        parser.error("--dense-degree and --mixed-degree must be at least 1")

    base = yaml.safe_load((ROOT / "data" / "concepts.yml").read_text(encoding="utf-8"))
    domains = yaml.safe_load((ROOT / "data" / "domains.yml").read_text(encoding="utf-8"))
    domain_ids = {item["id"] for item in domains["domains"]}
    published_pages = {page.page_id for page in load_published_pages(ROOT / "site")}
    report = benchmark(
        base,
        published_pages,
        domain_ids,
        args.sizes,
        args.repeats,
        args.shapes,
        args.dense_degree,
        args.mixed_degree,
    )

    invalid = [row for row in report["results"] if any(row["validation_error_counts"])]
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    if invalid:
        sys.stderr.write("Synthetic fixture validation failed; inspect validation_error_counts.\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
