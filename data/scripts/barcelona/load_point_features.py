# data/scripts/barcelona/load_point_features.py

import pandas as pd
from shapely.geometry import Point
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
city_id = 1  # Barcelona
geo_level_id = 3  # Neighbourhood level for point features

# === MAPEO DE CATEGORÍAS ===
feature_type_map = {
    "Biblioteques de Barcelona": "Bibliotecas",
    "Ateneus": "Centros culturales",
    "Grans auditoris": "Auditorios",
    "Espais d'interès patrimonial": "Espacios patrimoniales",
    "Fàbriques de Creació": "Fábricas de creación",
    "Centres cívics": "Centros culturales",
    "Cases de la Festa": "Centros culturales",
    "Museus i col·leccions": "Museos",
    "Cinemes": "Cines",
    "Centres d'exposicions": "Centros de exposiciones",
    "Arxius de districte": "Archivos",
    "Sales de música en viu": "Salas de música en vivo",
    "Arxius i biblioteques patrimonials": "Archivos",
    "Sales d'arts escèniques": "Salas de artes escénicas",
}


def get_neighbourhood_map():
    """Fetch neighbourhood_id values from Supabase for Barcelona."""
    response = (
        supabase.table("neighbourhoods")
        .select("id, neighbourhood_code, district_id, city_id")
        .eq("city_id", city_id)
        .execute()
    )

    if not response.data:
        raise Exception("❌ No neighbourhoods found for Barcelona (city_id = 1) in Supabase.")

    return {(n["district_id"], n["neighbourhood_code"]): n["id"] for n in response.data}


def get_feature_type_id_map():
    """Fetch feature_type_id values from Supabase for normalized categories."""
    response = supabase.table("feature_types").select("id, name").execute()
    if not response.data:
        raise Exception("❌ No feature types found in Supabase.")
    return {item["name"]: item["id"] for item in response.data}


def run():
    input_path = BASE_DIR / "data/raw/Equipaments_del_mapa.csv"
    output_path = BASE_DIR / "data/processed/insert_ready_point_features_bcn.json"

    df = pd.read_csv(input_path)
    neighbourhood_map = get_neighbourhood_map()
    feature_type_id_map = get_feature_type_id_map()

    prepared_data = []
    errores = []

    for _, row in df.iterrows():
        try:
            district_code = int(row["Codi_Districte"])
            neighbourhood_code = int(row["Codi_Barri"])
            geo_id = neighbourhood_map.get((district_code, neighbourhood_code))

            if geo_id is None:
                errores.append(f"{district_code}-{neighbourhood_code}")
                continue

            lat = float(row["Latitud"])
            lon = float(row["Longitud"])
            geom = Point(lon, lat).wkt

            original_type = row["Tipus_Equipament"].strip()
            normalized_type = feature_type_map.get(original_type)

            if normalized_type is None or normalized_type not in feature_type_id_map:
                errores.append(original_type)
                continue

            feature_type_id = feature_type_id_map[normalized_type]
            name = row["Nom_Equipament"].strip()

            # Group all other fields as JSON properties
            properties = {
                k: row[k]
                for k in row.index
                if k
                not in [
                    "Tipus_Equipament",
                    "Nom_Equipament",
                    "Latitud",
                    "Longitud",
                    "Codi_Barri",
                    "Codi_Districte",
                    "Id_Equipament",
                    "Te_Subseus",
                    "Id_Seu_Principal",
                    "Es_subseu_de",
                    "Es_seu_principal",
                    "Nom_Districte",
                    "Nom_Barri",
                    "Notes_Equipament",
                ]
            }

            prepared_data.append(
                {
                    "feature_type_id": feature_type_id,
                    "name": name,
                    "latitude": lat,
                    "longitude": lon,
                    "geom": f"SRID=4326;{geom}",
                    "geo_level_id": geo_level_id,
                    "geo_id": geo_id,
                    "properties": properties,
                }
            )

        except Exception as e:
            errores.append(row.get("Nom_Equipament", "Unknown"))
            print(f"⚠️ Error with row: {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(prepared_data)} point features to {output_path}")
    if errores:
        print("❗ Issues with the following entries:", set(errores))


if __name__ == "__main__":
    run()
