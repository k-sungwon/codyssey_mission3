from typing import Callable, Iterable, Tuple

from mini_npu.models import MatchResult


class ConsoleReporter:
    def __init__(self, output_func: Callable[[str], None] = print):
        self.output_func = output_func

    def report_result(self, result: MatchResult) -> None:
        case_id = result.case_id or "manual"
        if result.reason:
            self.output_func("CASE {0} | FAIL | {1}".format(case_id, result.reason))
            return

        score_text = ", ".join(
            "{0}={1:.6f}".format(label, score)
            for label, score in sorted(result.scores.items())
        )
        line = "CASE {0} | {1} | predicted={2}".format(case_id, score_text, result.predicted_label)
        if result.expected_label is not None:
            status = "PASS" if result.passed else "FAIL"
            line += " | expected={0} | {1}".format(result.expected_label, status)
        self.output_func(line)

    def report_measurements(self, measurements: Iterable[Tuple[str, object]]) -> None:
        for filter_label, measurement in measurements:
            self.output_func(
                "PERFORMANCE | {0} | filter={1} | score={2:.6f} | {3}x{3} | {4:.6f} ms | {5} MACs".format(
                    measurement.calculator_name,
                    filter_label,
                    measurement.score,
                    int(measurement.operation_count ** 0.5),
                    measurement.average_ms,
                    measurement.operation_count,
                )
            )

    def report_summary(self, summary: dict) -> None:
        self.output_func(
            "SUMMARY | total={0} | pass={1} | fail={2}".format(
                summary["total"], summary["passed"], summary["failed"]
            )
        )
        for result in summary.get("failed_cases", []):
            if result.reason:
                self.output_func(
                    "FAILED_CASE | case={0} | reason={1}".format(
                        result.case_id, result.reason
                    )
                )
            else:
                self.output_func(
                    "FAILED_CASE | case={0} | predicted={1} | expected={2}".format(
                        result.case_id, result.predicted_label, result.expected_label
                    )
                )

    def report_error(self, message: str) -> None:
        self.output_func("ERROR | {0}".format(message))
