"""Regression tests for parsing generated timeline HTML after Quarto rendering."""

SCRIPT = __file__.replace(
    "/tests/unit/test_history_rendered.py",
    "/scripts/check_history_rendered.py",
)
GENERATOR = __file__.replace(
    "/tests/unit/test_history_rendered.py",
    "/scripts/render_history_pilot.py",
)
render_timeline = __import__("runpy").run_path(
    GENERATOR, run_name="render_history_pilot"
)["render"]
TimelineParser = __import__("runpy").run_path(
    SCRIPT, run_name="check_history_rendered"
)["TimelineParser"]


def test_nested_quarto_sections_do_not_end_timeline_scope() -> None:
    parser = TimelineParser()
    parser.feed(
        """
        <section class="history-timeline" aria-label="Historical timeline">
          <section id="era" class="level3">
            <h3>Era heading</h3>
          </section>
          <ol>
            <li class="history-timeline__item" data-event-id="example" data-event-type="research">
              <time datetime="2020-01-01">1 January 2020</time>
              <a href="https://example.org/paper">Primary source</a>
            </li>
          </ol>
        </section>
        """
    )
    parser.close()

    assert parser.events == [("example", "research")]
    assert parser.times == ["2020-01-01"]
    assert parser.links == ["https://example.org/paper"]
    assert "Era heading" in parser.timeline_text


def test_generated_fragment_is_a_raw_html_block() -> None:
    dataset = {
        "sources": [
            {
                "id": "paper",
                "url": "https://example.org/paper",
                "title": "Primary source",
            }
        ],
        "events": [
            {
                "id": "example",
                "type": "research",
                "date": {
                    "value": "2020-01-01",
                    "precision": "day",
                    "kind": "submission",
                },
                "era": "neural-sequence-modelling-and-attention",
                "title": {"fr": "Exemple", "en": "Example"},
                "summary": {"fr": "Résumé", "en": "Summary"},
                "source_ids": ["paper"],
            }
        ],
    }
    rendered = render_timeline(dataset, "en")
    assert rendered.startswith("```{=html}\n")
    assert rendered.rstrip().endswith("```")
    assert '<time datetime="2020-01-01">1 January 2020</time>' in rendered
    assert (
        '<a href="https://example.org/paper" rel="external">Primary source</a>' in rendered
    )
