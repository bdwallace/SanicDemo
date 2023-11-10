# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren blueprint_api
All rights reserved
create time '2019/6/27 10:18'
Usage:
各种第三方插件 通过 init_app() 注册的方式 都集中此地
"""
import logging.config
import os
from sanic_redis import SanicRedis
from arq import create_pool
from arq.connections import RedisSettings
from settings import REDIS_CONFIG

# Log
logger = logging.getLogger("sanic.root")

# redis
redis = SanicRedis()

async def get_arq_obj():
    redis_arq = await create_pool(
        RedisSettings(host=REDIS_CONFIG.get('REDIS_HOST'),
                      port=int(REDIS_CONFIG.get("REDIS_PORT")),
                      password=REDIS_CONFIG.get("REDIS_PASSWORD"))
    )
    return redis_arq

# __all__ = ['logger', 'redis']