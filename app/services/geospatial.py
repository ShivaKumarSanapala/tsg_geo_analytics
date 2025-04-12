import json
from flask import jsonify
from sqlalchemy import text
from geoalchemy2.functions import ST_Distance, ST_SetSRID, ST_GeomFromText, ST_Within, ST_Contains

from app.services import cache
from app.services.database import get_db, SessionLocal
from app.models.entities import City, County, State, StateDemography, CountyDemography
from app.utils.geo_utils import to_geojson_from_wkb

def get_nearby_cities_from_redis(lat, lng, radius, page, limit):
    offset = (page - 1) * limit
    redis_client = cache.redis_client

    all_city_ids = redis_client.geosearch(
        "cities:geo",
        longitude=lng,
        latitude=lat,
        radius=radius,
        unit='m',
        withdist=True,
        sort='ASC'
    )

    total_count = len(all_city_ids)
    paginated_city_ids = all_city_ids[offset:offset + limit]
    city_ids = [item[0] for item in paginated_city_ids]
    distances = {item[0]: item[1] for item in paginated_city_ids}

    session = SessionLocal()
    try:
        nearby = []
        missing_ids = []
        city_map = {}

        # Try to get cached cities from Redis
        for cid in city_ids:
            key = f"city:data:{cid}"
            cached_city = redis_client.get(key)
            if cached_city:
                city = json.loads(cached_city)
                city_map[cid] = city
            else:
                missing_ids.append(cid)

        # Fetch missing cities from DB
        if missing_ids:
            db_cities = session.query(City).filter(City.geoidfq.in_(missing_ids)).all()
            for city in db_cities:
                city_data = {
                    "name": city.name,
                    "geoidfq": city.geoidfq,
                    "lat": city.centroid_lat,
                    "lng": city.centroid_lon,
                    "geojson": to_geojson_from_wkb(city.wkb_geometry)
                }
                redis_client.set(f"city:data:{city.geoidfq}", json.dumps(city_data))
                city_map[city.geoidfq] = city_data

        # Build nearby list
        for cid in city_ids:
            city_data = city_map.get(cid)
            if city_data:
                city_data["distance"] = distances[cid]
                nearby.append(city_data)

        return {
            "latitude": lat,
            "longitude": lng,
            "radius": radius,
            "page": page,
            "limit": limit,
            "total_count": total_count,
            "nearby": nearby
        }

    finally:
        session.close()

