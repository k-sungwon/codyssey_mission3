import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from mini_npu.helpers import extract_size_from_key, normalize_label, validate_matrix
from mini_npu.models import Filter, MatchResult, Pattern


@dataclass
class LoadedData:
    filters_by_size: Dict[int, Dict[str, Filter]]
    patterns: List[Pattern]
    failures: List[MatchResult]


class DataLoader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load(self) -> LoadedData:
        payload = self._read_payload()
        filters_by_size = self._load_filters(payload["filters"])
        patterns, failures = self._load_patterns(payload["patterns"], filters_by_size)
        return LoadedData(filters_by_size, patterns, failures)

    def _read_payload(self) -> dict:
        try:
            payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        except FileNotFoundError as error:
            raise ValueError("data.json file was not found") from error
        except json.JSONDecodeError as error:
            raise ValueError("data.json is not valid JSON") from error

        if not isinstance(payload, dict):
            raise ValueError("JSON top level must be an object")
        if not isinstance(payload.get("filters"), dict):
            raise ValueError("JSON must contain an object named filters")
        if not isinstance(payload.get("patterns"), dict):
            raise ValueError("JSON must contain an object named patterns")
        return payload

    def _load_filters(self, raw_filters: dict) -> Dict[int, Dict[str, Filter]]:
        filters_by_size = {}
        for size_key, raw_set in raw_filters.items():
            match = re.fullmatch(r"size_(\d+)", size_key)
            if not match or not isinstance(raw_set, dict):
                raise ValueError("each filter set must be size_{N}: {label: matrix}")
            size = int(match.group(1))
            filter_set = {}
            for raw_label, matrix in raw_set.items():
                label = normalize_label(raw_label)
                actual_size = validate_matrix(matrix)
                if actual_size != size:
                    raise ValueError("filter matrix size does not match its size key")
                if label in filter_set:
                    raise ValueError("duplicate normalized filter label")
                filter_set[label] = Filter(label, matrix, size)
            if set(filter_set) != {"Cross", "X"}:
                raise ValueError("each filter set must contain Cross and X")
            filters_by_size[size] = filter_set
        return filters_by_size

    def _load_patterns(self, raw_patterns: dict, filters_by_size):
        patterns = []
        failures = []
        for case_id, raw_case in raw_patterns.items():
            try:
                size = extract_size_from_key(case_id)
                if size not in filters_by_size:
                    raise ValueError("no filters exist for this pattern size")
                if not isinstance(raw_case, dict):
                    raise ValueError("pattern case must be an object")
                matrix = raw_case["input"]
                actual_size = validate_matrix(matrix)
                if actual_size != size:
                    raise ValueError("pattern matrix size does not match its size key")
                expected_label = normalize_label(raw_case["expected"])
                patterns.append(Pattern(case_id, matrix, size, expected_label))
            except (KeyError, TypeError, ValueError) as error:
                failures.append(
                    MatchResult(case_id, {}, "FAIL", None, False, str(error))
                )
        return patterns, failures
