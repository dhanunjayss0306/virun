# Virun — City Image Dataset v1

40 real photos (10 per city) + 3 AI-generated decorative images for UI corners.

## Layout

```
virun-assets/
  kashmir/photos/kashmir_01.jpg … kashmir_10.jpg       (real photos)
  goa/photos/goa_01.jpg … goa_10.jpg                   (real photos)
  hyderabad/photos/hyderabad_01.jpg … hyderabad_10.jpg (real photos)
  visakhapatnam/photos/visakhapatnam_01.jpg … _10.jpg  (real photos)
  ui-art/corner-waves.jpg      (AI decoration: background pattern / card corners)
  ui-art/corner-compass.jpg    (AI decoration: compass emblem / empty states)
  ui-art/corner-mountains.jpg  (AI decoration: divider strip / section banner)
  manifest.json    — per-image author, license, source URL
  raw_meta.json    — raw Wikimedia Commons metadata (build artifact)
  build_dataset.py — re-run to add more cities
```

## Licensing — read this before shipping

- **`photos/`** come from **Wikimedia Commons**. They are freely licensed
  (mostly CC BY / CC BY-SA), which means you **must credit the photographer**
  and link the license + source somewhere in the app (an "Image credits"
  screen or section is the standard way). Every photo's author, license and
  source URL is in `manifest.json` — wire that into your credits screen.
- **`ui-art/`** images are AI-generated for this project: no attribution
  needed, safe to use anywhere including commercial.
- **`un-tourism/`** — UN Tourism official bulk statistics (05_2026): 15 Excel
  files of country-level tourism data + `india_summary.json` (India arrivals,
  expenditure, source markets 2017–2024, extracted for the gov dashboard and
  pitch deck). See `un-tourism/DATA_README.md`.
- **`pois/`** — 312 real points of interest (Kashmir 80, Goa 80, Hyderabad 80,
  Visakhapatnam 72) from OpenStreetMap: name, category, lat/lng, hours/fees/
  website where mapped. ODbL — credit "© OpenStreetMap contributors".
  See `pois/README.md`.
- **`hotels/`** — 320 real accommodations (80 per city) from OpenStreetMap:
  name, type, lat/lng, stars/rooms/phone/website where mapped. **No prices or
  availability** — pair with a booking API at runtime. ODbL — same credit.
  See `hotels/README.md`.
- **`gov-data/`** — official Indian tourism statistics for the gov dashboard:
  state-wise domestic + foreign tourist visits 2023–2024 for all 36 States/UTs
  (millions), extracted from Ministry of Tourism's India Tourism Data
  Compendium 2025, Table 4.1.2. Cite the Ministry as source. See
  `gov-data/README.md`.

Do NOT mix these up: Commons photos always need credit; AI art never does.

## Adding more cities later

Edit the `QUERIES` dict in `build_dataset.py`, then run:

```bash
python3 build_dataset.py
```

It downloads ~1600px-wide images, skips tiny files, and records attribution
into `raw_meta.json`.

## Suggested use in the app

- `photos/` → destination detail pages, guide cards, discovery feed seeds
- `ui-art/` → decorative corners, empty states, section dividers
