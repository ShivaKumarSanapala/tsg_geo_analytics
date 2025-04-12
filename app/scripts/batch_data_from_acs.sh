#!/bin/bash

# Create the data directory if it doesn't exist
if [ ! -d "data" ]; then
  mkdir scripts/data
  echo "Created 'data' directory"
fi

for year in {2017..2023}
do
    # Determine the API URL based on the year
    if [ "$year" -eq 2020 ]; then
        api_url="https://api.census.gov/data/2020/acs/acs5"
    else
        api_url="https://api.census.gov/data/${year}/acs/acs1"
    fi

    # Define the query string and variable mapping for county data
    query_string="get=NAME,GEO_ID,B01003_001E,B01001_026E,B25064_001E,B19013_001E,B15002_015E,B15002_032E&for=county:*&in=state:*"
    variable_mapping="B01003_001E=total_population,B01001_026E=female_population,B25064_001E=median_gross_rent_in_dollars,B19013_001E=median_household_income_past12months,B15002_015E=male_bachelors_degree_25yrs_above,B15002_032E=female_bachelors_degree_25yrs_above"

    # Output file for county data
    county_output_file="data/${year}_counties_demography.csv"
    ./fetch_data_from_acs.sh "$api_url" "$query_string" "$variable_mapping" >> "$county_output_file"
    echo "Data for ${year} counties saved to ${county_output_file}"

    # Define the query string for state data
    query_string="get=NAME,GEO_ID,B01003_001E,B01001_026E,B25064_001E,B19013_001E,B15002_015E,B15002_032E&for=state:*"

    # Output file for state data
    state_output_file="data/${year}_states_demography.csv"
    ./fetch_data_from_acs.sh "$api_url" "$query_string" "$variable_mapping" >> "$state_output_file"
    echo "Data for ${year} states saved to ${state_output_file}"
done
