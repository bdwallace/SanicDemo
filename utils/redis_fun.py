# -*- coding: utf-8 -*-
import asyncio
import json
from core import redis


async def redis_get(name):
    """
    获取某个key的值
    :param name:
    :return:
    """
    r = await redis.conn
    return await r.get(name)


async def redis_llen(name):
    """
    获取list长度
    :param name:
    :return:
    """
    r = await redis.conn
    return await r.llen(name)


async def redis_lrange(name, start, end):
    """
    获取list范围数据
    :param name:
    :param start:
    :param end:
    :return:
    """
    r = await redis.conn
    return await r.lrange(name, start, end)


async def redis_rpush(name, val):
    """
    list中尾部添加新数据
    :param name:
    :param val:
    :return:
    """
    r = await redis.conn
    return await r.rpush(name, val)


async def redis_del(key):
    """
    删除某个key
    :param key:
    :return:
    """
    r = await redis.conn
    return await r.delete(key)

async def redis_set(key, value, expire_time=3600):
    """
    存储键值
    :param key:
    :param value:
    :return:
    """
    r = await redis.conn
    return await r.set(key, value, ex=expire_time)

async def redis_setdict(key, data, expire_time=None):
    """
    存储字典数据
    :param key: 字符串类型
    :param data: 字典数据类型
    :return:
    """
    data_str = json.dumps(data)
    r = await redis.conn
    if not expire_time:
        return await r.set(key, data_str)
    return await r.set(key, data_str, ex=expire_time)


async def redis_getdict(key):
    """
    存储字典数据
    :param key: 字符串类型
    :return: 返回字典数据类型
    """
    r = await redis.conn
    data_str = await r.get(key)
    return json.loads(data_str)


if __name__ == "__main__":
    data = {'name': 'baidu.com', 'status': 'pedding'}
    asyncio.run(redis_setdict('test', data))