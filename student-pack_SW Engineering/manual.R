# Manual starter: move compare's display into the caller (two TODOs).
# Source from the extracted pack folder. No report runs on source.
source("validation.R")

# Return six sorted country-year rows. Null remains NA_real_; invalid envelopes
# and duplicate/missing keys stop. Source associations and input are preserved.
extract <- function(payload) {
  rows <- lapply(validate_envelope(payload), function(record) {
    data.frame(country_code=record$countryiso3code,
               country_name=record$country$value, year=as.integer(record$date),
               population=if (is.null(record$value)) NA_real_ else record$value)
  })
  check_table(do.call(rbind, rows))
}

# Initial behavior: print the formatted comparison; invisibly return that
# display table, whose growth column is character text.
# Target after TODOs: return one row per country in code order, with unrounded
# numeric growth (%); let the caller format and print.
# Input: six keyed rows from extract; populations in persons. Missing values
# or nonpositive 2023 baselines stop. Current-year zero is valid.
# Columns: country_code, population_2023, population_2024, increase, growth_pct.
# Both versions preserve input and use no file access or network.
# Only the target version does no printing.
compare <- function(table) {
  table <- check_table(table)
  if (anyNA(table$population))
    stop("Missing population: cannot compute complete growth comparison")
  rows <- lapply(sort(unique(table$country_code)), function(code) {
    country <- table[table$country_code == code, ]
    previous <- country$population[country$year == 2023]
    current <- country$population[country$year == 2024]
    if (previous <= 0) stop("Baseline must be positive for percentage growth")
    rate <- 100 * (current - previous) / previous
    data.frame(country_code=code, population_2023=previous,
               population_2024=current, increase=current-previous,
               growth_pct=rate)
  })
  result <- do.call(rbind, rows)
  rownames(result) <- NULL
  # TODO A: return result here; move the next three lines to the caller.
  shown <- result
  shown$growth_pct <- sprintf("%.3f", result$growth_pct)
  print(shown, row.names=FALSE)
}
