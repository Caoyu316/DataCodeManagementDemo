# Code literacy I — read, change and check

DCM · Week 4 · Thursday, 8 October 2026 · two 45-minute periods

Use **one language**. Python is the live route; R is fully supported. Predict
before running. Write down what you expect and what you checked. No report,
GitHub login, paid AI account or second implementation is required today.

## Start

Extract `student-pack.zip` to your own folder. Open that folder in VS Code.
The same five-player historical teaching fixture is supplied in `tennis.py`
and `tennis.R`. Do not replace it with current rankings.

### Before class: check your chosen route

**Python:** Python 3, NumPy and pandas. In the VS Code terminal, use your working
launcher (`python3`, `python` or `py`):

```bash
python3 -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"
```

If an import fails, complete package setup in your chosen Python environment
before class; ask for help with the exact command and error. No plotting package
is needed for the core activity. Do not spend the exercise installing tools.

**R:** base R is enough. In the terminal, check `R --version`. No tidyverse,
reticulate or Quarto installation is needed for these tasks.

### Open the supplied table in a fresh session

Python, from the extracted folder's terminal:

```bash
python3 -i tennis.py
```

You now have a Python prompt (`>>>`). Run the Python snippets there, one line
or complete block at a time. `tennis` and `pd` are supplied by the starter;
examples introduce `numpy as np` when needed. Restart this command for a fresh
session. Do not type shell commands at the Python prompt; `exit()` returns you
to the terminal. Printing is explicit in the guide where useful; a bare expression
also displays its value at the interactive prompt.

R: start R in this same folder, then run:

```r
source("tennis.R")
```

You now have `tennis`. Run the R alternatives in that R session. Sourcing the
starter again reconstructs the original table. In either language, preserve the
starter file and make your changes in a separate practice file if you save them.

If local execution is blocked, pair with a working machine and be the reviewer:
write predictions, explain the code and inspect the actual output. Finish your
own run later. The table on the slides also supports reading without a runtime;
do not claim you personally ran code you only inspected.

## Read the objects

Start by reading the five-player table in your supplied starter: one player per
row, birth date and title count in columns. The early examples use its title
counts and the existing mixed-type coercion exercise.
Try the snippets on the slides in order; answers follow the prediction, not before.

### Assignment and a simple summary

**Python**

```python
grand_slam_win = [16, 19, 20, 0, 0]
grand_slam_win
len(grand_slam_win)
```

**R alternative**

```r
grand_slam_win <- c(16, 19, 20, 0, 0)
grand_slam_win
length(grand_slam_win)
```

**Python**

```python
sum(grand_slam_win)
import statistics as st
st.mean(grand_slam_win)
```

**R alternative**

```r
sum(grand_slam_win)
mean(grand_slam_win)
```
### Inspecting and coercing types

Predict which values remain numeric before running.

**Python**

```python
type(12.5), type(2), type(True), type("hi")
val = [True, 2, "3"]
val
import numpy as np
np.array(val)
```

**R alternative**

```r
typeof(12.5); typeof(2L); typeof(TRUE); typeof("hi")
val <- c(TRUE, 2, "3")
val
typeof(val)
```
### Inspect the supplied table

**Python**

```python
# Start from the supplied tennis.py
print(tennis)
tennis.info()
tennis.shape
list(tennis.columns)
```

**R alternative**

```r
# Start from the supplied tennis.R
tennis
str(tennis)
dim(tennis)
names(tennis)
```

The original table has five player labels and two columns, `date_of_birth`
(initially text) and `grand_slam_win` (numeric). Counts are 16, 19, 20, 0, 0,
as supplied in the historical lecture. Reference date: **30 September 2019**.
Zero is an observed count, not a missing value.

### Select by position, label, column and condition

In pandas, `.iloc` means position and `.loc` means label. Both examples select
Nadal in this original table. After sorting, the second row may be someone else.
Python positions start at 0; R positions start at 1.

