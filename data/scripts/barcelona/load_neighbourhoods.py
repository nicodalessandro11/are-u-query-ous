# data/scripts/barcelona/load_neighbourhoods.py

import json
from shapely import wkt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]  # up to the root of the project

# Mapeo de nombre de distrito a ID en Supabase
district_map = {
    "Ciutat Vella": 1,
    "Eixample": 2,
    "Sants-Montjuïc": 3,
    "Les Corts": 4,
    "Sarrià-Sant Gervasi": 5,
    "Gràcia": 6,
    "Horta-Guinardó": 7,
    "Nou Barris": 8,
    "Sant Andreu": 9,
    "Sant Martí": 10
}

def run():
    input_path = BASE_DIR / "data/raw/bcn-neighbourhoods.json"
    output_path = BASE_DIR / "data/processed/insert_ready_neighbourhoods_bcn.json"

    with input_path.open(encoding="utf-8") as f:
        raw_data = json.load(f)

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
                "code": code,
                "district_id": district_id,
                "geom": f"SRID=4326;{wkt_geom}"
            })

        except Exception as e:
            errores.append(name)
            print(f"⚠️ Error in neighbourhood '{name}': {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} neighbourhoods to {output_path}")

    if errores:
        print("❗ Issues with the following entries:", set(errores))

if __name__ == "__main__":
    run()
