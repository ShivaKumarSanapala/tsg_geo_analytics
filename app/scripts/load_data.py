from app import load_cities_to_redis_from_db
from app.scripts.load_demographic_data import load_demographic_data
from app.scripts.load_geographical_data import load_geographical_data
from app.services.database import get_db
from sqlalchemy.sql import text

def calculate_centroids_lat_lng():
    session = next(get_db())
    try:
        print("Updating centroids for all cities...")

        session.execute(text("""
            UPDATE gis.city_table
            SET 
                centroid_lon = ST_X(ST_Centroid(wkb_geometry)),
                centroid_lat = ST_Y(ST_Centroid(wkb_geometry))
            WHERE wkb_geometry IS NOT NULL;
        """))

        session.commit()
        print("Centroids updated successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error calculating centroids: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    load_demographic_data()
    print("Loaded demographic data")
    load_geographical_data()
    print("Loaded geographical data")
    calculate_centroids_lat_lng()
    print("Calculated centroids for all cities...")
    load_cities_to_redis_from_db()
