# ETL Pipeline Structure for Open Geodata Project

This document describes the standardized ETL process for integrating open geospatial datasets from multiple cities into a unified Supabase database.

The pipeline is designed to ensure modularity, traceability, and scalability for loading datasets into a web application focused on everyday urban data.

---

## 🔁 Standard ETL Flow

Each dataset follows the same three-phase process:

1. **Extract**: The raw dataset (e.g., CSV or GeoJSON) is manually or programmatically downloaded and saved in `data/raw/`.

2. **Transform**: The dataset is cleaned, normalized, and transformed to match the database schema. Transformed data is saved to `data/processed/`.

3. **Load**: The processed data is uploaded to Supabase using the Supabase Python client.

---

## 📂 Project Structure

```
project/
│
├── data/
│   ├── raw/               # Original unprocessed datasets
│   ├── processed/         # Transformed datasets ready for upload
│   ├── __init__.py        # Package initialization
│   ├── scripts/
│   │   ├── barcelona/
│   │   │   └── load_[table_name].py    # ETL scripts for Barcelona datasets tables
│   │   │   └── ...
│   │   ├──madrid/
│   │   │    └── load_[table_name].py    # ETL scripts for Madrid datasets tables
│   │   │    └── ...
│   │   └── upload/
│   │       └── upload_to_supabase.py    # Upload logic using Supabase SDK
│   ├── ingest_data.py    # Main orchestrator script to run ETLs, tests, and uploads
│   ├── tests/            # Integrity and schema validation tests
│   │   └── __init__.py   # Test package initialization
```

---

## 🚀 Orchestration Logic (`run_all.py`)

This script:

- Runs ETLs for districts and neighbourhoods
- Uploads results to Supabase
- Executes pytest validation tests
- Continues uploading only if all tests pass

### Simplified Execution Flow Example:

```python
bcn_d.run()         # Barcelona districts
mad_d.run()         # Madrid districts
upload_to_supabase.run_district_upload()

bcn_n.run()         # Barcelona neighbourhoods
mad_n.run()         # Madrid neighbourhoods
run_tests()         # Pytest validations

upload_to_supabase.run_neighbourhood_upload()

# Continue with other datasets...
```

---

## ✅ Benefits of This Structure

- **Modular**: Each dataset is handled by an independent ETL script.
- **Maintainable**: Easy to update or extend without affecting the entire pipeline.
- **Automatable**: Ready for scheduled or CI/CD-based execution.
- **Testable**: Includes validation stage before uploading any data.

---

## 📌 Naming Conventions

- Raw files: `data/raw/[city]_[dataset].csv`
- Processed files: `data/processed/[city]_[dataset]_clean.csv`
- ETL script: `data/scripts/[city]/load_[table_name].py`

---

## 🛠 Technologies Used

- **Pandas**: For data manipulation
- **Shapely** (optional): For geometry handling
- **Supabase Python SDK**: For data upload
- **Pytest**: For data integrity tests

---

## 👀 Example Datasets

- Museums, schools, public libraries
- Bus stops, metro stations, markets
- Population by district, average income
- Parks and green zones

---

## 🔒 Licensing & Attribution

Always verify dataset licensing. Most datasets used are:
- **CC BY 4.0** (Barcelona Open Data)
- **Open Municipal License** (Madrid)

Attribution must be retained when integrating or displaying data in the application.
