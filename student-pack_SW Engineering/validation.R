# Supplied infrastructure. Run/source from the extracted practice folder. No network.
load_data <- function(name = "raw/population-2023-2024.json") {
  jsonlite::fromJSON(file.path("data", name), simplifyVector = FALSE)
}
country_names <- c(CHE="Switzerland", DEU="Germany", FRA="France")
expected_keys <- as.vector(outer(names(country_names), c(2023,2024), paste, sep="/"))
validate_envelope <- function(payload) {
  if (is.list(payload) && length(payload)>0 && "message" %in% names(payload[[1]]))
    stop("API application error: inspect message, even if HTTP was 200")
  if (!is.list(payload) || !is.null(names(payload)) || length(payload)!=2 || !is.list(payload[[1]]) || is.null(names(payload[[1]]))) stop("Expected metadata and records")
  meta <- payload[[1]]; records <- payload[[2]]
  if (is.null(records)) stop("No observations: records is null, not population zero")
  if (!is.list(records) || !is.null(names(records))) stop("Records must be an array")
  counts <- c("page","pages","total","per_page")
  if (!all(vapply(counts,function(k) is.integer(meta[[k]]) && length(meta[[k]])==1 && !is.na(meta[[k]]),logical(1))))
    stop("Metadata counts must be integers, not Boolean/string values")
  if (meta$per_page < length(records)) stop("Metadata page size is smaller than records received")
  if (!identical(meta$page,1L) || !identical(meta$pages,1L) || !identical(meta$total,6L) || length(records)!=6)
    stop("Incomplete coverage: need one complete page and six observations")
  for (record in records) {
    if (!is.list(record) || !all(c("country","countryiso3code","indicator","date","value") %in% names(record)))
      stop("Missing required field in record")
    if (!is.list(record$indicator) || !identical(record$indicator$id,"SP.POP.TOTL")) stop("Wrong indicator")
    code <- record$countryiso3code
    if (!is.character(code) || length(code)!=1 || !code %in% names(country_names)) stop("Unexpected country code")
    if (!is.list(record$country) || !identical(record$country$value,unname(country_names[code]))) stop("Country name/code mismatch")
    if (!is.character(record$date) || length(record$date)!=1 || !record$date %in% c("2023","2024")) stop("Unexpected year")
    value <- record$value
    if (!is.null(value) && (!is.numeric(value) || length(value)!=1 || !is.finite(value) || value<0))
      stop("Population must be a nonnegative finite number or null")
  }
  records
}
check_table <- function(tab) {
  if (!is.data.frame(tab) || !identical(names(tab),c("country_code","country_name","year","population"))) stop("Unexpected table columns")
  keys <- paste(tab$country_code,tab$year,sep="/")
  if (anyDuplicated(keys)) stop("Duplicate country-year key")
  if (nrow(tab)!=6 || !setequal(keys,expected_keys)) stop("Missing or unexpected country-year keys")
  if (!is.character(tab$country_name) || anyNA(tab$country_name)) stop("Country names must be strings")
  if (!is.numeric(tab$population) || any(is.nan(tab$population)) ||
      any(!is.finite(tab$population[!is.na(tab$population)])) || any(tab$population<0,na.rm=TRUE))
    stop("Population must be nonnegative finite numeric data or missing")
  tab <- tab[order(tab$country_code,tab$year),]; rownames(tab)<-NULL; tab
}
check_source <- function(tab, payload) {
  # Compare this table with this source, not hardcoded historical populations.
  records <- validate_envelope(payload); tab <- check_table(tab)
  source_keys <- vapply(records,function(r) paste(r$countryiso3code,r$date,sep="/"),character(1))
  if (anyDuplicated(source_keys) || !setequal(source_keys,expected_keys)) stop("Duplicate or missing source country-year key")
  for (i in seq_len(nrow(tab))) {
    record <- records[[match(paste(tab$country_code[i],tab$year[i],sep="/"),source_keys)]]
    if (!identical(tab$country_name[i],record$country$value)) stop("Source fidelity: country name/code mismatch")
    expected <- record$value; actual <- tab$population[i]
    agrees <- if (is.null(expected)) is.na(actual) else !is.na(actual) && actual==expected
    if (!agrees) stop("Source fidelity: population differs from its source record")
  }
  tab
}
