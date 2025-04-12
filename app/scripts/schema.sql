-- Create extension for PostGIS (you already have this)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create schema
CREATE SCHEMA IF NOT EXISTS gis;

-- -------------------------------------
-- State Demography Table
-- -------------------------------------
CREATE TABLE IF NOT EXISTS gis.state_demography (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geoidfq TEXT,
    total_population TEXT,
    female_population TEXT,
    median_gross_rent_in_dollars TEXT,
    median_household_income_past12months TEXT,
    male_bachelors_degree_25yrs_above TEXT,
    female_bachelors_degree_25yrs_above TEXT,
    state TEXT,
    year INTEGER
);

CREATE INDEX IF NOT EXISTS idx_state_demography_state_year_geoidfq
ON gis.state_demography(state, year, geoidfq);

ALTER TABLE gis.state_demography
ADD CONSTRAINT year_check_state CHECK (year > 0);

-- -------------------------------------
-- County Demography Table
-- -------------------------------------
CREATE TABLE IF NOT EXISTS gis.county_demography (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geoidfq TEXT,
    total_population TEXT,
    female_population TEXT,
    median_gross_rent_in_dollars TEXT,
    median_household_income_past12months TEXT,
    male_bachelors_degree_25yrs_above TEXT,
    female_bachelors_degree_25yrs_above TEXT,
    state TEXT,
    county TEXT,
    year INTEGER
);

CREATE INDEX IF NOT EXISTS idx_county_demography_state_county_year_geoidfq
ON gis.county_demography(state, county, year, geoidfq);

ALTER TABLE gis.county_demography
ADD CONSTRAINT year_check_county CHECK (year > 0);

-- -------------------------------------
-- City Table
-- -------------------------------------
CREATE TABLE IF NOT EXISTS gis.city_table (
    ogc_fid SERIAL PRIMARY KEY,
    statefp VARCHAR,
    placefp VARCHAR,
    placens VARCHAR,
    geoidfq VARCHAR,
    geoid VARCHAR,
    name VARCHAR,
    namelsad VARCHAR,
    stusps VARCHAR,
    state_name VARCHAR,
    lsad VARCHAR,
    aland BIGINT,
    awater BIGINT,
    wkb_geometry geometry(Geometry, 4326),
    centroid_lat DOUBLE PRECISION,
    centroid_lon DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS city_table_wkb_geometry_geom_idx
ON gis.city_table USING GIST (wkb_geometry);

-- -------------------------------------
-- Counties Table
-- -------------------------------------
CREATE TABLE IF NOT EXISTS gis.counties_table (
    ogc_fid SERIAL PRIMARY KEY,
    statefp VARCHAR,
    countyfp VARCHAR,
    countyns VARCHAR,
    geoidfq VARCHAR,
    geoid VARCHAR,
    name VARCHAR,
    namelsad VARCHAR,
    stusps VARCHAR,
    state_name VARCHAR,
    lsad VARCHAR,
    aland BIGINT,
    awater BIGINT,
    wkb_geometry geometry(Geometry, 4326)
);

CREATE INDEX IF NOT EXISTS counties_table_wkb_geometry_geom_idx
ON gis.counties_table USING GIST (wkb_geometry);

-- -------------------------------------
-- States Table
-- -------------------------------------
CREATE TABLE IF NOT EXISTS gis.states_table (
    ogc_fid SERIAL PRIMARY KEY,
    statefp VARCHAR,
    statens VARCHAR,
    geoidfq VARCHAR,
    geoid VARCHAR,
    stusps VARCHAR,
    name VARCHAR,
    lsad VARCHAR,
    aland BIGINT,
    awater BIGINT,
    wkb_geometry geometry(Geometry, 4326)
);

CREATE INDEX IF NOT EXISTS states_table_wkb_geometry_geom_idx
ON gis.states_table USING GIST (wkb_geometry);

-- -------------------------------------
-- ZCTA Table
-- -------------------------------------
CREATE TABLE IF NOT EXISTS gis.zcta_table (
    ogc_fid SERIAL PRIMARY KEY,
    zcta5ce20 VARCHAR,
    affgeoid20 VARCHAR,
    geoid20 VARCHAR,
    name20 VARCHAR,
    lsad20 VARCHAR,
    aland20 BIGINT,
    awater20 BIGINT,
    wkb_geometry geometry(Geometry, 4326)
);

CREATE INDEX IF NOT EXISTS zcta_table_wkb_geometry_geom_idx
ON gis.zcta_table USING GIST (wkb_geometry);
