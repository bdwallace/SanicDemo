import os

PROJECT_PATH = os.getcwd()
ENV = os.environ.get("ENV")
DB_CONFIG = {
    'DB_USER': os.environ.get("DB_USER", 'root'),
    'DB_PASSWORD': os.environ.get("DB_PASSWORD", '@Root123456'),
    "DB_HOST": os.environ.get("DB_HOST", '192.168.85.10'),
    'DB_PORT': os.environ.get("DB_PORT", '3306')
}


TORTOISE_ORM = {
    'db_url': f"mysql://{DB_CONFIG['DB_USER']}:{DB_CONFIG['DB_PASSWORD']}@{DB_CONFIG['DB_HOST']}:{DB_CONFIG['DB_PORT']}/demo",
    'modules': {'models': ['modules.demo']}
}



REDIS_CONFIG = {
    "REDIS_HOST": os.environ.get("REDIS_HOST", '192.168.85.10'),
    "REDIS_PORT": os.environ.get("REDIS_PORT", 6388),
    "REDIS_PASSWORD": os.environ.get("REDIS_PASSWORD", 'GwNouyMM345Wh3maKwz'),
    "REDIS_DB": os.environ.get("REDIS_DB", 0),
    'REDIS': f"redis://:{os.environ.get('REDIS_PASSWORD', 'GwNouyMM345Wh3maKwz')}@{os.environ.get('REDIS_HOST', '192.168.85.10')}:{os.environ.get('REDIS_PORT', 6388)}/{os.environ.get('REDIS_DB', 10)}"
}