**Python**

```python
tennis.iloc[1]                 # second row, by position
tennis.loc["Rafael Nadal"]     # row with this label
```

**R alternative**

```r
tennis[2, ]                    # second row, by position
tennis["Rafael Nadal", ]       # row with this name
```

**Python**

```python
wins = tennis["grand_slam_win"]
cols = tennis[["grand_slam_win", "date_of_birth"]]
print(cols)
```

**R alternative**

```r
wins <- tennis[["grand_slam_win"]]
cols <- tennis[c("grand_slam_win", "date_of_birth")]
cols
```

**Python**

```python
mask = tennis["grand_slam_win"] > 0
positive = tennis.loc[mask]
print(mask)
print(positive)
```

**R alternative**

```r
mask <- tennis$grand_slam_win > 0
positive <- tennis[mask, ]
mask
positive
```

## Quick wins

**5 minutes working + 3 minutes debrief.** Use the existing values 3, 6, 9, 12.

1. Predict the second value, last value and descending order without running.
2. Select the second value by position, then the last value. Explain what each
   selection means.
3. Sort with the built-in sorter. Run and compare your result with a partner.

Starter: Python `x = [3, 6, 9, 12]`; R `x <- c(3, 6, 9, 12)`.
Hints: Python `sorted(x, reverse=True)`; R `sort(x, decreasing = TRUE)`.

<details><summary>Worked answers — open after your attempt</summary>


**Python**

```python
x = [3, 6, 9, 12]
x[1]                         # second value
x[-1]                        # last value
sorted(x, reverse=True)
```

**R alternative**

```r
x <- c(3, 6, 9, 12)
x[2]                         # second value
tail(x, 1)                   # last value
sort(x, decreasing = TRUE)
```

Expected: second 6; last 12; descending values 12, 9, 6, 3. Explain which values
were selected. The sorter returns a reordered sequence; `x` stays unchanged
unless you assign the result back to it.

</details>

## Tennis task

**10 minutes working + 4 minutes debrief/checking associations.** Start with the supplied five-player
`tennis` table. This task adapts the first historical tennis challenge; no later
ranking dataset is used. We read the supplied date calculation rather than learn
a date library from scratch.

### Supplied transformation: add approximate age

Predict the number of rows and columns before running:


**Python**

```python
work = tennis.copy()
work["date_of_birth"] = pd.to_datetime(work["date_of_birth"])
ref_date = pd.Timestamp("2019-09-30")
work["age_years"] = (
    (ref_date - work["date_of_birth"]).dt.days / 365.2425
)
work.shape
```

**R alternative**

```r
work <- tennis
work$date_of_birth <- as.Date(work$date_of_birth)
ref_date <- as.Date("2019-09-30")
work$age_years <- as.numeric(
    difftime(ref_date, work$date_of_birth, units = "days")
) / 365.2425
dim(work)
```

`work` is an edited copy; `tennis` should remain unchanged. The result is
approximate age in years at the fixed reference date, not completed birthdays
or current age. Dates and title counts keep the same player associations.

### Select, modify, sort and check

1. **3 minutes:** run the supplied transformation. Keep players with more than
   zero titles and sort their whole rows by age, oldest first.
2. **4 minutes:** change the condition to **at least 19** titles. Before running,
   predict which players remain. Display only title count and age for the result.
3. **3 minutes:** check the original/derived row counts, retained names and each
   player's title count. Explain your condition change to a partner.

Starting code to adapt (choose one language):

```python
positive = work.loc[work["grand_slam_win"] > 0]
ranked = positive.sort_values("age_years", ascending=False)
print(ranked[["grand_slam_win", "age_years"]])
```

```r
positive <- work[work$grand_slam_win > 0, ]
ranked <- positive[order(-positive$age_years), ]
ranked[c("grand_slam_win", "age_years")]
```

