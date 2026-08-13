import unittest

from mini_npu.performance import PerformanceMeasurement
from mini_npu.reporter import ConsoleReporter


class ReporterTests(unittest.TestCase):
    def test_report_measurements_includes_calculated_score(self):
        output = []
        reporter = ConsoleReporter(output.append)
        measurement = PerformanceMeasurement(
            calculator_name="Flat",
            score=12.0,
            average_ms=0.25,
            operation_count=16,
        )

        reporter.report_measurements([("Cross", measurement)])

        self.assertEqual(
            output,
            ["PERFORMANCE | Flat | filter=Cross | score=12.000000 | 4x4 | 0.250000 ms | 16 MACs"],
        )


if __name__ == "__main__":
    unittest.main()
