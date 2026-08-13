from dataclasses import dataclass
from typing import Dict, List, Optional


Matrix = List[List[float]]


@dataclass
class Filter:
    label: str
    matrix: Matrix
    size: int


@dataclass
class Pattern:
    case_id: str
    matrix: Matrix
    size: int
    expected_label: Optional[str] = None


@dataclass
class MatchResult:
    case_id: Optional[str]
    scores: Dict[str, float]
    predicted_label: str
    expected_label: Optional[str] = None
    passed: Optional[bool] = None
    reason: Optional[str] = None
