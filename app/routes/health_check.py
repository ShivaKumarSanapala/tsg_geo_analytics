from flask import Blueprint, jsonify
from app.services import cache
from app.services.database import get_db
from sqlalchemy import text

health_api = Blueprint('health_api', __name__)

@health_api.route("/health", methods=["GET"])
def health_check():
    redis_status = check_redis()
    db_status = check_db()

    status_code = 200
    overall_health = "OK"

    if isinstance(redis_status, tuple) or isinstance(db_status, tuple):
        overall_health = "DEGRADED"
        status_code = 500

    return jsonify({
        "health": overall_health,
        "redis": redis_status if not isinstance(redis_status, tuple) else redis_status[0],
        "postgres": db_status if not isinstance(db_status, tuple) else db_status[0]
    }), status_code


@health_api.route("/health/ping_redis", methods=["GET"])
def ping_redis():
    result = check_redis()
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify({"redis": result}), 200


@health_api.route("/health/ping_db", methods=["GET"])
def ping_db():
    result = check_db()
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify({"postgres": result}), 200


def check_redis():
    try:
        pong = cache.redis_client.ping()
        return {"status": "OK", "ping": pong}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}, 500


def check_db():
    try:
        session = next(get_db())
        session.execute(text("SELECT 1"))  # lightweight health check
        session.close()
        return {"status": "OK"}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}, 500
