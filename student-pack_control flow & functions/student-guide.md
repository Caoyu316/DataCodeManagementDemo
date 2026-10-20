# Code literacy II — trace, modify and verify

DCM · Week 5 · Thursday, 15 October 2026 · two 45-minute periods

Use **one language**. In the HTML deck, click “R alternative” to switch the code;
the PDF shows Python, and this guide includes both languages. Predict before running; inspect a proposal before accepting it.
No new dataset, paid AI account, package installation or GitHub setup is required.

## Start

Extract `student-pack.zip` and open that folder in VS Code. Use your working Python
or R installation from Week 4. The Python examples need only the standard library;
the R examples use base R. If your own runtime is blocked, pair with a working
machine and take the reviewer role, recording predictions and checking real output.

- `control-flow.py` / `control-flow.R`: the supplied branch, finite-loop and FizzBuzz
  examples. Read and predict each section before running it. Running the whole file
  prints all four sections, including FizzBuzz; wait until your predictions are written.
- `functions.py` / `functions.R`: supplied `f` and `my_div`. These files define
  functions without calling the intentionally failing examples. Save edits here.

From the extracted folder, start an interactive Python session:

```sh
python3 -i functions.py
```

Use your usual `python` or `py` launcher if appropriate. At the `>>>` prompt, enter
Python calls, not shell commands. After editing the file, use `exit()` and repeat
this terminal command: the new definitions are now loaded. `math` and `warnings`
are already imported by the starter. A bare call displays its returned value at
the interactive prompt; `print(...)` also works.

For R, start a fresh R session in the extracted folder and run:

```r
source("functions.R")
```

After an edit, source the file again. For the final fresh-session check, restart R
and source it. Run calls expected to error **individually**, then continue with the
next call at the prompt; an error in a sourced script can stop later checks.

## Trace control flow

The historical examples below are supplied, not blank-page programming tasks.
First predict the value of `x` at each test, then run.

`%` is Python’s remainder operator: `7 % 2 == 1`, `8 % 2 == 0`. R uses `%%`. A zero remainder means divisible.

**Python · live route**

```python
x = -4
if x < 0:
    x = -x
if x % 2 == 0:
    print(f"{x} is even")
```

**R alternative**

```r
x <- -4
if (x < 0) {
  x <- -x
}
if (x %% 2 == 0) {
  cat(x, "is even\n")
}
```

Next, predict which single branch runs for `x = 0`, then change only the input to `3`.

**Python · live route**

```python
x = 0
if x == 0:
    print("zero")
elif x % 2 == 0:
    print("even")
else:
    print("odd")
```

**R alternative**

```r
x <- 0
if (x == 0) {
  cat("zero\n")
} else if (x %% 2 == 0) {
  cat("even\n")
} else {
  cat("odd\n")
}
```

A branch uses one non-missing Boolean/logical answer. Last week's tennis mask gave
one answer per player; that sequence is a different object. R vector `if` and vector
`||` error in the current teaching runtime. A multi-value NumPy condition is also
ambiguous. Ordinary Python lists are different again: even `[False]` is nonempty
and truthy. Do not use these objects as substitutes for an explicit scalar condition.

`any(mask)` asks whether at least one element is true; `all(mask)` asks whether every
one is true. Those are deliberate new questions, not automatic repairs for a mask
that was used in the wrong place. We do not need to rerun the tennis analysis.

For the finite loop, trace current value → body → next value → stopping point.

**Python · live route**

```python
for number in range(1,7):
    print(number)
```

**R alternative**

```r
for (number in 1:6) {
  print(number)
}
```

<details><summary>Checks — after your predictions</summary>

The negative-input example changes −4 to 4 and prints “4 is even”. The branch chain prints “zero” for 0 and “odd” for 3. The loop prints 1 through 6 in order. Python excludes the stop value 7; R’s `1:6` includes 6.

</details>

## FizzBuzz

**7 minutes including debrief.** Use the supplied code below (also in the control-flow
file). You do not need to write it from scratch.

1. Predict the output at inputs **3, 5 and 15**. Mark the first true condition.
2. Explain why the combined case precedes the separate cases.
3. Change only the loop bound so it includes **21**. Predict, run and check the last output.
4. Explain the change to a partner. Use one language.

**Python · live route**

```python
for i in range(1, 21):
    if i % 15 == 0: print("FizzBuzz")
    elif i % 3 == 0: print("Fizz")
    elif i % 5 == 0: print("Buzz")
    else: print(i)
```

**R alternative**

```r
for (i in 1:20) {
  if (i %% 15 == 0) cat("FizzBuzz\n")
  else if (i %% 3 == 0) cat("Fizz\n")
  else if (i %% 5 == 0) cat("Buzz\n")
  else cat(i, "\n")
}
```

