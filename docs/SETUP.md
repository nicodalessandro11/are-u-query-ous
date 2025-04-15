# 🛠️ Project: Are-U-Query-ous – Setup Guide

This document walks you through the full setup process to run the project from scratch.

---

## ✅ System Requirements

Make sure you have the following installed:

### 🐍 Python 3.10 or higher

> It's recommended to use a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### 🐘 PostgreSQL Client (`psql`)

> Required to run SQL scripts (`schema.sql`, `views.sql`, `seed.sql`) against Supabase.

#### ▪ Ubuntu / Debian

```bash
sudo apt update
sudo apt install postgresql-client
```

#### ▪ macOS (Homebrew)

```bash
brew install postgresql
```

#### ▪ Windows

- Install PostgreSQL from: https://www.postgresql.org/download/windows/
- Ensure `psql` is added to your `PATH`
- Alternatively, use WSL with a Linux distribution

---

### ⚙️ `make`

Used to automate the full setup process:

- **Linux/macOS**: pre-installed by default
- **Windows**: install [Git Bash](https://gitforwindows.org/) or use WSL

---

## 🔐 Environment Variables

Create a `.env` file in the root of the project (or copy from the provided template):

```bash
cp .env.example .env
```

Fill in your Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
DATABASE_URL=postgresql://user:password@host:port/database
```

---

## 🚀 Run the Full Setup

```bash
make all
```

This will automatically:

1. Run SQL scripts (`schema.sql`, `views.sql`, `seed.sql`)
2. Process geospatial data using ETL scripts (districts + neighbourhoods)
3. Validate geometry integrity with automated tests (`pytest`)
4. Upload data to Supabase via the service role key
5. Clean up temp files, `__pycache__`, and processed JSON

---

## 🧪 Run Tests Only (Optional)

```bash
make test
```

Validates the geometry and output files of all processed datasets.

---

## 🧼 Clean the Workspace

```bash
make clean
```

Removes:

- `data/processed/*`
- Python cache files
- `.pytest_cache`

---

## 🔁 Reset the Database (Danger Zone 🚨)

If you need to **drop all existing tables and start fresh**:

```bash
make reset-db
```

> ⚠️ Requires `database/drop_all.sql` to exist. Use with caution in real environments.

---

## 🔧 Customize Upload Behavior

You can run just the ETL or upload process manually from Python:

```bash
# Run only ETL
python data/scripts/ingest_data.py

# Manually upload to Supabase
python data/scripts/upload/upload_to_supabase.py
```

---

## 🧠 Notes

- All uploads use the `service_role` key — ensure your Supabase permissions are granted in `schema.sql`.
- If **tests fail**, the upload is aborted to keep your data clean and consistent.
- Uses `Shapely`, `GeoPandas`, and `Supabase-py` for geometry + upload logic.

---

🎉 That’s it! You're ready to explore the data, visualize insights, or extend the project.