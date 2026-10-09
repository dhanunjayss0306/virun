# UN Tourism bulk data (05_2026) — what's in here

Official UN Tourism statistical database, extracted 2026-10-09 into this folder.
~9.4MB, 15 Excel files + 3 metadata PDFs.

## Structure

Every `.xlsx` has an `Overview` sheet (definitions) and a `Data` sheet with
columns: `indicator_code | indicator_label | reporter_area_label |
partner_area_label | year | value | flag`. Country-level, 1995–2024.

| Folder | Contents |
|---|---|
| `01_Domestic` | Domestic trips + domestic accommodation by country |
| `02_Inbound` | Arrivals, expenditure, arrivals by region / purpose / transport mode, accommodation guests |
| `03_Outbound` | Departures + expenditure by country |
| `04_Accommodation` | Hotel capacity / occupancy indicators |
| `05_Macroeconomic` | Tourism direct GDP (SDG 8.9.1) |
| `06_Employment` | Tourism employment (SDG 8.9.2) |
| `07_SDGs` | Sustainable tourism indicators |

## Extracted for the app

**`india_summary.json`** — India-only cut, ready for the government dashboard
and pitch deck: inbound arrivals 2017–2024, inbound expenditure, outbound
departures, top source markets (2024). Units: arrivals/trips in **thousands**,
expenditure in **USD millions** (verify against the Overview sheet per file
before publishing any number).

## What this data is (and isn't) for in Virun

- **Good for:** the Government tourism dashboard (arrivals trends, receipts,
  source markets, employment, tourism GDP) and market-size numbers in the
  pitch deck. This is real, citable, official data.
- **NOT for:** the traveler app itself. This data is country-level and
  statistical — it cannot power itineraries, guide matching, or place
  discovery. The app needs the city POI dataset (see main README / next step).
