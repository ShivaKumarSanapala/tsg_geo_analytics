from flask import request, jsonify

from app.services.geospatial import fetch_cities_within_polygon, fetch_nearby_cities, fetch_encompassing_boundaries, \
    get_nearby_cities_from_redis
from flask import Blueprint

geo_api = Blueprint('geo_api', __name__)

@geo_api.route('/nearby-redis', methods=['GET'])
def get_nearby_from_redis():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 5000))
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid parameters"}), 400

    if page < 1 or limit < 1:
        return jsonify({"error": "Page and limit must be positive integers"}), 400

    try:
        result = get_nearby_cities_from_redis(lat, lng, radius, page, limit)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@geo_api.route('/query_cities_within_polygon', methods=['POST'])
def query_cities_within_polygon():
    data = request.get_json()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'aland')
    sort_order = request.args.get('sort_order', 'asc')
    return fetch_cities_within_polygon(data, page, per_page, sort_by, sort_order)

@geo_api.route('/nearby', methods=['GET'])
def get_nearby():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 5000))
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid lat/lng, radius, page, or limit"}), 400

    return fetch_nearby_cities(lat, lng, radius, page, limit)

@geo_api.route('/encompassing_boundaries', methods=['GET'])
def encompassing_boundaries():
    geoidfq = request.args.get('geoidfq')
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid page or limit parameters"}), 400

    return fetch_encompassing_boundaries(geoidfq, page, limit)
