# Software Engineering with AI — student guide

DCM · HEC Lausanne · Thursday, 12 November 2026  
**Make the change small. Make the evidence clear.**

[Start](#start) · [Contract](#contract) · [Manual task](#manual) · [Tests](#tests) · [AI activity](#ai) · [Handover](#handover) · [Troubleshooting](#troubleshooting)

## Start here {#start}

Download and extract the supplied **student-pack.zip** into a new folder. Open **that extracted folder** in VS Code. The pack is self-contained: no sibling lecture, instructor-only file, API request, GitHub account, API key or paid AI subscription is needed. Use **one language**, not both. Installation is before class.

Python uses the pandas already introduced in the course, plus the standard library. R uses jsonlite already used in Week 8, plus base R. Quarto and Pandoc are author tools, not student dependencies. Check your selected route:

```bash
python3 -c "import pandas; print('Python ready')"
```

```bash
Rscript --vanilla -e 'library(jsonlite); cat("R ready\n")'
```

Run all commands from the extracted folder. If your working Python launcher is `python` or `py`, substitute it consistently after verifying pandas is installed in that interpreter. In R, using `Rscript --vanilla` starts a fresh process without your saved workspace. Do not spend activity time installing tools: pair with a working machine if necessary.

For class, open this guide and your chosen-language **manual, pipeline and my-check** files. **candidate does not exist yet:** create it at the start of the AI/partner activity. The full file map below is reference; you do not need to read the loader or validation internals.

## Classroom route — do these steps in order

Use VS Code **Terminal → New Terminal**, in the extracted pack folder. Edit files in the editor and save with **Ctrl+S** (macOS **Cmd+S**) before running commands. Copy only your language's command; press Enter. Read the terminal output before proceeding.

| Stage | Open / action | Success / resume |
|---|---|---|
| Initial demonstration | Watch instructor run `script.py` / `.R` | Three country comparisons; no student edit |
| [Manual exercise](#manual), 6 min | Open manual files; two TODO edits | Same report, BASIC 14/14; everyone then uses pipeline |
| [Independent check](#tests), 4 min | Open my-check; change four constants | PRECISION PASS on pipeline; explain the rounding gap |
| [AI/partner exercise](#ai), 13 min | Create candidate; choose IDE, chat-only or offline | Save candidate, review diff, run both candidate checks |
| Final decision, within those 13 min | Open `evidence/review-template.txt` | Accept/revise/reject with results and a limitation |

**During class:** follow Open, Edit, Run, Expected result and If blocked in each activity. **Optional/reference:** file map, detailed contract explanations, worked-answer panels, sources and full fresh-extraction handover. Read those when needed; they are not extra timed tasks. All three AI/partner routes are equally legitimate.

### Reference: file map

| File | Role |
|---|---|
| `script.py` / `.R` | Working but tangled teaching adaptation; run once at the start |
| `manual.py`, `manual.R`, `manual-run.R` | Two small manual edits, with full calculation supplied |
| `pipeline.py` / `.R` | Complete public checkpoint; everyone starts the AI task here |
| `report.py` / `.R` | Explicit report entry point; selects a candidate file |
| `validation.py` / `.R` | Supplied Week 8 guards and local loading; do not edit |
| `runner.py` / `.R` | Loads the explicitly selected candidate; no reference fallback |
| `checks.py` / `.R` | Basic suite: useful but deliberately insufficient for precision |
| `my-check.py` / `.R` | Your independently chosen precision case |
| `proposal.py` / `.R` | Constructed faulty proposal for review and offline fallback |
| `worked.py` / `.R` | Open final worked solution, used only when explicitly selected |
| `data/raw`, `data/constructed` | Authentic captures versus clearly labeled teaching alterations |
| `evidence/review-template.txt` | Local prediction and acceptance record |

This is not a new graded submission.

## Today's workflow {#workflow}

| Slot | Work |
|---|---|
| 09:15–09:20 | Separate Kahoot; priority subset if time is limited |
| 09:20–10:05 | Contracts, functions/modules, documentation; six-minute manual task |
| 10:05–10:15 | Break |
| 10:15–11:00 | Test design; 13-minute AI/partner task; handover and questions |

Each teaching block has 40 committed minutes and five recovery minutes. A public checkpoint lets you continue even if an earlier activity is unfinished. No interactive names or prior terminal sessions are required.

## One familiar pipeline {#example}

A colleague wants to reuse last week's World Bank population comparison. The question remains CHE/DEU/FRA, 2023–2024, indicator `SP.POP.TOTL`. Population is measured in persons; it does not measure customer demand. The snapshots and their provenance are copied unchanged from Week 8; see [data/README.md](data/README.md) and [provenance](data/provenance.json). Estimates may be revised by the provider; no live retrieval occurs here.

Run the starting script:

```bash
python3 script.py
```

```bash
Rscript --vanilla script.R
```

It prints the correct comparison, but combines loading, extraction, calculation and display. This is a **teaching adaptation**, not a claim that Week 8's actual code lacked functions. The guarded response parsing is supplied so that today's work focuses on engineering boundaries.

| Code | Population 2023 | Population 2024 | Increase | Growth displayed |
|---|---:|---:|---:|---:|
| CHE | 8,888,822 | 9,005,582 | 116,760 | 1.314% |
| DEU | 83,287,273 | 83,516,593 | 229,320 | 0.275% |
| FRA | 68,372,286 | 68,551,653 | 179,367 | 0.262% |

Independently check Switzerland: subtract the two source values, then divide the increase by the 2023 population and multiply by 100. Keep precision until display.

## The agreement we will preserve {#contract}

`extract(payload)` takes the saved parsed response and returns six rows, sorted by code and year. Columns are `country_code`, `country_name`, `year`, `population`. Source associations matter, not just row count. Explicit null becomes Python numeric missingness / R `NA_real_`. An absent required field is an error.

`compare(table)` takes those rows and returns three rows in CHE, DEU, FRA order. Columns in **both Week 9 routes** are `country_code`, `population_2023`, `population_2024`, `increase`, `growth_pct`. This explicitly named common schema is a Week 9 teaching adaptation; Week 8's Python comparison used an index and year-labeled columns. We preserve the Week 9 baseline schema during this refactor, alongside Week 8's data and policies.

| Input or operation | Expected behavior |
|---|---|
| Six valid keys and numeric values | Preserve source values and names |
| Partial page, application error, no observations | Reject with a useful diagnosis |
| Duplicate key, absent field, wrong indicator or Boolean population | Reject |
| Explicit null | Retain the keyed missing row; comparison stops |
| Current population = 0, previous > 0 | Valid; percentage change = −100% |
| Previous population = 0 | Stop; percentage growth denominator must be positive |
| Calculation precision | Return unrounded numeric results; display may round |
| Input objects | Do not mutate them |
| Reusable calculation | No printing, network calls or file writes |

We are **not** extending the domain to arbitrary countries, years or API shapes. That would be a feature with a new specification. Tests establish evidence for this bounded task, not universal correctness.

### Documentation with a job

A function docstring/comment states purpose, inputs, output units, errors and side effects. The README tells a new person how to run the whole project. A local comment explains a decision such as why zero current population is allowed. You do not need generated documentation or a package website.

Python `import pipeline` should not print a report. Its explicit entry script is `report.py`; the `if __name__ == "__main__":` guard keeps calling `main()` separate from importing definitions. In R, `source("pipeline.R")` executes definitions and supplied setup but should not print a report; `report.R` is the explicit entry script. R source and Python import have different semantics; the separation of responsibilities transfers.

## Manual activity: return the calculation {#manual}

**Six minutes: one predict, three edit, two run and compare. No AI.**

The arithmetic is complete. The starter puts presentation at the end of `compare`. Make the result reusable while keeping the script's displayed answer unchanged. We introduce an internal return interface here; afterward, that interface becomes part of the contract preserved by the AI task.

### Open and Edit — Python

Open `manual.py`. At TODO A, replace the final `print(...)` with `return result`. At TODO B, replace the single call with assignment plus the same formatted print in the caller. Save. **Run** in the terminal:

```bash
python3 manual.py
python3 checks.py manual.py
```

### Open and Edit — R

Open `manual.R`. At TODO A, replace the three display lines with `return(result)`. Move those display lines into `manual-run.R` after assigning `result <- compare(extract(load_data()))`. Save both. **Run** in the terminal:

```bash
Rscript --vanilla manual-run.R
Rscript --vanilla checks.R manual.R
```

### Expected result

Unchanged displayed values and **BASIC 14/14 PASS**.

The original Python starter returns `None`; the original R starter invisibly returns a display table with a character growth column. Neither satisfies the desired reusable numeric-table contract. After your edit, the display is unchanged and the basic suite should pass 14/14.

### If blocked

Open the worked edits below, or stop editing and proceed directly to the supplied pipeline checkpoint. Everybody uses that checkpoint next; finishing the manual task is not required.

<details><summary>Worked manual edits</summary>

Python: the end of `compare` becomes `return result`. The entry-point block becomes:

```python
if __name__ == "__main__":
    from validation import load
    result = compare(extract(load()))
    print(result.to_string(index=False, float_format=lambda value: f"{value:.3f}"))
```

R: the end of `compare` becomes `return(result)`. The complete caller is:

```r
source("manual.R")
result <- compare(extract(load_data()))
shown <- result
shown$growth_pct <- sprintf("%.3f", result$growth_pct)
print(shown, row.names=FALSE)
```

</details>

### Required checkpoint — everyone

Preserve your attempt. **Everyone now uses the supplied `pipeline.py` / `pipeline.R`**, even if the manual exercise was skipped. This transition does not depend on opening an answer, finishing TODOs or keeping a terminal session alive.

```bash
python3 checks.py pipeline.py
python3 report.py pipeline.py
```

```bash
Rscript --vanilla checks.R pipeline.R
Rscript --vanilla report.R pipeline.R
```

Both basic suites report 14/14. Read the candidate path. The report prints three country comparisons. The runners never silently substitute `worked` or an unchanged comparison from `validation`.

## Tests: choose expectations before code {#tests}

A unit check targets a small operation; an integration check exercises connections. A regression check protects existing behavior and may be either small or broad. A function doc example that merely runs is not the same as asserting an independently expected value.

The basic suite covers source fidelity, schema, ordering, errors, simple growth and **displayed** precision. It does not establish full numeric precision. This deliberate limitation is stated in the runner output. No test was removed from previous lectures: this is a new, labeled teaching suite.

| Constructed input | Independent expectation |
|---|---|
| 100 → 110 | 10%, since the increase is one tenth |
| 300 → 400 | 100/3 percent, since the increase is one third |
| 100 → 0 | −100% |
| 0 → 100 | Comparison stops |

### Four-minute test-design task

#### Open and Edit

Open `my-check.py` or `my-check.R`. The supplied runnable case uses CHE, 300 → 400 and expected `100 / 3`. **Minimum supported route:** use DEU, 600 → 700, expected `100 / 6`, and explain the arithmetic in your own words before using AI. This changes the seed case. Change the four constants (`CODE`, `PREVIOUS`, `CURRENT`, `EXPECTED_PERCENT`); keep the rest of the scaffold.

**Optional challenge:** choose another ratio and justify its expected and rounded values.

**Your case must distinguish full precision from premature rounding.** Change the ratio as well as the country, then record (1) the expected percentage from your arithmetic, (2) that percentage rounded to three decimals, and (3) why their absolute difference exceeds `1e-9` percentage points. For 600 → 700, `100 / 6 ≈ 16.666666666667` differs from `16.667` by about `0.000333333333` percentage points, so it detects rounding. A case such as 100 → 110 gives exactly 10%: rounding to three decimals leaves it unchanged, so it cannot detect this fault. Choose for this decimal-rounding distinction; binary floating-point representation is a separate issue.

Changing only the country does not satisfy this test-design task. Do not claim the unchanged supplied seed as your own test design. These numbers are constructed in memory, not real population estimates; raw files stay unchanged.

#### Run

Run your chosen case against the checkpoint:

```bash
python3 my-check.py pipeline.py
```

```bash
Rscript --vanilla my-check.R pipeline.R
```

#### Expected result

Expected: `PRECISION PASS`. For the seed, expected and actual print as `33.333333333333`; for 600 → 700 they print approximately `16.666666666667`. The tolerance is an absolute `1e-9` percentage points: enough for floating-point representation, too small to accept rounding to thousandths. Never loosen it simply to obtain a pass.

#### If blocked

Use the supported four values above, save, and rerun on pipeline. Check spelling, quotes around DEU and your filename. Keep this check for the next activity. Pair with a working machine if your runtime is unavailable.

The scaffold calls **the selected candidate's extraction and comparison**, so it also tests whether `compare` actually uses a correct helper. A correct helper that is never called does not fix the report pipeline.

## AI-assisted activity: inspect, test, decide {#ai}

**Thirteen minutes.** Work only in the extracted project, with public/constructed data. The course's responsible-AI rules still apply. You own the acceptance decision.

| Minutes | Action |
|---|---|
| 0–2 | Copy the checkpoint to candidate; confirm your prediction and baseline |
| 2–5 | Request a small plan and proposal; switch to fallback if blocked |
| 5–7 | Read the diff and explain each changed line |
| 7–11 | Run basic and independent checks on the actual candidate; diagnose/revise |
| 11–13 | Save an evidence note and accept, revise or reject |

### Open — all routes

In VS Code Explorer, select `pipeline.py`, copy and paste it in the same folder, and rename the copy `candidate.py`; use `pipeline.R` → `candidate.R` for R. Open the new candidate. Preserve pipeline as the baseline and your modified my-check as your independent test. **Only now does candidate exist.**

### Edit — choose one equally valid route

**Route 1 · IDE coding agent with workspace access.** Open the agent panel in the extracted folder. Provide candidate plus `README.md` (contract), `validation.py` / `.R` and `checks.py` / `.R` as read-only context. Use the bounded prompt below. Permit changes only to candidate; review the agent's proposed edits and save the local file. Panel names depend on your installed assistant. If you cannot select the folder/files promptly, choose route 2 or 3.

**Route 2 · Chat-only AI in a browser.** A chat response does **not** change your local files. In VS Code, open and copy the complete text of `candidate.py` / `.R`, `README.md`, `validation.py` / `.R` and `checks.py` / `.R`. Paste them into the chat as separate code blocks labeled with their filenames; the latter three are read-only context. Do not send other projects, credentials or your independently designed my-check. Paste the bounded prompt below, then add: **“You have no access to my local files or terminal. Return one complete replacement candidate file in one code block, with no omitted sections or placeholders, followed by a short explanation of changed lines. Do not claim you saved or ran anything.”**

When the response arrives, copy only the code inside the candidate code block (no backticks or explanation). In the local candidate editor, select all, paste the code and save with Ctrl+S / Cmd+S. Check the tab filename before replacing anything. If the response is partial, ask once for the complete file; switch to route 3 at the three-minute limit. Do not execute pasted commands from the chat. Continue with the local diff and your own tests below.

**Route 3 · Complete offline partner route.** No account, connection or AI is required. Open `proposal.py` / `.R`, select all and copy its contents. Open candidate, select all, paste and save. With a partner, explain the proposed changes and run the same review/tests below. This constructed proposal intentionally contains a subtle fault. You may choose this route from the start.

### Concrete prompt

> I am refactoring this offline population-report project. Read my candidate file, the contract and the supplied basic checks. First give a brief plan.
>
> Extract the percentage-growth arithmetic from `compare(table)` into `growth_percent(previous, current)` in my candidate file, then make `compare` call it. Add concise documentation of inputs, returned units and preconditions.
>
> The helper receives validated finite numeric scalars: previous must be positive, current may be zero. It returns percentage change with full calculation precision. The caller keeps validation; formatting and rounding belong to the report script.
>
> Preserve the `compare(table)` signature, output columns/order, useful errors and nonmutation. Preserve extraction behavior. Modify only `candidate.py` (or `candidate.R`), limited to this helper, its documentation and the relevant calculation in `compare`. Do not change data, validation, tests, expected answers, dependencies or report formatting. No network or reference-solution imports.
>
> Show the diff and explain changed lines. Report exactly which checks you actually ran, and which you did not. I will inspect the changes and run independent checks before accepting them.

The helper is internal to this bounded pipeline. Its preconditions are enforced by the caller; it does not promise to validate arbitrary text, vectors or missing inputs on its own. Adding a second general-purpose validator is unnecessary for this task.

### Review — all routes converge here

In Explorer, right-click `pipeline.py` → **Select for Compare**; right-click `candidate.py` → **Compare with Selected**. R uses the corresponding files. Inspect changed files as well as lines. Confirm the formula's denominator, lack of early rounding, unchanged guards and call from `compare`. Prompt instructions do not prevent a tool from exceeding scope; inspect what actually changed.

### Run

Open **Terminal → New Terminal** in the extracted folder. Run both commands against the **same saved candidate**:

```bash
python3 checks.py candidate.py
python3 my-check.py candidate.py
```

```bash
Rscript --vanilla checks.R candidate.R
Rscript --vanilla my-check.R candidate.R
```

The runners print the selected absolute path and a file fingerprint. They check that `extract` and `compare` are defined in that selected file rather than imported from an unchanged reference. This is a diagnostic, not a security sandbox. Read the actual diff; do not execute arbitrary unreviewed code.

### Expected result and final decision

**BASIC 14/14 PASS + PRECISION PASS:** review the diff and constraints before accepting; state one limitation. **BASIC PASS + precision failure:** the returned-value contract is broken even if the report looks right. Revise or reject; do not loosen the test. Any basic failure also requires diagnosis before acceptance.

For the offline proposal, expect BASIC 14/14 PASS followed by a precision failure and a nonzero exit. A correct AI proposal can pass both. Record the actual result, not the result you hoped for.

### If blocked — complete offline partner route

If AI is unavailable or does not produce a bounded proposal within three minutes, copy **`proposal.py` / `.R` to `candidate.py` / `.R`** instead. The proposal is explicitly constructed for teaching; it is not a measurement of real AI failure frequency. Use the same diff review, commands, prediction and decision note. Do not debug an account or connection during the activity.

The prepared proposal gives:

| Check | Expected result in both languages |
|---|---|
| `checks` on `proposal` | **14/14 PASS** |
| `my-check` on `proposal` | **FAIL**, nonzero exit |
| Returned value for 300 → 400 | 33.333, incorrectly rounded |
| Required value | Approximately 33.333333333333 |

This is the point of the exercise: useful basic tests can still miss a violation. An agent may also produce a fully correct proposal; the prepared case guarantees everyone can examine the testing limitation.

<details><summary>Worked repair and expected solution</summary>

Remove `round(..., 3)` from the helper. Keep presentation rounding in the report. The relevant Python helper is:

```python
def growth_percent(previous, current):
    """Return unrounded growth (%) for validated finite numeric scalars.

    Preconditions: previous > 0 and current >= 0; caller checks these.
    No I/O or mutation.
    """
    return 100 * (current - previous) / previous
```

The R equivalent is:

```r
# Return unrounded growth (%) for validated finite numeric scalars.
# Preconditions: previous > 0, current >= 0; caller checks these.
# No I/O or mutation.
growth_percent <- function(previous, current) {
  100 * (current - previous) / previous
}
```

In the existing comparison function, replace only the rate assignment with `rate = growth_percent(previous, current)` in Python or `rate <- growth_percent(previous, current)` in R. Keep guards and output assembly unchanged. There is no need to generalize the API, change dependencies or reformat the whole project.

The complete correct files are openly provided as `worked.py` and `worked.R`; tests load them only if you explicitly select them. If blocked, use that reference and still explain the difference, execute both checks and disclose that you used the worked answer. Do not present reference output as verification of your own candidate.

</details>

### Evidence note

Complete `evidence/review-template.txt`: your prediction; candidate filename; relevant changed line; basic and independent commands/results; accept/revise/reject with a reason; a remaining limitation; AI/partner/reference assistance used. You may record output with terminal copy/paste. A green status or the assistant's narrative is not enough.

## Reproducible handover {#handover}

Close old interactive sessions. Open a new terminal in a freshly extracted copy. For the distributed final checkpoint:

```bash
python3 report.py worked.py
python3 checks.py worked.py
python3 my-check.py worked.py
```

```bash
Rscript --vanilla report.R worked.R
Rscript --vanilla checks.R worked.R
Rscript --vanilla my-check.R worked.R
```

To hand over **your own work**, include your `candidate` and your modified `my-check` alongside the pack files, then substitute `candidate.py` / `.R` in all three commands. State dependencies, working directory, input provenance and expected outputs in your README/evidence note. The final reference passes both check sets; selected cases do not prove all possible behavior. Recreating environments is the next lecture.

## Troubleshooting {#troubleshooting}

- **Missing pandas/jsonlite:** use the existing Week 8 setup; pair now and fix installation before the next class.
- **Missing data or `validation.R`:** run from the extracted folder, not its parent. Python loads data relative to its module; R's documented route uses the pack working directory.
- **Wrong candidate:** check the printed path/fingerprint. Both commands must name your candidate, not the checkpoint.
- **Manual exercise unfinished:** continue using the public pipeline checkpoint. No answer panel needs to be opened first.
- **R shows rounded numbers:** inspect the returned numeric value with `sprintf("%.12f", ...)`. Display precision and calculation precision differ.
- **Expected failure:** the prepared proposal should pass basic checks and fail precision. A nonzero exit is intentional for that demonstration.
- **All checks green:** inspect the diff and keep a stated limitation; don't infer universal correctness.
- **No AI:** the prepared proposal, complete worked solution and partner route support the full activity offline.
- **No working runtime:** pair with a working laptop. If none is available, compare the printed diff and expected/actual table, write your acceptance decision, then run the same commands later. Mark this honestly as reasoning without execution.

## Sources and further reading {#sources}

Established principles: [Fowler on refactoring](https://refactoring.com/), [Software Carpentry on functions and documentation](https://swcarpentry.github.io/python-novice-inflammation/08-func.html), [Python modules](https://docs.python.org/3/tutorial/modules.html), [Python automated testing](https://docs.python.org/3/library/unittest.html).

AI-specific operating guidance: [GitHub's responsible-use application card](https://docs.github.com/en/copilot/responsible-use/agents) recommends scoped tasks, review and testing, and acknowledges incorrect generated code. This lecture makes no quantitative productivity or model-reliability claim. The scoped-task/review approach also follows the course's existing responsible-AI guidance. External readings are optional; all exercises work offline.
