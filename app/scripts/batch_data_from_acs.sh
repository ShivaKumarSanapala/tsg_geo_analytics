#!/bin/bash

# ===============================
# batch_data_from_acs.sh
# Location: app/scripts/
# ===============================

# Help message
if [[ "$1" == "--help" ]]; then
  echo ""
  echo "Usage: ./app/scripts/batch_data_from_acs.sh"
  echo ""
  echo "This script downloads demographic data from the U.S. Census Bureau API"
  echo "for the years 2017 to 2023 and saves it into CSV files."
  echo ""
  echo "Outputs:"
  echo "- app/scripts/data/{year}_counties_demography.csv"
  echo "- app/scripts/data/{year}_states_demography.csv"
  echo ""
  echo "Make sure 'fetch_data_from_acs.sh' is executable and in the same directory."
  echo ""
  exit 0
fi

# Get absolute path to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/data"
FETCH_SCRIPT="${SCRIPT_DIR}/fetch_data_from_acs.sh"

# Check if fetch script exists and is executable
if [ ! -x "$FETCH_SCRIPT" ]; then
  echo "❌ Error: fetch_data_from_acs.sh not found or not executable at $FETCH_SCRIPT"
  exit 1
fi

# Create the data directory if it doesn't exist
mkdir -p "$DATA_DIR"

# Loop over years
for year in {2017..2023}; do
  echo "📦 Processing year: $year"

  # Choose ACS API endpoint
  if [ "$year" -eq 2020 ]; then
    api_url="https://api.census.gov/data/2020/acs/acs5"
  else
    api_url="https://api.census.gov/data/${year}/acs/acs1"
  fi

  variable_mapping="B01003_001E=total_population,B01001_026E=female_population,B25064_001E=median_gross_rent_in_dollars,B19013_001E=median_household_income_past12months,B15002_015E=male_bachelors_degree_25yrs_above,B15002_032E=female_bachelors_degree_25yrs_above"

  # --- County ---
  query_string="get=NAME,GEO_ID,B01003_001E,B01001_026E,B25064_001E,B19013_001E,B15002_015E,B15002_032E&for=county:*&in=state:*"
  county_output_file="${DATA_DIR}/${year}_counties_demography.csv"
  "$FETCH_SCRIPT" "$api_url" "$query_string" "$variable_mapping" > "$county_output_file"
  echo "✔️  Saved county data → $county_output_file"

  # --- State ---
  query_string="get=NAME,GEO_ID,B01003_001E,B01001_026E,B25064_001E,B19013_001E,B15002_015E,B15002_032E&for=state:*"
  state_output_file="${DATA_DIR}/${year}_states_demography.csv"
  "$FETCH_SCRIPT" "$api_url" "$query_string" "$variable_mapping" > "$state_output_file"
  echo "✔️  Saved state data → $state_output_file"
done

echo "✅ All data fetched and saved in: $DATA_DIR"
