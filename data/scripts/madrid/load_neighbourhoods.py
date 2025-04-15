import geopandas as gpd
from shapely.wkt import dumps
from pathlib import Path
import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# === SETUP ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_DIR = Path(__file__).resolve().parents[3]
city_id = 2  # Madrid

def get_district_map():
    """Fetch real district_id values from Supabase for Madrid."""
    response = supabase.table("districts") \
        .select("id, district_code, city_id") \
        .eq("city_id", city_id) \
        .execute()
    
    if not response.data:
        raise Exception("❌ No districts found for Madrid (city_id = 2) in Supabase.")
    
    return {
        d["district_code"]: d["id"]
        for d in response.data
    }

def run():
    input_path = BASE_DIR / "data/raw/madrid-neighbourhoods.json"
    output_path = BASE_DIR / "data/processed/insert_ready_neighbourhoods_madrid.json"

    gdf = gpd.read_file(input_path)
    prepared_data = []
    errores = []

    try:
        district_map = get_district_map()
    except Exception as e:
        print(f"❌ Error fetching district map: {e}")
        return

    for _, row in gdf.iterrows():
        props = row.get("properties", row)

        raw_name = props.get("NOMBRE", "Unnamed").strip()
        raw_code = props.get("COD_BAR", "").strip()
        raw_district_code = props.get("COD_DIS_TX", "").strip()

        if not raw_code or not raw_district_code:
            print(f"⚠️ Missing code or district_code in '{raw_name}'. Skipping.")
            continue

        code = raw_code.zfill(2)
        district_code = raw_district_code.zfill(2)

        district_id = district_map.get(district_code)
        if not district_id:
            errores.append(district_code)
            continue

        try:
            geom_wkt = dumps(row.geometry)
        except Exception as e:
            print(f"⚠️ Error in neighbourhood '{raw_name}': {e}")
            continue

        prepared_data.append({
            "name": raw_name,
            "neighbourhood_code": code,
            "district_id": district_id,
            "city_id": city_id,
            "geom": f"SRID=4326;{geom_wkt}"
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} Madrid neighbourhoods to {output_path}")
    if errores:
        print("❗ Some district codes were not matched:", set(errores))

if __name__ == "__main__":
    run()
