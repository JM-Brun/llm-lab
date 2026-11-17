#!/usr/bin/env python3
"""Compare one-hot supervision with soft teacher targets on a tiny categorical task.

This is a deterministic optimization illustration, not a neural-network benchmark.
Only the standard library is required.
"""


from __future__ import annotations

import json
import math

TEACHER = (0.7, 0.2, 0.1)
HARD_TARGET = (1.0, 0.0, 0.0)
INITIAL_LOGITS = (0.0, 0.0, 0.0)
LEARNING_RATE = 0.1
STEPS = 400


def softmax(logits: tuple[float, ...] | list[float]) -> tuple[float, ...]:
    if not logits:
        raise ValueError("At least one logit is required")
    maximum = max(logits)
    exponentials = tuple(math.exp(value - maximum) for value in logits)
    total = sum(exponentials)
    return tuple(value / total for value in exponentials)


def cross_entropy(target: tuple[float, ...], predicted: tuple[float, ...]) -> float:
    if len(target) != len(predicted):
        raise ValueError("Target and prediction dimensions must match")
    if any(value < 0 for value in target) or not math.isclose(sum(target), 1.0):
        raise ValueError("Target must be a probability distribution")
    if any(value <= 0 for value in predicted) or not math.isclose(sum(predicted), 1.0):
        raise ValueError("Prediction must be a strictly positive probability distribution")
    return -sum(q * math.log(p) for q, p in zip(target, predicted) if q > 0)


def kl_divergence(target: tuple[float, ...], predicted: tuple[float, ...]) -> float:
    return cross_entropy(target, predicted) + sum(q * math.log(q) for q in target if q > 0)


def fit_student(
    target: tuple[float, ...],
    *,
    steps: int = STEPS,
    learning_rate: float = LEARNING_RATE,
) -> tuple[float, ...]:
    """Minimize cross-entropy by gradient descent on student logits.

    For softmax logits z and target q, the gradient is p - q.
    """
    if steps < 1 or learning_rate <= 0:
        raise ValueError("steps and learning_rate must be positive")
    if any(value < 0 for value in target) or not math.isclose(sum(target), 1.0):
        raise ValueError("Target must be a probability distribution")
    logits = list(INITIAL_LOGITS)
    for _ in range(steps):
        predicted = softmax(logits)
        logits = [
            value - learning_rate * (probability - desired)
            for value, probability, desired in zip(logits, predicted, target)
        ]
    return softmax(logits)


def main() -> None:
    hard_student = fit_student(HARD_TARGET)
    soft_student = fit_student(TEACHER)
    teacher_entropy = -sum(q * math.log(q) for q in TEACHER)
    report = {
        "experiment": "one-hot-vs-soft-target-distillation",
        "setup": {
            "teacher_distribution": TEACHER,
            "one_hot_target": HARD_TARGET,
            "initial_student_distribution": softmax(INITIAL_LOGITS),
            "optimizer": "gradient descent on student logits",
            "learning_rate": LEARNING_RATE,
            "steps": STEPS,
            "units": "nats",
        },
        "one_hot_student": {
            "predicted_distribution": hard_student,
            "teacher_cross_entropy": cross_entropy(TEACHER, hard_student),
            "teacher_kl": kl_divergence(TEACHER, hard_student),
        },
        "soft_target_student": {
            "predicted_distribution": soft_student,
            "teacher_cross_entropy": cross_entropy(TEACHER, soft_student),
            "teacher_kl": kl_divergence(TEACHER, soft_student),
        },
        "teacher_entropy": teacher_entropy,
        "identity_check": math.isclose(
            cross_entropy(TEACHER, soft_student),
            teacher_entropy + kl_divergence(TEACHER, soft_student),
            rel_tol=1e-10,
            abs_tol=1e-10,
        ),
        "interpretation_limits": [
            "The teacher distribution is stipulated, not learned from data.",
            "The student is a three-logit categorical model, not a neural network.",
            "The one-hot and soft-target objectives differ by design; this isolates "
            "information retained in the target, not a universal performance gain.",
            "Teacher probabilities are supervision signals, not ground truth; "
            "distillation can transfer teacher errors and biases.",
            "No compression bitstream is constructed in this experiment.",
        ],
    }
    print(json.dumps(report, indent=2))
    if not report["identity_check"]:
        raise AssertionError("Cross-entropy/KL identity failed")
    if report["soft_target_student"]["teacher_kl"] >= report["one_hot_student"]["teacher_kl"]:
        raise AssertionError("Soft-target student did not better match the teacher")


if __name__ == "__main__":
    main()
