#!/usr/bin/env python3
"""Controlled toy comparison of in-domain and shifted predictive code lengths."""

from __future__ import annotations

import sys

from run import sequence_cost_bits, train_bigram_model

TRAINING_AB = "AB" * 100
TRAINING_CD = "CD" * 100
TEST_AB = "AB" * 20
TEST_CD = "CD" * 20


def main() -> None:
    model_ab = train_bigram_model(TRAINING_AB)
    model_cd = train_bigram_model(TRAINING_CD)
    cases = (
        ("AB-trained model → AB test (in-domain)", sequence_cost_bits(TEST_AB, model_ab)),
        ("AB-trained model → CD test (shifted)", sequence_cost_bits(TEST_CD, model_ab)),
        ("CD-trained model → CD test (in-domain)", sequence_cost_bits(TEST_CD, model_cd)),
        ("CD-trained model → AB test (shifted)", sequence_cost_bits(TEST_AB, model_cd)),
    )
    report = [
        "Synthetic domain-shift experiment",
        "Training strings contain 200 symbols; each test contains 40 symbols.",
        "",
    ]
    report.extend(f"{label}: {cost:.3f} bits ({cost / 40:.3f} bits/symbol)" for label, cost in cases)
    sys.stdout.write("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
