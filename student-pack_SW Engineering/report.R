# Entry point: Rscript --vanilla report.R pipeline.R
source("runner.R")
source("validation.R")
args <- commandArgs(trailingOnly=TRUE)
if (length(args)!=1) stop("Usage: Rscript --vanilla report.R CANDIDATE.R")
code <- candidate(args[1])
result <- code$compare(code$extract(load_data()))
# Format only a display copy; the candidate result retains full precision.
shown <- result
shown$growth_pct <- sprintf("%.3f", result$growth_pct)
print(shown, row.names=FALSE)
