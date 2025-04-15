# tests/test_geometry_integrity.py

import json
from pathlib import Path
import pytest
from shapely import wkt

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data/raw"
PROCESSED_DIR = BASE_DIR / "data/processed"

# Utility to compare geometries from raw and processed files
def compare_geometries(raw_geom, processed_geom):
    try:
        shape_raw = wkt.loads(raw_geom)
        shape_processed = wkt.loads(processed_geom.replace("SRID=4326;", ""))
        return shape_raw.equals_exact(shape_processed, tolerance=0.00001)
    except Exception:
        return False

# Test: processed files exist and are not empty
@pytest.mark.parametrize("filename", [
    "insert_ready_districts_bcn.json",
    "insert_ready_neighbourhoods_bcn.json",
    "insert_ready_districts_madrid.json",
    "insert_ready_neighbourhoods_madrid.json",
])
def test_processed_file_not_empty(filename):
    path = PROCESSED_DIR / filename
    assert path.exists(), f"Missing file: {filename}"
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) > 0, f"{filename} is empty"

# Test: geometry preservation for the first Barcelona district
def test_bcn_district_geometry_preserved():
    raw_path = RAW_DIR / "bcn-districts.json"
    processed_path = PROCESSED_DIR / "insert_ready_districts_bcn.json"

    with raw_path.open(encoding="utf-8") as f:
        raw = json.load(f)
    with processed_path.open(encoding="utf-8") as f:
        processed = json.load(f)

    raw_geom = raw[0]["geometria_wgs84"]
    processed_geom = processed[0]["geom"]

    assert compare_geometries(raw_geom, processed_geom), "Geometry mismatch for Barcelona districts"

# Test: geometry preservation for the first Barcelona neighbourhood
def test_bcn_neighbourhood_geometry_preserved():
    raw_path = RAW_DIR / "bcn-neighbourhoods.json"
    processed_path = PROCESSED_DIR / "insert_ready_neighbourhoods_bcn.json"

    with raw_path.open(encoding="utf-8") as f:
        raw = json.load(f)
    with processed_path.open(encoding="utf-8") as f:
        processed = json.load(f)

    raw_geom = raw[0]["geometria_wgs84"]
    processed_geom = processed[0]["geom"]

    assert compare_geometries(raw_geom, processed_geom), "Geometry mismatch for Barcelona neighbourhoods"

# Test: geometry preservation for the first Madrid district
def test_madrid_district_geometry_preserved():
    raw_path = RAW_DIR / "madrid-districts.json"
    processed_path = PROCESSED_DIR / "insert_ready_districts_madrid.json"

    with raw_path.open(encoding="utf-8") as f:
        raw = json.load(f)
    with processed_path.open(encoding="utf-8") as f:
        processed = json.load(f)

    raw_geom = raw["objects"]["districts"]["geometries"][0]["properties"]["wkt"]
    processed_geom = processed[0]["geom"]

    assert compare_geometries(raw_geom, processed_geom), "Geometry mismatch for Madrid districts"

# Test: geometry preservation for the first Madrid neighbourhood
def test_madrid_neighbourhood_geometry_preserved():
    raw_path = RAW_DIR / "madrid-neighbourhoods.json"
    processed_path = PROCESSED_DIR / "insert_ready_neighbourhoods_madrid.json"

    with raw_path.open(encoding="utf-8") as f:
        raw = json.load(f)
    with processed_path.open(encoding="utf-8") as f:
        processed = json.load(f)

    raw_geom = raw["objects"]["neighbourhoods"]["geometries"][0]["properties"]["wkt"]
    processed_geom = processed[0]["geom"]

    assert compare_geometries(raw_geom, processed_geom), "Geometry mismatch for Madrid neighbourhoods"