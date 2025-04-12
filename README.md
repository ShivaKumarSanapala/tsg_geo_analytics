python3 -m venv venv    
source venv/bin/activate

# Set file paths
cp cb_2023_us_state_500k.zip cb_2023_us_region_500k.zip /tmp/
unzip /tmp/cb_2023_us_state_500k.zip -d /tmp

# Convert SHP to GeoJSON
mapshaper /tmp/cb_2023_us_state_500k.shp -o format=geojson /tmp/cb_2023_us_state_500k.geo.json

# Load into PostgreSQL using environment variables
ogr2ogr \
  -f "PostgreSQL" \
  PG:"host=${POSTGRES_HOST} user=${POSTGRES_USER} dbname=${POSTGRES_DB} password=${POSTGRES_PASSWORD}" \
  /tmp/cb_2023_us_state_500k.geo.json \
  -nln gis.states_table \
  -append
