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
