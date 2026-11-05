"""Public, complete checkpoint for demonstrations or after the manual attempt."""
import pandas as pd
from support import load, validate_envelope, check_table, compare


def extract(payload):
    records = validate_envelope(payload)
    rows = []
    for record in records:
        rows.append({
            "country_code": record["countryiso3code"],
            "country_name": record["country"]["value"],
            "year": int(record["date"]),
            "population": record["value"],
        })
    return check_table(pd.DataFrame(rows))


if __name__ == "__main__":
    table = extract(load())
    print(table.to_string(index=False))
    print(compare(table).to_string(float_format=lambda x: f"{x:.3f}"))
