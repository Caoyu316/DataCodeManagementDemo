# Four synthetic orders

Count all orders and calculate total revenue and average order value.
Amounts are in CHF; these four records are a teaching example.

## Inputs

`data/raw/orders.csv` is the preserved source: 10.00, 15.00, 12.50, 12.50.
Code lives in `src/`; generated results live in `outputs/`.
Paths are anchored to this project folder, located from the script itself.
Moving the entire folder therefore keeps the input and output paths valid.

## Run

Tested with Python 3.14.7, standard library only. No extra packages are needed.
Open this project folder in VS Code and start its integrated terminal here:

```sh
python3 src/summarize.py
python3 src/check_summary.py
```

Use `python` or `py` instead if that is your already-working Python 3 launcher.
Check your installed version with `python3 --version`.

Today we document the environment. Later we will make the environment itself
reproducible.

## Expected result

The analysis creates (or replaces) `outputs/summary_final.txt`:

```text
Number of orders: 4
Total revenue (CHF): 50.00
Average order value (CHF): 12.50
```

The checker reads the current input and saved output independently, and exits
with `PASS` or a nonzero exit status and `FAIL`. Run the analysis first; checking
alone does not rerun it. A passing check on one dataset does not prove that the
code works for other data or answers a useful business question.

TODO: explain the independent arithmetic check for the expected output.

Generated output is ignored by Git and can be recreated with the same commands.
The filename `summary_final.txt` does not itself establish correctness.