<details><summary>FizzBuzz checks — after the attempt</summary>

3 → Fizz; 5 → Buzz; 15 → FizzBuzz. Testing the multiple-of-3 condition first would incorrectly label 15 as Fizz. For the bound edit, Python uses `range(1, 22)` and R uses `1:21`. The final output is Fizz at 21; the original final output at 20 was Buzz.

</details>

## Read the supplied function

Defining a function stores its body; calling it supplies inputs and executes it.
Identify the arguments, operation and returned result.

**Python · live route**

```python
def my_div(numerator, denominator):
    div = numerator / denominator
    return div
```

**R alternative**

```r
my_div <- function(numerator, denominator) {
  div <- numerator / denominator
  return(div)
}
```

**Python · live route**

```python
my_div(1, 2)
my_div(numerator=1, denominator=2)
```

**R alternative**

```r
my_div(1, 2)
my_div(numerator = 1, denominator = 2)
```
Both calls return 0.5. Named arguments identify the same inputs as the positional call. Now predict whether the outer `div` changes:

**Python · live route**

```python
div = 99
result = my_div(4, 2)
print(result)
print(div)
```

**R alternative**

```r
div <- 99
result <- my_div(4, 2)
result
div
```

<details><summary>Local-name check</summary>

The returned result is 2; the outer `div` is still 99. The assignment inside `my_div` is local to that function call. Printing a result is different from returning it to the caller.

</details>

## Small change

**6 minutes.** In `functions.py` / `functions.R`, use the supplied `f`. Its intended
behavior is “input plus one”. The R version already returns its last expression;
this is not an R bug.

1. Predict the supplied result before running.
2. Python: add the missing return. R: explain the implicit return, then make it explicit.
3. Reload your edited definition. Check **2 → 3** and **0 → 1**.
4. Change only the increment from one to two. Reload; check **2 → 4**.

**Python · live route**

```python
def f(x):
    x + 1
print(f(2))
```

**R alternative**

```r
f <- function(x) { x + 1 }
f(2)
```

<details><summary>Worked changes — after your attempt</summary>

The original Python function returns `None`; computing `x + 1` does not return it. R returns 3 for input 2.

**Python · live route**

```python
def f(x):
    return x + 1
print(f(2))
print(f(0))
```

**R alternative**

```r
f <- function(x) { return(x + 1) }
f(2)
f(0)
```

Then change the increment:

**Python · live route**

```python
def f(x):
    return x + 2
print(f(2))
```

**R alternative**

```r
f <- function(x) { return(x + 2) }
f(2)
```


</details>

## Assumptions, errors and warnings

The required division exercise takes **ordinary finite real scalar inputs**: one
number per argument. Negative values and a zero numerator are valid. We also
explicitly test text as invalid input. Arrays, vector recycling/broadcasting,
complex/Boolean inputs and pre-existing missing/non-finite values are outside this
exercise. This is not a general numeric-validation library.

An error stops the current operation. A warning ordinarily permits execution to
continue, but does not establish that the returned result is safe. Try the supplied
warning example in a fresh session:

**Python · live route**

```python
import warnings
warnings.warn("Check the inputs")
print("Execution continues")
```

**R alternative**

```r
warning("Check the inputs")
print("Execution continues")
```

The original `my_div(2, 0)` raises `ZeroDivisionError` in Python and returns `Inf`
in R. Neither is a language bug. Later we introduce a **new desired contract**:
missing result plus useful warning when the denominator is zero. Returning missing
is a chosen policy, not an automatic cure for every problem.


### A data-analysis reason for the policy

Average revenue per order is `revenue / number_of_orders`. Store A has revenue
1000 and 50 orders: average 20. Store B has revenue 0 and 0 orders: no per-order
average is defined. Zero would suggest an observed average; infinity would also
mislead. For this exercise we choose a warning plus a missing numeric result.
Original `my_div(0, 0)` raises a Python error or returns R `NaN`; original `(2, 0)`
returns R `Inf`. These are language rules, not bugs.

Python `math.nan` is a floating-point NaN; `None` is not a numeric NaN.
R `NA` marks a missing/unknown value; `NA_real_` is its numeric (double) form.
R `NaN` marks an undefined numerical result. `is.na` detects both, so our check
also excludes `NaN`. Detecting missing is separate from choosing this policy.

## Debugging workflow

**Reproduce → locate → hypothesize → change one thing → rerun → verify.**

Apply it to `f(2)` and `my_div("a", 2)`, which you already know:

