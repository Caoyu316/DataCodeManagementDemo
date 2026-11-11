# Independent precision check. Choose a new case BEFORE asking AI.
# Constructed data, not World Bank estimates. Modify only the next four values.
source("runner.R")
source("validation.R")
CODE <- "CHE"
PREVIOUS <- 300
CURRENT <- 400
EXPECTED_PERCENT <- 100 / 3  # increase is one third of baseline
# Alternative: DEU, 600 -> 700, expected 100/6. Write your reasoning.
args<-commandArgs(trailingOnly=TRUE)
if (length(args)!=1) stop("Usage: Rscript --vanilla my-check.R CANDIDATE.R")
code<-candidate(args[1])
table<-code$extract(load_data())
table$population[table$country_code==CODE & table$year==2023]<-PREVIOUS
table$population[table$country_code==CODE & table$year==2024]<-CURRENT
result<-code$compare(table) # actual candidate, including its helper
actual<-result$growth_pct[result$country_code==CODE]
cat(sprintf("PRECISION %s: expected %.12f; actual %.12f\n",CODE,EXPECTED_PERCENT,actual))
if (length(actual)!=1 || !is.finite(actual) || abs(actual-EXPECTED_PERCENT)>1e-9)
  stop("Full-precision contract violated; do not relax the tolerance")
cat("PRECISION PASS (absolute tolerance 1e-9 percentage points)\n")