def fetch_demographics(lat, lng):
    if lat is None or lng is None:
        return jsonify({"error": "lat and lng query parameters are required"}), 400

    point_wkt = f'POINT({lng} {lat})'
    db = next(get_db())
    redis_client = cache.redis_client

    try:
        state_obj = db.query(State).filter(
            ST_Contains(State.wkb_geometry, ST_SetSRID(ST_GeomFromText(point_wkt), 4326))
        ).first()
        if not state_obj:
            return jsonify({"error": "No state found for given coordinates"}), 404

        county_obj = db.query(County).filter(
            ST_Contains(County.wkb_geometry, ST_SetSRID(ST_GeomFromText(point_wkt), 4326))
        ).first()
        if not county_obj:
            return jsonify({"error": "No county found for given coordinates"}), 404

        state_geo_key = f"geojson:state:{state_obj.geoidfq}"
        county_geo_key = f"geojson:county:{county_obj.geoidfq}"

        # Try to get cached geometry
        state_geojson = redis_client.get(state_geo_key)
        county_geojson = redis_client.get(county_geo_key)

        # If not cached, convert and cache
        if not state_geojson:
            state_geojson = to_geojson_from_wkb(state_obj.wkb_geometry)
            redis_client.set(state_geo_key, json.dumps(state_geojson))  # no TTL
        else:
            state_geojson = json.loads(state_geojson)

        if not county_geojson:
            county_geojson = to_geojson_from_wkb(county_obj.wkb_geometry)
            redis_client.set(county_geo_key, json.dumps(county_geojson))
        else:
            county_geojson = json.loads(county_geojson)

        state_demo = db.query(StateDemography).filter_by(geoidfq=state_obj.geoidfq).all()
        county_demo = db.query(CountyDemography).filter_by(geoidfq=county_obj.geoidfq).all()

        def model_to_dict(obj):
            return {col.name: getattr(obj, col.name) for col in obj.__table__.columns}

        return jsonify({
            "state": {
                "name": state_obj.name,
                "geography": state_geojson,
                "demographics": [model_to_dict(d) for d in state_demo]
            },
            "county": {
                "name": county_obj.name,
                "geography": county_geojson,
                "demographics": [model_to_dict(d) for d in county_demo]
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def fetch_cities_within_polygon(data, page, per_page, sort_by, sort_order):
    if "polygon_wkt" not in data:
        return jsonify({"error": "polygon_wkt is required"}), 400

    try:
        polygon_geom = ST_SetSRID(ST_GeomFromText(data["polygon_wkt"]), 4326)
    except Exception as e:
        return jsonify({"error": f"Invalid polygon WKT: {str(e)}"}), 400

    redis_client = cache.redis_client

    with next(get_db()) as db:
        query = db.query(City.geoidfq).filter(
            ST_Within(ST_SetSRID(City.wkb_geometry, 4326), polygon_geom)
        )

        if sort_order not in ['asc', 'desc']:
            return jsonify({"error": "Invalid sort_order. Must be 'asc' or 'desc'."}), 400

        order_column = getattr(City, sort_by)
        query = query.order_by(order_column.asc() if sort_order == 'asc' else order_column.desc())

        # Get just geoidfqs for pagination
        city_ids = [r[0] for r in query.offset((page - 1) * per_page).limit(per_page).all()]
        total = db.query(City).filter(
            ST_Within(ST_SetSRID(City.wkb_geometry, 4326), polygon_geom)
        ).count()

        cities = []
        missing_ids = []
        city_map = {}

        # Try Redis cache
        for cid in city_ids:
            key = f"city:data:{cid}"
            cached = redis_client.get(key)
            if cached:
                city_map[cid] = json.loads(cached)
            else:
                missing_ids.append(cid)

        # Fetch missing cities from DB
        if missing_ids:
            db_cities = db.query(City).filter(City.geoidfq.in_(missing_ids)).all()
            for city in db_cities:
                city_data = {
                    "name": city.name,
                    "state_name": city.state_name,
                    "aland": city.aland,
                    "lat": city.centroid_lat,
                    "lng": city.centroid_lon,
                    "geoidfq": city.geoidfq
                }
                redis_client.set(f"city:data:{city.geoidfq}", json.dumps(city_data))
                city_map[city.geoidfq] = city_data

        # Maintain original order
        cities = [city_map[cid] for cid in city_ids if cid in city_map]

        return jsonify({
            "cities": cities,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_cities": total,
                "total_pages": (total + per_page - 1) // per_page
            }
        })

def fetch_nearby_cities(lat, lng, radius, page, limit):
    offset = (page - 1) * limit
    session = SessionLocal()
    try:
        point_geom = ST_SetSRID(ST_GeomFromText(f'POINT({lng} {lat})'), 4326)

        count_query = session.query(City).filter(
            text("""
                ST_DWithin(
                    city_table.wkb_geometry::geography,
                    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
                    :radius
                )
            """)
        ).params(lat=lat, lng=lng, radius=radius)

        total_count = count_query.count()

        paginated_query = count_query.add_columns(
            ST_Distance(City.wkb_geometry, point_geom).label('distance')
        ).order_by('distance').offset(offset).limit(limit)

        results = paginated_query.all()

        nearby = [{
            "name": city.name,
            "geoidfq": city.geoidfq,
            "lat": city.centroid_lat,
            "lng": city.centroid_lon,
            "distance": distance,
            "geojson": to_geojson_from_wkb(city.wkb_geometry)
        } for city, distance in results]

        return jsonify({
            "latitude": lat, "longitude": lng, "radius": radius,
            "page": page, "limit": limit,
            "total_count": total_count, "nearby": nearby,
            "total_pages": (total_count + limit - 1) // limit
        })
    finally:
        session.close()

def fetch_encompassing_boundaries(geoidfq, page, limit):
    with next(get_db()) as db:
        state = db.query(State).filter(State.geoidfq == geoidfq).first()
        county = db.query(County).filter(County.geoidfq == geoidfq).first()
        city = db.query(City).filter(City.geoidfq == geoidfq).first()

        if not state and not county and not city:
            return jsonify({"error": "No regions found for the given geoidfq"}), 404

        encompassing_regions = []
        total_count = 0
        offset = (page - 1) * limit

        # Function to handle the building of response and pagination
        def add_encompassing_regions(query, region_type):
            nonlocal total_count
            total_count = query.count()
            regions = query.offset(offset).limit(limit).all()
            return [{
                "name": region.name,
                "type": region_type,
                "geoidfq": region.geoidfq,
                "geojson": to_geojson_from_wkb(region.wkb_geometry)
            } for region in regions]

        # If state is provided
        if state:
            counties_query = db.query(County).filter(
                ST_Within(County.wkb_geometry, state.wkb_geometry)
            )
            encompassing_regions = add_encompassing_regions(counties_query, "County")

        # If county is provided
        elif county:
            cities_query = db.query(City).filter(
                ST_Within(City.wkb_geometry, county.wkb_geometry)
            )
            encompassing_regions = add_encompassing_regions(cities_query, "City")

        # If city is provided (no encompassing boundaries for cities in the current setup)
        elif city:
            return jsonify({"message": "No encompassing boundaries for cities."}), 200

        return jsonify({
            "encompassing_regions": encompassing_regions,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_count": total_count,
                "total_pages": (total_count + limit - 1) // limit
            }
        })