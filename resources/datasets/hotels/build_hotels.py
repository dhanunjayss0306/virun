"""Extract hotel/accommodation POIs from OpenStreetMap for Virun cities.

tourism=hotel|guest_house|hostel|motel|resort|apartment|chalet|lodge
inside quadrant bboxes (same 504-resistant approach as POIs).

Writes ~/workspace/virun-assets/hotels/<city>.json
Data (c) OpenStreetMap contributors, ODbL — attribution required.
No API key needed.
"""
import json, os, time, urllib.request, urllib.parse

BASE = os.path.expanduser("~/workspace/virun-assets/hotels")
OVERPASS = "https://overpass-api.de/api/interpreter"
UA = {"User-Agent": "VirunPOIBot/1.0 (hackathon prototype)",
      "Content-Type": "application/x-www-form-urlencoded"}

AREAS = {
    "kashmir": [
        (33.93, 74.65, 34.23, 74.95),   # Srinagar
        (33.98, 74.31, 34.12, 74.45),   # Gulmarg
        (33.95, 75.25, 34.08, 75.38),   # Pahalgam
    ],
    "goa": [
        (15.45, 73.70, 15.65, 73.85),   # North Goa coast
        (15.40, 73.75, 15.55, 73.90),   # Old Goa + Panaji
    ],
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
  nwr["tourism"~"^(hotel|guest_house|hostel|motel|resort|apartment|chalet|lodge)$"]({bbox});
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


def main():
    os.makedirs(BASE, exist_ok=True)
    grand = 0
    for city, bboxes in AREAS.items():
        seen = {}
        for bbox in bboxes:
            print("[%s] bbox %s ..." % (city, bbox), flush=True)
            els = overpass(bbox).get("elements", [])
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
                addr = " ".join(tags.get(k, "") for k in
                                ("addr:housenumber", "addr:street", "addr:suburb",
                                 "addr:city")).strip()
                seen[key] = {
                    "name": name.strip(),
                    "type": tags.get("tourism", "hotel"),
                    "lat": round(lat, 6),
                    "lng": round(lon, 6),
                    "stars": tags.get("stars"),
                    "rooms": tags.get("rooms"),
                    "phone": tags.get("phone") or tags.get("contact:phone"),
                    "website": tags.get("website") or tags.get("contact:website"),
                    "address": addr or None,
                }
            time.sleep(4)
        hotels = sorted(seen.values(), key=lambda h: h["name"])[:80]
        with open(os.path.join(BASE, "%s.json" % city), "w") as f:
            json.dump({"city": city, "count": len(hotels),
                       "source": "OpenStreetMap (c) contributors, ODbL",
                       "hotels": hotels}, f, indent=1, ensure_ascii=False)
        grand += len(hotels)
        print("[%s] wrote %d hotels" % (city, len(hotels)), flush=True)
    print("HOTELS DONE: %d total" % grand, flush=True)


main()
