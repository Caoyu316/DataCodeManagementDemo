# Population report — Week 9 offline project

Open this extracted folder in VS Code. Choose Python (pandas plus standard library) or R (jsonlite plus base R). Install dependencies before class using your existing Week 8 environment. No network/API key/Quarto required to run the project.

Read student-guide.html for exact tasks, prompt, fallbacks and worked answers. Run all commands from this folder, in fresh processes.

## Complete checkpoint

Python: `python3 report.py pipeline.py`, `python3 checks.py pipeline.py`, `python3 my-check.py pipeline.py`.

R: `Rscript --vanilla report.R pipeline.R`, `Rscript --vanilla checks.R pipeline.R`, `Rscript --vanilla my-check.R pipeline.R`.

## Refactor

Copy pipeline to candidate in your chosen language. Extract growth_percent(previous,current) and call it from compare. Only edit candidate. Preserve extract/compare signatures, source associations, error policies, output columns/order, full numeric precision and input objects. Do not change checks, data, validation, report or dependencies. Internal helper preconditions: validated finite numeric scalars, previous>0 and current>=0. It returns percentage change, with no I/O or rounding. Caller retains validation.

compare returns country_code, population_2023, population_2024, increase, growth_pct, in CHE/DEU/FRA order. extract returns country_code, country_name, year, population sorted by code/year. Scope: CHE/DEU/FRA, 2023–2024, SP.POP.TOTL. Null remains missing in extraction and prevents comparison; zero current year allowed; zero baseline rejected.

Run checks and my-check on candidate, not on an unchanged checkpoint. Basic suite is deliberately insufficient: the constructed proposal passes 14/14 but fails precision. Your independently chosen test should distinguish these implementations. Complete worked files are openly supplied and only run when explicitly selected. Use them if blocked, with disclosure.

## Final handover

Explicit final reference: substitute worked.py / worked.R in the three checkpoint commands. To hand over your own result, include candidate plus your independent check and evidence/review-template.txt, and name candidate in all three commands. Expect 14 basic passes and PRECISION PASS. A report has three countries; CHE increase 116760, displayed growth 1.314%. These checks do not prove every possible input or scientific inference.

Raw snapshots and provenance come unchanged from Week 8 (World Bank WDI). Constructed inputs are separate and labeled. Never overwrite raw. Environments/Docker are next week's topic.
