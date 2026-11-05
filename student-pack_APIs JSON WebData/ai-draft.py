"""INTENTIONALLY FLAWED teaching draft; not an actual AI transcript.
Copy to repair.py, then edit that copy. This code is supposed to fail checks.
"""
import pandas as pd


def extract(payload):
    rows = []
    for record in payload[1]:
        rows.append({
            "country_code": record["countryiso3code"],
            "country_name": record["country"]["value"],
            "year": int(record["date"]),
            "population": record.get("value") or 0,
        })
    if len(rows) == 0:
        raise ValueError("No rows")
    return pd.DataFrame(rows)
