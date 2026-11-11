"""Canonical validation for explicit Understand stage transitions.

Transitions describe explanatory relationships, never prerequisites. This
module validates the source model without projecting or rendering it.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class LocalizedPurpose(StrictModel):
    fr: str = Field(min_length=1)
    en: str = Field(min_length=1)

    @field_validator("fr", "en")
    @classmethod
    def non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("transition purpose must not be blank")
        return value


class LocalizedTransitionPages(StrictModel):
    fr: list[str] = Field(min_length=1)
    en: list[str] = Field(min_length=1)

    @field_validator("fr", "en")
    @classmethod
    def unique_language_page_ids(cls, value: list[str]) -> list[str]:
        if any(not page_id.strip() for page_id in value):
            raise ValueError("transition page identifiers must not be blank")
        if len(value) != len(set(value)):
            raise ValueError("transition page identifiers must be unique per language")
        return value


class GuidedRouteTransition(StrictModel):
    id: str = Field(pattern=_ID.pattern)
    from_stage: str = Field(alias="from", pattern=_ID.pattern)
    to_stage: str = Field(alias="to", pattern=_ID.pattern)
    direction: Literal["directed", "symmetric"]
    pages: LocalizedTransitionPages
    purpose: LocalizedPurpose

    @model_validator(mode="after")
    def distinct_endpoints(self) -> GuidedRouteTransition:
        if self.from_stage == self.to_stage:
            raise ValueError("transition endpoints must be distinct")
        return self


class GuidedRouteTransitionDocument(StrictModel):
    transitions: list[GuidedRouteTransition] = Field(default_factory=list)

    @model_validator(mode="after")
    def unique_transition_ids(self) -> GuidedRouteTransitionDocument:
        identifiers = [item.id for item in self.transitions]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("guided-route transition identifiers must be unique")
        return self


def validate_guided_route_transitions(
    route_payload: dict,
    published_page_ids: set[str] | list[str],
) -> list[GuidedRouteTransition]:
    """Validate stage endpoints, bilingual page references and associations."""
    stages = route_payload.get("stages")
    if not isinstance(stages, list):
        raise ValueError("guided-route stages must be a list")
    stage_by_id = {stage.get("id"): stage for stage in stages if isinstance(stage, dict)}
    if len(stage_by_id) != len(stages):
        raise ValueError("guided-route stage identifiers must be present and unique")

    document = GuidedRouteTransitionDocument.model_validate(
        {"transitions": route_payload.get("transitions", [])}
    )
    published = set(published_page_ids)

    def stage_members(stage: dict, language: str) -> set[str]:
        return set(stage.get("pages", {}).get(language, [])) | set(
            stage.get("optional_pages", {}).get(language, [])
        )

    for transition in document.transitions:
        for endpoint in (transition.from_stage, transition.to_stage):
            if endpoint not in stage_by_id:
                raise ValueError(
                    f"transition {transition.id!r} references unknown stage {endpoint!r}"
                )
        for language in ("fr", "en"):
            expected_prefix = f"{language}/"
            page_ids = getattr(transition.pages, language)
            for page_id in page_ids:
                if not page_id.startswith(expected_prefix):
                    raise ValueError(
                        f"transition {transition.id!r} {language} pages must use "
                        f"the {expected_prefix!r} language prefix: {page_id!r}"
                    )
                if page_id not in published:
                    raise ValueError(
                        f"transition {transition.id!r} references unpublished or "
                        f"missing {language} page {page_id!r}"
                    )
            endpoint_members = stage_members(
                stage_by_id[transition.from_stage], language
            ) | stage_members(stage_by_id[transition.to_stage], language)
            unrelated = set(page_ids) - endpoint_members
            if unrelated:
                raise ValueError(
                    f"transition {transition.id!r} {language} pages must belong to "
                    f"at least one endpoint stage: {sorted(unrelated)}"
                )
    return document.transitions
