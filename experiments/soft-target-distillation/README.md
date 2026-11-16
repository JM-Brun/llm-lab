# Soft targets vs one-hot supervision: a controlled distillation experiment

## Question

What information is retained when a student is trained on a teacher's full probability distribution instead of only the teacher's most likely class?

## Run

From the repository root:

```bash
python experiments/soft-target-distillation/run.py
uv run pytest tests/unit/test_soft_target_distillation.py
```

Only the Python standard library is required.

## Setup

A teacher distribution is stipulated as (q_T=(0.7,0.2,0.1)). The student is a categorical model with three trainable logits, initialized uniformly. We train it twice using the same gradient-descent procedure:

1. **Hard target:** the teacher's most likely class is converted to the one-hot vector ((1,0,0)).
2. **Soft target:** the student receives the full distribution ((0.7,0.2,0.1)).

For softmax logits (z), prediction (p=operatorname{softmax}(z)), and target (q), the cross-entropy gradient with respect to logits is (p-q).

## Reproducible result

With learning rate 0.1 and 400 steps, the soft-target student approaches the teacher distribution:

- Soft-target student: approximately ((0.6999,0.1998,0.1003)).
- One-hot student: approximately ((0.9825,0.0088,0.0088)).

The teacher-to-student KL divergence is approximately (7.4\times10^{-7}) nats for soft targets and (0.632) nats for the one-hot target. The soft target preserves the teacher's relative preference for the second and third classes; the one-hot target discards that information.

## What this does and does not show

- It illustrates why a full teacher distribution carries more information than its argmax label.
- It numerically checks (H(q_T,p_S)=H(q_T)+D_{KL}(q_T\|p_S)).
- It does **not** show that distillation always improves downstream accuracy, generalization, or compression.
- The teacher is stipulated rather than trained; no dataset, neural network, or bitstream is used.
- A teacher distribution is not ground truth. Distillation may transfer teacher errors, calibration problems, and biases.
- This is a controlled optimization illustration, not a reproduction of a particular distillation paper.

## Connection to the compression series

Part 2 explains cross-entropy and soft-target distillation. This experiment isolates the information carried by the target distribution. The separate [predictive-compression experiment](../predictive-compression/README.md) demonstrates conditional probabilities and exact arithmetic-coding round trips. These are related through predictive distributions, but this script does not itself encode a message.

See the bilingual [cross-entropy lesson](../../site/en/cross-entropy.qmd) and [advanced language-modeling mathematics](../../site/en/language-modeling-math.qmd).
