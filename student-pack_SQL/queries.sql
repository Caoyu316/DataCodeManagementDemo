-- DCM: save your query, prediction, observed output and checks here.
-- Run ONE statement inside a Python/R string; this is not a Python/R program.
-- Replace ... before running the incomplete tasks.

-- A1 / warm-up: predict CH customers; run, then check.
SELECT name, country FROM customers
WHERE country = 'CH'
ORDER BY name ASC LIMIT 3;

-- A2 / slide 7: the three largest orders above 100.
SELECT order_id, amount FROM orders
WHERE ...
ORDER BY ...
LIMIT ...;

-- A5 / slide 11: top three customers by average order amount.
SELECT customer_id, ROUND(AVG(amount), 2) AS avg_amount
FROM orders GROUP BY customer_id
ORDER BY ...
LIMIT ...;

-- B4 / slide 15: customers without orders.
SELECT c.customer_id, c.name
FROM customers c LEFT JOIN orders o
  ON o.customer_id = c.customer_id
WHERE ... ORDER BY c.customer_id;

-- C1 / slides 18-21: AI-authored teaching draft with deliberate errors.
-- Contract: every customer once; count orders; zero count and total for none.
SELECT c.customer_id, c.name, COUNT(*) AS n_orders,
       SUM(o.amount) AS total
FROM customers c INNER JOIN orders o
  ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id;

-- Write your repaired C2 query below. Inspect before running.
-- Evidence: all customer IDs; Farah; count and total sums; source-row spot check.
