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
        name = row.get("NOMBRE", row.get("name", "Unnamed")).strip()
        code = str(row.get("CODDIST", row.get("CODIGO", "")).strip()).zfill(2)
        try:
            geom_wkt = dumps(row.geometry)
        except Exception as e:
            print(f"⚠️ Error in district '{name}': {e}")
            continue

        prepared_data.append({
            "name": name,
            "code": code,
            "city_id": city_id,
            "geom": f"SRID=4326;{geom_wkt}"
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} Madrid districts to {output_path}")

if __name__ == "__main__":
    run()
