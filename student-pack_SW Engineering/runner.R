# Isolated candidate environment; never sources pipeline/worked as a fallback.
candidate <- function(path) {
  path <- normalizePath(path, mustWork=TRUE)
  cat("Candidate:", path, "\nMD5:", unname(tools::md5sum(path)), "\n")
  env <- new.env(parent=globalenv())
  sys.source(path, envir=env, keep.source=TRUE)
  for (name in c("extract", "compare")) {
    if (!exists(name, envir=env, inherits=FALSE)) stop("Missing candidate function: ", name)
    fn <- get(name, envir=env, inherits=FALSE)
    ref <- attr(fn, "srcref")
    file <- if (is.null(ref)) "" else getSrcFilename(fn, full.names=TRUE)
    if (!is.function(fn) || length(file)!=1 || !nzchar(file) ||
        normalizePath(file, mustWork=TRUE)!=path)
      stop(name, " must be defined in the selected candidate")
  }
  env
}
