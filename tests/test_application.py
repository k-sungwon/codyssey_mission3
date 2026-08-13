import json
import tempfile
import unittest
from pathlib import Path

from mini_npu.application import Application
from mini_npu.models import Filter, Pattern


class ApplicationTests(unittest.TestCase):
    def test_analyze_case_uses_scores_to_make_pass_result(self):
        app = Application(output_func=lambda _: None)
        pattern = Pattern("case", [[1, 0], [0, 1]], 2, "Cross")
        filters = {
            "Cross": Filter("Cross", [[1, 0], [0, 1]], 2),
            "X": Filter("X", [[0, 1], [1, 0]], 2),
        }

        result = app.analyze_case(pattern, filters)

        self.assertEqual(result.predicted_label, "Cross")
        self.assertTrue(result.passed)
        self.assertEqual(result.scores, {"Cross": 2.0, "X": 0.0})

    def test_run_json_mode_includes_invalid_case_in_summary(self):
        content = {
            "filters": {"size_2": {"cross": [[1, 0], [0, 1]], "x": [[0, 1], [1, 0]]}},
            "patterns": {
                "size_2_1": {"input": [[1, 0], [0, 1]], "expected": "+"},
                "size_2_2": {"input": [[1]], "expected": "x"},
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            path.write_text(json.dumps(content), encoding="utf-8")
            output = []
            summary = Application(path, output_func=output.append).run_json_mode()

        self.assertEqual(summary, {"total": 2, "passed": 1, "failed": 1})
        self.assertTrue(any("SUMMARY" in line for line in output))


if __name__ == "__main__":
    unittest.main()