`>` means greater than; `>=` means greater than or equal to. Change the condition,
not the original data. Sorting a column by itself would lose the intended
row association: sort the table, then select the columns you want to display.

<details><summary>Checks and worked solution — open after your attempt</summary>


**Python**

```python
positive = work.loc[work["grand_slam_win"] > 0]
ranked = positive.sort_values("age_years", ascending=False)
selected = work.loc[work["grand_slam_win"] >= 19]
selected = selected.sort_values("age_years", ascending=False)
print(selected[["grand_slam_win", "age_years"]])
```

**R alternative**

```r
positive <- work[work$grand_slam_win > 0, ]
ranked <- positive[order(-positive$age_years), ]
selected <- work[work$grand_slam_win >= 19, ]
selected <- selected[order(-selected$age_years), ]
selected[c("grand_slam_win", "age_years")]
```

- Original `tennis`: 5 rows × 2 columns; historical title total 55.
- `work` after age assignment: 5 rows × 3 columns. Original remains unchanged.
- More than zero titles: Federer (20), Nadal (19), Djokovic (16), oldest first.
- At least 19 titles: Federer (20), Nadal (19), oldest first.
- Final ages approximately 38.14 and 33.33. Keep full precision in the calculation.

Check that each birth date and title count still belongs to the same named player;
a correct row count alone cannot establish this.

</details>

### Why row count alone is insufficient

A deliberately wrong operation on a disposable copy (predict before running):

```python
broken = work.copy()
broken["grand_slam_win"] = sorted(work["grand_slam_win"])
```

```r
broken <- work
broken$grand_slam_win <- sort(work$grand_slam_win)
```

Five rows and 55 total titles remain, but Djokovic now has 0 rather than 16 and
Federer 16 rather than 20. The sorted counts were attached by position to unchanged
player rows. Sort the **whole table** so names, birth dates, titles and ages move
together. Keep this incorrect `broken` copy separate from the real result.

**Optional after the core task:** use the original challenge's wins-versus-age plot
if you already know the plotting tools. Explain which rows you are plotting.
No plotting installation or chart is required for Week 4.

## Understanding missing-value behavior

In our tennis fixture, **0 Grand Slam titles is an observed value**. An unknown
or unrecorded title count would be missing. Missing is not zero. Empty text is
not automatically missing either. Detecting
missing values and deciding what to do about them are separate tasks.
Use the explicit missing-value test, not equality to `NA`/`NaN`.


**Python**

```python
sample = np.array([2, np.nan, 4])
np.isnan(sample)
```

**R alternative**

```r
sample <- c(2, NA, 4)
is.na(sample)
```

**Python**

```python
np.mean(sample)
np.nanmean(sample)
pd.Series(sample).mean()
pd.Series(sample).mean(skipna=False)
```

**R alternative**

```r
mean(sample)
mean(sample, na.rm = TRUE)
```

For 2, missing, 4: ordinary R/NumPy mean is missing. The explicit missing-skipping
mean is 3, with denominator 2. A pandas floating-point Series mean skips missing
values by default here; `skipna=False` instead propagates missingness.
Always identify the library and denominator. A default is not a justification.

## Better performance ≠ better learning?

**Five-minute discussion before the activity.** If AI helps students complete an
exercise, do you expect greater understanding too? Predict, then discuss the
Bassner et al. (2026) finding on the slide: higher task scores and less frustration
without a detected advantage in knowledge gains or code comprehension in that
setting. The practical response is to keep predicting and checking while using AI.

## AI activity

**12 minutes total.** Use the original masking exercise below. It is an artificial
mechanics example: replacing odd values is **not** a recommended real-data
cleaning rule. Remainder (`%` in Python, `%%` in R) identifies odd values here.

### Minutes 0–3: predict without running and without AI

Read the snippet in your chosen language. Annotate the construction, mask and
assignment. Predict the values, length, number missing and number observed.
Does this remove elements or replace their values? Write your prediction first.


