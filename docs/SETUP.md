# 🛠️ Project: Are-U-Query-ous – Setup Guide

This document walks you through the full setup process to run the project from scratch.

---

## ✅ System Requirements

Before getting started, make sure you have the following tools installed:

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

### ⚙️ make

Used to automate the full setup process:

- **Linux/macOS**: pre-installed by default
- **Windows**: install [Git Bash](https://gitforwindows.org/) or use WSL

---

## 🔐 Environment Variables

Create a `.env` file in the root of the project (or copy from the provided template):

```bash
cp .env.example .env
```

And fill in your Supabase connection string:

```env
SUPABASE_DB_URL=postgres://user:password@host:port/database
```

---

## 🚀 Run the Full Setup

Once everything is installed and configured, run:

```bash
make all
```

This will automatically:

1. Run SQL scripts (`schema.sql`, `views.sql`, `seed.sql`)
2. Process geospatial data using ETL scripts
3. Validate geometries with automated tests
4. Upload data to Supabase (only if all tests pass)
5. Clean up temp files and cache

---

## 🧪 Run Only the Tests (Optional)

To run just the test suite:

```bash
make test
```

---

## 🧼 Clean the Workspace

To remove temporary files, Python cache, and processed JSON files:

```bash
make clean
```

---

## 🧠 Additional Notes

- This project was designed to be fully reproducible across environments.
- If any step fails, the `Makefile` will stop execution to prevent inconsistent data.

---

🎉 That’s it! You can now explore the data, connect to Supabase, or continue building.