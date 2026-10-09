"""Build Virun city POI dataset from OpenStreetMap (Overpass API).

Queries tourism/historic/leisure/beach/place_of_worship features inside
per-city bounding boxes, keeps named features, dedupes, and writes
~/workspace/virun-assets/pois/<city>.json

Data (c) OpenStreetMap contributors, ODbL — attribution required.
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.expanduser("~/workspace/virun-assets/pois")
OVERPASS = "https://overpass-api.de/api/interpreter"
UA = {"User-Agent": "VirunPOIBot/1.0 (hackathon prototype; contact: dhanunjay)",
      "Content-Type": "application/x-www-form-urlencoded"}

# (south, west, north, east)
AREAS = {
    "kashmir": [
        (33.93, 74.65, 34.23, 74.95),   # Srinagar: Dal Lake, Mughal gardens, old city
        (33.98, 74.31, 34.12, 74.45),   # Gulmarg
        (33.95, 75.25, 34.08, 75.38),   # Pahalgam
    ],
    "goa": [
        (15.45, 73.70, 15.65, 73.85),   # North Goa coast: Baga, Calangute, Anjuna
        (15.40, 73.75, 15.55, 73.90),   # Old Goa churches + Panaji
    ],
    "hyderabad": [(17.28, 78.38, 17.50, 78.60)],
    "visakhapatnam": [(17.60, 83.15, 17.78, 83.35)],
}

QUERY = """
[out:json][timeout:90];
(
  nwr["tourism"~"^(attraction|museum|viewpoint|artwork|gallery|theme_park|zoo|aquarium)$"]({bbox});
  nwr["historic"]({bbox});
  nwr["leisure"~"^(park|garden|beach_resort)$"]({bbox});
  nwr["natural"="beach"]({bbox});
  nwr["amenity"="place_of_worship"]({bbox});
);
out center tags;
""".strip()


def overpass(bbox, retries=2):
    q = QUERY.format(bbox=",".join(map(str, bbox)))
    data = urllib.parse.urlencode({"data": q}).encode()
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(OVERPASS, data=data, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except Exception as e:
            print("  overpass error (attempt %d): %s" % (attempt + 1, str(e)[:100]))
            time.sleep(8)
    return {"elements": []}


def categorize(tags):
    t = tags.get("tourism")
    if t == "museum": return "museum"
    if t == "viewpoint": return "viewpoint"
    if t in ("artwork", "gallery"): return "art"
    if t in ("theme_park", "zoo", "aquarium"): return "entertainment"
    if t == "attraction": return "attraction"
    if "historic" in tags: return "historic"
    if tags.get("natural") == "beach": return "beach"
    if tags.get("leisure") in ("park", "garden", "beach_resort"): return "park"
    if tags.get("amenity") == "place_of_worship":
        rel = (tags.get("religion") or "").lower()
        if "hindu" in rel: return "temple"
        if "christian" in rel: return "church"
        if "muslim" in rel or "islam" in rel: return "mosque"
        if "sikh" in rel: return "gurudwara"
        if "buddhist" in rel: return "monastery"
        return "worship"
    return "place"


def main():
    os.makedirs(BASE, exist_ok=True)
    grand = 0
    for city, bboxes in AREAS.items():
        seen = {}
        for bbox in bboxes:
            print("[%s] querying bbox %s ..." % (city, bbox), flush=True)
            res = overpass(bbox)
            els = res.get("elements", [])
            print("  got %d elements" % len(els), flush=True)
            for el in els:
                tags = el.get("tags", {})
                name = tags.get("name") or tags.get("name:en")
                if not name:
                    continue
                lat = el.get("lat") or (el.get("center") or {}).get("lat")
                lon = el.get("lon") or (el.get("center") or {}).get("lon")
                if lat is None or lon is None:
                    continue
                key = (name.strip().lower(), round(lat, 4), round(lon, 4))
                if key in seen:
                    continue
                seen[key] = {
                    "name": name.strip(),
                    "category": categorize(tags),
                    "lat": round(lat, 6),
                    "lng": round(lon, 6),
                    "details": {k: tags[k] for k in
                                ("opening_hours", "fee", "website", "wikipedia",
                                 "description", "religion", "tourism", "historic")
                                if k in tags},
                }
            time.sleep(3)  # be nice to the public API
        pois = sorted(seen.values(), key=lambda p: p["name"])
        # cap at 80 per city, keep alphabetical spread
        pois = pois[:80]
        path = os.path.join(BASE, "%s.json" % city)
        with open(path, "w") as f:
            json.dump({"city": city, "count": len(pois),
                       "source": "OpenStreetMap (c) contributors, ODbL",
                       "pois": pois}, f, indent=1, ensure_ascii=False)
        grand += len(pois)
        cats = {}
        for p in pois:
            cats[p["category"]] = cats.get(p["category"], 0) + 1
        print("[%s] wrote %d POIs %s" % (city, len(pois), cats), flush=True)
    print("TOTAL %d POIs" % grand, flush=True)


main()
