---
title: "DCM · SQL and relational data"
date: "Thursday, 29 October 2026"
lang: en
---

Two 45-minute periods · Python live · R alternative · one language per student.

**The question:** can we produce a correct order count and total for **every customer**, including a customer with no orders?

## Start here {#start}

Extract the student pack into a folder and open that folder in your editor. The pack contains `sql.py`, `sql.R`, `queries.sql`, this guide and its HTML version. The Python/R files supply the complete synthetic database; you do not need a database server, cloud account or internet connection during the exercises.

Before class, check **one** route:

```bash
python3 -c "import sqlite3, pandas; print(sqlite3.sqlite_version)"
```

Or in R:

```r
library(DBI)
library(RSQLite)
```

Python needs pandas from Week 4; sqlite3 and datetime are standard-library modules. R needs DBI and RSQLite. If an import is unavailable, resolve it before class or pair with a working runtime; do not spend the activity installing packages. The reviewer can predict, inspect the actual output and record checks.

### Python workflow

From the extracted folder, start:

```bash
python3 -i sql.py
```

Use `python` or `py` if that is your usual launcher. You should see `n_customers = 6`. At the `>>>` prompt, put **one SQL query inside a Python string**, then print its result:

```python
q = """
SELECT name, country FROM customers
WHERE country = 'CH'
ORDER BY name ASC LIMIT 3;
"""
print(pd.read_sql_query(q, con).to_string(index=False))
```

Alternatively, edit the `q` string near the bottom of `sql.py`, save, exit Python and run the starter again. Your SQL edits can also be saved in `queries.sql`. That file is a record of your work: select and copy one statement into `q`; do not run it as a Python script or send all its statements to `read_sql_query` at once.

### R workflow

Start `R --vanilla` in the extracted folder, then:

```r
source("sql.R")
q <- "SELECT name, country FROM customers
      WHERE country = 'CH'
      ORDER BY name ASC LIMIT 3;"
print(DBI::dbGetQuery(con, q))
```

The SQL is identical. Only the host-language string and query call differ. Do not implement both routes.

### Restart and finish

The database lives in memory. A **fresh run** recreates it, including Farah. After editing a Python/R file, exit and restart to avoid stale definitions or reusing an old connection. Do not rerun CREATE/INSERT snippets manually against an already populated database. When finished, use `con.close()` in Python or `DBI::dbDisconnect(con)` in R; save your SQL and evidence first.

## The complete synthetic data {#data}

These are teaching records from historical DCM Lecture 3, with one added customer, Farah, who has no orders. The dates deliberately remain in September 2025. Amounts share one common synthetic monetary unit; country does not indicate currency. One order row is a whole order, not an order line.

### customers — one row per customer

| customer_id | name | country |
| ---: | --- | --- |
| 1 | Ada | CH |
| 2 | Bruno | FR |
| 3 | Chloé | CH |
| 4 | Dinesh | IN |
| 5 | Elena | US |
| 6 | Farah | CH |

### orders — one row per order

| order_id | customer_id | order_date | amount |
| ---: | ---: | --- | ---: |
| 1 | 1 | 2025-09-20 | 120 |
| 2 | 1 | 2025-09-21 | 75 |
| 3 | 2 | 2025-09-20 | 300 |
| 4 | 3 | 2025-09-22 | 42 |
| 5 | 3 | 2025-09-25 | 88 |
| 6 | 3 | 2025-09-26 | 150 |
| 7 | 4 | 2025-09-21 | 60 |
| 8 | 4 | 2025-09-27 | 500 |
| 9 | 5 | 2025-09-23 | 20 |
| 10 | 5 | 2025-09-29 | 220 |

Schema to inspect or share with an assistant for this exercise:

```sql
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  country TEXT NOT NULL
);
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  order_date TEXT NOT NULL,
  amount REAL NOT NULL,
  FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
```

Setup already creates these tables and enables foreign keys. The schema is a reference, **not another command to run** in your populated database. Customer IDs can repeat in orders; order IDs cannot.

## Period 1 — select and summarise {#period-one}

**Warm-up (A1).** Predict the CH customers before running the query in the startup example. Check names, country and order. Expect Ada, Chloé and Farah.

**Three large orders (A2, slide 7, 6 minutes).** Spend two minutes predicting from the source rows, two completing the starter and two comparing results. Return the three largest orders whose amount is greater than 100. Show order ID/amount; use order ID to break amount ties.

**Top three averages (A5, slide 11, 6 minutes).** Spend one minute predicting, three completing/running and two comparing. Return customer ID and mean order amount, ordered by the **unrounded** mean descending, then ID ascending; limit to three. Round the displayed mean to two decimals. Who has the largest mean? Who has the largest total?

Record for each: **prediction → query → observed rows → checks**. Replace every `...` placeholder before executing.

<details>
<summary>Worked answers — open after your attempt</summary>

```sql
-- A2
SELECT order_id, amount FROM orders
WHERE amount > 100
ORDER BY amount DESC, order_id ASC LIMIT 3;
```

Expected `(order_id, amount)`: **(8, 500), (3, 300), (10, 220)**. Five orders qualify before LIMIT, but only the largest three are returned.

