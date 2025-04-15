# data/upload/upload_to_supabase.py

import json
from pathlib import Path
from supabase import create_client, Client
import os

# === CONFIGURACIÓN ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === FUNCIONES AUXILIARES ===
def load_json_data(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

def upload(table_name, records):
    if not records:
        print(f"⚠️ No records to upload for table '{table_name}'")
        return

    try:
        response = supabase.table(table_name).insert(records).execute()
        if response.data:
            print(f"✅ Uploaded {len(response.data)} records to '{table_name}'")
        if response.error:
            print(f"❌ Error uploading to '{table_name}': {response.error}")
    except Exception as e:
        print(f"❌ Exception in upload to '{table_name}': {e}")

# === FUNCIÓN PRINCIPAL ===
def run_all_uploads():
    print("📡 Uploading data to Supabase...")

    base_path = Path("data/processed")

    files_to_upload = [
        ("districts", base_path / "insert_ready_districts_bcn.json"),
        ("districts", base_path / "insert_ready_districts_madrid.json"),
        ("neighbourhoods", base_path / "insert_ready_neighbourhoods_bcn.json"),
        ("neighbourhoods", base_path / "insert_ready_neighbourhoods_madrid.json"),
    ]

    for table, file_path in files_to_upload:
        if file_path.exists():
            data = load_json_data(file_path)
            upload(table, data)
        else:
            print(f"⚠️ File not found: {file_path}")

    print("✅ Upload to Supabase complete.")

if __name__ == "__main__":
    run_all_uploads()
