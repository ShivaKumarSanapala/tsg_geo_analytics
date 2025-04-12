import os
import pandas as pd

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
    # List of years for which we have CSV data
    years = range(2017, 2024)

    for year in years:
        state_csv = f'./data/{year}_states_demography.csv'
        county_csv = f'./data/{year}_counties_demography.csv'

        # Load state and county data for each year
        if os.path.exists(state_csv) and os.path.exists(county_csv):
            print(f"Loading data for year {year}...")
            load_state_data(state_csv, year)
            load_county_data(county_csv, year)
        else:
            print(f"Data files for year {year} not found. Skipping...")


if __name__ == '__main__':
    print("Demographic Data loading in Database....please wait...")
    load_data_for_all_years()
    print("Data loading completed.")
