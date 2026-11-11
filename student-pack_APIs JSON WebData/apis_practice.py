"""Manual starter. Run python3 -i apis.py from the extracted practice folder.
No solutions imported. Finish three TODO expressions before calling manual_table().
"""
import pandas as pd
from support import load, check_table, check_source

payload = load()
metadata, records = payload


def manual_table():
    rows = []
    for record in records:
        rows.append({
            "country_code": record["countryiso3code"],  # TODO: record's three-letter country code
            "country_name": record["country"]["value"],
            "year": int(record["date"]),          # TODO: convert the record's date to int
            "population": record["value"],    # TODO: preserve the record's value
        })
    return check_table(pd.DataFrame(rows))


# if __name__ == "__main__":
#     print("OFFLINE snapshot: metadata +", len(records), "records")
#     print("Predict payload[1][0]['country']['value']; then run it.")
#     print("Complete manual_table() before calling it; see guide for the public checkpoint.")


manual = manual_table()
print(check_source(manual, payload))