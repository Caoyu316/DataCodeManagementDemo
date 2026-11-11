# CONSTRUCTED teaching proposal; review before accepting. Source from the extracted pack folder. No report runs here.
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

# Unrounded percentage change for validated finite numeric scalars.
# Preconditions: previous > 0, current >= 0; caller validates these.
# No I/O or mutation. Example: growth_percent(100, 110) returns 10.
growth_percent <- function(previous, current) {
  round(100 * (current - previous) / previous, 3)
}


# Return one row per country in code order, with unrounded growth (%).
# Input: six keyed rows from extract; populations in persons. Missing values
# or nonpositive 2023 baselines stop. Current-year zero is valid.
# Columns: country_code, population_2023, population_2024, increase, growth_pct.
# Preserve input; no printing, file access or network.
compare <- function(table) {
  table <- check_table(table)
  if (anyNA(table$population))
    stop("Missing population: cannot compute complete growth comparison")
  rows <- lapply(sort(unique(table$country_code)), function(code) {
    country <- table[table$country_code == code, ]
    previous <- country$population[country$year == 2023]
    current <- country$population[country$year == 2024]
    if (previous <= 0) stop("Baseline must be positive for percentage growth")
    rate <- growth_percent(previous, current)
    data.frame(country_code=code, population_2023=previous,
               population_2024=current, increase=current-previous,
               growth_pct=rate)
  })
  result <- do.call(rbind, rows)
  rownames(result) <- NULL
  result
}
