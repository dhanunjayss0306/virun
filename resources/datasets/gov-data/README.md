# Virun — Government / Official Tourism Statistics

Official numbers for the government dashboard and pitch deck. Not city-level,
so not for traveler itineraries.

## Files

`state_tourist_visits_2023_2024.json` — extracted from **Table 4.1.2**
of the **India Tourism Data Compendium 2025** (Ministry of Tourism, Government
of India). All 36 States/UTs, each with:

```json
{
  "state_ut": "Goa",
  "dtv_2023": 8.175, "ftv_2023": 0.453,
  "dtv_2024": 9.941, "ftv_2024": 0.468,
  "growth_dtv_pct_2024_23": 21.6, "growth_ftv_pct_2024_23": 3.36,
  "share_dtv_2024_pct": 0.34, "share_ftv_2024_pct": 2.23
}
```

Units: **million visits**. DTV = domestic tourist visits, FTV = foreign
tourist visits.

Headline numbers (2024): **2,948.19 million domestic visits** (up 17.51%),
**20.94 million foreign visits** (up 8.84%). Top domestic states: Uttar
Pradesh (646.81M, 21.94%), Tamil Nadu (306.84M, 10.41%), Karnataka (304.56M,
10.33%). Top foreign-visit states: Maharashtra (3.70M, 17.69%), West Bengal
(3.12M, 14.92%).

## Provenance

- Extracted from the official PDF: `India_Tourism_Data_Compendium_2025`
  (Ministry of Tourism, 66th edition). The 16 MB source PDF is kept with the
  user's uploads, not in this repo; the JSON is the reusable asset.
- State names are transcribed exactly as printed, including the compendium's
  own typo **"Jammu & Pradesh"** (intended: Jammu & Kashmir) — noted in the
  JSON's `note_on_names` field.
- Parse validated: per-state 2024 sums match the table's printed India totals
  (2,948.191 / 20.942).

## License note

Government of India publication; figures are public statistics. Cite the
Ministry of Tourism as the source when displaying them.
