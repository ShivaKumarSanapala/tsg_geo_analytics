from sqlalchemy import Float
from app.services.database import Base
from sqlalchemy import Column, Integer, String, BigInteger
from geoalchemy2 import Geometry

class StateDemography(Base):
    __tablename__ = 'state_demography'
    __table_args__ = {'schema': 'gis'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    geoidfq = Column(String, index=True)
    total_population = Column(String)  # Change to String (Text)
    female_population = Column(String)  # Change to String (Text)
    median_gross_rent_in_dollars = Column(String)  # Change to String (Text)
    median_household_income_past12months = Column(String)  # Change to String (Text)
    male_bachelors_degree_25yrs_above = Column(String)  # Change to String (Text)
    female_bachelors_degree_25yrs_above = Column(String)  # Change to String (Text)
    state = Column(String)
    year = Column(Integer)

class CountyDemography(Base):
    __tablename__ = 'county_demography'
    __table_args__ = {'schema': 'gis'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    geoidfq = Column(String, index=True)
    total_population = Column(String)  # Change to String (Text)
    female_population = Column(String)  # Change to String (Text)
    median_gross_rent_in_dollars = Column(String)  # Change to String (Text)
    median_household_income_past12months = Column(String)  # Change to String (Text)
    male_bachelors_degree_25yrs_above = Column(String)  # Change to String (Text)
    female_bachelors_degree_25yrs_above = Column(String)  # Change to String (Text)
    state = Column(String)
    county = Column(String)
    year = Column(Integer)

class City(Base):
    __tablename__ = "city_table"
    __table_args__ = {"schema": "gis"}

    ogc_fid = Column(Integer, primary_key=True, index=True)
    statefp = Column(String)
    placefp = Column(String)
    placens = Column(String)
    geoidfq = Column(String)
    geoid = Column(String)
    name = Column(String)
    namelsad = Column(String)
    stusps = Column(String)
    state_name = Column(String)
    lsad = Column(String)
    aland = Column(BigInteger)
    awater = Column(BigInteger)
    wkb_geometry = Column(Geometry("GEOMETRY", srid=4326))
    centroid_lat = Column(Float)
    centroid_lon = Column(Float)

class State(Base):
    __tablename__ = "states_table"
    __table_args__ = {"schema": "gis"}

    ogc_fid = Column(Integer, primary_key=True, index=True)
    statefp = Column(String)
    statens = Column(String)
    geoidfq = Column(String)
    geoid = Column(String)
    stusps = Column(String)
    name = Column(String)
    lsad = Column(String)
    aland = Column(BigInteger)
    awater = Column(BigInteger)
    wkb_geometry = Column(Geometry(geometry_type="GEOMETRY", srid=4326))

class County(Base):
    __tablename__ = "counties_table"
    __table_args__ = {"schema": "gis"}

    ogc_fid = Column(Integer, primary_key=True, index=True)
    statefp = Column(String)
    countyfp = Column(String)
    countyns = Column(String)
    geoidfq = Column(String)
    geoid = Column(String)
    name = Column(String)
    namelsad = Column(String)
    stusps = Column(String)
    state_name = Column(String)
    lsad = Column(String)
    aland = Column(BigInteger)
    awater = Column(BigInteger)
    wkb_geometry = Column(Geometry(geometry_type="GEOMETRY", srid=4326))

class ZCTA(Base):
    __tablename__ = "zcta_table"
    __table_args__ = {"schema": "gis"}

    ogc_fid = Column(Integer, primary_key=True, index=True)
    zcta5ce20 = Column(String)
    affgeoid20 = Column(String)
    geoid20 = Column(String)
    name20 = Column(String)
    lsad20 = Column(String)
    aland20 = Column(BigInteger)
    awater20 = Column(BigInteger)
    wkb_geometry = Column(Geometry(geometry_type="GEOMETRY", srid=4326))