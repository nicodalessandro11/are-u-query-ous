# data/scripts/madrid/load_districts.py

import geopandas as gpd
from shapely.wkt import dumps
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[3]  # up to the root of the project

def run():
    input_path = BASE_DIR / "data/raw/madrid-districts.json"
    output_path = BASE_DIR / "data/processed/insert_ready_districts_madrid.json"
    city_id = 2  # Madrid

    gdf = gpd.read_file(input_path)

    prepared_data = []

    for _, row in gdf.iterrows():
        props = row.get("properties", row)

        raw_name = props.get("NOMBRE", props.get("name", "")).strip()
        raw_code = props.get("COD_DIS_TX", "").strip()

        if not raw_code:
            print(f"⚠️ District '{raw_name}' has empty code. Skipping.")
            continue

        name = raw_name
        code = str(raw_code).zfill(2)

        try:
            geom_wkt = dumps(row.geometry)
        except Exception as e:
            print(f"⚠️ Error in district '{name}': {e}")
            continue

        prepared_data.append({
            "name": name,
            "district_code": code,
            "city_id": city_id,
            "geom": f"SRID=4326;{geom_wkt}"
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} Madrid districts to {output_path}")

if __name__ == "__main__":
    run()
