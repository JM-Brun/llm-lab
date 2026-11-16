from __future__ import annotations

import runpy
from pathlib import Path


def test_entropy_and_realized_surprisal_are_distinct() -> None:
    script = Path("experiments/entropy-surprisal-toy/run.py")
    namespace = runpy.run_path(str(script))

    entropy_bits = namespace["entropy_bits"]
    surprisal_bits = namespace["surprisal_bits"]

    distribution = (0.99, 0.01)
    assert entropy_bits(distribution) < 0.1
    assert surprisal_bits(distribution[1]) > 6.6
    assert surprisal_bits(distribution[0]) < 0.02
