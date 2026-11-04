#!/usr/bin/env python3
"""Validate the language-independent concept registry."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "concepts.yml"
DOMAINS = ROOT / "data" / "domains.yml"
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
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
PAGE_ID = re.compile(r"(?:fr|en)/[a-z0-9]+(?:-[a-z0-9]+)*")


def _published_page_ids() -> set[str]:
    """Return stable IDs of published FR/EN Quarto pages."""
    published: set[str] = set()
    for language in ("fr", "en"):
        for path in (ROOT / "site" / language).glob("*.qmd"):
            source = path.read_text(encoding="utf-8")
            match = re.search(
                r"<!--\s*\nLLM-LAB-PAGE-MAP v1\n(.*?)\n-->",
                source,
                re.DOTALL,
            )
            if match is None:
                continue
            try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        domain_data = yaml.safe_load(DOMAINS.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"Cannot read concept/domain registry: {exc}\\n")
        return 1
    domain_ids, domain_errors = validate_domains(domain_data)
    errors = [*domain_errors, *validate_registry(data, _published_page_ids(), domain_ids)]
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        return 1
    sys.stdout.write(
        f"Validated {len(data['concepts'])} concepts and {len(data['relations'])} relations.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
