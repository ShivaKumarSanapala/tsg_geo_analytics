#!/bin/bash

# Set working directory
WORKDIR="/tmp"

# Declare a mapping from file prefix to table name
declare -A table_names=(
  ["cb_2023_us_state_500k"]="states_table"
  ["cb_2023_us_region_500k"]="regions_table"
  ["cb_2023_us_county_500k"]="counties_table"
  ["cb_2023_us_place_500k"]="cities_table"
  ["cb_2020_us_zcta520_500k"]="zip_codes_table"
)

# Make sure required env vars are set
: "${POSTGRES_HOST:?Need to set POSTGRES_HOST}"
: "${POSTGRES_DB:?Need to set POSTGRES_DB}"
: "${POSTGRES_USER:?Need to set POSTGRES_USER}"
: "${POSTGRES_PASSWORD:?Need to set POSTGRES_PASSWORD}"

for zipfile in cb_*.zip; do
  echo "Processing $zipfile..."

  # Get the base name without .zip
  base=$(basename "$zipfile" .zip)

  # Skip if we don't have a table name mapping
  tablename=${table_names[$base]}
  if [ -z "$tablename" ]; then
    echo "Skipping $zipfile - no table name mapping found."
    continue
  fi

  # Unzip
  unzip -o "$zipfile" -d "$WORKDIR"

  # Find the .shp file (assumes there's only one per zip)
  shp_file=$(find "$WORKDIR" -name "${base}.shp")
  if [ ! -f "$shp_file" ]; then
    echo "Shapefile not found for $zipfile"
    continue
  fi

  # Convert to GeoJSON
  geojson_file="$WORKDIR/${base}.geo.json"
  mapshaper "$shp_file" -o format=geojson "$geojson_file"

  # Load into Postgres
  ogr2ogr \
    -f "PostgreSQL" \
    PG:"host=${POSTGRES_HOST} user=${POSTGRES_USER} dbname=${POSTGRES_DB} password=${POSTGRES_PASSWORD}" \
    "$geojson_file" \
    -nln "gis.${tablename}" \
    -append

  echo "Done importing $zipfile → gis.${tablename}"
done
