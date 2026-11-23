"""Shared integrity error for the project metadata projection."""

from __future__ import annotations


class ProjectIndexIntegrityError(ValueError):
    """A canonical project relation points to a missing or invalid record."""

    def __init__(self, *, source: str, record_id: str, relation: str, target: object) -> None:
        self.source = source
        self.record_id = record_id
        self.relation = relation
        self.target = target
        super().__init__(
            f"{source}: record {record_id!r} has invalid {relation} reference {target!r}"
        )
