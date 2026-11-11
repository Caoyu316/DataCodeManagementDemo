# BASIC checks intentionally assess display precision, not calculation precision.
source("runner.R")
source("validation.R")
require_true <- function(condition, message) {
  if (!isTRUE(condition)) stop(message)
}
verify_source <- function(table,payload) {
  keys <- paste(table$country_code,table$year,sep="/")
  require_true(identical(names(table),c("country_code","country_name","year","population")),"Extraction columns")
  require_true(identical(keys,sort(expected_keys)),"Six sorted keys")
  source_keys <- vapply(payload[[2]],function(r) paste(r$countryiso3code,r$date,sep="/"),character(1))
  for (i in seq_len(nrow(table))) {
    r <- payload[[2]][[match(keys[i],source_keys)]]
    require_true(table$country_name[i]==r$country$value && r$country$value==country_names[r$countryiso3code],"Name association")
    require_true(if (is.null(r$value)) is.na(table$population[i]) else table$population[i]==r$value,"Source fidelity")
  }
}
run_checks <- function(code) {
  results <- list()
  check <- function(name,fn) {
    reason <- tryCatch({fn(); ""},error=function(e) conditionMessage(e))
    results[[length(results)+1L]] <<- list(name=name,ok=!nzchar(reason),reason=reason)
  }
  output <- function() {
    payload<-load_data();table<-code$extract(payload);verify_source(table,payload)
    require_true(identical(as.numeric(table$population),c(8888822,9005582,83287273,83516593,68372286,68551653)),"Snapshot values")
    result<-code$compare(table)
    require_true(identical(names(result),c("country_code","population_2023","population_2024","increase","growth_pct")),"Comparison columns")
    require_true(identical(result$country_code,c("CHE","DEU","FRA")),"Comparison order")
    require_true(all(result$population_2023==c(8888822,83287273,68372286)) && all(result$population_2024==c(9005582,83516593,68551653)),"Comparison source association")
    require_true(all(result$increase==c(116760,229320,179367)),"Increase")
    require_true(identical(sprintf("%.3f",result$growth_pct),c("1.314","0.275","0.262")),"Displayed growth only")
  }
  simple <- function() {
    table<-code$extract(load_data())
    table$population[table$country_code=="CHE" & table$year==2023]<-100
    table$population[table$country_code=="CHE" & table$year==2024]<-110
    result<-code$compare(table)
    require_true(result$growth_pct[result$country_code=="CHE"]==10,"100 -> 110 = 10%")
  }
  rejects <- function(file,reason) {
    message<-tryCatch({code$extract(load_data(file));""},error=function(e) conditionMessage(e))
    require_true(nzchar(message) && grepl(reason,message,fixed=TRUE),paste("Expected rejection:",reason))
  }
  null <- function() {
    payload<-load_data("constructed/null-value.json");table<-code$extract(payload);verify_source(table,payload)
    message<-tryCatch({code$compare(table);""},error=function(e) conditionMessage(e))
    require_true(grepl("Missing population",message,fixed=TRUE),"Missing must block comparison")
  }
  zero <- function() {
    payload<-load_data("constructed/zero-value.json");table<-code$extract(payload);verify_source(table,payload)
    result<-code$compare(table)
    require_true(result$growth_pct[result$country_code=="CHE"]==-100,"Zero current year gives -100%")
  }
  baseline <- function() {
    table<-code$extract(load_data());table$population[table$country_code=="CHE" & table$year==2023]<-0
    message<-tryCatch({code$compare(table);""},error=function(e) conditionMessage(e))
    require_true(grepl("Baseline",message,fixed=TRUE),"Zero baseline must fail")
  }
  shuffle <- function() {
    payload<-load_data();payload[[2]]<-rev(payload[[2]]);saved<-serialize(payload,NULL)
    table<-code$extract(payload);verify_source(table,payload);before<-serialize(table,NULL)
    result<-code$compare(table)
    require_true(identical(result$country_code,c("CHE","DEU","FRA")),"Comparison order")
    require_true(identical(serialize(payload,NULL),saved) && identical(serialize(table,NULL),before),"Input mutated")
  }
  changed <- function() {
    payload<-load_data();payload[[2]][[1]]$value<-payload[[2]][[1]]$value+37
    table<-code$extract(payload);verify_source(table,payload);r<-payload[[2]][[1]];result<-code$compare(table)
    require_true(result[result$country_code==r$countryiso3code,paste0("population_",r$date)]==r$value,"Hardcoded comparison value")
  }
  check("snapshot, schema, increases and DISPLAY precision",output)
  check("simple growth: 100 to 110",simple)
  files<-c("raw/population-page1.json","raw/invalid-indicator.json","raw/unavailable-year.json","constructed/missing-value.json","constructed/duplicate-key.json","constructed/boolean-value.json","constructed/wrong-indicator.json")
  reasons<-c("Incomplete coverage","API application error","No observations","Missing required","Duplicate","Population must","Wrong indicator")
  for (i in seq_along(files)) check(files[i],function() rejects(files[i],reasons[i]))
  check("null retained; comparison blocked",null)
  check("zero current year retained",zero)
  check("zero baseline rejected",baseline)
  check("shuffled input and nonmutation",shuffle)
  check("changed valid source value",changed)
  results
}
args<-commandArgs(trailingOnly=TRUE)
if (length(args)!=1) stop("Usage: Rscript --vanilla checks.R CANDIDATE.R")
results<-run_checks(candidate(args[1]))
for (r in results) cat(if(r$ok) "PASS" else "FAIL",r$name,r$reason,"\n")
ok<-vapply(results,function(r) r$ok,logical(1))
cat("BASIC:",sum(ok),"/",length(ok),". Precision not established.\n")
quit(status=if(all(ok)) 0L else 1L)