- Record intended behavior, the exact input and actual output/error.
- Identify the error type/message (if any), the relevant operation in your own
  code and the actual arguments. Here text reaches the division operation.
- Form a hypothesis before editing. `None` after `f(2)` suggests that computation
  did not become a returned value; it is not an exception.
- Inspect the small edit, rerun the original case and check other valid inputs.

No debugger software is needed. Preserve a small reproducible example rather than
relying on objects or old function definitions left over in your session.

## Manual division

**10 minutes including debrief; no AI yet.** Work on your supplied `my_div`.

1. Run `my_div("a", 2)` and identify the error message, operation and actual inputs.
2. Insert the supplied guard below **inside the function, before division**.
   Read it as “is either argument text?”. Python indentation is part of the block;
   R uses braces. Do not silently convert text to missing.
3. Reload your edited function. Check `(4,2) → 2`, `(0,2) → 0`, `(-4,2) → -2`.
   Each should complete without a warning. Check text in each position separately: `my_div("a", 2)` and `my_div(2, "a")` must raise useful errors.
4. Predict and observe `(2,0)` separately. **Do not add zero handling yet.**

These guards reject text; they are not checks of every excluded input domain.

**Python · live route**

```python
if isinstance(numerator, str) or isinstance(denominator, str):
    raise TypeError("numerator and denominator must be numbers, not text")
```

**R alternative**

```r
if (is.character(numerator) || is.character(denominator)) {
  stop("numerator and denominator must be numbers, not text")
}
```

<details><summary>Guarded my_div — compare after the attempt; use this if you are stuck</summary>


**Python · live route**

```python
def my_div(numerator, denominator):
    if isinstance(numerator, str) or isinstance(denominator, str):
        raise TypeError("numerator and denominator must be numbers, not text")
    return numerator / denominator
```

**R alternative**

```r
my_div <- function(numerator, denominator) {
  if (is.character(numerator) || is.character(denominator)) {
    stop("numerator and denominator must be numbers, not text")
  }
  return(numerator / denominator)
}
```

The normal results remain 2, 0 and −2. Text is rejected before division. Zero denominator still gives the original Python error / R infinity.

</details>

## AI continuation

**19 minutes total.** Modify the same guarded `my_div(numerator, denominator)`
in place to satisfy the new zero-denominator requirement. Keep its name and arguments.
Use no third-party libraries. Python standard-library modules are permitted;
R base functions are sufficient. No paid account is required.

### Contract and independent cases — set before asking AI

For the stated scalar domain: nonzero denominator returns the quotient; zero
denominator returns missing **and** emits a useful warning; text still errors.
Negative inputs and a zero numerator remain valid.

| Inputs | Expected result | Expected signal |
| --- | --- | --- |
| `(4, 2)` | 2 | No warning |
| `(2, 0)` | Python `math.nan` / R `NA_real_` | Useful zero-denominator warning |
| `(0, 2)` | 0 | No warning |
| `(-4, 2)` | −2 | No warning |
| `("a", 2)` | No result | Useful input error |
| `(2, "a")` | No result | Useful input error |

### Minutes 0–3: predict and reproduce before AI

Write what the new contract requires at `(4,2)` and `(2,0)`. Run the current
`my_div(2,0)` and record the result/error. Locate the division operation. Explain
why the current code does not implement the newly requested policy.

### Minutes 3–5: ask for a small proposal

Paste your current code, prediction and actual failing call with this prompt:

> This supplied function currently divides two ordinary scalar numbers. We now
> require a missing result and a useful warning when the denominator is zero;
> text inputs must still raise an error. Here are my prediction, current code
> and the observed failing call. Explain the relevant execution path and propose
> the smallest change to the existing `my_div(numerator, denominator)`.
> Keep its name and argument names. Return Python `math.nan` / R `NA_real_`. Preserve ordinary division, including zero numerators and negative
> values. Use no third-party libraries: Python standard-library modules are permitted;
> R base functions are sufficient. Do not add vector support or a broad catch-all exception.
> Explain each changed line. I will run my own checks.

**No AI access:** propose the edit with a partner, then compare with the worked
scalar solution below. Inspect and test it using the same steps. Do not spend
activity time troubleshooting a login.

### Minutes 5–8: inspect before running

Compare old and proposed code. Point to all five components: zero check, warning,
returned missing value, normal division path and text-input rejection. Reject
unrelated rewrites, a hard-coded answer, returning zero for missing, or hiding every
error. A small diff tells you what changed; it does not prove the change is correct.

### Minutes 8–16: verify independently

Save the reviewed function in your functions file and reload the definition.
Python's `math` and `warnings` imports are supplied; R needs no package. Run the
six cases, recording both returned value and warning/error. The commands below
are supplied independently of the AI. Enter expected-error calls individually.

