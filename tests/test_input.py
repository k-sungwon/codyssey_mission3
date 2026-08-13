import unittest

from mini_npu.input import parse_matrix_row


class InputTests(unittest.TestCase):
    def test_parse_matrix_row_accepts_flexible_whitespace(self):
        self.assertEqual(parse_matrix_row(" 1\t0  2.5 ", 3), [1.0, 0.0, 2.5])

    def test_parse_matrix_row_rejects_wrong_column_count(self):
        with self.assertRaises(ValueError):
            parse_matrix_row("1 0", 3)


if __name__ == "__main__":
    unittest.main()
