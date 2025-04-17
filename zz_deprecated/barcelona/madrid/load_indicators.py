# data/scripts/madrid/load_indicators.py

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client
from shared.emoji_logger import info, success, warning, error


# Define base directory and city ID
BASE_DIR = Path(__file__).resolve().parents[3]
city_id = 2  # Madrid
geo_level_id = 3  # Neighbourhood level for indicators

# === SETUP ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling datetime objects and numpy types."""
    def default(self, obj):
        if isinstance(obj, (datetime, pd.Timestamp)):
            return obj.isoformat()
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        if isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        return super().default(obj)

class MadridIndicatorsETL:
    def __init__(self, input_files: List[str], output_dir: str):
        """
        Initialize the ETL process for Madrid indicators.
        
        Args:
            input_files (List[str]): List of input CSV files to process
            output_dir (str): Directory to save the processed output
        """
        self.input_files = input_files
        self.output_dir = Path(output_dir)
        self.processed_data = None
        self.neighbourhood_map = None
        self.indicator_definitions = {}

    def get_indicator_definition_id(self, indicator_name: str) -> int:
        """
        Fetch indicator_definition_id from Supabase based on indicator name.
        Caches results to avoid multiple queries for the same indicator.
        """
        if indicator_name in self.indicator_definitions:
            return self.indicator_definitions[indicator_name]

        info(f"Looking up indicator definition for: {indicator_name}")
        response = (
            supabase.table("indicator_definitions")
            .select("id")
            .eq("name", indicator_name)
            .execute()
        )

        if not response.data:
            error(f"Indicator definition '{indicator_name}' not found in Supabase")
            raise Exception(f"❌ Indicator definition '{indicator_name}' not found in Supabase")

        indicator_id = response.data[0]["id"]
        self.indicator_definitions[indicator_name] = indicator_id
        success(f"Found indicator definition ID: {indicator_id} for {indicator_name}")
        return indicator_id

    def get_neighbourhood_map(self):
        """Fetch neighbourhood_id values from Supabase for Madrid."""
        info("Fetching neighbourhood mapping from Supabase...")
        response = (
            supabase.table("neighbourhoods")
            .select("id, neighbourhood_code, district_id, city_id")
            .eq("city_id", city_id)
            .execute()
        )

        if not response.data:
            error("No neighbourhoods found for Madrid (city_id = 2) in Supabase.")
            raise Exception("❌ No neighbourhoods found for Madrid (city_id = 2) in Supabase.")

        self.neighbourhood_map = {n["neighbourhood_code"]: n["id"] for n in response.data}
        success(f"Found {len(self.neighbourhood_map)} neighbourhoods for Madrid")

    def _convert_spanish_number(self, value: str) -> float:
        """Convert a Spanish formatted number (with comma as decimal separator) to float."""
        try:
            return float(str(value).replace(',', '.'))
        except (ValueError, TypeError):
            return None

    def extract(self) -> None:
        """Extract data from all input CSV files and combine them."""
        all_data = []
        
        for file in self.input_files:
            if not os.path.exists(file):
                warning(f"File {file} not found, skipping...")
                continue
            
            file_path = Path(file)
            # Determine indicator type from filename
            if "superficie" in file_path.name.lower():
                indicator_name = "Surface"
            elif "habitantes" in file_path.name.lower():
                indicator_name = "Population"
            else:
                warning(f"Unknown indicator type for file: {file_path.name}")
                continue

            # Get indicator definition ID
            try:
                indicator_def_id = self.get_indicator_definition_id(indicator_name)
            except Exception as e:
                error(f"Failed to get indicator definition ID: {e}")
                continue

            df = pd.read_csv(file, sep=';', encoding='utf-8')
            df['indicator_def_id'] = indicator_def_id  # Add indicator type to the dataframe
            info(f"Loaded {len(df)} rows from {file_path.name}")
            all_data.append(df)
        
        if all_data:
            self.processed_data = pd.concat(all_data, ignore_index=True)
            success(f"Combined {len(self.processed_data)} total rows from {len(all_data)} files")
        else:
            error("No valid input files found to process")
            raise ValueError("No valid input files found to process")

    def transform(self) -> None:
        """Transform the data according to the target schema."""
        if self.processed_data is None:
            error("No data to transform. Run extract() first.")
            raise ValueError("No data to transform. Run extract() first.")

        info("Starting data transformation...")

        # Get neighbourhood mapping
        if self.neighbourhood_map is None:
            self.get_neighbourhood_map()

        # Standardize column names
        self.processed_data.columns = self.processed_data.columns.str.lower()

        # Validate data completeness
        info("Validating data completeness...")
        periodos = self.processed_data['periodo panel'].unique()
        expected_entries = len(self.neighbourhood_map)  # Should be 131
        
        # Track complete and incomplete periods
        complete_periods = set()
        incomplete_periods = set()
        
        for periodo in sorted(periodos):
            period_data = self.processed_data[self.processed_data['periodo panel'] == periodo]
            entries_count = len(period_data)
            
            # Each neighborhood should have 2 entries (superficie + habitantes)
            expected_period_entries = expected_entries * 2
            
            if entries_count != expected_period_entries:
                warning(f"Period {periodo} has {entries_count} entries (expected {expected_period_entries})")
                incomplete_periods.add(periodo)
            else:
                success(f"Period {periodo} has correct number of entries: {entries_count}")
                complete_periods.add(periodo)

            # Check for duplicate neighborhoods in the same period
            duplicates = period_data.groupby(['cod_barrio', 'indicator_def_id']).size()
            if (duplicates > 1).any():
                dup_barrios = duplicates[duplicates > 1].index.tolist()
                warning(f"Period {periodo} has duplicate entries for neighborhoods: {dup_barrios}")

            # Check for missing neighborhoods
            present_barrios = set(period_data['cod_barrio'].unique())
            all_barrios = set(self.neighbourhood_map.keys())
            missing_barrios = all_barrios - present_barrios
            if missing_barrios:
                warning(f"Period {periodo} is missing data for neighborhoods: {sorted(missing_barrios)}")
                incomplete_periods.add(periodo)

        if incomplete_periods:
            warning(f"Filtering out incomplete periods: {sorted(incomplete_periods)}")
            # Filter out incomplete periods
            self.processed_data = self.processed_data[self.processed_data['periodo panel'].isin(complete_periods)]
            success(f"Keeping complete periods: {sorted(complete_periods)}")

        # Prepare the transformed data structure
        transformed_data = []
        processed_entries = set()  # Track unique combinations to avoid duplicates

        # Group by period and indicator type to handle multiple periods and indicators
        for (periodo, indicator_def_id), group in self.processed_data.groupby(['periodo panel', 'indicator_def_id']):
            info(f"Processing data for period {periodo}, indicator {indicator_def_id}")
            
            for _, row in group.iterrows():
                try:
                    neighbourhood_code = int(row['cod_barrio'])
                    geo_id = self.neighbourhood_map.get(neighbourhood_code)
                    year = int(row['año'])
                    
                    if geo_id is None:
                        warning(f"No matching neighbourhood found for code {neighbourhood_code}")
                        continue

                    value = self._convert_spanish_number(row['valor_indicador'])
                    if value is None:
                        warning(f"Could not convert value {row['valor_indicador']} to number")
                        continue

                    # Create a unique key for this combination
                    entry_key = (year, indicator_def_id, geo_id)
                    if entry_key in processed_entries:
                        continue  # Skip duplicate entries
                    processed_entries.add(entry_key)

                    # Use año as the year in the output, but group by periodo panel
                    transformed_data.append({
                        "indicator_def_id": indicator_def_id,
                        "geo_level_id": geo_level_id,
                        "geo_id": geo_id,
                        "year": year,
                        "value": value
                    })

                except (ValueError, KeyError) as e:
                    warning(f"Error processing row: {e}")
                    continue

        # Final validation of transformed data
        transformed_by_year = {}
        for item in transformed_data:
            year = item['year']
            transformed_by_year.setdefault(year, set()).add(item['geo_id'])
        
        # Filter out incomplete years from the final transformed data
        complete_transformed_data = []
        for item in transformed_data:
            year = item['year']
            if len(transformed_by_year[year]) == expected_entries:
                complete_transformed_data.append(item)
            elif not any(x['year'] == year for x in complete_transformed_data):  # Only warn once per incomplete year
                warning(f"Filtering out incomplete year {year} with {len(transformed_by_year[year])} entries (expected {expected_entries})")

        self.processed_data = complete_transformed_data
        success(f"Final transformed data contains {len(complete_transformed_data)} indicators")

        # Final validation report
        final_years = set(item['year'] for item in complete_transformed_data)
        for year in sorted(final_years):
            year_entries = sum(1 for item in complete_transformed_data if item['year'] == year)
            success(f"Year {year} has {year_entries} indicators (for {year_entries//2} neighborhoods)")

    def load(self) -> None:
        """Save the processed data as JSON."""
        if self.processed_data is None:
            error("No data to load. Run transform() first.")
            raise ValueError("No data to load. Run transform() first.")

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save to processed directory with JSON format
        output_path = self.output_dir / f'insert_ready_indicators_madrid.json'
        
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(self.processed_data, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)

        success(f"Saved {len(self.processed_data)} indicators to {output_path}")

    def run(self) -> None:
        """Execute the full ETL pipeline."""
        info("Starting Madrid Indicators ETL process...")
        self.extract()
        self.transform()
        self.load()
        success("ETL process completed successfully")


def run():
    """Main entry point for the ETL process."""
    data_dir = BASE_DIR / "data/raw"
    output_dir = BASE_DIR / "data/processed"
    
    input_files = [
        data_dir / 'superficie_madrid.csv',
        data_dir / 'habitantes_madrid.csv'
    ]
    
    etl = MadridIndicatorsETL(
        input_files=[str(f) for f in input_files],
        output_dir=str(output_dir)
    )
    etl.run()


if __name__ == "__main__":
    run()
