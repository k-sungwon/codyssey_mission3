# Mini NPU Simulator Implementation Plan

**Goal:** Implement the Mini NPU Simulator console assignment with both required modes and the flat-array bonus.

**Architecture:** Domain objects retain filter, pattern, and result state. Stateless validation and classification stay as functions. Named calculator strategy objects enable basic and optimized MAC comparison; application, loader, reporter, and performance analyzer coordinate their separate boundaries.

**Tech Stack:** Python 3.8+, standard library `dataclasses`, `json`, `time`, and `unittest`.

## File Plan

- `mini_npu/models.py`: `Filter`, `Pattern`, `MatchResult`.
- `mini_npu/helpers.py`: validation, parsing support, normalization,
  classification, and flattening.
- `mini_npu/calculators.py`: 2D and flat MAC strategies.
- `mini_npu/performance.py`: repeated timing.
- `mini_npu/loader.py`: JSON-to-domain-object conversion and per-case errors.
- `mini_npu/input.py`: line-by-line console matrices.
- `mini_npu/reporter.py`: all console presentation.
- `mini_npu/application.py`: mode orchestration.
- `main.py`, `data.json`, `README.md`, and focused `unittest` test modules.

## Delivery Order

1. Tests and implementation for domain data plus pure helpers.
2. Tests and implementation for both MAC strategies and timing.
3. Tests and implementation for JSON loading and failure isolation.
4. Tests and implementation for application flow and reporting.
5. README, sample JSON, full-suite verification, and a scripted console smoke test.
