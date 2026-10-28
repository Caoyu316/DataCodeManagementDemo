# DCM SQL, 29 October 2026. Synthetic fixture from class/lecture03.qmd.
# Run R --vanilla, then source("sql.R"). Restart R to rebuild from scratch.
library(DBI)
library(RSQLite)

build_database <- function(include_unmatched = TRUE) {
  con <- dbConnect(SQLite(), ":memory:")
  dbExecute(con, "PRAGMA foreign_keys = ON")

  DBI::dbExecute(con, "
  CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL
  );
  ")
  DBI::dbExecute(con, "
  CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL, -- ISO8601
    amount REAL NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
  );
  ")

  DBI::dbWriteTable(con, "customers",
    data.frame(customer_id=1:5,
               name=c("Ada","Bruno","Chloé","Dinesh","Elena"),
               country=c("CH","FR","CH","IN","US")),
    append=TRUE)

  DBI::dbWriteTable(con, "orders",
    data.frame(order_id=1:10,
               customer_id=c(1,1,2,3,3,3,4,4,5,5),
               order_date=as.character(as.Date("2025-09-20") + c(0,1,0,2,5,6,1,7,3,9)),
               amount=c(120,75,300,42,88,150,60,500,20,220)),
    append=TRUE)

  if (include_unmatched) {
    dbExecute(con, "INSERT INTO customers VALUES (6, 'Farah', 'CH')")
  }
  con
}

con <- build_database()
q <- "SELECT COUNT(*) AS n_customers FROM customers;"
print(DBI::dbGetQuery(con, q))
