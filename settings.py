import os

PROJECT_PATH = os.getcwd()

# DB_CONFIG = {
#     'DB_USER': os.environ.get("DB_USER"),
#     'DB_PASSWORD': os.environ.get("DB_PASSWORD"),
#     "DB_HOST": os.environ.get("DB_HOST"),
#     'DB_PORT': os.environ.get("DB_PORT")
# }

DB_CONFIG = {
    'DB_USER': 'root',
    'DB_PASSWORD': "Root123456",
    "DB_HOST": "192.168.10.10",
    'DB_PORT': 3306
}

TORTOISE_ORM = {
    'db_url': f"mysql://{DB_CONFIG['DB_USER']}:{DB_CONFIG['DB_PASSWORD']}@{DB_CONFIG['DB_HOST']}:{DB_CONFIG['DB_PORT']}/Demo",
    'modules': {'models': ['modules.demo']}
}




# REDIS_CONFIG = {
#     "REDIS_HOST": os.environ.get("REDIS_HOST"),
#     "REDIS_PORT": os.environ.get("REDIS_PORT"),
#     "REDIS_PASSWORD": os.environ.get("REDIS_PASSWORD"),
#     'REDIS': f"redis://:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/{os.environ.get('REDIS_DB')}"
# }
REDIS_CONFIG = {
    "REDIS_HOST": "192.168.10.10",
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    'REDIS_PASSWORD': "e910qCKTYXRyjKLj",
}