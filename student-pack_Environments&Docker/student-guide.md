# Week 10 · Environments & Docker
HEC Lausanne · 19 November 2026

## Preflight — distribute Tuesday, 17 November
Allow 15–25 minutes before class. Download student-pack.zip and extract it to a local folder. Open a terminal **inside student-pack**, where report.py and Dockerfile are visible. Do not work inside the ZIP preview. Keep the whole folder, including data and .dockerignore.

1. Install Python 3.14 from https://www.python.org/downloads/ if needed. Check `python3 --version` (macOS/Linux) or `py -3.14 --version` (Windows PowerShell).
2. Install Docker Desktop for your platform from https://docs.docker.com/desktop/ (Linux users may already have Docker Engine). Complete platform prerequisites and restart if prompted. **Start Docker before class and wait until its engine is ready.** `docker version` must show both Client and Server. Seeing only Client is insufficient.
3. Create the project environment and install the supplied requirements below. Initial downloads require internet.
4. Run `docker build -t dcm-w10 .` now, while online, then `docker run --rm dcm-w10`. This builds the actual dependency layer; pulling the Python image alone is insufficient. A first build may take several minutes. Do not add `--no-cache` during class.
5. Bring the extracted pack and a charged laptop. If blocked, arrange to pair or use supplied-output-analysis.md. We will not troubleshoot individual Docker installations during core lecture time.

## Local Python route
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
python report.py pipeline.py
python checks.py pipeline.py
python my-check.py pipeline.py
```
Windows PowerShell:
```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
python report.py pipeline.py
python checks.py pipeline.py
python my-check.py pipeline.py
```
The interpreter path must contain `.venv`. If activation is blocked, replace every subsequent `python` with `.venv/bin/python` (macOS/Linux) or `.\.venv\Scripts\python.exe` (PowerShell). This requires no execution-policy change. `deactivate` leaves an activated environment. Do not share .venv; recreate it from requirements.txt. Linux systems missing venv support need their distribution's Python venv component installed before class; pair if unavailable.

A fresh venv without the install step should report `ModuleNotFoundError: No module named 'pandas'`. If preflight already installed it, analyse that supplied error in Activity A; do not delete your environment.

## Build, run, verify — both platforms
Use the supplied complete Dockerfile for Activity C:
```bash
docker build -t dcm-w10 .
docker run --rm dcm-w10
docker run --rm dcm-w10 python checks.py pipeline.py
docker run --rm dcm-w10 python my-check.py pipeline.py
```
The dot is the current build context. `--rm` removes the finished container, not the image. These commands run Python inside a container; they do not use your local .venv. There is no host-folder mount. No Docker registry login/push is needed.

## Activity D — one-line repair
First execute the deliberately defective version:
```bash
docker build -f Dockerfile.broken -t dcm-w10-broken .
docker run --rm dcm-w10-broken
```
Expected: build succeeds; report raises FileNotFoundError for `/app/data/raw/population-2023-2024.json`. A build/network failure is a different problem.

In your editor, add `COPY data/ data/` immediately before CMD in Dockerfile.broken. Keep all Python and checks unchanged. Then:
```bash
docker build -f Dockerfile.broken -t dcm-w10-fixed .
docker run --rm dcm-w10-fixed
docker run --rm dcm-w10-fixed python checks.py pipeline.py
docker run --rm dcm-w10-fixed python my-check.py pipeline.py
```
Expected: report values in expected-report.txt, BASIC 14/14, PRECISION PASS. Compare with Dockerfile.reference if blocked. Dockerfile.starter is an optional one-line completion copy of the recipe; the supplied Dockerfile already works for C.

## Expected evidence
CHE: increase 116760, growth 1.314%; DEU: 229320, 0.275%; FRA: 179367, 0.262%. Six input observations → three country rows. All populations are persons. Growth is calculated unrounded, formatted to three decimals for display. The independent 300→400 case expects 100/3, not 33.333. Basic checks deliberately cannot establish full precision.

Record interpreter path for B, and the image tag plus actual report/basic/precision output for C/D. If paired, record who ran the commands. If using supplied output, label it analysis, not execution. The supplied expected-output file is a comparison aid, not a successful Docker run log.

## Browser activities and recovery
The three editable lecture cells execute **browser Python (Pyodide/WebAssembly), not local Python or Docker**. They require internet for initial runtime loading. Wait for the loading indicator before Run Code. Show Hint then Show Solution are available in the rounding exercise. Start Over resets code to its original state, including the deliberate rounding defect. Browser snapshot values: CHE 9005582, FRA 68551653. The independent 600→700 browser example expects 100/6. These exercises do not install local packages or create containers.

If browser Python does not initialize, use lecture08-static.html or lecture08-static.pdf supplied by the instructor. If Docker is unavailable, pair or complete supplied-output-analysis.md. Do not change report code or assertions, fetch live API data, or relax precision tolerances.

## Contents and provenance
pipeline.py, report.py, runner.py, validation.py, checks.py, my-check.py and all data/ files are byte copies from the Week 9 practice pack. See data/provenance.json and data/README.md. Requirements and Docker packaging are the Week 10 additions. No API requests occur in this report. The Python base image tag may change over time; this teaching recipe is not a fully immutable artifact.

Reference: [Python venv](https://docs.python.org/3/library/venv.html), [pip user guide](https://pip.pypa.io/en/stable/user_guide/), [Dockerfile instructions](https://docs.docker.com/build/concepts/dockerfile/).
