"""Tests for the sequential-compression teaching experiment."""

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[2] / "experiments" / "compression-strategy-spectrum" / "run.py"
SPEC = importlib.util.spec_from_file_location("compression_strategy_spectrum_run", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

ALPHABET = MODULE.ALPHABET
bigram_cross_entropy = MODULE.bigram_cross_entropy
evaluate = MODULE.evaluate
make_sequence = MODULE.make_sequence
permute_preserving_marginals = MODULE.permute_preserving_marginals
split_sequence = MODULE.split_sequence
unigram_cross_entropy = MODULE.unigram_cross_entropy


def test_permutation_preserves_marginal_frequencies():
    sequence = make_sequence(300)
    permuted = permute_preserving_marginals(sequence, seed=11)
    assert sorted(sequence) == sorted(permuted)


def test_split_is_disjoint_and_complete():
    sequence = make_sequence(100)
    train, test = split_sequence(sequence)
    assert train + test == sequence
    assert len(train) + len(test) == len(sequence)


def test_losses_are_finite_and_positive():
    train, test = split_sequence(make_sequence(300))
    assert 0 < unigram_cross_entropy(train, test) < 10
    assert 0 < bigram_cross_entropy(train, test) < 10


def test_bigram_exploits_ordered_pattern():
    sequence = make_sequence(1200)
    unigram, bigram = evaluate(sequence)
    assert bigram < unigram


def test_alphabet_is_finite_and_used():
    sequence = make_sequence(300)
    assert set(sequence).issubset(set(ALPHABET))
