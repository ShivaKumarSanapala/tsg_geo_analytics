import subprocess
import os

def load_geographical_data():
    script_path = os.path.join(os.path.dirname(__file__), "load_shapefiles_into_db.sh")

    print("Running geographical data loader script...")

    try:
        result = subprocess.run(
            ["bash", script_path],
            check=True,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "POSTGRES_HOST": os.environ.get("POSTGRES_HOST", "postgres-db"),
                "POSTGRES_DB": os.environ.get("POSTGRES_DB", "tsg_db"),
                "POSTGRES_USER": os.environ.get("POSTGRES_USER", "tsg_user"),
                "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD", "tsg_pass"),
            }
        )
        print("Geographical data loaded successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while loading geographical data:")
        print(e.stderr)
