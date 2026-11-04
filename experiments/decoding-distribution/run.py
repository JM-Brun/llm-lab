"""Compare decoding distributions for one fixed synthetic logit vector."""

import json
import platform

import numpy as np

from llm_lab.foundations.attention import softmax_with_temperature
from llm_lab.foundations.decoding_filters import top_k_filter


def main() -> None:
    logits = np.array([2.0, 1.0, 0.0, -1.0])
    rows = []
    for temperature, k in ((0.5, None), (1.0, None), (2.0, None), (1.0, 2)):
        base = softmax_with_temperature(logits, temperature)
        if k is None:
            probabilities = base
            retained_mass = 1.0
        else:
            probabilities = top_k_filter(base, k)
            retained_mass = float(base[probabilities > 0].sum())
        positive = probabilities[probabilities > 0]
        rows.append(
            {
                "temperature": temperature,
                "top_k": k,
                "probabilities": probabilities.tolist(),
                "entropy_nats": float(-(positive * np.log(positive)).sum()),
                "retained_mass_before_renormalization": retained_mass,
            }
        )
    print(  # noqa: T201 - the experiment's JSON result is its command-line output
        json.dumps(
            {
                "synthetic_logits": logits.tolist(),
                "python": platform.python_version(),
                "numpy": np.__version__,
                "platform": platform.platform(),
                "randomness": "none",
                "results": rows,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