**Python · live route**

```python
print(my_div(4, 2))
print(math.isnan(my_div(2, 0)))
print(my_div(0, 2))
print(my_div(-4, 2))
my_div("a", 2)  # expected input error
my_div(2, "a")  # run separately; expected input error
```

**R alternative**

```r
my_div(4, 2)
result <- my_div(2, 0)
is.na(result) && !is.nan(result)
my_div(0, 2)
my_div(-4, 2)
my_div("a", 2)  # expected input error
my_div(2, "a")  # run separately; expected input error
```

`math.isnan(...)` should be true in Python. In R, `is.na(result) && !is.nan(result)` distinguishes the chosen missing result from NaN. These expressions check the **returned value only**, not whether a warning occurred.
Do not compare missing values with equality. The zero-numerator case catches a
check of the wrong argument; the negative case checks valid signed arithmetic;
the text case catches overbroad error suppression.

For the final check, restart the interpreter and load your edited file again.
Python may suppress repeated warnings from the same location; confirm the warning
on the first zero-denominator call in that fresh session. Do not add logging or
warning-filter machinery to the student function.

Before accepting, **invent one additional input** that could reveal a mistake.
Write its expected value and signal before running it. Explain what the observed
result tells you. Do not ask AI to provide your only additional check.

<details><summary>Optional: check the warning separately from the value</summary>

A missing result does not prove a warning occurred. First observe the message in a
fresh session. If uncertain, these supplied checks capture the signal separately;
do not put this checking machinery inside your function.

```python
import math
import warnings
with warnings.catch_warnings(record=True) as signals:
    warnings.simplefilter("always")
    result = my_div(2, 0)
print(math.isnan(result))  # value check
print(len(signals))        # signal check: expect 1
print(str(signals[0].message) if signals else "NO WARNING")
```

```r
warned <- FALSE
result <- withCallingHandlers(my_div(2, 0), warning = function(w) {
  warned <<- TRUE
  message(conditionMessage(w))
  invokeRestart("muffleWarning")
})
is.na(result) && !is.nan(result)  # value check
warned                           # signal check: expect TRUE
```

</details>

### Minutes 16–19: decide

Say “I accept / reject this proposal because…” and cite observed evidence. A
successful repair meets the new zero policy while preserving normal division and
text rejection. You must also be able to explain which branch ran. These cases do
not establish universal robustness or justify silently replacing other errors
with missing results.

**AI-generated code is a proposal; the analyst must understand the change and
provide evidence that it satisfies the intended behavior.**

## Worked safe division

Open only after your attempt, or for the no-AI fallback after proposing your own
small edit. This reuses the historical warning and missing-result policy with an
explicit scalar branch. It deliberately does not implement broader domains.

<details><summary>Show the scalar solution</summary>

Python uses the `math` and `warnings` imports already at the top of the starter. The text guard runs before the zero check. Returning from that zero branch prevents ordinary division from running.

**Python · live route**

```python
import math
import warnings

def my_div(numerator, denominator):
    if isinstance(numerator, str) or isinstance(denominator, str):
        raise TypeError("numerator and denominator must be numbers, not text")
    if denominator == 0:
        warnings.warn("denominator is 0; returning NaN")
        return math.nan
    return numerator / denominator
```

**R alternative**

```r
my_div <- function(numerator, denominator) {
  if (is.character(numerator) || is.character(denominator)) {
    stop("numerator and denominator must be numbers, not text")
  }
  if (denominator == 0) {
    warning("denominator is 0; returning NA")
    return(NA_real_)
  }
  return(numerator / denominator)
}
```


</details>

## Article discussion · Beyond passing tests

**6 minutes:** 1 minute reflection or neighbor discussion, 4 minutes whole-class,
1 minute conclusion. Connect your decision about `my_div()` to these questions:

1. Why could passing tests still leave code unsuitable for use?
2. Our function passes all supplied checks: should we accept it? What else matters?
3. Is this specific to AI-generated code?

Preparatory reading: David Rein (METR), **13 August 2025**,
[Research Update: Algorithmic vs. Holistic Evaluation](https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/).
The **TL;DR, Results and Caveats** sections are sufficient; no full-article reading
is required. The study concerns an early-2025 agent and two mature repositories,
not all AI-generated software. Instructor discussion notes are in the slide source.

## Exit check

Explain one executed branch, one useful error and one independent check that
supports your decision. Keep your prediction, reviewed edit and observed checks.

22 October: Responsible AI at UNIL, asynchronous. 29 October: SQL & relational data.
