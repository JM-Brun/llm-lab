"""Regression tests for parsing generated timeline HTML after Quarto rendering."""

from pathlib import Path
from runpy import run_path


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_history_rendered.py"
TimelineParser = run_path(str(SCRIPT), run_name="check_history_rendered")["TimelineParser"]


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
