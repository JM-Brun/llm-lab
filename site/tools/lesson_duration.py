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
FENCED_DIV_OPEN = re.compile(r"^\s*(?P<fence>:{3,})\s+(?P<attrs>\{.*\})\s*$")
FENCED_DIV_CLOSE = re.compile(r"^\s*(?P<fence>:{3,})\s*$")
EXCLUDE_FROM_READING_TIME = re.compile(
    r"""(?:^|\s)data-reading-time\s*=\s*(?:"exclude"|'exclude'|exclude)(?=\s|$)""",
    re.IGNORECASE,
)
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
WORD = re.compile(r"[\w]+(?:[\u2019'][\w]+)*", re.UNICODE)

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


def _remove_excluded_fenced_divs(markdown: str) -> str:
    """Strip Quarto fenced-div markup and omit content explicitly excluded from reading time.

    Optional callouts can remain available to interested readers without
    being part of the required reading path. The data attribute is the
    semantic contract; collapsed presentation alone does not imply
    optionality. Opening and closing div markers are markup, not prose.
    """
    output: list[str] = []
    # Each entry stores the opening fence length and whether its contents
    # should be omitted (inherited from an excluded parent or local to it).
    stack: list[tuple[int, bool]] = []

    for line in markdown.splitlines(keepends=True):
        line_without_newline = line.rstrip("\r\n")
        opening = FENCED_DIV_OPEN.match(line_without_newline)
        closing = FENCED_DIV_CLOSE.match(line_without_newline)

        if opening:
            fence_length = len(opening.group("fence"))
            attributes = opening.group("attrs")
            parent_is_excluded = stack[-1][1] if stack else False
            is_excluded = parent_is_excluded or bool(
                EXCLUDE_FROM_READING_TIME.search(attributes[1:-1])
            )
            stack.append((fence_length, is_excluded))
            continue

        if closing and stack and len(closing.group("fence")) >= stack[-1][0]:
            _, is_excluded = stack.pop()
            parent_is_excluded = stack[-1][1] if stack else False
            continue

        if stack and stack[-1][1]:
            continue
        output.append(line)

    return "".join(output)


def _main_lesson(markdown: str) -> str:
    """Remove metadata and content explicitly outside the main learning lesson."""
    text = FRONT_MATTER.sub("", markdown, count=1)
    text = HTML_COMMENT.sub("", text)
    text = INCLUDE_LINE.sub("", text)
    text = END_OF_CORE.split(text, maxsplit=1)[0]
    text = _remove_excluded_fenced_divs(text)
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
