# Virun Resources

Everything the app needs, in two parts. Grab a whole part, or just one folder —
each folder is self-contained (data + README + build script where applicable).

```
resources/
├── datasets/        # structured data (JSON / Excel) — no images
│   ├── pois/        # 312 places of interest, 4 cities (OpenStreetMap)
│   ├── hotels/      # 320 accommodations, 4 cities (OpenStreetMap)
│   ├── gov-data/    # official India tourism stats, 36 States/UTs (MoT)
│   └── un-tourism/  # UN Tourism bulk stats 05_2026 + India summary
└── images/          # visual assets
    ├── kashmir/photos/       # 10 real photos (Wikimedia Commons)
    ├── goa/photos/           # 10 real photos
    ├── hyderabad/photos/     # 10 real photos
    ├── visakhapatnam/photos/ # 10 real photos
    └── ui-art/               # 3 AI decorative images (no attribution needed)
```

## Extracting what you need

Copy any single folder — it works standalone:

```bash
cp -r resources/datasets/pois ./my-app/data/
cp -r resources/images/goa ./my-app/assets/
```

`manifest.json` (repo root) is the machine-readable index: every file with its
path, author/license (photos), and category. Point your credits screen at it.

## Licenses at a glance

| Folder | License | Rule |
|---|---|---|
| `images/*/photos/` | CC BY / CC BY-SA (Wikimedia Commons) | **Credit the photographer** — authors in `manifest.json` |
| `images/ui-art/` | AI-generated, ours | Free to use, no credit needed |
| `datasets/pois/`, `datasets/hotels/` | ODbL (OpenStreetMap) | Credit "© OpenStreetMap contributors" |
| `datasets/gov-data/`, `datasets/un-tourism/` | Public official statistics | Cite the source (MoT / UN Tourism) |

## Refreshing data

- Photos: `python3 build_dataset.py` (repo root; edit `QUERIES` to add cities)
- POIs: `resources/datasets/pois/build_pois.py` / `build_pois2.py`
- Hotels: `resources/datasets/hotels/build_hotels.py`

All scrapers need **no API key**.
