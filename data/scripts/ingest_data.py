from barcelona import load_districts as bcn_d
from barcelona import load_neighbourhoods as bcn_n
from madrid import load_districts as mad_d
from madrid import load_neighbourhoods as mad_n
from barcelona import load_point_features as bcn_p 

from upload import upload_to_supabase
import subprocess
import sys

def run_etls_and_upload():
    print("🚀 Running ETL scripts...\n")

    bcn_d.run()
    mad_d.run()
    print("✅ District ETLs completed.\n")

    upload_to_supabase.run_district_upload()

    bcn_n.run()
    mad_n.run()
    print("✅ Neighbourhood ETLs completed.\n")

    upload_to_supabase.run_neighbourhood_upload()

    bcn_p.run()
    print("✅ Point features ETL completed.\n")

def run_tests():
    print("🧪 Running integrity tests...\n")
    result = subprocess.run(["pytest", "data/tests"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Tests failed. Upload aborted.")
        sys.exit(1)
    print("✅ All tests passed.\n")

def run_all():
    run_etls_and_upload()
    run_tests()
    upload_to_supabase.run_point_feature_upload()

if __name__ == "__main__":
    run_all()
