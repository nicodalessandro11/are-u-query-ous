# data/scripts/barcelona/load_districts.py

import json
import requests
from shapely import wkt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]  # up to the root of the project

def run():
    input_url= "https://xwzmngtodqmipubwnceh.supabase.co/storage/v1/object/public/data/barcelona/bcn-districts.json"
    output_path = BASE_DIR / "data/processed/insert_ready_districts_bcn.json"
    city_id = 1  # Barcelona

    # 📥 Download JSON file from URL
    response = requests.get(input_url)
    response.raise_for_status()
    raw_data = response.json()


    prepared_data = []

    for d in raw_data:
        try:
            name = d["nom_districte"].strip()
            code = d["Codi_Districte"].strip()
            wkt_geom = d["geometria_wgs84"].strip()

            try:
                code = int(code)
            except ValueError:
                print(f"⚠️ Invalid district code '{code}' in '{name}'. Skipping.")
                continue

            # Validate WKT
            _ = wkt.loads(wkt_geom)

            prepared_data.append({
                "name": name,
                "district_code": code,
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
