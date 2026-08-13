import unittest

from mini_npu.helpers import (
    classify,
    extract_size_from_key,
    flatten_matrix,
    generate_cross_pattern,
    generate_x_pattern,
    normalize_label,
    validate_matrix,
)
from mini_npu.models import Filter, MatchResult, Pattern


class HelperTests(unittest.TestCase):
    def test_validate_matrix_returns_square_size(self):
        self.assertEqual(validate_matrix([[1, 0], [0, 1]]), 2)

    def test_validate_matrix_rejects_ragged_rows(self):
        with self.assertRaises(ValueError):
            validate_matrix([[1, 0], [1]])

    def test_normalize_label_accepts_json_aliases(self):
        self.assertEqual(normalize_label("cross"), "Cross")
        self.assertEqual(normalize_label("+"), "Cross")
        self.assertEqual(normalize_label("x"), "X")

    def test_normalize_label_rejects_unknown_label(self):
        with self.assertRaises(ValueError):
            normalize_label("circle")

    def test_extract_size_from_key(self):
        self.assertEqual(extract_size_from_key("size_13_2"), 13)

    def test_extract_size_from_key_rejects_invalid_shape(self):
        with self.assertRaises(ValueError):
            extract_size_from_key("pattern_13")

    def test_flatten_matrix_uses_row_major_order(self):
        self.assertEqual(flatten_matrix([[1, 2], [3, 4]]), [1, 2, 3, 4])

    def test_pattern_generators_make_cross_and_x(self):
        self.assertEqual(
            generate_cross_pattern(3), [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 0.0]]
        )
        self.assertEqual(
            generate_x_pattern(3), [[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 1.0]]
        )

    def test_classify_returns_top_label(self):
        self.assertEqual(classify({"A": 9.0, "B": 2.0}), "A")

    def test_classify_returns_undecided_inside_epsilon(self):
        self.assertEqual(
            classify({"Cross": 2.0, "X": 1.9999999995}), "UNDECIDED"
        )

    def test_domain_objects_keep_input_and_result_state(self):
        pattern = Pattern("case-1", [[1, 0], [0, 1]], 2, "Cross")
        filter_ = Filter("Cross", [[1, 0], [0, 1]], 2)
        result = MatchResult("case-1", {"Cross": 2.0}, "Cross", "Cross", True)

        self.assertEqual(pattern.expected_label, "Cross")
        self.assertEqual(filter_.label, "Cross")
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
