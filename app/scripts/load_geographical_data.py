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
            text=True
        )
        print("Geographical data loaded successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while loading geographical data:")
        print(e.stderr)
