# run_etl.py

"""
ETL Script Runner (Development Use Only)

Usage:
    python run_etl.py barcelona.load_districts
    python run_etl.py madrid.load_neighbourhoods

This script dynamically imports and runs a specific ETL module
by calling its `run()` function. Use this to test individual
ETL jobs during development before integrating them into the full
ETL pipeline (`ingest.py`).

Author: Nico D'Alessandro <nicodalessandro11@gmail.com>
Date: 2025-04-17
"""

import importlib
import sys
from shared.emoji_logger import info, success, warning, error

def main():
    if len(sys.argv) != 2:
        error("Usage: python run_etl.py [etl_module_path]")
        info("Example: python run_etl.py barcelona.load_districts")
        return

    job = sys.argv[1]
    module_path = f"scripts.etl.{job}"

    try:
        info(f"🚀 Importing ETL module: {module_path}")
        module = importlib.import_module(module_path)
        module.run()
        success(f"ETL job '{job}' completed successfully.")
    except ModuleNotFoundError:
        error(f"Module '{module_path}' not found.")
    except AttributeError:
        error(f"Module '{module_path}' does not contain a 'run()' function.")
    except Exception as e:
        error(f"ETL job '{job}' failed with error: {e}")

if __name__ == "__main__":
    main()
