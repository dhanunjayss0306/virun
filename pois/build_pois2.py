"""POI pass 2: Hyderabad + Visakhapatnam via quadrant-split bboxes.

Smaller bboxes avoid the 504s that killed the full-city queries.
Writes hyderabad.json / visakhapatnam.json next to kashmir.json / goa.json.
Data (c) OpenStreetMap contributors, ODbL.
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.expanduser("~/workspace/virun-assets/pois")
OVERPASS = "https://overpass-api.de/api/interpreter"
UA = {"User-Agent": "VirunPOIBot/1.0 (hackathon prototype)",
      "Content-Type": "application/x-www-form-urlencoded"}

# quadrants of the original city bboxes
AREAS = {
    "hyderabad": [
        (17.28, 78.38, 17.39, 78.49), (17.28, 78.49, 17.39, 78.60),
        (17.39, 78.38, 17.50, 78.49), (17.39, 78.49, 17.50, 78.60),
    ],
    "visakhapatnam": [
        (17.60, 83.15, 17.69, 83.25), (17.60, 83.25, 17.69, 83.35),
        (17.69, 83.15, 17.78, 83.25), (17.69, 83.25, 17.78, 83.35),
    ],
}

QUERY = """
[out:json][timeout:60];
(
  nwr["tourism"~"^(attraction|museum|viewpoint|artwork|gallery|theme_park|zoo|aquarium)$"]({bbox});
  nwr["historic"~"^(monument|memorial|castle|ruins|archaeological_site|building)$"]({bbox});
  nwr["leisure"~"^(park|garden|beach_resort)$"]({bbox});
  nwr["natural"="beach"]({bbox});
  nwr["amenity"="place_of_worship"]({bbox});
);
out center tags;
""".strip()


def overpass(bbox, retries=3):
    q = QUERY.format(bbox=",".join(map(str, bbox)))
    data = urllib.parse.urlencode({"data": q}).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(OVERPASS, data=data, headers=UA)
            with urllib.request.urlopen(req, timeout=100) as r:
                return json.load(r)
        except Exception as e:
            print("  retry %d: %s" % (attempt + 1, str(e)[:80]), flush=True)
            time.sleep(10)
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
        for key, cat in (("hindu", "temple"), ("christian", "church"),
                         ("muslim", "mosque"), ("islam", "mosque"),
                         ("sikh", "gurudwara"), ("buddhist", "monastery")):
            if key in rel: return cat
        return "worship"
    return "place"


def main():
    for city, bboxes in AREAS.items():
        seen = {}
        for bbox in bboxes:
            print("[%s] quadrant %s ..." % (city, bbox), flush=True)
            els = overpass(bbox).get("elements", [])
            print("  got %d elements" % len(els), flush=True)
            for el in els:
                tags = el.get("tags", {})
                name = tags.get("name") or tags.get("name:en")
                if not name: continue
                lat = el.get("lat") or (el.get("center") or {}).get("lat")
                lon = el.get("lon") or (el.get("center") or {}).get("lon")
                if lat is None or lon is None: continue
                key = (name.strip().lower(), round(lat, 4), round(lon, 4))
                if key in seen: continue
                seen[key] = {
                    "name": name.strip(), "category": categorize(tags),
                    "lat": round(lat, 6), "lng": round(lon, 6),
                    "details": {k: tags[k] for k in
                                ("opening_hours", "fee", "website", "wikipedia",
                                 "description", "religion", "tourism", "historic")
                                if k in tags},
                }
            time.sleep(4)
        pois = sorted(seen.values(), key=lambda p: p["name"])[:80]
        with open(os.path.join(BASE, "%s.json" % city), "w") as f:
            json.dump({"city": city, "count": len(pois),
                       "source": "OpenStreetMap (c) contributors, ODbL",
                       "pois": pois}, f, indent=1, ensure_ascii=False)
        cats = {}
        for p in pois: cats[p["category"]] = cats.get(p["category"], 0) + 1
        print("[%s] wrote %d POIs %s" % (city, len(pois), cats), flush=True)
    print("PASS 2 DONE", flush=True)


main()
