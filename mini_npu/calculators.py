from mini_npu.helpers import flatten_matrix, validate_matrix
from mini_npu.models import Filter, Pattern


def _validate_inputs(pattern: Pattern, filter_: Filter) -> int:
    pattern_size = validate_matrix(pattern.matrix)
    filter_size = validate_matrix(filter_.matrix)
    if pattern.size != pattern_size or filter_.size != filter_size:
        raise ValueError("declared matrix size does not match matrix data")
    if pattern_size != filter_size:
        raise ValueError("pattern and filter sizes must match")
    return pattern_size


class BasicMacCalculator:
    name = "2D"

    def calculate(self, pattern: Pattern, filter_: Filter) -> float:
        size = _validate_inputs(pattern, filter_)
        score = 0.0
        for row_index in range(size):
            for column_index in range(size):
                score += (
                    pattern.matrix[row_index][column_index]
                    * filter_.matrix[row_index][column_index]
                )
        return score


class OptimizedMacCalculator:
    name = "Flat"

    def calculate(self, pattern: Pattern, filter_: Filter) -> float:
        _validate_inputs(pattern, filter_)
        pattern_values = flatten_matrix(pattern.matrix)
        filter_values = flatten_matrix(filter_.matrix)
        score = 0.0
        for index in range(len(pattern_values)):
            score += pattern_values[index] * filter_values[index]
        return score
