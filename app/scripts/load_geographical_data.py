import subprocess
import os

def load_geographical_data():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(current_dir, "load_shapefiles_into_db.sh")

    print("Running geographical data loader script...\n")

    try:
        subprocess.run(
            ["bash", script_path],
            check=True,
            stdout=None,
            stderr=None,
            text=True
        )
        print("\nGeographical data loaded successfully.")
    except subprocess.CalledProcessError as e:
        print("\nError while loading geographical data:")
        print(f"Exit code: {e.returncode}")
