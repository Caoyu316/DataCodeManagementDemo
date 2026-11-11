"""BASIC checks. Intentionally insufficient for full-precision correctness.
Run python3 checks.py CANDIDATE.py. No precision check is silently disabled.
"""
import copy
import math
import sys
import pandas as pd
from runner import candidate
from validation import load

EXPECTED = {("CHE", 2023): 8888822, ("CHE", 2024): 9005582,
            ("DEU", 2023): 83287273, ("DEU", 2024): 83516593,
            ("FRA", 2023): 68372286, ("FRA", 2024): 68551653}
NAMES = {"CHE": "Switzerland", "DEU": "Germany", "FRA": "France"}
COLUMNS = ["country_code", "population_2023", "population_2024", "increase", "growth_pct"]

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def verify_source(table, payload):
    source = {(r["countryiso3code"], int(r["date"])): r for r in payload[1]}
    keys = [(r.country_code, int(r.year)) for r in table.itertuples()]
    require(list(table.columns)==["country_code","country_name","year","population"], "Extraction columns")
    require(keys==sorted(EXPECTED) and set(keys)==set(source), "Six sorted keys")
    for row in table.itertuples():
        original = source[(row.country_code, row.year)]
        require(row.country_name==original["country"]["value"]==NAMES[row.country_code], "Name association")
        expected = original["value"]
        require(pd.isna(row.population) if expected is None else row.population==expected, "Source fidelity")

def run(code):
    results = []
    def check(name, fn):
        try:
            fn(); results.append((name, True, ""))
        except Exception as error:
            results.append((name, False, str(error)))
    def output():
        payload=load(); table=code.extract(payload); verify_source(table,payload)
        require({(r.country_code,r.year):r.population for r in table.itertuples()}==EXPECTED,"Snapshot values")
        result=code.compare(table)
        require(list(result.columns)==COLUMNS and list(result.country_code)==["CHE","DEU","FRA"],"Comparison schema/order")
        for row, delta, display in zip(result.itertuples(),[116760,229320,179367],["1.314","0.275","0.262"]):
            require(row.population_2023==EXPECTED[(row.country_code,2023)] and row.population_2024==EXPECTED[(row.country_code,2024)],"Comparison source association")
            require(row.increase==delta,"Increase")
            require(f"{row.growth_pct:.3f}"==display,"Displayed growth only")
    def simple():
        table=code.extract(load())
        table.loc[(table.country_code=="CHE") & (table.year==2023),"population"]=100
        table.loc[(table.country_code=="CHE") & (table.year==2024),"population"]=110
        require(code.compare(table).set_index("country_code").loc["CHE","growth_pct"]==10,"100 -> 110 = 10%")
    def rejects_input(name, reason):
        try: code.extract(load(name))
        except ValueError as error:
            require(reason in str(error),"Wrong rejection reason: "+str(error)); return
        raise AssertionError("Expected a useful ValueError")
    def null():
        payload=load("constructed/null-value.json");table=code.extract(payload);verify_source(table,payload)
        try: code.compare(table)
        except ValueError as error:
            require("Missing population" in str(error),"Wrong missing-value diagnosis");return
        raise AssertionError("Missing required population must block comparison")
    def zero():
        payload=load("constructed/zero-value.json");table=code.extract(payload);verify_source(table,payload)
        require(code.compare(table).set_index("country_code").loc["CHE","growth_pct"]==-100,"Zero current year must give -100%")
    def baseline():
        table=code.extract(load());table.loc[(table.country_code=="CHE")&(table.year==2023),"population"]=0
        try: code.compare(table)
        except ValueError as error:
            require("Baseline" in str(error),"Wrong baseline diagnosis");return
        raise AssertionError("Zero baseline must fail")
    def shuffle():
        payload=load();payload[1].reverse();saved=copy.deepcopy(payload)
        table=code.extract(payload);verify_source(table,payload);before=table.copy(deep=True)
        result=code.compare(table)
        require(list(result.country_code)==["CHE","DEU","FRA"],"Sorted comparison")
        require(payload==saved,"Payload mutated");pd.testing.assert_frame_equal(table,before)
    def changed():
        payload=load();payload[1][0]["value"]+=37
        table=code.extract(payload);verify_source(table,payload)
        changed=payload[1][0];result=code.compare(table).set_index("country_code")
        require(result.loc[changed["countryiso3code"],"population_"+changed["date"]]==changed["value"],"Hardcoded comparison value")
    check("snapshot, schema, increases and DISPLAY precision",output)
    check("simple growth: 100 to 110",simple)
    for name,reason in [("raw/population-page1.json","Incomplete coverage"),("raw/invalid-indicator.json","API application error"),("raw/unavailable-year.json","No observations"),("constructed/missing-value.json","Missing required"),("constructed/duplicate-key.json","Duplicate"),("constructed/boolean-value.json","Population must"),("constructed/wrong-indicator.json","Wrong indicator")]:
        check(name,lambda name=name,reason=reason:rejects_input(name,reason))
    check("null retained; comparison blocked",null)
    check("zero current year retained",zero)
    check("zero baseline rejected",baseline)
    check("shuffled input and nonmutation",shuffle)
    check("changed valid source value",changed)
    return results

if __name__ == "__main__":
    if len(sys.argv)!=2: raise SystemExit("Usage: python3 checks.py CANDIDATE.py")
    results=run(candidate(sys.argv[1]))
    for name,ok,why in results: print("PASS" if ok else "FAIL",name,why)
    print(f"BASIC: {sum(ok for _,ok,_ in results)}/{len(results)}. Precision not established.")
    sys.exit(0 if all(ok for _,ok,_ in results) else 1)
