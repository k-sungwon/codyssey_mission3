import unittest

from mini_npu.calculators import BasicMacCalculator, OptimizedMacCalculator
from mini_npu.models import Filter, Pattern


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.pattern = Pattern("case", [[1, 2], [3, 4]], 2)
        self.filter_ = Filter("A", [[4, 3], [2, 1]], 2)

    def test_basic_calculator_returns_hand_calculated_mac_score(self):
        self.assertEqual(BasicMacCalculator().calculate(self.pattern, self.filter_), 20.0)

    def test_optimized_calculator_matches_basic_score(self):
        basic_score = BasicMacCalculator().calculate(self.pattern, self.filter_)
        optimized_score = OptimizedMacCalculator().calculate(self.pattern, self.filter_)
        self.assertEqual(optimized_score, basic_score)

    def test_calculator_rejects_different_matrix_sizes(self):
        wrong_filter = Filter("B", [[1]], 1)
        with self.assertRaises(ValueError):
            BasicMacCalculator().calculate(self.pattern, wrong_filter)


if __name__ == "__main__":
    unittest.main()
