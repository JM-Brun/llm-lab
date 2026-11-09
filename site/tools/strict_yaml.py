"""Safe YAML loading that rejects duplicate authored mapping keys.

The loader preserves PyYAML's safe types and YAML merge semantics. Explicit
overrides of merged defaults remain valid; repeating a key in the same mapping
is an error with the source location of both occurrences.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore[import-untyped]


class _UniqueKeyLoader(yaml.SafeLoader):  # type: ignore[misc]
    """Check explicit keys before SafeLoader expands YAML merges."""

    def construct_mapping(self, node: Any, deep: bool = False) -> dict[Any, Any]:
        if isinstance(node, yaml.MappingNode):
            seen: dict[Any, Any] = {}
            merge_mark = None
            for key_node, _ in node.value:
                if key_node.tag == "tag:yaml.org,2002:merge":
                    if merge_mark is not None:
                        raise yaml.constructor.ConstructorError(
                            "while constructing a mapping",
                            merge_mark,
                            "found duplicate key '<<'",
                            key_node.start_mark,
                        )
                    merge_mark = key_node.start_mark
                    continue
                key = self.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in seen
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        "found an unhashable key",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        seen[key],
                        f"found duplicate key {key!r}",
                        key_node.start_mark,
                    )
                seen[key] = key_node.start_mark
        return cast(dict[Any, Any], super().construct_mapping(node, deep=deep))


class _NamedStringIO(StringIO):
    def __init__(self, text: str, name: str) -> None:
        super().__init__(text)
        self.name = name


def parse_yaml(text: str, *, source: str) -> Any:
    """Parse a YAML fragment and identify its source in parser errors."""
    with _NamedStringIO(text, source) as stream:
        return yaml.load(stream, Loader=_UniqueKeyLoader)


def load_yaml(path: Path) -> Any:
    """Load a UTF-8 YAML document with filename and line-number diagnostics."""
    with path.open(encoding="utf-8") as stream:
        return yaml.load(stream, Loader=_UniqueKeyLoader)
