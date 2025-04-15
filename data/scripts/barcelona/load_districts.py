# data/scripts/barcelona/load_districts.py

import json
from shapely import wkt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]  # up to the root of the project

def run():
    input_path = BASE_DIR / "data/raw/bcn-districts.json"
    output_path = BASE_DIR / "data/processed/insert_ready_districts_bcn.json"
    city_id = 1  # Barcelona

    with input_path.open(encoding="utf-8") as f:
        raw_data = json.load(f)

    prepared_data = []

    for d in raw_data:
        try:
            name = d["nom_districte"].strip()
            code = d["Codi_Districte"].strip().zfill(2)
            wkt_geom = d["geometria_wgs84"].strip()

            # Validate WKT
            _ = wkt.loads(wkt_geom)

            prepared_data.append({
                "name": name,
                "code": code,
                "city_id": city_id,
                "geom": f"SRID=4326;{wkt_geom}"
            })

        except Exception as e:
            print(f"⚠️ Error in district '{d.get('nom_districte', 'unknown')}': {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} districts to {output_path}")

if __name__ == "__main__":
    run()
