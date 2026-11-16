from experiments.compression_strategy_spectrum.run import (
    ALPHABET,
    bigram_cross_entropy,
    evaluate,
    make_sequence,
    permute_preserving_marginals,
    split_sequence,
    unigram_cross_entropy,
)


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
