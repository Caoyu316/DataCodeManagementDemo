"""DCM SQL, 29 October 2026. Synthetic fixture from class/lecture03.qmd.
Run: python3 -i sql.py. Restart after edits to recreate a fresh database.
Requires pandas; sqlite3 and datetime are in the Python standard library.
"""
import sqlite3
import datetime as dt
import pandas as pd


def build_database(include_unmatched=True):
    """Create a fresh constrained database; False restores the historical fixture."""
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE customers (
      customer_id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      country TEXT NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE orders (
      order_id INTEGER PRIMARY KEY,
      customer_id INTEGER NOT NULL,
      order_date TEXT NOT NULL,
      amount REAL NOT NULL,
      FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    """)

    customers = pd.DataFrame({
      "customer_id": [1,2,3,4,5],
      "name": ["Ada","Bruno","Chloé","Dinesh","Elena"],
      "country": ["CH","FR","CH","IN","US"]
    })
    orders = pd.DataFrame({
      "order_id": range(1,11),
      "customer_id": [1,1,2,3,3,3,4,4,5,5],
      "order_date": [(dt.date(2025,9,20)+dt.timedelta(days=d)).isoformat() for d in [0,1,0,2,5,6,1,7,3,9]],
      "amount": [120,75,300,42,88,150,60,500,20,220]
    })
    customers.to_sql("customers", con, if_exists="append", index=False)
    orders.to_sql("orders", con, if_exists="append", index=False)
    if include_unmatched:
        con.execute("INSERT INTO customers VALUES (6, 'Farah', 'CH')")
    con.commit()
    return con


con = build_database()
q = "SELECT COUNT(*) AS n_customers FROM customers;"

if __name__ == "__main__":
    print(pd.read_sql_query(q, con).to_string(index=False))
    print("Ready: edit q or paste one query as a triple-quoted Python string.")
    print("Run print(pd.read_sql_query(q, con).to_string(index=False)) to inspect it.")
