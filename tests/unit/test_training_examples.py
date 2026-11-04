"""Tests for the reference training-example construction."""

import numpy as np
import pytest

from llm_lab.foundations.training_examples import sliding_input_target_pairs


def test_matches_the_lesson_worked_example() -> None:
    stream = [8, 3, 3, 9, 2, 7]

    inputs, targets = sliding_input_target_pairs(stream, context_length=3)

    np.testing.assert_array_equal(inputs, np.array([[8, 3, 3], [3, 3, 9], [3, 9, 2]]))
    np.testing.assert_array_equal(targets, np.array([[3, 3, 9], [3, 9, 2], [9, 2, 7]]))


def test_every_target_is_the_next_token_in_the_stream() -> None:
    stream = np.arange(10, dtype=np.int64)

    inputs, targets = sliding_input_target_pairs(stream, context_length=4, stride=3)

    np.testing.assert_array_equal(targets[:, :-1], inputs[:, 1:])
    np.testing.assert_array_equal(targets[:, -1], stream[inputs[:, -1] + 1])


def test_targets_are_shifted_not_copied() -> None:
    stream = [8, 3, 3, 9, 2, 7]

    inputs, targets = sliding_input_target_pairs(stream, context_length=3)

    assert not np.array_equal(targets, inputs)
    assert inputs[0, 0] == 8
    assert targets[0, 0] == 3


def test_stride_equal_to_context_length_has_no_input_overlap() -> None:
    stream = np.arange(10, dtype=np.int64)

    inputs, targets = sliding_input_target_pairs(stream, context_length=4, stride=4)

    assert inputs.shape == (2, 4)
    np.testing.assert_array_equal(inputs[0], stream[:4])
    np.testing.assert_array_equal(inputs[1], stream[4:8])
    np.testing.assert_array_equal(targets[1], stream[5:9])


def test_smaller_stride_overlaps_consecutive_windows() -> None:
    stream = np.arange(11, dtype=np.int64)

    inputs, _ = sliding_input_target_pairs(stream, context_length=4, stride=2)

    assert inputs.shape == (4, 4)
    np.testing.assert_array_equal(inputs[1], stream[2:6])
    np.testing.assert_array_equal(inputs[0, 2:], inputs[1, :2])


def test_corpus_of_context_length_plus_one_yields_one_window() -> None:
    stream = [5, 6, 7, 8]

    inputs, targets = sliding_input_target_pairs(stream, context_length=3)

    assert inputs.shape == (1, 3)
    np.testing.assert_array_equal(inputs[0], [5, 6, 7])
    np.testing.assert_array_equal(targets[0], [6, 7, 8])
    assert targets[0, -1] == stream[-1]


def test_window_count_follows_the_documented_formula() -> None:
    cases = [(7, 3, 1), (10, 4, 4), (11, 4, 2), (5, 2, 3)]

    for length, context, step in cases:
        stream = np.arange(length, dtype=np.int64)

        inputs, targets = sliding_input_target_pairs(stream, context, step)

        expected = 1 + (length - context - 1) // step
        assert inputs.shape == (expected, context)
        assert targets.shape == (expected, context)


def test_output_is_deterministic_and_stream_is_not_mutated() -> None:
    stream = np.array([4, 4, 4, 5, 5], dtype=np.int64)
    original = stream.copy()

    first_inputs, first_targets = sliding_input_target_pairs(stream, 2)
    second_inputs, second_targets = sliding_input_target_pairs(stream, 2)

    np.testing.assert_array_equal(first_inputs, second_inputs)
    np.testing.assert_array_equal(first_targets, second_targets)
    np.testing.assert_array_equal(stream, original)


@pytest.mark.parametrize(
    ("token_ids", "context_length", "stride"),
    [
        ([], 1, 1),
        ([1, 2, 3], 3, 1),
        ([[1, 2], [3, 4]], 1, 1),
        ([1.5, 2.5, 3.5], 1, 1),
        (np.array([1, 2, 3], dtype=np.float64), 1, 1),
        ([1, 2, 3], 0, 1),
        ([1, 2, 3], 2, 0),
        ([1, 2, 3], -1, 1),
        ([1, 2, 3], 1, -2),
    ],
)
def test_invalid_inputs_raise_value_error(
    token_ids: object,
    context_length: int,
    stride: int,
) -> None:
    with pytest.raises(ValueError):
        sliding_input_target_pairs(token_ids, context_length, stride)
