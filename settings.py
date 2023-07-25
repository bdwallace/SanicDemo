import os

PROJECT_PATH = os.getcwd()

# DB_CONFIG = {
#     'DB_USER': os.environ.get("DB_USER"),
#     'DB_PASSWORD': os.environ.get("DB_PASSWORD"),
#     "DB_HOST": os.environ.get("DB_HOST"),
#
# }

DB_CONFIG = {
    'DB_USER': 'root',
    'DB_PASSWORD': "Root12456",
    "DB_HOST": "192.168.10.10",
}

TORTOISE_ORM = {
    'db_url': f"mysql://{DB_CONFIG['DB_USER']}:{DB_CONFIG['DB_PASSWORD']}@{DB_CONFIG['DB_HOST']}/Demo",
    'modules': {'models': ['modules.demo']}
}



SystemSetting = {
    "DNS_CHECK_HZ": 3,  # dns检查频率
    "DNS_CHECK_TIMES": 50,  # DNS检查次数
    "CHALLENGE_HZ": 3,  # 挑战频率
    "ALERT_TIMES": 1,  # 告警次数
    "RENEW_DAYS": 7,  # 提前续费天数
    "REFRESH_HZ": 1,  # 刷新频率
    "WAIT_TIME": 60
}

#
# REDIS_CONFIG = {
#     "REDIS_HOST": os.environ.get("REDIS_HOST"),
#     "REDIS_PORT": os.environ.get("REDIS_PORT"),
#     "REDIS_PASSWORD": os.environ.get("REDIS_PASSWORD"),
#     'REDIS': f"redis://:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/0"
# }
REDIS_CONFIG = {
    "REDIS_HOST": "192.168.10.10",
    "REDIS_PORT": 6379,
    'REDIS_PASSWORD': "e910qCKTYXRyjKLj",
    'REDIS': f"redis://:e910qCKTYXRyjKLj@192.168.10.10:6379/0"
}