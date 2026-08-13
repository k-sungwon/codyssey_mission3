from typing import Callable, List


def parse_matrix_row(raw: str, expected_size: int) -> List[float]:
    tokens = raw.split()
    if len(tokens) != expected_size:
        raise ValueError("row must contain exactly {0} values".format(expected_size))
    try:
        return [float(token) for token in tokens]
    except ValueError as error:
        raise ValueError("every matrix value must be numeric") from error


def read_matrix_from_console(
    title: str,
    size: int,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> List[List[float]]:
    output_func(title)
    matrix = []
    while len(matrix) < size:
        row_number = len(matrix) + 1
        try:
            matrix.append(parse_matrix_row(input_func("row {0}/{1}: ".format(row_number, size)), size))
        except ValueError as error:
            output_func("Input error: {0}".format(error))
    return matrix
