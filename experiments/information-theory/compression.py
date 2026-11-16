"""Compare known source entropy rates with deterministic zlib coding costs."""

import json

from numpy.typing import NDArray

import numpy as np


FloatArray = NDArray[np.float64]
UIntArray = NDArray[np.uint8]

SEED = 20261116
SEQUENCE_LENGTH = 100_000
ALPHABET_SIZE = 4


def entropy_bits(probabilities: FloatArray) -> float:
    positive = probabilities > 0.0
    return float(-np.sum(probabilities[positive] * np.log2(probabilities[positive])))


def generate_markov(length: int, transition: FloatArray, rng: np.random.Generator) -> UIntArray:
    sequence = np.empty(length, dtype=np.uint8)
    sequence[0] = rng.integers(0, transition.shape[0])
    for index in range(1, length):
        previous = int(sequence[index - 1])
        sequence[index] = rng.choice(transition.shape[0], p=transition[previous])
    return sequence


def describe_sequence(sequence: UIntArray, entropy_rate: float) -> dict[str, float | int]:
    import zlib

    counts = np.bincount(sequence, minlength=ALPHABET_SIZE)
    marginal = counts / counts.sum()
    compressed = zlib.compress(sequence.tobytes(), level=9)
    return {
        "symbols": int(sequence.size),
        "marginal_entropy_bits_per_symbol": entropy_bits(marginal),
        "source_entropy_rate_bits_per_symbol": entropy_rate,
        "zlib_bytes_including_container_overhead": len(compressed),
        "zlib_bits_per_symbol_including_overhead": len(compressed) * 8 / sequence.size,
    }


def main() -> None:
    rng_iid = np.random.default_rng(SEED)
    rng_markov = np.random.default_rng(SEED + 1)
    iid = rng_iid.integers(0, ALPHABET_SIZE, size=SEQUENCE_LENGTH, dtype=np.uint8)

    stay_probability = 0.9
    transition = np.full(
        (ALPHABET_SIZE, ALPHABET_SIZE),
        (1.0 - stay_probability) / (ALPHABET_SIZE - 1),
    )
    np.fill_diagonal(transition, stay_probability)
    markov = generate_markov(SEQUENCE_LENGTH, transition, rng_markov)
    constant = np.zeros(SEQUENCE_LENGTH, dtype=np.uint8)

    markov_entropy_rate = entropy_bits(transition[0])
    output = {
        "experiment": "deterministic-source-entropy-and-zlib",
        "seed": SEED,
        "sequence_length_symbols": SEQUENCE_LENGTH,
        "alphabet_size": ALPHABET_SIZE,
        "compression": "zlib level 9 on raw uint8 symbols; container overhead included",
        "sources": {
            "constant": describe_sequence(constant, 0.0),
            "iid_uniform": describe_sequence(iid, 2.0),
            "symmetric_markov_p_stay_0_9": describe_sequence(markov, markov_entropy_rate),
        },
        "interpretation": [
            "For the symmetric Markov source, the stationary marginal is uniform "
            "(2 bits per symbol), but dependencies reduce the entropy rate.",
            "The entropy rate is the asymptotic optimal lossless coding benchmark for "
            "the specified source, not a prediction of exact finite-file zlib size.",
            "zlib is one practical compressor, not an optimal code; finite samples and "
            "container overhead affect its measured size.",
            "The fixed seed makes this generated sample reproducible.",
        ],
    }
    print(json.dumps(output, indent=2))  # noqa: T201 - experiment CLI output


if __name__ == "__main__":
    main()
