# data/scripts/ingest_data.py

from barcelona import load_districts as bcn_d
from barcelona import load_neighbourhoods as bcn_n
from madrid import load_districts as mad_d
from madrid import load_neighbourhoods as mad_n
from upload import upload_to_supabase

def run_all_etls():
    print("🚀 Running all ETL scripts...\n")
    bcn_d.run()
    bcn_n.run()
    mad_d.run()
    mad_n.run()
    print("\n✅ All ETLs completed.")

def run_all():
    run_all_etls()
    # upload_to_supabase.run_all_uploads()

if __name__ == "__main__":
    run_all()
