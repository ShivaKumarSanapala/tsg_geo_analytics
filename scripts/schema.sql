-- Create extension for PostGIS (you already have this)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS gis;

-- Create state_demography table with TEXT columns, excluding geom
CREATE TABLE gis.state_demography (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geoidfq TEXT,
    total_population TEXT,  -- Change to TEXT
    female_population TEXT,  -- Change to TEXT
    median_gross_rent_in_dollars TEXT,  -- Change to TEXT
    median_household_income_past12months TEXT,  -- Change to TEXT
    male_bachelors_degree_25yrs_above TEXT,  -- Change to TEXT
    female_bachelors_degree_25yrs_above TEXT,  -- Change to TEXT
    state TEXT,
    year INTEGER
);

-- Create county_demography table with TEXT columns, excluding geom
CREATE TABLE gis.county_demography (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geoidfq TEXT,
    total_population TEXT,  -- Change to TEXT
    female_population TEXT,  -- Change to TEXT
    median_gross_rent_in_dollars TEXT,  -- Change to TEXT
    median_household_income_past12months TEXT,  -- Change to TEXT
    male_bachelors_degree_25yrs_above TEXT,  -- Change to TEXT
    female_bachelors_degree_25yrs_above TEXT,  -- Change to TEXT
    state TEXT,
    county TEXT,
    year INTEGER
);

-- Create indexes as necessary
CREATE INDEX idx_state_demography_state_year_geoidfq ON gis.state_demography(state, year, geoidfq);
CREATE INDEX idx_county_demography_state_county_year_geoidfq ON gis.county_demography(state, county, year, geoidfq);

-- Add constraints
ALTER TABLE gis.state_demography ADD CONSTRAINT year_check_state CHECK (year > 0);
ALTER TABLE gis.county_demography ADD CONSTRAINT year_check_county CHECK (year > 0);

-- If you need to drop the existing tables (use caution)
-- DROP TABLE gis.state_demography;
-- DROP TABLE gis.county_demography;
