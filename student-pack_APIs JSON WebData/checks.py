"""Independent expectations. Run: python3 checks.py checkpoint.py (or repair.py).
The intentionally flawed ai-draft.py should fail. No network or hidden solution.
"""
import copy
import importlib.util
import math
from pathlib import Path
import sys
from support import load, compare
import pandas as pd

EXPECTED = {("CHE",2023):8888822, ("CHE",2024):9005582,
            ("DEU",2023):83287273, ("DEU",2024):83516593,
            ("FRA",2023):68372286, ("FRA",2024):68551653}


def verify_source(table, payload):
    names = {"CHE": "Switzerland", "DEU": "Germany", "FRA": "France"}
    source = {(r["countryiso3code"], int(r["date"])):
              (r["country"]["value"], r["value"]) for r in payload[1]}
    keys = [(r.country_code, int(r.year)) for r in table.itertuples()]
    assert len(keys) == len(set(keys)) == 6 and set(keys) == set(source)
    for row in table.itertuples():
        name, value = source[(row.country_code, int(row.year))]
        assert row.country_name == name == names[row.country_code], "Country code/name association"
        assert (pd.isna(row.population) if value is None else
                not pd.isna(row.population) and row.population == value), "Population/source association"


def run_checks(extract):
    results = []
    def check(name, test):
        try:
            test()
            results.append((name, True, ""))
        except Exception as error:
            results.append((name, False, str(error)))
    def same_values():
        table = extract(load())
        verify_source(table, load())
        actual = {(r.country_code, int(r.year)):r.population for r in table.itertuples()}
        assert len(table) == 6 and actual == EXPECTED, "Six source values/keys must agree"
        rates = compare(table)
        for code, delta in [("CHE",116760),("DEU",229320),("FRA",179367)]:
            assert rates.loc[code,"increase"] == delta
            assert math.isclose(rates.loc[code,"growth_pct"],100*delta/EXPECTED[(code,2023)], rel_tol=1e-12)
    def rejects(name):
        try:
            extract(load(name))
        except ValueError as e:
            expected_reason = {"raw/population-page1.json":"Incomplete coverage",
                "raw/invalid-indicator.json":"API application error", "raw/unavailable-year.json":"No observations",
                "constructed/missing-value.json":"Missing required", "constructed/duplicate-key.json":"Duplicate",
                "constructed/boolean-value.json":"Population must", "constructed/wrong-indicator.json":"Wrong indicator"}[name]
            assert expected_reason in str(e), f"Wrong diagnosis: {e}"
            return
        raise AssertionError("Must reject with a useful ValueError")
    def null_preserved():
        table = extract(load("constructed/null-value.json"))
        verify_source(table, load("constructed/null-value.json"))
        value = table.loc[(table.country_code=="CHE") & (table.year==2024),"population"].iloc[0]
        assert math.isnan(value), "Explicit null must remain missing, not zero"
        try:
            compare(table)
        except ValueError:
            return
        raise AssertionError("Do not compute growth with a required missing value")
    def zero_preserved():
        table=extract(load("constructed/zero-value.json"))
        verify_source(table, load("constructed/zero-value.json"))
        assert table.loc[(table.country_code=="CHE") & (table.year==2024),"population"].iloc[0]==0
    def shuffled():
        payload=load(); original=copy.deepcopy(payload); payload[1].reverse()
        table=extract(payload)
        verify_source(table, payload)
        assert {(r.country_code,int(r.year)):r.population for r in table.itertuples()}==EXPECTED
        assert payload[1]==list(reversed(original[1])), "Input mutated"
    def changed_source():
        payload=load(); payload[1][0]["value"] += 37
        verify_source(extract(payload), payload)
    check("changed valid source value", changed_source)
    check("six values and growth arithmetic", same_values)
    for name in ["raw/population-page1.json","raw/invalid-indicator.json","raw/unavailable-year.json",
                 "constructed/missing-value.json","constructed/duplicate-key.json","constructed/boolean-value.json","constructed/wrong-indicator.json"]:
        check(name,lambda name=name: rejects(name))
    check("explicit null retained; growth blocked",null_preserved)
    check("synthetic zero retained",zero_preserved)
    check("shuffled records and input preservation",shuffled)
    return results


if __name__ == "__main__":
    path=Path(sys.argv[1] if len(sys.argv)>1 else "ai-draft.py").resolve()
    spec=importlib.util.spec_from_file_location("candidate",path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    print("Candidate:",path)
    results=run_checks(module.extract)
    for name,ok,why in results: print(("PASS" if ok else "FAIL"),name,why)
    print(f"{sum(ok for _,ok,_ in results)}/{len(results)} checks passed")
    sys.exit(0 if all(ok for _,ok,_ in results) else 1)
