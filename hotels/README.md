# Virun — Hotel / Accommodation Dataset v1

320 real accommodations across 4 cities, extracted from OpenStreetMap.

| City | Hotels |
|---|---|
| Kashmir | 80 |
| Goa | 80 |
| Hyderabad | 80 |
| Visakhapatnam | 80 |

Type mix (all cities): hotel 176, guest_house 76, hostel 40, apartment 25,
motel 2, chalet 1.

## Files

`hotels/<city>.json` — each a list of:
```json
{
  "name": "Abhinand Grand Hotel and Restaurant",
  "type": "hotel | guest_house | hostel | motel | resort | apartment | chalet | lodge",
  "lat": 17.35309, "lng": 78.555342,
  "stars": null, "rooms": null,
  "phone": null, "website": null,
  "address": "5"
}
```

## Source & license

Data (c) **OpenStreetMap contributors**, **ODbL license**. Credit
"© OpenStreetMap contributors" in the app and share-alike if you remix.

## How it was built

`hotels/build_hotels.py` queries the Overpass API for
`tourism=hotel|guest_house|hostel|motel|resort|apartment|chalet|lodge` inside
per-city bounding boxes. No API key needed. Re-run to refresh or add cities.

## Known gaps (v1)

- OSM is a map, not a booking inventory: **no prices, no availability, no
  ratings**. `stars`/`rooms`/`phone`/`website` are present only where mappers
  added them (often null). Do not present nulls as facts.
- Some bounding boxes timed out on Overpass and returned fewer raw elements;
  the script still filled 80 named places per city, so coverage leans toward
  the quadrants that responded.
- For live prices and bookable inventory, pair this with a hotel booking API
  at runtime — this dataset is for place identity, location, and contact.

## Suggested use

- "Where to stay" sections on destination pages, map pins
- Matching travelers with nearby stays
- Feeding the AI planner real hotel names + coordinates (it can't invent them)
