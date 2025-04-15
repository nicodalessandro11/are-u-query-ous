# data/scripts/barcelona/load_neighbourhoods.py

import json
from shapely import wkt
from pathlib import Path
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# === SETUP ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_DIR = Path(__file__).resolve().parents[3]
city_id = 1  # Barcelona

def get_district_map():
    """Fetch real district_id values from Supabase for Barcelona."""
    response = supabase.table("districts") \
        .select("id, name, city_id") \
        .eq("city_id", city_id) \
        .execute()

    if not response.data:
        raise Exception("❌ No districts found for Barcelona (city_id = 1) in Supabase.")
    
    # Mapping by district name (case-sensitive)
    return {
        d["name"]: d["id"]
        for d in response.data
    }

def run():
    input_path = BASE_DIR / "data/raw/bcn-neighbourhoods.json"
    output_path = BASE_DIR / "data/processed/insert_ready_neighbourhoods_bcn.json"

    with input_path.open(encoding="utf-8") as f:
        raw_data = json.load(f)

    try:
        district_map = get_district_map()
    except Exception as e:
        print(f"❌ Error fetching district map: {e}")
        return

    prepared_data = []
    errores = []

    for b in raw_data:
        try:
            name = b["nom_barri"].strip()
            code = b["codi_barri"].strip().zfill(2)
            district_name = b["nom_districte"].strip()
            wkt_geom = b["geometria_wgs84"].strip()

            district_id = district_map.get(district_name)
            if not district_id:
                errores.append(district_name)
                continue

            # Validar geometría
            _ = wkt.loads(wkt_geom)

            prepared_data.append({
                "name": name,
                "neighbourhood_code": code,
                "district_id": district_id,
                "city_id": city_id,
                "geom": f"SRID=4326;{wkt_geom}"
            })

        except Exception as e:
            errores.append(name)
            print(f"⚠️ Error in neighbourhood '{name}': {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} Barcelona neighbourhoods to {output_path}")

    if errores:
        print("❗ Issues with the following entries:", set(errores))

if __name__ == "__main__":
    run()
