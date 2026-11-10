"""Compare decoding distributions for one fixed synthetic logit vector."""

import json
import platform
from collections.abc import Sequence
from dataclasses import asdict, dataclass

import numpy as np
from numpy.typing import NDArray

from llm_lab.foundations.attention import softmax_with_temperature
from llm_lab.foundations.decoding_filters import top_k_filter

FloatArray = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class DecodingMeasurement:
    """Results for one temperature and optional top-k setting."""

    temperature: float
    top_k: int | None
    probabilities: list[float]
    entropy_nats: float
    retained_mass_before_renormalization: float


@dataclass(frozen=True, slots=True)
class DecodingScenario:
    """A single, explicit decoding configuration."""

    temperature: float
    top_k: int | None = None

    def evaluate(self, logits: FloatArray) -> DecodingMeasurement:
        """Compute a distribution and its descriptive measurements."""
        base = softmax_with_temperature(logits, self.temperature)
        if self.top_k is None:
            probabilities = base
            retained_mass = 1.0
        else:
            probabilities = top_k_filter(base, self.top_k)
            retained_mass = float(base[probabilities > 0].sum())
        positive = probabilities[probabilities > 0]
        return DecodingMeasurement(
            temperature=self.temperature,
            top_k=self.top_k,
            probabilities=probabilities.tolist(),
            entropy_nats=float(-(positive * np.log(positive)).sum()),
            retained_mass_before_renormalization=retained_mass,
        )


@dataclass(frozen=True, slots=True)
class ExperimentReport:
    """Measurements and the environment needed to interpret a run."""

    synthetic_logits: list[float]
    python: str
    numpy: str
    platform: str
    randomness: str
    results: list[DecodingMeasurement]

    def to_json(self) -> str:
        """Serialize with the same JSON format as the published report."""
        return json.dumps(asdict(self), indent=2)


def run_experiment(logits: FloatArray, scenarios: Sequence[DecodingScenario]) -> ExperimentReport:
    """Evaluate scenarios in order and capture the execution environment."""
    return ExperimentReport(
        synthetic_logits=logits.tolist(),
        python=platform.python_version(),
        numpy=np.__version__,
        platform=platform.platform(),
        randomness="none",
        results=[scenario.evaluate(logits) for scenario in scenarios],
    )


def main() -> None:
    logits = np.array([2.0, 1.0, 0.0, -1.0])
    scenarios = (
        DecodingScenario(temperature=0.5),
        DecodingScenario(temperature=1.0),
        DecodingScenario(temperature=2.0),
        DecodingScenario(temperature=1.0, top_k=2),
    )
    print(run_experiment(logits, scenarios).to_json())  # noqa: T201 - CLI output


if __name__ == "__main__":
    main()
