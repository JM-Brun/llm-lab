"""Regression tests for the minimal/optional foundations import boundary."""

import subprocess
import sys


def test_package_and_greedy_generation_do_not_import_optional_filters() -> None:
    script = """
import sys
import numpy as np

import llm_lab.foundations as foundations
assert "llm_lab.foundations.decoding_filters" not in sys.modules

config = foundations.GPTConfig(
    vocab_size=16,
    context_length=8,
    embedding_dim=8,
    num_heads=2,
    num_layers=1,
    mlp_hidden_dim=16,
    seed=0,
)
model = foundations.GPT(config)
result = foundations.generate(model, np.array([1, 2], dtype=np.int64), 1)
assert result.shape == (3,)
assert "llm_lab.foundations.decoding_filters" not in sys.modules
"""
    subprocess.run([sys.executable, "-c", script], check=True)


def test_sampling_loads_optional_filters_only_when_requested() -> None:
    script = """
import sys
import numpy as np

from llm_lab.foundations import GPT, GPTConfig, generate
assert "llm_lab.foundations.decoding_filters" not in sys.modules

config = GPTConfig(
    vocab_size=16,
    context_length=8,
    embedding_dim=8,
    num_heads=2,
    num_layers=1,
    mlp_hidden_dim=16,
    seed=0,
)
model = GPT(config)
generate(
    model,
    np.array([1, 2], dtype=np.int64),
    2,
    greedy=False,
    top_k=3,
    rng=np.random.default_rng(7),
)
assert "llm_lab.foundations.decoding_filters" in sys.modules
"""
    subprocess.run([sys.executable, "-c", script], check=True)


def test_package_level_filter_exports_remain_compatible() -> None:
    script = """
from llm_lab.foundations import top_k_filter, top_p_filter

assert callable(top_k_filter)
assert callable(top_p_filter)
"""
    subprocess.run([sys.executable, "-c", script], check=True)
