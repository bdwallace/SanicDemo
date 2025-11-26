import random
import time
from functools import wraps

from sanic import json


def getRandChar(count):
    chars = []
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    for i in range(count):
        char = random.choice(alphabet)
        chars.append(char)
    return ''.join(chars)

def rate_limit(limit=5, window=60):
    """限速方法"""
    history = {}

    def decorator(f):
        @wraps(f)
        async def wrapper(self, request, *args, **kwargs):
            ip = request.ip
            now = time.time()
            timestamps = history.get(ip, [])

            # 清理过期记录
            timestamps = [t for t in timestamps if now - t < window]

            if len(timestamps) >= limit:
                return json({"code": 429, "msg": "该接口调用过于频繁"}, status=429)

            timestamps.append(now)
            history[ip] = timestamps
            return await f(self, request, *args, **kwargs)
        return wrapper
    return decorator