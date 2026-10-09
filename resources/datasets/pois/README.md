# Virun — City POI Dataset v1

312 real points of interest across 4 cities, extracted from OpenStreetMap.

| City | POIs | Coverage |
|---|---|---|
| Kashmir | 80 | Srinagar (Dal Lake, Mughal gardens, old city) + Pahalgam |
| Goa | 80 | Old Goa churches + Panaji + beaches |
| Hyderabad | 80 | Full city (4 quadrants) |
| Visakhapatnam | 72 | Full city (4 quadrants) |

## Files

`<city>.json` — each a list of:
```json
{
  "name": "Charminar",
  "category": "historic | temple | church | mosque | museum | park | beach | attraction | viewpoint | art | entertainment | worship | place",
  "lat": 17.3616, "lng": 78.4747,
  "details": { "opening_hours": "...", "fee": "...", "website": "...", "wikipedia": "...", "description": "...", "religion": "..." }
}
```

## Source & license

Data (c) **OpenStreetMap contributors**, **ODbL license**. You must credit
"© OpenStreetMap contributors" in the app (a line in About/Credits is enough)
and share-alike if you remix the data.

## How it was built

`build_pois.py` + `build_pois2.py` query the Overpass API for
`tourism=*`, `historic=*`, `leisure=park|garden`, `natural=beach`,
`amenity=place_of_worship` inside per-city bounding boxes (quadrant-split to
avoid API timeouts). No API key needed. Re-run to refresh or add cities.

## Known gaps (v1)

- Gulmarg area queries timed out — Kashmir set leans Srinagar/Pahalgam.
- One Visakhapatnam quadrant timed out — 72 POIs instead of 80.
- OSM coverage varies: hours/fees are present only where mappers added them.
  Treat `details` as best-effort; verify hours/fees before showing as fact.

## Suggested use

- Destination detail pages, map pins
- Grounding the AI itinerary planner (real place names + coordinates, so the
  AI can't invent places)
- "Nearby" features via lat/lng
