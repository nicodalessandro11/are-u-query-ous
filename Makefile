# Makefile — Are-U-Query-ous
# Automates full setup, ETL, testing, upload and cleanup

# Load environment variables from .env
include .env
export

SUPABASE_SQL_DIR=database
ETL_SCRIPT=data/scripts/ingest_data.py
TEST_DIR=data/tests
PROCESSED_DIR=data/processed

# Default command: full pipeline
.DEFAULT_GOAL := all

## 📦 Install required Python packages inside virtual environment
install:
	@echo "📦 Installing Python dependencies from requirements.txt..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed."

## 🔁 Drop all existing tables (DEV ONLY — use with caution!)
reset-db:
	@echo "🧨 Dropping all existing tables in Supabase..."
	psql "$$DATABASE_URL" -f $(SUPABASE_SQL_DIR)/drop_all.sql
	@echo "✅ Database reset complete."


## 🛠️ Set up Supabase: schema, views, and seed data
setup:
	@echo "🔧 Creating schema, views and inserting initial data..."
	psql "$$DATABASE_URL" -f $(SUPABASE_SQL_DIR)/schema.sql
	psql "$$DATABASE_URL" -f $(SUPABASE_SQL_DIR)/views.sql
	psql "$$DATABASE_URL" -f $(SUPABASE_SQL_DIR)/seed.sql
	@echo "✅ Setup complete."

## ⚙️ Run ETL scripts (generate processed JSON files only)
etl:
	@echo "⚙️ Running ETL scripts..."
	python $(ETL_SCRIPT) --skip-upload

## 🧪 Run geometry validation tests
test:
	@echo "🧪 Running geometry integrity tests..."
	pytest $(TEST_DIR)

## 🚀 Run full ingestion (ETL + tests + upload)
ingest:
	@echo "🚀 Running full ingestion (ETL + tests + upload)..."
	python $(ETL_SCRIPT)

## 👨‍💻 Developer mode: ETL + tests (no upload)
dev:
	@echo "👨‍💻 Developer mode: ETL + tests (no upload)..."
	python $(ETL_SCRIPT) --skip-upload
	make test

## 🧼 Clean processed files and Python cache
clean:
	@echo "🧼 Cleaning processed files and cache..."
	rm -rf $(PROCESSED_DIR)/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	@echo "✅ Clean complete."

## 🧪 Test-only: run tests without upload
test-only: etl test

## 🚀 Run the entire workflow: install + setup + ETL + test + upload + clean
all: install setup ingest clean
	@echo "🏁 All steps completed. Supabase is now fully populated!"

## 📚 Show all available commands
help:
	@echo ""
	@echo "📦 Are-U-Query-ous Makefile — Available Commands"
	@echo ""
	@echo "  make            - Run full pipeline (install + setup + ingest + clean)"
	@echo "  make install    - Install Python dependencies (requirements.txt)"
	@echo "  make setup      - Run schema.sql, views.sql, and seed.sql"
	@echo "  make etl        - Run ETL scripts (no upload)"
	@echo "  make test       - Run geometry tests"
	@echo "  make test-only  - Run ETL and geometry tests (no upload)"
	@echo "  make ingest     - Run ETL + test + upload to Supabase"
	@echo "  make dev        - Run ETL + test (skip upload)"
	@echo "  make clean      - Delete processed files and caches"
	@echo ""
