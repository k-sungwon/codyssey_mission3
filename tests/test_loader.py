import json
import tempfile
import unittest
from pathlib import Path

from mini_npu.loader import DataLoader


def write_json(directory, content):
    path = Path(directory) / "data.json"
    path.write_text(json.dumps(content), encoding="utf-8")
    return path


class DataLoaderTests(unittest.TestCase):
    def test_load_creates_normalized_objects_for_valid_case(self):
        content = {
            "filters": {"size_2": {"cross": [[1, 0], [0, 1]], "x": [[0, 1], [1, 0]]}},
            "patterns": {"size_2_1": {"input": [[1, 0], [0, 1]], "expected": "+"}},
        }
        with tempfile.TemporaryDirectory() as directory:
            loaded = DataLoader(write_json(directory, content)).load()

        self.assertEqual(loaded.filters_by_size[2]["Cross"].label, "Cross")
        self.assertEqual(loaded.patterns[0].expected_label, "Cross")
        self.assertEqual(loaded.failures, [])

    def test_load_rejects_missing_top_level_sections(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write_json(directory, {"filters": {}})
            with self.assertRaises(ValueError):
                DataLoader(path).load()

    def test_load_records_bad_pattern_and_keeps_valid_patterns(self):
        content = {
            "filters": {"size_2": {"cross": [[1, 0], [0, 1]], "x": [[0, 1], [1, 0]]}},
            "patterns": {
                "size_2_1": {"input": [[1, 0], [0, 1]], "expected": "cross"},
                "size_2_2": {"input": [[1]], "expected": "x"},
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            loaded = DataLoader(write_json(directory, content)).load()

        self.assertEqual([pattern.case_id for pattern in loaded.patterns], ["size_2_1"])
        self.assertEqual(loaded.failures[0].case_id, "size_2_2")
        self.assertIn("size", loaded.failures[0].reason)


if __name__ == "__main__":
    unittest.main()
