# Teaching adaptation of Week 8; correct report, tangled responsibilities.
source("validation.R")
payload <- load_data()
rows <- lapply(validate_envelope(payload), function(record) {
  data.frame(country_code=record$countryiso3code,
             country_name=record$country$value, year=as.integer(record$date),
             population=if (is.null(record$value)) NA_real_ else record$value)
})
table <- check_table(do.call(rbind, rows))
if (anyNA(table$population)) stop("Missing population: cannot compute complete growth comparison")
rows <- lapply(sort(unique(table$country_code)), function(code) {
  x <- table[table$country_code==code, ]
  previous <- x$population[x$year==2023]; current <- x$population[x$year==2024]
  if (previous<=0) stop("Baseline must be positive for percentage growth")
  data.frame(country_code=code, population_2023=previous, population_2024=current,
             increase=current-previous, growth_pct=100*(current-previous)/previous)
})
result <- do.call(rbind,rows)
shown <- result
shown$growth_pct <- sprintf("%.3f",result$growth_pct)
print(shown,row.names=FALSE)
