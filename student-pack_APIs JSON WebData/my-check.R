# Independent extra case. Run: Rscript --vanilla my-check.R repair.R
# Predict first: a missing baseline stays missing; growth must stop.
source("support.R")
args <- commandArgs(trailingOnly=TRUE)
candidate <- if(length(args)) args[1] else "repair.R"
source(candidate)
payload <- load_data()
CODE <- "DEU"; YEAR <- "2023" # Change to your independently chosen key.
for (i in seq_along(payload[[2]])) {
  r <- payload[[2]][[i]]
  if(r$countryiso3code==CODE && r$date==YEAR)
    payload[[2]][[i]]["value"] <- list(NULL) # Preserve field; do not delete it.
}
tab <- extract(payload)
check_source(tab,payload)
value <- tab$population[tab$country_code==CODE & tab$year==as.integer(YEAR)]
stopifnot(length(value)==1,is.na(value))
blocked <- tryCatch({compare(tab);FALSE},error=function(e) grepl("Missing population",conditionMessage(e),fixed=TRUE))
stopifnot(blocked)
cat("PASS extra case: missing baseline; candidate:",candidate,"\n")
