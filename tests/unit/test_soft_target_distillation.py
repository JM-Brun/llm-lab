from __future__ import annotations

import runpy
from pathlib import Path


def experiment():
    root = Path(__file__).resolve().parents[2]
    return runpy.run_path(str(root / "experiments/soft-target-distillation/run.py"))


def test_soft_target_student_recovers_teacher_distribution() -> None:
    module = experiment()
    teacher = module["TEACHER"]
    student = module["fit_student"](teacher)

    assert max(abs(a - b) for a, b in zip(student, teacher)) < 0.002


def test_soft_targets_retain_more_teacher_information_than_one_hot_label() -> None:
    module = experiment()
    teacher = module["TEACHER"]
    hard_student = module["fit_student"](module["HARD_TARGET"])
    soft_student = module["fit_student"](teacher)

    assert module["kl_divergence"](teacher, soft_student) < module["kl_divergence"](
        teacher, hard_student
    )


def test_cross_entropy_kl_decomposition() -> None:
    module = experiment()
    teacher = module["TEACHER"]
    predicted = module["fit_student"](teacher)
    entropy = -sum(q * __import__("math").log(q) for q in teacher)

    assert abs(
        module["cross_entropy"](teacher, predicted)
        - entropy
        - module["kl_divergence"](teacher, predicted)
    ) < 1e-10


def test_softmax_is_normalized_and_stable() -> None:
    module = experiment()
    predicted = module["softmax"]((1000.0, 1001.0, 999.0))

    assert all(0.0 < value < 1.0 for value in predicted)
    assert abs(sum(predicted) - 1.0) < 1e-12