```sql
-- A3: baseline summary
SELECT COUNT(*) AS n_orders, SUM(amount) AS total,
       AVG(amount) AS avg_amount FROM orders;

-- A4: customer groups
SELECT customer_id, COUNT(*) AS n_orders, SUM(amount) AS total,
       ROUND(AVG(amount), 2) AS avg_amount
FROM orders GROUP BY customer_id ORDER BY customer_id;

-- A5
SELECT customer_id, ROUND(AVG(amount), 2) AS avg_amount
FROM orders GROUP BY customer_id
ORDER BY AVG(amount) DESC, customer_id ASC LIMIT 3;
```

A3 returns one row: **10, 1575, 157.5**. Check the ten source amounts by hand. A4 returns:

| customer_id | n_orders | total | avg_amount |
| ---: | ---: | ---: | ---: |
| 1 | 2 | 195 | 97.50 |
| 2 | 1 | 300 | 300.00 |
| 3 | 3 | 280 | 93.33 |
| 4 | 2 | 560 | 280.00 |
| 5 | 2 | 240 | 120.00 |

Farah has no input row in orders. A5 returns **(2, 300), (4, 280), (5, 120)**. Bruno has the largest mean; Dinesh has the largest total, 560. Averaging customer means weights customers equally, whereas the overall order mean weights every order equally.

</details>

## Period 2 — join and check missing matches {#joins}

Predict counts before running these demonstration queries. `c` and `o` are table aliases; `ON` tells the engine which rows match.

```sql
-- B1: matching order/customer pairs
SELECT o.order_id, o.order_date, o.amount, c.name
FROM orders o INNER JOIN customers c
  ON o.customer_id = c.customer_id
ORDER BY o.order_id;

-- B2: every customer, with matching orders where present
SELECT c.customer_id, c.name, o.order_id, o.amount
FROM customers c LEFT JOIN orders o
  ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_id;

-- B3: joined rows versus observed orders
SELECT COUNT(*) AS joined_rows, COUNT(o.order_id) AS matched_orders,
       SUM(o.amount) AS total
FROM customers c LEFT JOIN orders o
  ON o.customer_id = c.customer_id;
```

B1 returns **ten** rows, one per order. B2 returns **eleven**: ten matches plus Farah with NULL order fields. LEFT JOIN retains all customers, but can produce several rows per customer. B3 returns **(11, 10, 1575)**. Count a non-null order key to count orders.

**Who has no orders? (B4, slide 15, 6 minutes).** Predict for one minute, complete/run the starter for three and explain the result for two. Test a right-side field that cannot be NULL in a stored order. Use `IS NULL`, not `= NULL`.

<details>
<summary>Worked answer — customers without orders</summary>

```sql
SELECT c.customer_id, c.name
FROM customers c LEFT JOIN orders o
  ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL ORDER BY c.customer_id;
```

Only **(6, Farah)**. Her customer ID is not missing; her order ID is. For Farah's joined group, `COUNT(o.order_id)` is 0, while `SUM(o.amount)` and `AVG(o.amount)` are NULL. A zero-total reporting policy can use `COALESCE(SUM(o.amount), 0)`; it does not establish an observed average of zero.

SQLite NULL appears as Python `None` in raw rows, R `NA`, or a missing-value display such as pandas `NaN`. These displays do not turn NULL into zero.

</details>

## AI critique — specify, inspect, repair, verify {#ai}

**18 minutes, slides 18–21.** Work from the supplied deliberately flawed AI-authored teaching draft in `queries.sql`. This is a local teaching adaptation, not a quotation of the historical cloud-query transcript.

**Contract:** every customer exactly once; return customer ID, name, order count and total amount. Customers without orders must have count 0 and total 0. Keep the schema and data unchanged.

1. **3 minutes:** write expected coverage/counts/totals and choose one customer for a manual source-row check.
2. **3 minutes:** inspect the supplied draft; predict who is excluded. Ask for a bounded repair if an assistant is available.
3. **8 minutes:** inspect each changed clause, run the repair and check it independently.
4. **4 minutes:** compare with the worked answer and justify acceptance/rejection.

```sql
-- C1: plausible but incorrect for the contract
SELECT c.customer_id, c.name, COUNT(*) AS n_orders,
       SUM(o.amount) AS total
FROM customers c INNER JOIN orders o
  ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id;
```

Suggested prompt:

> Using this SQLite schema and synthetic fixture, inspect this query against the stated contract. Explain who is excluded and how unmatched rows affect counts and sums. Propose the smallest SQL-only repair; do not alter the tables or data. Explain each change. I will check the output independently.

Supply the schema, contract and draft, using only these synthetic records. **No assistant?** Work in pairs on the same draft, then compare with the answer. No paid tool or installation is required. Record significant AI assistance and your own checks; a second AI's agreement is not independent evidence.

### Evidence to retain

- Six rows; IDs 1–6, each once; correct names.
- Farah has zero orders and zero total.
- Returned counts sum to 10; returned totals sum to 1,575.
- One independently chosen source-row check: count the orders and add the amounts by hand.
- Explain changed clauses and write “I accept / reject this proposal because …”.

