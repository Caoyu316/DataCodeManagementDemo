# Independent expectations. Run Rscript --vanilla checks.R checkpoint.R (or repair.R).
source("support.R")
verify_source <- function(tab,payload) {
  expected_names <- c(CHE="Switzerland",DEU="Germany",FRA="France")
  keys <- paste(tab$country_code,tab$year,sep="/")
  src <- vapply(payload[[2]],function(r) paste(r$countryiso3code,r$date,sep="/"),character(1))
  stopifnot(nrow(tab)==6,!anyDuplicated(keys),setequal(keys,src))
  for (i in seq_len(nrow(tab))) {
    r <- payload[[2]][[match(keys[i],src)]]
    stopifnot(tab$country_name[i]==r$country$value,tab$country_name[i]==expected_names[[tab$country_code[i]]])
    stopifnot(if(is.null(r$value)) is.na(tab$population[i]) else !is.na(tab$population[i]) && tab$population[i]==r$value)
  }
}

run_checks <- function(extract) {
  result <- list()
  check <- function(name,fun) {
    error <- tryCatch({fun();NULL},error=function(e) conditionMessage(e))
    result[[length(result)+1]] <<- data.frame(name=name,ok=is.null(error),detail=if(is.null(error)) "" else error)
  }
  expected <- c("CHE/2023"=8888822,"CHE/2024"=9005582,"DEU/2023"=83287273,
                "DEU/2024"=83516593,"FRA/2023"=68372286,"FRA/2024"=68551653)
  verify_values <- function(tab) {
    keys<-paste(tab$country_code,tab$year,sep="/")
    stopifnot(nrow(tab)==6, setequal(keys,names(expected)), all(tab$population==expected[keys]))
  }
  rejects <- function(name) {
    reasons <- c("raw/population-page1.json"="Incomplete coverage", "raw/invalid-indicator.json"="API application error",
      "raw/unavailable-year.json"="No observations", "constructed/missing-value.json"="Missing required",
      "constructed/duplicate-key.json"="Duplicate", "constructed/boolean-value.json"="Population must",
      "constructed/wrong-indicator.json"="Wrong indicator")
    caught <- tryCatch({extract(load_data(name));FALSE}, error=function(e) grepl(reasons[[name]],conditionMessage(e),fixed=TRUE))
    stopifnot(caught)
  }
  check("changed valid source value",function() {
    payload<-load_data();payload[[2]][[1]]$value<-payload[[2]][[1]]$value+37
    verify_source(extract(payload),payload)
  })
  check("six values and growth arithmetic",function() {
    tab<-extract(load_data());verify_values(tab);verify_source(tab,load_data());r<-compare(tab)
    delta<-c(116760,229320,179367);stopifnot(all(r$increase==delta))
    stopifnot(isTRUE(all.equal(r$growth_pct,100*delta/c(8888822,83287273,68372286))))
  })
  for (name in c("raw/population-page1.json","raw/invalid-indicator.json","raw/unavailable-year.json",
                 "constructed/missing-value.json","constructed/duplicate-key.json","constructed/boolean-value.json","constructed/wrong-indicator.json"))
    check(name,local({n<-name;function() rejects(n)}))
  check("explicit null retained; growth blocked",function() {
    tab<-extract(load_data("constructed/null-value.json"));v<-tab$population[tab$country_code=="CHE" & tab$year==2024]
    verify_source(tab,load_data("constructed/null-value.json"))
    stopifnot(length(v)==1,is.na(v),!is.nan(v))
    blocked<-tryCatch({compare(tab);FALSE},error=function(e) TRUE);stopifnot(blocked)
  })
  check("synthetic zero retained",function() {
    tab<-extract(load_data("constructed/zero-value.json"));verify_source(tab,load_data("constructed/zero-value.json"));stopifnot(tab$population[tab$country_code=="CHE" & tab$year==2024]==0)
  })
  check("shuffled records and input preservation",function() {
    payload<-load_data();payload[[2]]<-rev(payload[[2]]);original<-payload
    verify_source(extract(payload),payload);verify_values(extract(payload));stopifnot(identical(payload,original))
  })
  do.call(rbind,result)
}
if (sys.nframe()==0) {
  args<-commandArgs(trailingOnly=TRUE);candidate<-if(length(args)) args[1] else "ai-draft.R"
  cat("Candidate:",candidate,"\n");source(candidate);out<-run_checks(extract);print(out,row.names=FALSE)
  cat(sum(out$ok),"/",nrow(out),"checks passed\n")
  quit(status=if(all(out$ok)) 0 else 1)
}
