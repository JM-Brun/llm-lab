"""Estimate reading time for the published core lessons.

This is an editorial heuristic, not a promise about an individual reader's pace.
Only the main lesson body is measured: front matter, generated navigation,
exercise sections, and optional/deepening sections are excluded.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass

FRONT_MATTER = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
INCLUDE_LINE = re.compile(r"^\s*\{\{<\s*include\b.*?>\}\}\s*$", re.MULTILINE)
END_OF_CORE = re.compile(
    r"^##\s+(?:exercices|exercises|approfondir|deep(?:en|er)|"
    r"références|references|pour aller plus loin|further reading)\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
FENCED_BLOCK = re.compile(
    r"^\s*(`{3,}|~{3,})([^\n]*)\n([\s\S]*?)^\s*\1\s*$",
    re.MULTILINE,
)
DISPLAY_MATH = re.compile(
    r"\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|"
    r"\\begin\{(?!array\b)[^}]+\}[\s\S]*?\\end\{[^}]+\}",
)
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$")
IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
WORD = re.compile(r"[\\w]+(?:[\\u2019'][\\w]+)*", re.UNICODE)

# Deliberately conservative rates for technical educational material.
WORDS_PER_MINUTE = 140
CODE_LINES_PER_MINUTE = 20
DISPLAY_EQUATION_MINUTES = 0.20
INLINE_EQUATION_MINUTES = 0.035
FIGURE_MINUTES = 0.25
DIAGRAM_MINUTES = 0.50

# Add an exception only when the lesson genuinely needs more than 25 minutes.
# The value must explain why the length is pedagogically justified.
DURATION_EXCEPTIONS: dict[str, str] = {}


@dataclass(frozen=True)
class LessonDuration:
    """Inspectable components of one deterministic reading-time estimate."""

    minutes: float
    prose_words: int
    code_lines: int
    display_equations: int
    inline_equations: int
    figures: int
    diagrams: int


def _main_lesson(markdown: str) -> str:
    """Remove metadata and content explicitly outside the main learning lesson."""
    text = FRONT_MATTER.sub("", markdown, count=1)
    text = HTML_COMMENT.sub("", text)
    text = INCLUDE_LINE.sub("", text)
    text = END_OF_CORE.split(text, maxsplit=1)[0]
    return text


def estimate_lesson_duration(markdown: str) -> LessonDuration:
    """Estimate active reading/inspection time without rendering the Quarto page."""
    text = _main_lesson(markdown)
    code_lines = 0
    diagrams = 0

    def remove_fence(match: re.Match[str]) -> str:
        nonlocal code_lines, diagrams
        info = match.group(2).strip().lower()
        body = match.group(3)
        if "mermaid" in info:
            diagrams += 1
        else:
            code_lines += sum(bool(line.strip()) for line in body.splitlines())
        return " "

    text = FENCED_BLOCK.sub(remove_fence, text)

    display_equations = len(DISPLAY_MATH.findall(text))
    text = DISPLAY_MATH.sub(" ", text)
    inline_equations = len(INLINE_MATH.findall(text))
    text = INLINE_MATH.sub(" ", text)

    figures = len(IMAGE.findall(text))
    text = IMAGE.sub(" ", text)
    text = LINK.sub(r"\1", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = HTML_TAG.sub(" ", text)
    text = html.unescape(text)

    prose_words = len(WORD.findall(text))
    minutes = (
        prose_words / WORDS_PER_MINUTE
        + code_lines / CODE_LINES_PER_MINUTE
        + display_equations * DISPLAY_EQUATION_MINUTES
        + inline_equations * INLINE_EQUATION_MINUTES
        + figures * FIGURE_MINUTES
        + diagrams * DIAGRAM_MINUTES
    )
    # Half-minute granularity avoids false precision in a heuristic estimate.
    rounded_minutes = max(0.5, round(minutes * 2) / 2)
    return LessonDuration(
        minutes=rounded_minutes,
        prose_words=prose_words,
        code_lines=code_lines,
        display_equations=display_equations,
        inline_equations=inline_equations,
        figures=figures,
        diagrams=diagrams,
    )
