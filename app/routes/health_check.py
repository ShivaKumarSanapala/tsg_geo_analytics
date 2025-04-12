from flask import Blueprint, jsonify
from app.services import cache

health_api = Blueprint('health_api', __name__)

@health_api.route("/health", methods=["GET"])
def health_check():
    redis_status = check_redis()
    if isinstance(redis_status, tuple):
        return jsonify({
            "health": "DEGRADED",
            "redis": redis_status[0]
        }), 500

    return jsonify({
        "health": "OK",
        "redis": redis_status
    }), 200

@health_api.route("/health/ping_redis", methods=["GET"])
def ping_redis():
    result = check_redis()
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify({"redis": result}), 200

def check_redis():
    try:
        pong = cache.redis_client.ping()
        return {"status": "OK", "ping": pong}
    except Exception as e:
        return {"error": str(e)}, 500
