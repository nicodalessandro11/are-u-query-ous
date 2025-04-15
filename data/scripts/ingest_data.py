# data/scripts/ingest_data.py

from barcelona import load_districts as bcn_d
from barcelona import load_neighbourhoods as bcn_n
from madrid import load_districts as mad_d
from madrid import load_neighbourhoods as mad_n
from upload import upload_to_supabase

def run_all_etls():
    print("🚀 Running ETL scripts...\n")

    # Step 1: ETL for districts first
    bcn_d.run()
    mad_d.run()
    print("\n✅ District ETLs completed.\n")

    # Step 2: Upload districts
    upload_to_supabase.run_district_upload()
    print("✅ Districts uploaded. Proceeding to neighbourhood ETL...\n")

    # Step 3: ETL for neighbourhoods (districts must be in Supabase first)
    bcn_n.run()
    mad_n.run()
    print("\n✅ Neighbourhood ETLs completed.\n")

    # Step 4: Upload neighbourhoods
    upload_to_supabase.run_neighbourhood_upload()
    print("✅ Neighbourhoods uploaded.\n")

def run_all():
    run_all_etls()

if __name__ == "__main__":
    run_all()
