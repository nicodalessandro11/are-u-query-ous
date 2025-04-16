# data/scripts/barcelona/load_indicators.py

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv
from supabase import create_client, Client

# Define base directory and city ID
BASE_DIR = Path(__file__).resolve().parents[3]
city_id = 1  # Barcelona
geo_level_id = 3  # Neighbourhood level for indicators

# === SETUP ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Add the project root to the Python path and import the emoji_logger
import sys
sys.path.insert(0, str(BASE_DIR))
from shared.emoji_logger import info, success, warning, error

def get_neighbourhood_map():
    """Fetch neighbourhood_id values from Supabase for Barcelona."""
    response = (
        supabase.table("neighbourhoods")
        .select("id, neighbourhood_code, district_id, city_id")
        .eq("city_id", city_id)
        .execute()
    )

    if not response.data:
        error("No neighbourhoods found for Barcelona (city_id = 1) in Supabase.")
        raise Exception("❌ No neighbourhoods found for Barcelona (city_id = 1) in Supabase.")

    return {(n["district_id"], n["neighbourhood_code"]): n["id"] for n in response.data}

def get_indicator_definition_id():
    """Fetch indicator_definition_id for Average gross household income."""
    response = (
        supabase.table("indicator_definitions")
        .select("id")
        .eq("name", "Average gross household income")
        .execute()
    )
    
    if not response.data:
        error("Indicator definition 'Average gross household income' not found in Supabase.")
        raise Exception("❌ Indicator definition 'Average gross household income' not found in Supabase.")
    
    return response.data[0]["id"]

def run():
    input_path = BASE_DIR / "data/raw/2022_atles_renda_bruta_llar.csv"
    output_path = BASE_DIR / "data/processed/insert_ready_indicators_bcn.json"

    info(f"Processing income data from {input_path}")
    
    # Read the CSV file
    df = pd.read_csv(input_path)
    success(f"Loaded {len(df)} rows from CSV")
    
    # Calculate mean income per neighborhood
    neighborhood_means = df.groupby(['Codi_Districte', 'Codi_Barri'])['Import_Renda_Bruta_€'].mean().reset_index()
    success(f"Calculated mean income for {len(neighborhood_means)} neighborhoods")
    
    neighbourhood_map = get_neighbourhood_map()
    indicator_def_id = get_indicator_definition_id()

    prepared_data = []
    errores = []

    for _, row in neighborhood_means.iterrows():
        try:
            district_code = int(row["Codi_Districte"])
            neighbourhood_code = int(row["Codi_Barri"])
            geo_id = neighbourhood_map.get((district_code, neighbourhood_code))

            if geo_id is None:
                errores.append(f"{district_code}-{neighbourhood_code}")
                continue

            value = float(row["Import_Renda_Bruta_€"])

            prepared_data.append(
                {
                    "indicator_def_id": indicator_def_id,
                    "geo_level_id": geo_level_id,
                    "geo_id": geo_id,
                    "year": 2022,
                    "value": value
                }
            )

        except Exception as e:
            errores.append(f"Error with row: {e}")
            warning(f"Error with row: {e}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_data, f, ensure_ascii=False, indent=2)

    success(f"Saved {len(prepared_data)} indicators to {output_path}")
    if errores:
        error(f"Issues with the following entries: {set(errores)}")

if __name__ == "__main__":
    run()
