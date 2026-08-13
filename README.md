# Mini NPU Simulator

Python 3.8+ standard-library console program for the Codyssey mini NPU assignment.

Run it from the project root:

```bash
python3 main.py
```

Mode 1 reads two 3x3 filters and one 3x3 pattern row by row. Rows accept any
whitespace-separated real numbers, and invalid rows are requested again. Mode 2
loads `data.json`; bad whole-file JSON/schema errors stop that mode, while bad
individual pattern cases are reported as `FAIL` and the remaining cases run.

The score is a multiply-accumulate over matching matrix positions. Classification
uses the largest score; a gap smaller than `1e-9` is `UNDECIDED`. The program
reports each score, predicted label, optional PASS/FAIL, and average MAC time
over ten runs.

The bonus implementation compares the ordinary 2D loop (`2D`) with a flattened
1D loop (`Flat`). Both use O(N^2) MAC operations for an N by N matrix. The
performance table prints the measured average milliseconds and N^2 MAC count.

`mini_npu.helpers` also provides `generate_cross_pattern(size)` and
`generate_x_pattern(size)` for arbitrary square sizes.

Run tests:

```bash
python3 -m unittest discover -s tests -v
```