For example, after running a repaired query in Python:

```python
result = pd.read_sql_query(q, con)
print(result.to_string(index=False))
print(result["n_orders"].sum(), result["total"].sum())
```

In R:

```r
result <- DBI::dbGetQuery(con, q)
print(result)
print(c(sum(result$n_orders), sum(result$total)))
```

These checks of the returned table supplement your manual source check; they do not replace coverage or association checks.

### Worked repair {#ai-answer}

<details>
<summary>Open after your attempt — diagnosis, query and complete result</summary>

INNER JOIN drops Farah. Its totals still sum to 1,575, which does not demonstrate complete customer coverage. Changing only INNER to LEFT gives Farah an incorrect order count of **1** and a **NULL** total: `COUNT(*)` counts the null-extended joined row.

```sql
-- C2
SELECT c.customer_id, c.name, COUNT(o.order_id) AS n_orders,
       COALESCE(SUM(o.amount), 0) AS total
FROM customers c LEFT JOIN orders o
  ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id;
```

| customer_id | name | n_orders | total |
| ---: | --- | ---: | ---: |
| 1 | Ada | 2 | 195 |
| 2 | Bruno | 1 | 300 |
| 3 | Chloé | 3 | 280 |
| 4 | Dinesh | 2 | 560 |
| 5 | Elena | 2 | 240 |
| 6 | Farah | 0 | 0 |

LEFT JOIN retains every customer. COUNT(order_id) counts real orders. COALESCE applies the stated zero-total policy. Manual example: Chloé has orders 4/5/6; `42 + 88 + 150 = 280`, count 3. Check your own chosen customer too. Passing these checks supports this query for this contract; it does not prove correctness for arbitrary data models.

</details>

## Optional appendix — outside the 90-minute lecture {#appendix}

### A1. HAVING filters groups

Historical Lecture 3's country-level example, retained for independent practice:

```sql
SELECT c.country, ROUND(AVG(o.amount), 2) AS avg_amount,
       COUNT(*) AS n_orders
FROM orders o JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.country
HAVING COUNT(*) >= 2
ORDER BY avg_amount DESC;
```

Expected `(country, avg_amount, n_orders)`: **(IN, 280, 2), (US, 120, 2), (CH, 95, 5)**. WHERE filters input rows; HAVING filters groups. France's single order does not meet the group condition. Farah adds no order to the CH mean.

### A2. A filter can remove a retained customer

```sql
SELECT c.customer_id, c.name, o.order_id
FROM customers c LEFT JOIN orders o
  ON c.customer_id = o.customer_id
WHERE o.amount > 0
ORDER BY c.customer_id, o.order_id;
```

This returns ten rows and drops Farah: her NULL amount does not satisfy `> 0`. To retain every customer while matching only positive orders, put that condition in ON instead:

```sql
SELECT c.customer_id, c.name, o.order_id
FROM customers c LEFT JOIN orders o
  ON c.customer_id = o.customer_id AND o.amount > 0
ORDER BY c.customer_id, o.order_id;
```

This returns eleven rows, including Farah. Predicate placement changes the question. Another diagnostic: a Cartesian join pairs every customer with every order — **6 × 10 = 60** rows and six copies of each amount, total **9,450**. A large result is not automatically more information.

### A3. BigQuery and historical AI answers

BigQuery is an optional cloud route, not required for this local session. Historical Lecture 3 used OpenAQ, bikeshare and traffic data plus R/Python connectors. One ChatGPT bikeshare draft named `bigquery-public-data.san_francisco` where the teaching example expected `bigquery-public-data.san_francisco_bikeshare`. A plausible-looking query still needs the actual dataset/table/column names and the right SQL dialect.

Cloud UI, dataset availability, credentials and costs have **not** been rechecked for this lesson. Do not copy old screenshots or cached results as evidence of current output. COUNT of accident rows is also not necessarily a count of fatalities. LIMIT controls output rows; it is not a general guarantee of lower scanning costs. See [Google's cost guidance](https://docs.cloud.google.com/bigquery/docs/best-practices-costs) if pursuing cloud work later.

## Troubleshooting and exit {#finish}

| Symptom | Check |
| --- | --- |
| `SyntaxError` at SELECT in Python | Put SQL inside the quoted `q` string, then call the query function. |
| SQL syntax error near `...` | Replace all starter placeholders; execute one statement at a time. |
| No such table / name `con` not defined | Run/source the supplied starter in this session; use its connection. |
| Table exists / unique-key failure after setup | Restart with a fresh in-memory database; do not seed twice. |
| Old result after an edit | Save the file, restart/reload it, and check the current `q` string. |
| NULL/None/NA/NaN in the joined result | Inspect whether the right-side record matched before replacing anything. |
| AI access or runtime unavailable | Use the supplied draft; pair with a working runtime and take the reviewer role. |

Before leaving, explain **10 INNER JOIN rows versus 11 LEFT JOIN rows**, and name a check beyond “it ran.” Save your SQL and evidence. No new graded submission is introduced here. Next meeting: 5 November, APIs/JSON and validating external data.
