from dataclasses import dataclass
from time import perf_counter

from mini_npu.models import Filter, Pattern


@dataclass
class PerformanceMeasurement:
    calculator_name: str
    score: float
    average_ms: float
    operation_count: int


class PerformanceAnalyzer:
    def __init__(self, repeats: int = 10):
        if repeats < 10:
            raise ValueError("repeats must be at least 10")
        self.repeats = repeats

    def measure(self, calculator, pattern: Pattern, filter_: Filter) -> PerformanceMeasurement:
        elapsed_seconds = 0.0
        score = 0.0
        for _ in range(self.repeats):
            started_at = perf_counter()
            score = calculator.calculate(pattern, filter_)
            elapsed_seconds += perf_counter() - started_at

        return PerformanceMeasurement(
            calculator.name,
            score,
            elapsed_seconds / self.repeats * 1000,
            pattern.size * pattern.size,
        )
