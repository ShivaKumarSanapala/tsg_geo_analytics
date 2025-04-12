import os
import pandas as pd
import subprocess
import traceback

from app.models.entities import StateDemography, CountyDemography
from app.services.database import get_db

session = next(get_db())

def load_state_data(csv_file, year):
    # Read state data from CSV
    state_df = pd.read_csv(csv_file)

    for index, row in state_df.iterrows():
        # Create StateDemography record
        state_record = StateDemography(
            name=row['NAME'],
            geoidfq=row['GEO_ID'],
            total_population=row['total_population'],
            female_population=row['female_population'],
            median_gross_rent_in_dollars=row['median_gross_rent_in_dollars'],
            median_household_income_past12months=row['median_household_income_past12months'],
            male_bachelors_degree_25yrs_above=row['male_bachelors_degree_25yrs_above'],
            female_bachelors_degree_25yrs_above=row['female_bachelors_degree_25yrs_above'],
            state=row['state'],
            year=year
        )

        session.add(state_record)
    session.commit()


def load_county_data(csv_file, year):
    # Read county data from CSV
    county_df = pd.read_csv(csv_file)

    for index, row in county_df.iterrows():
        # Create CountyDemography record
        county_record = CountyDemography(
            name=row['NAME'],
            geoidfq=row['GEO_ID'],
            total_population=row['total_population'],
            female_population=row['female_population'],
            median_gross_rent_in_dollars=row['median_gross_rent_in_dollars'],
            median_household_income_past12months=row['median_household_income_past12months'],
            male_bachelors_degree_25yrs_above=row['male_bachelors_degree_25yrs_above'],
            female_bachelors_degree_25yrs_above=row['female_bachelors_degree_25yrs_above'],
            state=row['state'],
            county=row['county'],
            year=year
        )

        session.add(county_record)
    session.commit()

def load_data_for_all_years():
    years = range(2017, 2024)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "./data"))

    for year in years:
        state_csv = os.path.join(base_dir, f"{year}_states_demography.csv")
        county_csv = os.path.join(base_dir, f"{year}_counties_demography.csv")

        print(f"\n📅 Processing year {year}...state: {state_csv} county: {county_csv}")

        # Flags for each
        state_ok = os.path.exists(state_csv)
        county_ok = os.path.exists(county_csv)

        if not state_ok and not county_ok:
            print(f"⚠️  No data files found for {year}. Skipping...")
            continue

        if state_ok:
            try:
                print(f"📥 Loading state data from {state_csv}")
                load_state_data(state_csv, year)
            except Exception as e:
                print(f"❌ Failed to load state data for {year}: {e}")
                traceback.print_exc()

        if county_ok:
            try:
                print(f"📥 Loading county data from {county_csv}")
                load_county_data(county_csv, year)
            except Exception as e:
                print(f"❌ Failed to load county data for {year}: {e}")
                traceback.print_exc()

    print("\n✅ Finished processing all available data files.")

def generate_csv_files():
    print("Generating CSVs using batch_data_from_acs.sh...")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "batch_data_from_acs.sh")
        subprocess.run(["bash", script_path], check=True)
        print("CSV generation completed.")
    except subprocess.CalledProcessError as e:
        print("CSV generation failed!")
        print(e)
        exit(1)

def load_demographic_data():
    # generate_csv_files()
    print("Demographic Data loading into Database....please wait...")
    load_data_for_all_years()
    print("Demographic Data loading into Database for States and Counties completed!")

