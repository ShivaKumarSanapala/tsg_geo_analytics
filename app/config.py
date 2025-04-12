import os
import dotenv

class Config:
    dotenv.load_dotenv()
    POSTGRES_USER = os.getenv("POSTGRES_USER", "tsg_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "tsg_pass")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "tsg_db")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db") #
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    REDIS_HOST = os.getenv("REDIS_HOST", "redis-cache")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
