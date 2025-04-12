#!/bin/bash

set -e

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set paths
SHAPEFILES_DIR="${SCRIPT_DIR}/shapefiles"
WORKDIR="/tmp"

# Declare a mapping from file prefix to table name
declare -A table_names=(
  ["cb_2023_us_state_500k"]="states_table"
  ["cb_2023_us_region_500k"]="regions_table"
  ["cb_2023_us_county_500k"]="counties_table"
  ["cb_2023_us_place_500k"]="city_table"
  ["cb_2020_us_zcta520_500k"]="zcta_table"
)

# Make sure required env vars are set
: "${POSTGRES_HOST:?Need to set POSTGRES_HOST}"
: "${POSTGRES_DB:?Need to set POSTGRES_DB}"
: "${POSTGRES_USER:?Need to set POSTGRES_USER}"
: "${POSTGRES_PASSWORD:?Need to set POSTGRES_PASSWORD}"

# Loop over all ZIP files in the shapefiles folder
for zipfile in "${SHAPEFILES_DIR}"/cb_*.zip; do
  echo "📦 Processing $(basename "$zipfile")..."

  base=$(basename "$zipfile" .zip)

  # Check for known table name
  tablename=${table_names[$base]}
  if [ -z "$tablename" ]; then
    echo "⚠️  Skipping $zipfile - no table name mapping found."
    continue
  fi

  # Unzip to working dir
  unzip -o "$zipfile" -d "$WORKDIR"

  # Find the .shp file
  shp_file=$(find "$WORKDIR" -name "${base}.shp")
  if [ ! -f "$shp_file" ]; then
    echo "❌ Shapefile not found for $zipfile"
    continue
  fi

  # Convert to GeoJSON
  geojson_file="$WORKDIR/${base}.geo.json"
  echo "🌍 Converting $shp_file to GeoJSON..."
  mapshaper "$shp_file" -o format=geojson "$geojson_file"

  # Load into PostgreSQL
  echo "🛢️  Importing into PostgreSQL: gis.${tablename}"
  ogr2ogr \
    -f "PostgreSQL" \
    PG:"host=${POSTGRES_HOST} user=${POSTGRES_USER} dbname=${POSTGRES_DB} password=${POSTGRES_PASSWORD}" \
    "$geojson_file" \
    -nln "gis.${tablename}" \
    -append

  echo "✅ Done importing $(basename "$zipfile") → gis.${tablename}"
done

