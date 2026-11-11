"""Supplied Week 8 validation and local loading. No comparison implementation; no network."""
import json
import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
COUNTRIES = {"CHE": "Switzerland", "DEU": "Germany", "FRA": "France"}
EXPECTED = {(country, year) for country in COUNTRIES for year in (2023, 2024)}


def load(name="raw/population-2023-2024.json"):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def validate_envelope(payload):
    if isinstance(payload, list) and payload and isinstance(payload[0], dict) and "message" in payload[0]:
        raise ValueError("API application error: inspect message, even if HTTP was 200")
    if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[0], dict):
        raise ValueError("Expected [metadata, records]")
    meta, records = payload
    if records is None:
        raise ValueError("No observations: records is null, not population zero")
    if not isinstance(records, list):
        raise ValueError("Records must be an array")
    if any(type(meta.get(key)) is not int for key in ("page", "pages", "total", "per_page")):
        raise ValueError("Metadata counts must be integers, not Boolean/string values")
    if meta["per_page"] < len(records):
        raise ValueError("Metadata page size is smaller than records received")
    if meta.get("page") != 1 or meta.get("pages") != 1 or meta.get("total") != 6 or len(records) != 6:
        raise ValueError("Incomplete coverage: need one complete page and six observations")
    for record in records:
        if not isinstance(record, dict) or not {"country", "countryiso3code", "indicator", "date", "value"} <= record.keys():
            raise ValueError("Missing required field in record")
        if not isinstance(record["indicator"], dict) or record["indicator"].get("id") != "SP.POP.TOTL":
            raise ValueError("Wrong indicator: expected population")
        code = record["countryiso3code"]
        if not isinstance(code, str) or code not in COUNTRIES:
            raise ValueError("Unexpected country code")
        if not isinstance(record["country"], dict) or record["country"].get("value") != COUNTRIES[code]:
            raise ValueError("Country name/code mismatch")
        if record["date"] not in ("2023", "2024"):
            raise ValueError("Unexpected year")
        value = record["value"]
        if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
            raise ValueError("Population must be a nonnegative finite number or null")
    return records


def check_table(table):
    columns = ["country_code", "country_name", "year", "population"]
    if not isinstance(table, pd.DataFrame) or list(table.columns) != columns:
        raise ValueError("Expected country_code, country_name, year, population columns")
    if table.duplicated(["country_code", "year"]).any():
        raise ValueError("Duplicate country-year key")
    keys = set(zip(table.country_code, table.year))
    if len(table) != 6 or keys != EXPECTED:
        raise ValueError("Missing or unexpected country-year keys")
    if not all(isinstance(v, str) for v in table.country_name):
        raise ValueError("Country names must be strings")
    if any(isinstance(v, bool) or (not pd.isna(v) and
           (not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0))
           for v in table.population):
        raise ValueError("Population must be nonnegative finite numeric data or missing")
    return table.sort_values(["country_code", "year"]).reset_index(drop=True)


def check_source(table, payload):
    """Check the student's actual table against THIS input, including zero/null.
    Structural checks alone cannot establish source fidelity. Bounded six-key task.
    """
    records = validate_envelope(payload)
    table = check_table(table)
    source = {(r["countryiso3code"], int(r["date"])): r for r in records}
    if len(source) != len(records) or set(source) != EXPECTED:
        raise ValueError("Duplicate or missing source country-year key")
    for row in table.itertuples():
        record = source[(row.country_code, row.year)]
        if row.country_name != record["country"]["value"]:
            raise ValueError("Source fidelity: country name/code mismatch")
        expected = record["value"]
        agrees = pd.isna(row.population) if expected is None else (
            not pd.isna(row.population) and row.population == expected)
        if not agrees:
            raise ValueError("Source fidelity: population differs from its source record")
    return table

