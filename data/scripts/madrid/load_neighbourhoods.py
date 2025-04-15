# data/scripts/madrid/load_neighbourhoods.py

import geopandas as gpd
from shapely.wkt import dumps
from pathlib import Path
import json

# Manual mapping of district codes to Supabase district IDs
district_map = {
    "01": 11, "02": 12, "03": 13, "04": 14, "05": 15,
    "06": 16, "07": 17, "08": 18, "09": 19, "10": 20,
    "11": 21, "12": 22, "13": 23, "14": 24, "15": 25,
    "16": 26, "17": 27, "18": 28, "19": 29, "20": 30,
    "21": 31
}

def run():
    input_path = Path("data/raw/madrid-neighbourhoods.json")
    output_path = Path("data/processed/insert_ready_neighbourhoods_madrid.json")

    gdf = gpd.read_file(input_path)
    prepared_data = []
    errores = []

    for _, row in gdf.iterrows():
        name = row.get("NOMBRE", "Unnamed").strip()
        code = str(row.get("CODBAR", row.get("CODIGO", "")).strip()).zfill(2)
        district_code = str(row.get("CODDIS", "")).zfill(2)

        district_id = district_map.get(district_code)
        if not district_id:
            errores.append(district_code)
            continue

        try:
            geom_wkt = dumps(row.geometry)
        except Exception as e:
            print(f"⚠️ Error in neighbourhood '{name}': {e}")
            continue

        prepared_data.append({
            "name": name,
            "code": code,
            "district_id": district_id,
            "geom": f"SRID=4326;{geom_wkt}"
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} Madrid neighbourhoods to {output_path}")
    if errores:
        print("❗ Some district codes were not found:", set(errores))

if __name__ == "__main__":
    run()
