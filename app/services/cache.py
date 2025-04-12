import redis

redis_client = None  # Global client instance

def init_redis(app):
    global redis_client
    print("Initializing Redis..")
    redis_client = redis.Redis(
        host=app.config.get("REDIS_HOST", "localhost"),
        port=app.config.get("REDIS_PORT", 6379),
        db=0,
        decode_responses=True
    )
    redis_client.ping()

def load_cities_to_redis_from_db():
    from app.services.database import SessionLocal
    from app.models.entities import City

    session = SessionLocal()
    try:
        cities = session.query(City).filter(
            City.centroid_lat.isnot(None),
            City.centroid_lon.isnot(None)
        ).all()

        CHUNK_SIZE = 1000
        for i in range(0, len(cities), CHUNK_SIZE):
            pipe = redis_client.pipeline()
            for city in cities[i:i + CHUNK_SIZE]:
                try:
                    lon = float(city.centroid_lon)
                    lat = float(city.centroid_lat)
                    pipe.geoadd("cities:geo", (lon, lat, city.geoidfq))
                except (TypeError, ValueError):
                    continue
            pipe.execute()
        print(f"Loaded {len(cities)} cities into Redis.")
        return len(cities)
    finally:
        session.close()

def city_data_key(geoidfq):
    return f"city:data:{geoidfq}"

def geojson_state_key(geoidfq):
    return f"geojson:state:{geoidfq}"

def geojson_county_key(geoidfq):
    return f"geojson:county:{geoidfq}"

def cities_geo_index():
    return "cities:geo"
