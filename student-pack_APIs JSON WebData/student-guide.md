---
title: "DCM · APIs, JSON & Web Data"
date: "Thursday, 5 November 2026"
lang: en
---

**Question:** how large were the populations of Switzerland, France and Germany in 2024, and how did they change from 2023? We need six country–year observations, in persons, for indicator `SP.POP.TOTL`.

The lecture demonstrations use Python; choose Python **or** R for your own work. Every required activity works offline. No API key, account or paid AI service is needed. A saved response is evidence for one version, not a promise that historical estimates never change. Population is not customer demand or a market-entry recommendation.

## Start here {#start}

Extract `student-pack.zip` into a new folder and open that folder in VS Code. Use that folder as your terminal working directory. Python needs pandas from Code Literacy I; everything else is standard library. R needs jsonlite and base R. Check your chosen route before class:

```bash
python3 -c "import json, urllib.request, pandas; print('Python ready')"
Rscript --vanilla -e 'library(jsonlite); cat("R ready\n")'
```

Only run the line for your language. If needed, install **before class** in the same environment selected in VS Code: `python3 -m pip install pandas` or, at the R prompt, `install.packages("jsonlite")`. Installation needs internet; the lesson does not. See [pandas installation](https://pandas.pydata.org/docs/getting_started/install.html) and [jsonlite on CRAN](https://cran.r-project.org/package=jsonlite). Re-run the preflight in your selected runtime. During class, pair with a working machine: one person predicts and reviews, one runs. Keep a note of what you ran and what you observed.

From the extracted folder:

```bash
python3 -i apis.py
```

Or start `R --vanilla`, then at its prompt:

```r
source("apis.R")
```

The starter loads a labeled OFFLINE snapshot and reports six records. It does not run the unfinished extraction. Shell commands belong in the terminal, not at Python's `>>>` or R's `>` prompt. Exit/restart after editing a Python file; source again or restart R after editing. `python` or `py` can replace `python3` if that is your normal launcher.

### Files in your pack

| File/folder | Purpose |
|---|---|
| `data/raw/` | Four genuine captured World Bank bodies; do not edit |
| `data/provenance.json`, `data/README.md` | Requests, hashes, definition, source, units, capture limitations |
| `data/constructed/` | Clearly labeled teaching modifications; not authentic measurements |
| `apis.py` / `.R` | Manual starter, three TODO fields |
| `support.py` / `.R` | Supplied validation and analysis infrastructure; read if useful |
| `checkpoint.py` / `.R` | Public complete checkpoint after your attempt or if blocked |
| `ai-draft.py` / `.R` | Intentionally flawed teaching draft, not an actual model transcript |
| `my-check.py` / `.R` | Runnable scaffold for your independently chosen extra case |
| `checks.py` / `.R` | Independent expected values and failure cases; keep unchanged |
| `fetch.py` / `fetch.R` | Optional explicit live retrieval; never runs automatically |

The pack includes everything you need: starters, a complete checkpoint, checks and worked answers. Try each activity before opening its answer.

## Request and source meaning {#request}

The single-line request used for the full approved snapshot is:

```text
https://api.worldbank.org/v2/country/che;fra;deu/indicator/SP.POP.TOTL?date=2023:2024&format=json&per_page=100
```

The path identifies countries and indicator; the query selects years, JSON and page size. One page is not always the whole result. For this small request, verify pages=1, total=6 and the exact six keys. A general client would follow all documented pages/cursors; we are not building one today. [World Bank request documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures).

The indicator means midyear resident population estimates, in persons, not GDP. The response's blank `unit` does not mean unitless. [Definition](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SP.POP.TOTL) and [World Bank WDI source/license (CC BY 4.0)](https://data.worldbank.org/indicator/SP.POP.TOTL). Underlying demographic sources include UN Population Division, national statistical offices and Eurostat. Attribution and capture details are retained with the data.

### A minimal live GET (optional; slides 13–15)

The URL chooses CHE/FRA/DEU, population (`SP.POP.TOTL`), years 2023–2024, JSON and a maximum of two records per page. [Open this request](https://api.worldbank.org/v2/country/che;fra;deu/indicator/SP.POP.TOTL?date=2023:2024&format=json&per_page=2). Live code requires internet; the archived route below works offline.

Copy **one** complete block into a new file in your extracted folder: `request-demo.R` or `request-demo.py`. Run `Rscript --vanilla request-demo.R` or `python3 request-demo.py` in the VS Code terminal. R needs only existing jsonlite; Python uses only its standard library. Stop after ten seconds if the service stalls; do not retry during class.

R — GET saves fresh bytes; jsonlite parses the saved response:

```{.r .live-example}
url <- paste0("https://api.worldbank.org/v2/country/che;fra;deu/indicator/",
              "SP.POP.TOTL?date=2023:2024&format=json&per_page=2")
options(timeout = 8)
snapshot <- tempfile(fileext = ".json")
download.file(url, snapshot, mode = "wb", quiet = TRUE)
partial <- jsonlite::fromJSON(snapshot, simplifyVector = FALSE)
length(partial[[2]])
```

Python — GET exposes HTTP status and body; save bytes, then parse JSON:

```{.python .live-example}
import json, tempfile, urllib.request
url = ("https://api.worldbank.org/v2/country/che;fra;deu/indicator/"
       "SP.POP.TOTL?date=2023:2024&format=json&per_page=2")
with urllib.request.urlopen(url, timeout=8) as response:
    print(response.status); raw = response.read()
with tempfile.TemporaryFile() as snapshot:
    snapshot.write(raw); snapshot.seek(0); partial = json.load(snapshot)
print(len(partial[1]))
```

For the captured behavior, R prints `[1] 2`; Python prints `200` then `2`. These are expected outcomes, not guarantees about future responses. `response.status` is the urllib equivalent of `response.status_code` in requests. The R downloader's return code is not an HTTP status. In a browser use **Network → reload → select the API request → Headers → Status Code**; the main page displays only the body. Check HTTP success, JSON syntax, application errors and usable observations separately.

Temporary files demonstrate the snapshot step; Python deletes its file at the end of the `with` block, and R uses its temporary directory. For a durable capture with URL/time/hash provenance use the existing fetchers below. Never replace `data/raw/` with a fresh response.

**Offline alternative:** in the extracted folder, Python: `from support import load; partial = load("raw/population-page1.json")`; R: `source("support.R"); partial <- load_data("raw/population-page1.json")`. These read the archived response without making a request. Inspect `partial[0]` / `partial[[1]]` for metadata and count `len(partial[1])` / `length(partial[[2]])`: two records, page 1 of 3, total 6. Increasing `per_page` to 100 changes page capacity, not the six matching country–year observations. For analysis use the full approved snapshot through the public checkpoint, since the partial response lacks four keys.

### Optional: retrieve a fresh response

Python:

```bash
python3 fetch.py
```

R:

```bash
Rscript --vanilla fetch.R
```

For optional R retrieval only, install `curl` (HTTP) and `openssl` (SHA-256) **before class**, alongside the existing `jsonlite`: `install.packages(c("curl", "openssl"))`. [curl documentation](https://jeroen.r-universe.dev/curl/doc/manual.html). These extra packages are not needed for the offline R activities. Run terminal commands from your extracted folder. If you already have an **R console open in VS Code**, use:

```text
source("fetch.R")
fetch_main(character())
```

Select the extracted folder as your working directory before the first line, or give `source()` the full path to `fetch.R`. Sourcing only defines helpers; the second line explicitly starts retrieval and returns to your console. `Rscript --vanilla fetch.R` belongs in a terminal, not at the R prompt. The script saves data beside itself, even if you later change your working directory.

One explicit attempt, a ten-second wall-clock deadline, no retries. It prints status/content type and retains response bytes and provenance in a **new** `data/live/` directory. It never overwrites approved raw snapshots. A failed or non-JSON response is not a usable population capture; inspect its manifest/body. If the request fails or times out, continue with the saved snapshot loaded by your starter. Skip this optional command when working offline. Both Python and R activities use the same saved data.

Success has layers: a network response, successful HTTP status, expected content type, valid JSON, expected application structure, required observations, then meaningful analysis. 4xx indicates a request/access problem, 429 rate limiting and 5xx a server problem; 200 still does not establish usable data. The supplied helper handles request failures; you do not need to write an exception handler.

## Read the JSON before extracting {#json}

The root array has two elements: metadata, then an array of records. Each record is an object with nested country and indicator objects. Names identify fields; position identifies array elements. JSON string `"2024"`, number `9005582`, `null`, absent key, empty string and Boolean `false` are different things.

Predict, then run in the Python starter:

```python
print(type(payload).__name__, len(payload))
record = payload[1][0]
print(record["country"]["value"])
print(record["countryiso3code"])
print(record["date"], record["value"])
```

R alternative:

```r
record <- payload[[2]][[1]]
print(record$country$value)
print(record$countryiso3code)
print(record$date)
print(record$value)
```

<details><summary>Check your prediction</summary>

Literal Python output (not display-formatted):

```text
list 2
Switzerland
CHE
2024 9005582
```

The year is a string even though `print` omits its quotation marks. First record in this snapshot: Switzerland, CHE, string `"2024"`, number 9005582. `country.value` is a name; `indicator.value` is a label; the record-level `value` is the population. Python starts at 0; R starts at 1. First-record inspection is not a robust way to identify a country for analysis: use code and year.

</details>

## Activity A — one row per country–year {#manual}

**6 minutes:** 1 minute predict; 3 minutes complete the three TODOs in `manual_table()` in your starter; 2 minutes restart, run and compare. The loop and country name are supplied. Set country code, integer year and population value. Work manually before AI.

Expected columns: `country_code`, `country_name`, `year`, `population`. One row is one country's population estimate for one year. Do not change raw records or reorder values separately from their keys.

After editing and restarting, run these commands in your **existing starter session**. They validate your actual manual table, not a replacement made by the checkpoint. Before editing, the starter should fail the key checks; that is intentional.

<!-- workflow:manual-python -->
```python
manual = manual_table()
print(check_table(manual))
print(check_source(manual, payload))
```

<!-- workflow:manual-r -->
```r
manual <- manual_table()
print(check_table(manual))
print(check_source(manual, payload))
```

`check_table` checks structure: columns, six unique keys and allowed value types. `check_source` checks fidelity: **every** country name and population must agree with the source record having that country code and year. Correct keys with all populations replaced by zero pass the structural checks but fail source fidelity. A zero or null genuinely present in the supplied input is valid when preserved. These checks provide evidence for this bounded task, not universal correctness.

<details><summary>Worked fields — reveal after attempting</summary>

Python fields: `record["countryiso3code"]`, `int(record["date"])`, `record["value"]`.
R fields: `record$countryiso3code`, `as.integer(record$date)`, `record$value`.

</details>

### Required transition — everyone uses the public checkpoint {#checkpoint}

**Do this even if your manual extraction worked and you did not open the answer.** Keep `manual` as your own result; the following imports/source statements supply names needed for Activity B. Run them at the language prompt, outside any optional answer.

<!-- workflow:checkpoint-python -->
```python
from checkpoint import extract
from support import load, compare, check_source
table = extract(payload)
print(compare(table))
```

<!-- workflow:checkpoint-r -->
```r
source("checkpoint.R")
table <- extract(payload)
print(compare(table))
```

If you restarted without the starter, first run `python3 -i apis.py`, or `source("apis.R")` in a fresh R session. Both define `payload`. The transition above is then required. The checkpoint is included in your pack so you can continue even if your manual task is unfinished.

### Checked comparison {#results}

| Country | 2023 persons | 2024 persons | Increase | Growth |
|---|---:|---:|---:|---:|
| CHE | 8,888,822 | 9,005,582 | 116,760 | 1.314% |
| DEU | 83,287,273 | 83,516,593 | 229,320 | 0.275% |
| FRA | 68,372,286 | 68,551,653 | 179,367 | 0.262% |

Growth (%) = (population_2024 - population_2023) / population_2023 × 100.

Switzerland: (9,005,582 - 8,888,822) / 8,888,822 × 100 ≈ **1.314%**. Independently calculate one country's difference and rate from its two raw records. Germany is largest and has the largest absolute increase; Switzerland has the largest proportional increase in this snapshot. Do not round inputs before computing. This does not establish purchasing power, market demand or causes of population change.

## Activity B — Should our pipeline accept these data? {#diagnose}

**Diagnosis only: keep code and data unchanged.** Choose one decision per case:

- **A · ACCEPT:** construct the table and calculate growth.
- **B · ACCEPT WITH MISSING VALUE:** retain the row, but block the complete growth calculation.
- **C · REJECT:** stop because the response is invalid or incomplete.

**2 minutes:** predict A, B or C for all six cases. **2 minutes:** inspect the supplied JSON in VS Code and run the checker in one language. **1 minute:** explain one surprising result. Response validation and table construction happen in `extract()`; calculation requirements are checked separately by `compare()`.

Open these files under `data/` in the extracted student pack:

| Case | File (relative to the extracted folder) | Your A/B/C prediction |
|---|---|---|
| Full response | [data/raw/population-2023-2024.json](data/raw/population-2023-2024.json) | |
| Partial page (`per_page=2`) | [data/raw/population-page1.json](data/raw/population-page1.json) | |
| Invalid indicator | [data/raw/invalid-indicator.json](data/raw/invalid-indicator.json) | |
| Unavailable year (2030) | [data/raw/unavailable-year.json](data/raw/unavailable-year.json) | |
| Absent `value` field — **synthetic** | [data/constructed/missing-value.json](data/constructed/missing-value.json) | |
| Explicit `value: null` — **synthetic** | [data/constructed/null-value.json](data/constructed/null-value.json) | |

The first four are genuine archived World Bank responses. The two constructed examples deliberately alter CHE/2024 in the full capture and are not observations about Switzerland.

From the extracted folder, run **one** command in the VS Code terminal:

Python:

```bash
python3 checks.py checkpoint.py
```

R:

```bash
Rscript --vanilla checks.R checkpoint.R
```

Expect **12/12 passing checks**, including checks that invalid inputs are rejected. **PASS for a rejection test means the pipeline correctly stopped on the problematic response.** It does not mean the response was accepted. The suite also checks associations and other cases beyond these six. Passing selected tests supplies evidence, not a universal guarantee. Keep your predictions, compare with results, then open the solution below.

<details><summary>Activity B solution — decisions, reasons and optional inspection code</summary>

| Case | Decision | Response/table validation (`extract`) | Growth (`compare`) |
|---|---|---|---|
| Full response | **A** | Accept six country–year observations | Calculate growth |
| Partial page | **C** | Reject incomplete coverage: page 1 of 3, only two observations | Do not calculate |
| Invalid indicator | **C** | Reject the application-level error | Do not calculate |
| Unavailable 2030 | **C** | Reject: no observations available; this is not population zero | Do not calculate |
| Synthetic absent `value` | **C** | Reject: a required field is absent | Do not calculate |
| Synthetic explicit `value: null` | **B** | Keep all six rows, including CHE/2024 with missing population | Reject the complete growth calculation |

**Absent field ≠ explicit null ≠ numerical zero.** The Python table stores this missing numeric population as `NaN`; R uses `NA`. Numerical zero stays a number; it must not be invented to fill missing data. A zero baseline separately makes percentage growth undefined. An empty string is neither null nor zero.

In R, accessing an absent field and explicit JSON null can both return `NULL`. Check `"value" %in% names(record)` **before** interpreting `record$value`; the supplied helper already does this.

Optional inspection in your existing public-checkpoint session (not required to run the terminal checker):

Inspect the genuine partial capture:

<!-- workflow:diagnosis-python -->
```python
partial = load("raw/population-page1.json")
print(partial[0])
print([r["countryiso3code"] for r in partial[1]])
```

<!-- workflow:diagnosis-r -->
```r
partial <- load_data("raw/population-page1.json")
print(partial[[1]])
print(vapply(partial[[2]], function(r) r$countryiso3code, character(1)))
```

### Check null without turning it into zero

<!-- workflow:null-python -->
```python
missing_table = extract(load("constructed/null-value.json"))
print(missing_table.loc[(missing_table.country_code == "CHE") &
                        (missing_table.year == 2024), "population"].isna().all())
```

<!-- workflow:null-r -->
```r
missing_table <- extract(load_data("constructed/null-value.json"))
selected <- missing_table$country_code=="CHE" & missing_table$year==2024
print(is.na(missing_table$population[selected]))
```

Python prints `True`; R prints `[1] TRUE`. Python dataframe represents this missing numeric value as NaN; R uses NA_real_. In R, check `"value" %in% names(record)` **before** interpreting `record$value`: an absent field and explicit JSON null can both produce NULL when accessed. Our helper checks presence separately. Calling `compare(missing_table)` must stop with a useful missing-population error.

</details>

Now that we know how the pipeline should behave, can we detect and repair code that violates these expectations? **Activity C starts the repair work.**

## Activity C — discover, repair and independently verify {#ai}

Activity B defined correct behavior. Now test plausible code against those expectations before asking for a repair. **14 minutes total: 4 minutes discovery, then 10 minutes repair/verification.** Choose Python or R throughout.

### Part 1 — It runs. But does it work? (4 minutes)

**1 minute — explain first:** open `ai-draft.py` or `ai-draft.R` in VS Code. Give the assistant the complete draft and matching `support` file, with this prompt:

> Explain what extract(payload) does: its input, output and assumptions. Do not rewrite or repair it yet.

The draft is **deliberately flawed teaching code of a kind an AI assistant might propose, not an actual AI transcript**. No AI? Ask your partner to trace its input, output and assumptions. If the assistant stalls, use partner explanation immediately.

**1 minute — try the original data:** open a terminal in the extracted student folder. Start **one** interactive session: `python3` or `R --vanilla`. Paste the corresponding block at its prompt (not in the shell):

Python interactive session:

```python
from runpy import run_path
from support import load, compare
extract = run_path("ai-draft.py")["extract"]
payload = load()
tab = extract(payload)
print(compare(tab))
```

R interactive session:

```r
source("support.R")
source("ai-draft.R")
payload <- load_data()
tab <- extract(payload)
print(compare(tab))
```

These blocks explicitly load the draft, replacing any earlier checkpoint `extract`. Expect the same plausible six-observation comparison as before: growth about CHE 1.314%, DEU 0.275%, FRA 0.262%. In Python, `run_path` loads the hyphenated filename and retrieves its `extract` function.

**2 minutes — challenge it:** open a **separate VS Code terminal** in the same extracted folder (Terminal → New Terminal). Run one shell command:

```bash
python3 checks.py ai-draft.py
```

Or:

```bash
Rscript --vanilla checks.R ai-draft.R
```

**Expected: 8 of 12 checks fail; exit status 1.** This failure is intentional. Read one failing case and connect it to Activity B. Keep the output for comparison later. Ask: **“The function works on our original data. Why shouldn't we trust it?”** Neither a convincing explanation nor a normal-data result establishes correct behavior on other inputs. Do not repair yet.

### Part 2 — Can AI repair it? (10 minutes)

**1 minute copy/predict · 2 minutes propose · 2 minutes inspect · 4 minutes test · 1 minute decide.**

1. In VS Code Explorer, right-click `ai-draft.py` → **Copy**, right-click the folder → **Paste**, then rename the copy `repair.py`. For R use `ai-draft.R` → `repair.R`. Keep both in the extracted folder. Open the copy, not the original.
2. Use Activity B's solution matrix to state the required behavior: preserve country–year/name/value associations; retain explicit null as missing; reject incomplete coverage, malformed responses, missing required fields and application errors. Do not modify raw data, supplied checks or expected outcomes.
3. Open `my-check.py` or `my-check.R`. Before asking AI, independently choose another baseline key (e.g. FRA/2023), change `CODE` and write your prediction in a comment. Or design another case by editing the mutation/assertions. Never alter raw data. The supplied null case covers CHE/2024; a different baseline case tests missingness in the denominator and another country. Explain that extra coverage; an unchanged scaffold is not your own design.

### Bounded prompt and exact context

Give the assistant the **complete contents of your `repair.py` and `support.py`**, or **`repair.R` and `support.R`**, plus the prompt below and the revealed Activity B solution table. Also provide `data/constructed/null-value.json` as the public sample. These are all in the pack. Keep `checks` and your predicted extra case independent; do not ask the assistant to rewrite them. No private data or credentials.

> Repair only extract(payload) and necessary imports/source statements. Use the supplied support helpers unchanged. Preserve the four columns, country–year/name/value associations and explicit null as missing. Require the specified indicator and six unique country–year keys. Reject incomplete or malformed responses, absent required fields and application errors. Do not change data, checks, expected outcomes, dependencies or helper code. Return the complete repair file and explain each change; I will test it independently.

Permitted setup: Python may keep `import pandas as pd` and import `validate_envelope, check_table` from `support`; R may `source("support.R")`. Keep the existing signature. No network, input mutation or hidden solution imports. The complete growth calculation must still reject missing inputs.

Paste the proposed complete file into `repair.py` / `.R`, then save. To compare in VS Code Explorer: right-click `ai-draft.py` → **Select for Compare**; right-click `repair.py` → **Compare with Selected** (equivalent R files). Read the additions/removals side by side. Explain the validation call, missing-value treatment and final table check **before running**. If AI proposes changes elsewhere, reject that scope expansion. A second AI's agreement is not independent evidence.

### Run the existing and your additional checks

Exact terminal commands, from the extracted folder:

```bash
python3 checks.py repair.py
python3 my-check.py repair.py
```

Or:

```bash
Rscript --vanilla checks.R repair.R
Rscript --vanilla my-check.R repair.R
```

Both launch fresh processes and print the candidate name. The supplied suite must pass 12/12 as necessary evidence for this task; your separate scaffold should print `PASS extra case: missing baseline`. A failed assertion/error is evidence to investigate, not a reason to weaken the expectation. The scaffold needs only the candidate file and public support/data; no additional solution file or interactive state. Decide whether your case extends coverage: name the new country/year/edge and the plausible error it catches. Repeating the supplied case adds little evidence. Passing these cases is not a proof for all possible responses.

### Complete partner-review fallback (same 10 minutes)

During discovery, partners explain and run the draft before repairing. During the ten-minute repair phase, one partner predicts and edits the extra-case scaffold; the other proposes the repair. Read `support` and the draft together. Replace the unchecked record iteration with `validate_envelope(payload)`, preserve each original value (R converts only explicit NULL to NA_real_), and return `check_table` of the rows. Add the permitted import/source statement. If blocked after the two-minute repair attempt, open the worked repair below and copy it into the repair file. Still perform the VS Code comparison, explain each change, and run **both** check commands. Swap roles for interpreting failures. Record the same acceptance note; state that this was partner review, not AI use. This fallback is entirely offline.

<details><summary>Worked repair — reveal after inspecting and testing</summary>

Python (`repair.py` can contain this complete version):

```python
"""Worked repair: only extract and its necessary imports."""
import pandas as pd
from support import validate_envelope, check_table


def extract(payload):
    records = validate_envelope(payload)
    rows = []
    for record in records:
        rows.append({
            "country_code": record["countryiso3code"],
            "country_name": record["country"]["value"],
            "year": int(record["date"]),
            "population": record["value"],
        })
    return check_table(pd.DataFrame(rows))


```

R (`repair.R`):

```r
# Public complete checkpoint: source from practice folder, then extract(load_data()).
source("support.R")
extract <- function(payload) {
  records <- validate_envelope(payload)
  rows <- lapply(records, function(record) {
    value <- record$value
    if (is.null(value)) value <- NA_real_
    data.frame(country_code=record$countryiso3code,
               country_name=record$country$value,
               year=as.integer(record$date), population=value)
  })
  check_table(do.call(rbind, rows))
}
```

</details>

### Decision note

Save four sentences: my prediction; input/check and observed outcome; changed line and why it matters; accept/reject plus remaining limits. Mention whether/how AI helped. Passing selected checks is evidence for this contract, not universal robustness.

## Transfer: an unfamiliar response {#transfer}

Open `data/constructed/stock.json`. It is an invented warehouse response with `items` and `next_cursor`, not a real API capture. Give a path to A's available stock, one completeness check and a conclusion you cannot make yet.

<details><summary>Reasoning</summary>

Python path: `stock["items"][0]["stock"]["available"]`; R: `stock$items[[1]]$stock$available`. A has numeric zero; B has explicit null; C lacks the field. A non-null next_cursor says more records remain. Need documentation and remaining pages plus a missingness policy before claiming complete total stock. Do not assume World Bank's two-element envelope applies here.

</details>

## Reproducible handover — guided follow-up {#handover}

Preserve raw JSON plus request URL/parameters, source/indicator/unit definition, capture UTC/date, provider update and a content hash. Observation year, retrieval time and update date differ. Keep constructed examples and new live captures separately labeled. Save analysis and checks; rerun from a fresh terminal using the printed commands. A checksum identifies bytes, not statistical correctness.

After class, close your interactive session and run from a fresh terminal:

```bash
python3 checkpoint.py
python3 checks.py repair.py
python3 my-check.py repair.py
```

R alternative:

```bash
Rscript --vanilla -e 'source("checkpoint.R"); print(compare(extract(load_data())))'
Rscript --vanilla checks.R repair.R
Rscript --vanilla my-check.R repair.R
```

Expect the same three-country comparison, 12/12 checks and the additional-case PASS. Include raw snapshots, provenance, your repair, extra case and decision note in a handover. Use this fresh-session check to confirm that a colleague can reproduce your result.

**Bounded validator:** these helpers cover one complete six-record World Bank response for this indicator and these keys. They require integer metadata counts (not Boolean/string substitutes), page size consistent with the record count, the expected nested country/indicator fields, and finite nonnegative numeric values or null. R requires unnamed lists for JSON arrays and named objects. Extra provider fields are allowed. This is not general pagination, a universal JSON validator or a check of the provider's statistical estimates. A different API needs its own documented contract.

Request narrowly and reuse cached data while debugging. Respect provider terms and limits; avoid tight retries. If another API requires credentials, keep them out of code, Git and AI prompts. This exercise needs none. Next lecture: make these steps readable, reusable, documented and testable.

## Troubleshooting {#troubleshooting}

- **File not found in R:** open the extracted folder and set it as terminal working directory. R examples use relative paths deliberately.
- **Module/package missing:** preflight pandas/jsonlite in your chosen runtime; pair rather than install during the timed task.
- **Manual starter rejects keys:** replace all three TODO fields, save, restart. Its initial failure is deliberate.
- **Draft checker fails:** expected. Test `checkpoint` to check the environment; then repair your copy.
- **Null drops an R row:** NULL has length zero; preserve its key and convert the value to NA_real_ after checking the field exists.
- **Live timeout/HTML/error:** stop; inspect the returned status/body if saved, and explicitly use OFFLINE data. Do not overwrite raw.
- **Values change in a new live capture:** retain both versions and their provenance; investigate revisions. The approved exercise uses the fixed snapshot.
- **A passing test feels weak:** ask which plausible mistake it would catch. Check exact keys, source associations, one hand calculation and edge cases, not just nonempty output.

[Back to start](#start) · [Manual task](#manual) · [Diagnosis](#diagnose) · [AI task](#ai)


## Optional extension — OMDb documentation challenge {#omdb}

**8 minutes, after the core lecture or as follow-up.** Use [the actual OMDb website](https://www.omdbapi.com/) (Usage and Parameters), not an AI-generated description. Task: design a GET request for *Inception* (2010) as JSON. Choose Python or R. No account is needed to design the request; an activated personal API key is needed for a live call. [Key registration](https://www.omdbapi.com/apikey.aspx) currently offers a free 1,000-request/day tier and uses email; delivery may be delayed. Do not wait for registration during the task.

1. **3 min:** identify the endpoint, key parameter, single-title versus search parameter, year, movie type and response format.
2. **2 min:** write a URL with `YOUR_KEY` and translate the slide 13 request pattern into your chosen language. Do not put a real key in your submission.
3. **2 min:** predict at least three checks: requested title/year/type, HTTP/JSON success, and how an application error should stop analysis. Explain why a successful request could still return the wrong movie.
4. **1 min:** partner review. Deliver code/request design, predictions and one limitation. Live execution is optional.

**If the website is unavailable:** this instructor summary of its documentation is sufficient for the design task: endpoint `https://www.omdbapi.com/`; `apikey` supplies access; `t` looks up one title while `s` searches; `y` selects a year; `type=movie` narrows the type; `r=json` requests JSON. Parameters and key page checked 4 November 2026. Use the real site when available to establish where each choice is documented.

<details><summary>OMDb hints and worked request — reveal after your attempt</summary>

A suitable request design is `https://www.omdbapi.com/?apikey=YOUR_KEY&t=Inception&y=2010&type=movie&r=json`. The placeholder is not an activated key. An `s` search requires handling a result list and choosing the right item; it is not the same as `t` lookup. Use HTTPS even though the Usage example shows HTTP. [Official API schema](https://www.omdbapi.com/swagger.json) also lists HTTPS and key authentication.

For optional live execution, first set `OMDB_API_KEY` privately in your local environment (VS Code terminal environment settings or your normal OS environment editor), then open a new terminal. Never commit the key, project it or paste it into AI. Copy one block to `omdb-request.py` or `omdb-request.R` and run `python3 omdb-request.py` or `Rscript --vanilla omdb-request.R`. These blocks stop before making a request if no key is set. One attempt only; stop after ten seconds if needed. No new packages beyond jsonlite for R.

Python:

```{.python .omdb-live-example}
import os, json
from urllib.parse import urlencode
from urllib.request import urlopen
key = os.environ.get("OMDB_API_KEY")
if not key:
    raise ValueError("Set OMDB_API_KEY privately, or use the design-only route")
params = {"apikey": key, "t": "Inception", "y": "2010",
          "type": "movie", "r": "json"}
with urlopen("https://www.omdbapi.com/?" + urlencode(params), timeout=8) as response:
    print("HTTP", response.status)
    movie = json.load(response)
if movie.get("Response") != "True":
    raise ValueError("OMDb did not return a successful movie result")
assert (movie.get("Title"), movie.get("Year"), movie.get("Type")) == ("Inception", "2010", "movie")
print(movie["Title"], movie["Year"])
```

R:

```{.r .omdb-live-example}
key <- Sys.getenv("OMDB_API_KEY")
if (!nzchar(key)) stop("Set OMDB_API_KEY privately, or use the design-only route")
params <- c(apikey=key, t="Inception", y="2010", type="movie", r="json")
query <- paste(names(params), vapply(params, utils::URLencode, character(1), reserved=TRUE),
               sep="=", collapse="&")
url <- paste0("https://www.omdbapi.com/?", query)
snapshot <- tempfile(fileext=".json")
options(timeout=8)
download.file(url, snapshot, mode="wb", quiet=TRUE)
movie <- jsonlite::fromJSON(snapshot, simplifyVector=FALSE)
if (!identical(movie$Response, "True")) stop("OMDb did not return a successful movie result")
stopifnot(identical(movie$Title, "Inception"), identical(movie$Year, "2010"),
          identical(movie$Type, "movie"))
cat(movie$Title, movie$Year, "\n")
```

The R downloader's return code is not the HTTP status: use the browser Network panel if you need to demonstrate it. These are small worked requests, not general API clients. Authentication/HTTP/JSON errors must stop interpretation. A provider error may appear in the JSON body; do not treat an error envelope as film data. Film fields such as runtime and ratings require type/unit/missingness checks before analysis. No real OMDb film response is included in this pack; offline author tests use clearly identified synthetic transport bodies, and authenticated live behavior has not been verified because no key was supplied. For a durable live analysis, preserve response bytes and provenance separately, never replacing the World Bank snapshots.

</details>
