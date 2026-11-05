# INTENTIONALLY FLAWED teaching draft, not an actual AI transcript.
# Copy to repair.R. No instructor solution is imported.
extract <- function(payload) {
  rows <- lapply(payload[[2]],function(record) {
    value <- record$value
    if (is.null(value)) value <- 0
    data.frame(country_code=record$countryiso3code,country_name=record$country$value,
               year=as.integer(record$date),population=value)
  })
  tab <- do.call(rbind,rows)
  if (is.null(tab) || nrow(tab)==0) stop("No rows")
  tab
}