**Python**

```python
import numpy as np
x = np.arange(1, 11, dtype=float)
x[x % 2 == 1] = np.nan
x
```

**R alternative**

```r
x <- 1:10
x[x %% 2 == 1] <- NA_integer_
x
```

### Minutes 3–5: ask for explanation, then compare

Name the language and library, paste the existing snippet, and use this prompt:

> Explain this R/Python snippet line by line without changing it. Predict its
> values, length and missing-value count. Does it remove observations or replace
> values? What does the mean include by default in this specific library, and
> what should I check myself? State any assumptions.

Do not request a rewrite. Identify an agreement, disagreement or unsupported
claim by comparing the response with your written prediction.

**No AI access:** compare with a partner's explanation and perform the same checks.
The instructor may show an available response. No paid account, agent installation
or AI login is required. Do not spend the activity troubleshooting access.

### Minutes 5–9: run the original code and verify

Run the original snippet above, then inspect its displayed values. Use the checks
below and verify the retained-value sum by hand. The Python session also needs
`import pandas as pd` (already supplied by `tennis.py`).


**Python**

```python
len(x), np.isnan(x).sum(), (~np.isnan(x)).sum()
np.nansum(x)
np.mean(x), np.nanmean(x)
pd.Series(x).mean()
np.nan_to_num(x, nan=0).mean()
```

**R alternative**

```r
length(x); sum(is.na(x)); sum(!is.na(x))
sum(x, na.rm = TRUE)
mean(x); mean(x, na.rm = TRUE)
zero_filled <- x
zero_filled[is.na(zero_filled)] <- 0
mean(zero_filled)
```

The last comparison replaces missing values by zero in a separate result. It
illustrates changed meaning; it is not advice to fill real missing observations.
The NumPy example contains only finite values and `NaN`.

### Minutes 9–12: debrief

<details><summary>Expected checks — open after prediction and execution</summary>

- Length 10; missing 5; observed 5.
- Displayed values: missing, 2, missing, 4, missing, 6, missing, 8, missing, 10.
- Observed values sum to 30. Their mean is 6 = 30 / 5.
- Ordinary R/NumPy mean is missing; pandas mean here is 6.
- Replacing missing by zero gives 3 = 30 / 10, a different denominator and question.

</details>

Spend at most one minute on this question: **“I ask one AI to write the code and
another to check it. Have I independently verified it?”** Li et al. (2026) reports
students delegating checks to AI; these are reported practices, not evidence of
check reliability. Model agreement can help review, but provide your own comparison
with the data, expected values and a manual sum before accepting the claim.

State one claim you independently verified and one analytical decision the code
cannot justify. Computational correctness does not justify discarding or replacing
observations in a real dataset.

**AI can explain code; the analyst remains responsible for understanding the
operation and validating the output.**

## Exit check

1. What are the input and the operation?
2. What should change — and what must NOT change?
3. What evidence tells me the result is correct?
 Keep the tennis edit and your prediction/check notes.
Next week, 15 October: control flow, functions and debugging in Code Literacy II.

## Discussion sources

- Bassner, P., Lenk-Ostendorf, B., Beinstingel, R., Wasner, T., & Krusche, S. (2026).
  *Less stress, better scores, same learning: The dissociation of performance and
  learning in AI-supported programming education*. Computers and Education:
  Artificial Intelligence, 10, 100537.
  [DOI](https://doi.org/10.1016/j.caeai.2025.100537).
- Li, S., Tang, J., Qiang, Z., & Wang, Z. (2026).
  *Examining Computer-Science Students’ Metacognitive Beliefs and Reported Practices
  in Verifying AI-Generated Code: A Concurrent Mixed-Methods Study*.
  Journal of Intelligence, 14(10), 232.
  [DOI](https://doi.org/10.3390/jintelligence14100232).

No full-paper reading or AI account is required for these discussions.
