import math
import re
from typing import Dict, List

EPSILON = 1e-9


def validate_matrix(matrix: List[List[float]]) -> int:
    if not isinstance(matrix, list) or not matrix:
        raise ValueError("matrix must be a non-empty list")

    size = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != size:
            raise ValueError("matrix must be square")
        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("matrix values must be numeric")
            if not math.isfinite(value):
                raise ValueError("matrix values must be finite")
    return size


def normalize_label(label: str) -> str:
    normalized = str(label).strip().lower()
    if normalized in {"cross", "+"}:
        return "Cross"
    if normalized == "x":
        return "X"
    raise ValueError("label must be cross/+ or x")


def extract_size_from_key(key: str) -> int:
    match = re.fullmatch(r"size_(\d+)_(\d+)", key)
    if not match:
        raise ValueError("pattern key must have the form size_{N}_{idx}")
    return int(match.group(1))


def flatten_matrix(matrix: List[List[float]]) -> List[float]:
    return [value for row in matrix for value in row]


def generate_cross_pattern(size: int) -> List[List[float]]:
    if size <= 0:
        raise ValueError("size must be positive")
    centers = _center_indices(size)
    return [
        [1.0 if row in centers or column in centers else 0.0 for column in range(size)]
        for row in range(size)
    ]


def generate_x_pattern(size: int) -> List[List[float]]:
    if size <= 0:
        raise ValueError("size must be positive")
    return [
        [1.0 if row == column or row + column == size - 1 else 0.0 for column in range(size)]
        for row in range(size)
    ]


def _center_indices(size: int) -> set:
    if size % 2:
        return {size // 2}
    return {size // 2 - 1, size // 2}


def classify(scores: Dict[str, float], epsilon: float = EPSILON) -> str:
    if not scores:
        raise ValueError("scores cannot be empty")

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if len(ranked) == 1:
        return ranked[0][0]
    if abs(ranked[0][1] - ranked[1][1]) < epsilon:
        return "UNDECIDED"
    return ranked[0][0]
