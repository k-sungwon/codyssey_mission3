# Mini NPU Simulator Design

## Goal

Build a Python console program that calculates MAC scores for filters and
patterns, classifies the best match, loads JSON cases, and compares a basic
2D implementation with a flat-array implementation.

## Architecture

- `Filter` and `Pattern` hold domain data: label, matrix, and size. `Pattern`
  has an optional expected label.
- `MatchResult` records one classification outcome: scores, prediction,
  optional expected label, optional PASS/FAIL state, and optional failure
  reason.
- `BasicMacCalculator` and `OptimizedMacCalculator` share a duck-typed
  contract: `name` and `calculate(pattern, filter) -> float`. The former uses
  two-dimensional indexing; the latter uses flattened arrays.
- Pure functions validate matrices, normalize labels, extract a size from a
  JSON pattern key, flatten a matrix, parse console rows, and classify score
  mappings using `abs(top - second) < 1e-9` for `UNDECIDED`.
- `DataLoader` owns a JSON path and turns validated JSON into domain objects.
  File/JSON/top-level schema errors stop mode 2. Invalid cases become FAIL
  results with reasons and do not stop remaining cases.
- `PerformanceAnalyzer` repeats a calculator call at least ten times and
  returns an average time in milliseconds and the N-squared operation count.
- `ConsoleReporter` owns display formatting. `Application` owns only menu and
  use-case orchestration.

## Input and Error Policy

- Console matrices are entered one row at a time. A row must contain exactly
  the expected number of whitespace-separated, float-parsable values. Invalid
  rows are re-requested.
- Numeric matrices accept `0`, `1`, and other real values as allowed by the
  assignment.
- Mode 1 compares user-provided filters A and B; no expected label exists.
- Mode 2 maps JSON labels `cross`/`+` to `Cross` and `x` to `X`.

## Constraints

- Python 3.8+ and standard library only.
- MAC uses explicit loops, without NumPy.
- Time measurement covers calculator calls and averages at least ten runs.
- README includes complexity, sample results, failures, and bonus comparison.
