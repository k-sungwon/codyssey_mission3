import unittest

from mini_npu.models import Filter, Pattern
from mini_npu.performance import PerformanceAnalyzer


class CountingCalculator:
    name = "counting"

    def __init__(self):
        self.calls = 0

    def calculate(self, pattern, filter_):
        self.calls += 1
        return 12.5


class PerformanceTests(unittest.TestCase):
    def test_measure_repeats_calculation_and_reports_metadata(self):
        calculator = CountingCalculator()
        pattern = Pattern("case", [[1, 0], [0, 1]], 2)
        filter_ = Filter("A", [[1, 0], [0, 1]], 2)

        measurement = PerformanceAnalyzer(repeats=10).measure(
            calculator, pattern, filter_
        )

        self.assertEqual(calculator.calls, 10)
        self.assertEqual(measurement.calculator_name, "counting")
        self.assertEqual(measurement.score, 12.5)
        self.assertEqual(measurement.operation_count, 4)
        self.assertGreaterEqual(measurement.average_ms, 0.0)


if __name__ == "__main__":
    unittest.main()
