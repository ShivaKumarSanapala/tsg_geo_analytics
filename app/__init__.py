from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.routes.data_api import data_api
from app.routes.geo_api import geo_api
from app.routes.health_check import health_api
from app.services.cache import init_redis, load_cities_to_redis_from_db

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=["http://localhost:3000"])

# Initialize Redis
init_redis(app)
load_cities_to_redis_from_db()
app.register_blueprint(geo_api)
app.register_blueprint(data_api)
app.register_blueprint(health_api)