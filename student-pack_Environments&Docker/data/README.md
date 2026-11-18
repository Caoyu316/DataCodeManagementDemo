# Data provenance

`raw/` holds four genuine World Bank Indicators API bodies captured on 29 October
2026 and preserved verbatim in the approved Week 8 planning note. Do not edit them.
`provenance.json` lists request URLs, hashes and evidence limits. Observations concern
2023–2024; provider metadata says last updated 8 October 2026. Full and partial
capture completion times: 15:40:21.881735 and 15:40:28.538387 UTC. Exact completion
times were not retained for the error/no-data bodies. HTTP 200 was observed for
those two probes; headers were not recorded for the full/partial captures.

Source: World Bank, World Development Indicators, SP.POP.TOTL, population (persons),
midyear resident estimates. Underlying demographic sources listed by WDI include
UN Population Division, national statistical offices and Eurostat.
[Definition](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SP.POP.TOTL)
· [Source and CC BY 4.0 license](https://data.worldbank.org/indicator/SP.POP.TOTL).
Historical estimates may be revised. These are not current population or customer counts.

`constructed/` contains teaching modifications, NOT authentic provider responses.
All population variants start from the full capture: null-value changes CHE/2024
value to null; missing-value removes that key; duplicate-key replaces CHE/2023
with a second CHE/2024; zero-value changes CHE/2024 to 0; boolean-value changes
it to false; wrong-indicator changes its indicator ID. `stock.json` is an invented
warehouse response for transfer. Its non-null next_cursor indicates more data.

Optional live downloads go to a new folder under `live/`, never into `raw/`.
