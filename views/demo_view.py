import asyncio
from sanic.response import json
from sanic.views import HTTPMethodView
from utils.redis_fun import redis_getdict, redis_setdict, redis_set, redis_get
from core import get_arq_obj


async def testdemo(ctx):
    while True:
        await asyncio.sleep(3)
        print('耗时任务测试')

class demoTest(HTTPMethodView):

    async def get(self, request):
        params = request.ctx.params
        print(params)

        # arq = await get_arq_obj()
        # await arq.enqueue_job("testdemo")
        return json({'code': 200, 'msg': 'successful'})

    async def post(self, request):
        data = request.ctx.json
        print(data)
        # await conn.rpush('name', 'spencer')
        # df = await conn.lrange('name', 0, -1)
        await redis_set('name', 'spencer')
        df = await redis_get('name')
        print(df)
        return json({'code': 200, 'status': 'success'})

        await redis_setdict('test', data)
        df = await redis_getdict('test')
        print(type(df), df)
        return json({'code': 200, 'status': 'success', 'data': df})
