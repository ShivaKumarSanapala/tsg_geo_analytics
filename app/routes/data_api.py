from flask import  request, jsonify
from app.services import cache
from app.services.geospatial import fetch_demographics
from flask import Blueprint

data_api = Blueprint('data_api', __name__)
@data_api.route('/load-cities-to-redis', methods=['POST'])
def load_cities_to_redis():
    try:
        cache.redis_client.ping()
        total = cache.load_cities_to_redis_from_db()
        return jsonify({"message": f"{total} cities loaded into Redis"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@data_api.route('/demographics', methods=['GET'])
def get_demographics():
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    return fetch_demographics(lat, lng)