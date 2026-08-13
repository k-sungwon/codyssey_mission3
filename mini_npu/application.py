from pathlib import Path
from typing import Callable, Dict, List, Tuple

from mini_npu.calculators import BasicMacCalculator, OptimizedMacCalculator
from mini_npu.helpers import (
    classify,
    generate_cross_pattern,
    generate_x_pattern,
    normalize_label,
)
from mini_npu.input import read_matrix_from_console
from mini_npu.loader import DataLoader
from mini_npu.models import Filter, MatchResult, Pattern
from mini_npu.performance import PerformanceAnalyzer
from mini_npu.reporter import ConsoleReporter


class Application:
    def __init__(
        self,
        data_path=Path("data.json"),
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ):
        self.data_path = Path(data_path)
        self.input_func = input_func
        self.reporter = ConsoleReporter(output_func)
        self.basic_calculator = BasicMacCalculator()
        self.optimized_calculator = OptimizedMacCalculator()
        self.performance_analyzer = PerformanceAnalyzer()

    def run(self) -> None:
        while True:
            choice = self.input_func(
                "Mode (1: manual, 2: JSON, 3: generated, 0: exit): "
            ).strip()
            if choice == "1":
                self.run_manual_mode()
            elif choice == "2":
                self.run_json_mode()
            elif choice == "3":
                self.run_generated_mode()
            elif choice == "0":
                return
            else:
                self.reporter.report_error("select 1, 2, 3, or 0")

    def run_manual_mode(self) -> MatchResult:
        size = 3
        filter_a = Filter("A", read_matrix_from_console("Filter A", size, self.input_func, self.reporter.output_func), size)
        filter_b = Filter("B", read_matrix_from_console("Filter B", size, self.input_func, self.reporter.output_func), size)
        pattern = Pattern("manual", read_matrix_from_console("Pattern", size, self.input_func, self.reporter.output_func), size)
        result = self.analyze_case(pattern, {"A": filter_a, "B": filter_b})
        self.reporter.report_result(result)
        self.reporter.report_measurements(self.measure_case(pattern, {"A": filter_a, "B": filter_b}))
        return result

    def run_generated_mode(self) -> MatchResult:
        size = self._read_positive_size()
        label = self._read_generated_label()
        pattern, filters = self.build_generated_case(size, label)
        result = self.analyze_case(pattern, filters)
        self.reporter.report_result(result)
        self.reporter.report_measurements(self.measure_case(pattern, filters))
        return result

    def run_json_mode(self) -> dict:
        try:
            loaded = DataLoader(self.data_path).load()
        except ValueError as error:
            self.reporter.report_error(str(error))
            return {"total": 0, "passed": 0, "failed": 0}

        results = []
        for pattern in loaded.patterns:
            result = self.analyze_case(pattern, loaded.filters_by_size[pattern.size])
            results.append(result)
            self.reporter.report_result(result)
            self.reporter.report_measurements(
                self.measure_case(pattern, loaded.filters_by_size[pattern.size])
            )
        for failure in loaded.failures:
            self.reporter.report_result(failure)

        summary = self._summarize(results + loaded.failures)
        self.reporter.report_summary(summary)
        return summary

    def analyze_case(self, pattern: Pattern, filters: Dict[str, Filter]) -> MatchResult:
        scores = {
            label: self.basic_calculator.calculate(pattern, filter_)
            for label, filter_ in filters.items()
        }
        predicted_label = classify(scores)
        passed = None
        if pattern.expected_label is not None:
            passed = predicted_label == pattern.expected_label
        return MatchResult(
            pattern.case_id,
            scores,
            predicted_label,
            pattern.expected_label,
            passed,
        )

    @staticmethod
    def build_generated_case(
        size: int, selected_label: str
    ) -> Tuple[Pattern, Dict[str, Filter]]:
        if size <= 0:
            raise ValueError("size must be positive")
        label = normalize_label(selected_label)
        cross_matrix = generate_cross_pattern(size)
        x_matrix = generate_x_pattern(size)
        filters = {
            "Cross": Filter("Cross", cross_matrix, size),
            "X": Filter("X", x_matrix, size),
        }
        return Pattern("generated_{0}_{1}".format(size, label), filters[label].matrix, size, label), filters

    def measure_case(
        self, pattern: Pattern, filters: Dict[str, Filter]
    ) -> List[Tuple[str, object]]:
        measurements = []
        for calculator in (self.basic_calculator, self.optimized_calculator):
            for label, filter_ in sorted(filters.items()):
                measurements.append(
                    (label, self.performance_analyzer.measure(calculator, pattern, filter_))
                )
        return measurements

    @staticmethod
    def _summarize(results: List[MatchResult]) -> dict:
        passed = sum(result.passed is True for result in results)
        return {"total": len(results), "passed": passed, "failed": len(results) - passed}

    def _read_positive_size(self) -> int:
        while True:
            try:
                size = int(self.input_func("Generated matrix size N: ").strip())
                if size <= 0:
                    raise ValueError
                return size
            except ValueError:
                self.reporter.report_error("N must be a positive integer")

    def _read_generated_label(self) -> str:
        while True:
            try:
                return normalize_label(
                    self.input_func("Generated pattern (Cross or X): ")
                )
            except ValueError:
                self.reporter.report_error("enter Cross or X")
