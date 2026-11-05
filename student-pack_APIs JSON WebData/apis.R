# Manual starter: source("apis.R") in R from the extracted practice folder.
source("support.R")
payload <- load_data(); metadata <- payload[[1]]; records <- payload[[2]]
manual_table <- function() {
  rows <- list()
  for (i in seq_along(records)) {
    record <- records[[i]]
    rows[[i]] <- data.frame(
      country_code=NA_character_,  # TODO: three-letter country code
      country_name=record$country$value,
      year=NA_integer_,            # TODO: date converted to integer
      population=NA_real_          # TODO: record value
    )
  }
  check_table(do.call(rbind,rows))
}
cat("OFFLINE snapshot:",length(records),"records. Complete three TODOs before manual_table().\n")
