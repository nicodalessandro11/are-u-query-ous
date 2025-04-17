# scripts/etl/ingest.py

"""
Script: ingest.py

This script runs the full ETL + Validation + Upload workflow in this order:
1. Districts
2. Neighbourhoods (requires districts)
3. Point Features
4. Indicators

Author: Nico D'Alessandro (nico.dalessandro@gmail.com)
Date: 2025-04-17
"""

import subprocess
import sys
import argparse
from scripts.etl.barcelona import load_districts as bcn_d
from scripts.etl.barcelona import load_neighbourhoods as bcn_n
# from scripts.etl.barcelona import load_point_features as bcn_p
# from scripts.etl.barcelona import load_indicators as bcn_i
from scripts.etl.madrid import load_districts as mad_d
from scripts.etl.madrid import load_neighbourhoods as mad_n
# from scripts.etl.madrid import load_point_features as mad_p
# from scripts.etl.madrid import load_indicators as mad_i
from scripts.etl.upload import upload_to_supabase as upload

# =====================
# Utility
# =====================

def run_tests(test_target: str):
    print(f"🧪 Running test suite for `{test_target}`...")
    result = subprocess.run(["pytest", f"tests/{test_target}"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Tests failed. Upload aborted.")
        sys.exit(1)
    print("✅ All tests passed.\n")

# =====================
# Base Data Pipeline
# =====================

def process_base_data():
    print("📊 Running BASE DATA ETLs...")

    # ETL: Districts
    bcn_d.run()
    mad_d.run()
    print("✅ District ETLs complete.")

    # Upload: Districts
    upload.run_district_upload()

    # ETL: Neighbourhoods
    bcn_n.run()
    mad_n.run()
    print("✅ Neighbourhood ETLs complete.")

    # Upload: Neighbourhoods
    upload.run_neighbourhood_upload()

    # Test: Geometry + Files
    run_tests("test_base_data_upload.py")

# =====================
# Point Feature Pipeline
# =====================

def process_point_features():
    print("📍 Running POINT FEATURE ETLs...")

    # ETL: Point Features
    # bcn_p.run()
    # mad_p.run()

    # Test: Geometry + Files
    # run_tests("test_point_features_upload.py")

    # Upload: Supabase
    # upload.run_point_feature_upload()

# =====================
# Indicator Pipeline
# =====================

def process_indicators():
    print("📈 Running INDICATOR ETLs...")

    # ETL: Indicators
    # bcn_i.run()
    # mad_i.run()

    # Test: Values and structure
    # run_tests("test_indicator_upload.py")

    # Upload: Supabase
    # upload.run_indicator_upload()

# =====================
# Entry Point
# =====================

def run_all():
    process_base_data()
    process_point_features()
    process_indicators()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full ETL pipeline for Are-U-Query-ous.")
    parser.add_argument("--skip-upload", action="store_true", help="Run ETLs only (skip Supabase upload)")

    args = parser.parse_args()

    if args.skip_upload:
        print("⚙️ Developer mode: running ETLs and tests only (no upload)...")
        bcn_d.run()
        mad_d.run()
        bcn_n.run()
        mad_n.run()
        run_tests("test_base_data_upload.py")
        # bcn_p.run()
        # mad_p.run()
        # run_tests("test_point_features_upload.py")
        # bcn_i.run()
        # mad_i.run()
        # run_tests("test_indicator_upload.py")
        print("✅ Developer ETL and test run complete.")
    else:
        run_all()
