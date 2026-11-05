# Optional live retrieval. Sourcing defines functions; it never downloads data.
# Terminal: Rscript --vanilla fetch.R
# RStudio console: source("fetch.R"); fetch_main(character())
# Optional live-only dependencies: curl (HTTP), openssl (SHA-256); jsonlite.
# Remember our location when sourced, instead of depending on the console's cwd.
.fetch_file <- local({
  source_files <- lapply(sys.frames(), function(frame) frame$ofile)
  source_files <- Filter(function(file) is.character(file) && length(file)==1 &&
                           basename(file)=="fetch.R", source_files)
  cli_file <- grep("^--file=", commandArgs(), value=TRUE)
  file <- if (length(source_files)) tail(source_files,1)[[1]] else if (length(cli_file))
    gsub("~+~", " ", sub("^--file=", "", cli_file[1]), fixed=TRUE) else "fetch.R"
  normalizePath(file, winslash="/", mustWork=TRUE)
})
.fetch_dir <- dirname(.fetch_file)
source(file.path(.fetch_dir, "support.R"))

URL <- paste0("https://api.worldbank.org/v2/country/che;fra;deu/indicator/",
              "SP.POP.TOTL?date=2023:2024&format=json&per_page=100")

fetch_transport <- function(url) {
  handle <- curl::new_handle(timeout = 8, connecttimeout = 8,
                            followlocation = TRUE, maxredirs = 5,
                            useragent = "DCM-teaching-demo/2026")
  curl::handle_setheaders(handle, Accept = "application/json")
  # curl_fetch_memory retains non-2xx bodies instead of treating them as data.
  response <- curl::curl_fetch_memory(url, handle = handle)
  list(content = response$content, status = response$status_code,
       content_type = response$type, final_url = response$url)
}

fetch_once <- function(url, destination, transport = fetch_transport) {
  if (!dir.exists(destination)) stop("Destination directory must exist")
  body_file <- file.path(destination, "response.json")
  manifest_file <- file.path(destination, "provenance.json")
  if (file.exists(body_file) || file.exists(manifest_file))
    stop("Refusing to overwrite a previous response")
  response <- transport(url)
  writeBin(response$content, body_file) # Preserve the exact response bytes.
  content_type <- if (is.null(response$content_type)) "" else response$content_type
  manifest <- list(kind = "optional fresh response, not approved snapshot",
                   request_url = url, final_url = response$final_url,
                   retrieved_utc = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
                   status = response$status, content_type = content_type,
                   sha256 = unclass(as.character(openssl::sha256(response$content))))
  jsonlite::write_json(manifest, manifest_file, auto_unbox = TRUE, pretty = TRUE)
  cat("LIVE", response$status, content_type, "saved to", destination, "\n")
  if (response$status < 200 || response$status >= 300)
    stop("HTTP failure: inspect retained response; use approved snapshot for class")
  if (!grepl("application/json", content_type, ignore.case = TRUE, fixed = FALSE))
    stop("Unexpected content type; retained response is not labeled usable JSON")
  payload <- jsonlite::fromJSON(rawToChar(response$content), simplifyVector = FALSE)
  validate_envelope(payload)
  cat("Envelope checked. Compare source values and keys before accepting a revised snapshot.\n")
  invisible(payload)
}

fetch_main <- function(args = character()) {
  if (identical(args, "--help")) {
    cat("Rscript --vanilla fetch.R [--url URL]\nOne attempt; 10-second worker deadline; no retries.\n")
    return(0L)
  }
  if (length(args) && (length(args) %% 2 != 0 || any(!args[seq(1, length(args), by = 2)] %in% c("--url", "--worker")))) {
    if (length(args)) stop("Use --url URL, or --help")
  }
  option <- function(name, default = NULL) {
    i <- match(name, args)
    if (is.na(i)) default else args[i + 1L]
  }
  for (package in c("jsonlite", "curl", "openssl")) {
    if (!requireNamespace(package, quietly = TRUE))
      stop("Install before live retrieval: install.packages(c('jsonlite', 'curl', 'openssl'))")
  }
  url <- option("--url", URL)
  worker <- option("--worker")
  if (!is.null(worker)) {
    fetch_once(url, worker)
    return(0L)
  }
  root <- file.path(.fetch_dir, "data", "live")
  dir.create(root, recursive = TRUE, showWarnings = FALSE)
  destination <- tempfile(paste0(format(Sys.time(), "%Y%m%dT%H%M%SZ-", tz = "UTC")), tmpdir = root)
  if (!dir.create(destination)) stop("Could not create unique live directory")
  script <- .fetch_file
  status <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript"),
    c("--vanilla", shQuote(script), "--worker", shQuote(destination), "--url", shQuote(url)),
    timeout = 10))
  if (status == 124L)
    cat("LIVE TIMEOUT after 10 seconds. Explicitly load the approved OFFLINE snapshot; no retry.\n")
  as.integer(status)
}

# A console or RStudio Run All must never quit the user's R session.
# Source the file, then explicitly call fetch_main(character()) to retrieve data.
if (!interactive() && sys.nframe() == 0L) {
  status <- tryCatch({
    fetch_main(commandArgs(trailingOnly = TRUE))
  }, error = function(error) {
    cat("LIVE FAILED:", conditionMessage(error), "\n")
    1L
  })
  quit(status = status)
}
