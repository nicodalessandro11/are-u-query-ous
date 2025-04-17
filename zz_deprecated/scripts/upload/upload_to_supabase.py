# data/upload/upload_to_supabase.py

import json
from pathlib import Path
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[3]  # up to the root of the project

# === CONFIGURATION ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === AUXILIARY FUNCTIONS ===
def load_json_data(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

def upload(table_name, records):
    if not records:
        print(f"⚠️ No records to upload for table '{table_name}'")
        return

    try:
        response = supabase.table(table_name).insert(records).execute()

        if hasattr(response, "status_code"):
            print(f"📦 [{table_name}] Status code: {response.status_code}")

        if hasattr(response, "data") and response.data:
            print(f"✅ Uploaded {len(response.data)} records to '{table_name}'")
        else:
            print(f"⚠️ No data returned from '{table_name}'. Possible silent error.")
            print(f"📄 Full response: {response}")
    except Exception as e:
        print(f"❌ Exception during upload to '{table_name}': {e}")
        import traceback
        traceback.print_exc()

# === UPLOAD SEPARATED BLOCKS ===
def run_district_upload():
    print("📤 Uploading districts to Supabase...")
    base_path = Path("data/processed")
    files = [
        ("districts", BASE_DIR / base_path / "insert_ready_districts_bcn.json"),
        ("districts", BASE_DIR / base_path / "insert_ready_districts_madrid.json"),
    ]

    for table, file_path in files:
        if file_path.exists():
            data = load_json_data(file_path)
            upload(table, data)
        else:
            print(f"⚠️ File not found: {file_path}")

def run_neighbourhood_upload():
    print("📤 Uploading neighbourhoods to Supabase...")
    base_path = Path("data/processed")
    files = [
        ("neighbourhoods", BASE_DIR / base_path / "insert_ready_neighbourhoods_bcn.json"),
        ("neighbourhoods", BASE_DIR / base_path / "insert_ready_neighbourhoods_madrid.json"),
    ]

    for table, file_path in files:
        if file_path.exists():
            data = load_json_data(file_path)
            upload(table, data)
        else:
            print(f"⚠️ File not found: {file_path}")

def run_point_feature_upload():
    print("📤 Uploading point features to Supabase...")
    base_path = Path("data/processed")
    files = [
        ("point_features", BASE_DIR / base_path / "insert_ready_point_features_bcn.json"),
        ("point_features", BASE_DIR / base_path / "insert_ready_point_features_madrid.json"),
    ]

    for table, file_path in files:
        if file_path.exists():
            data = load_json_data(file_path)
            upload(table, data)
        else:
            print(f"⚠️ File not found: {file_path}")

def run_indicator_upload():
    print("📤 Uploading indicators to Supabase...")
    base_path = Path("data/processed")
    files = [
        ("indicators", BASE_DIR / base_path / "insert_ready_indicators_bcn.json"),
        ("indicators", BASE_DIR / base_path / "insert_ready_indicators_madrid.json"),
    ]

    for table, file_path in files:
        if file_path.exists():
            data = load_json_data(file_path)
            upload(table, data)
        else:
            print(f"⚠️ File not found: {file_path}")

# === GENERAL FUNCTION
def run_all_uploads():
    print("📡 Uploading data to Supabase...")
    run_district_upload()
    run_neighbourhood_upload()
    run_point_feature_upload()
    print("✅ Upload to Supabase complete.")

if __name__ == "__main__":
    run_all_uploads()
