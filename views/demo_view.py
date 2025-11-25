import asyncio
from sanic.response import json
from sanic.views import HTTPMethodView
from tortoise.query_utils import Q

from modules.demo import Demo
from utils import datatime_serialize, uuid_serialize
from utils.redis_fun import redis_getdict, redis_setdict, redis_set, redis_get
from core import get_arq_obj


async def testdemo(ctx):
    count = 0
    while True:
        await asyncio.sleep(3)
        print('耗时任务测试')
        count += 1
        if count >= 3:
            break



async def auto_inject(app):
    count = 0
    while True:
        await asyncio.sleep(3)
        print('耗时任务测试', app.name)
        count += 1
        if count >= 3:
            break


class demoTest(HTTPMethodView):
    async def __fetchData(self, page=1, pagesize=10, search=""):
        if type(page) == str:
            page = int(page)
        if type(pagesize) == str:
            pagesize = int(pagesize)
        offset_num = (page - 1) * pagesize
        condition = Q(Q(user_name__icontains=search) | Q(email__icontains=search) | Q(login_ip__icontains=search) | Q(login_time__icontains=search))
        total = await Demo.filter(condition).distinct()
        total = len(total)
        result = await (Demo.filter(condition).offset(offset_num).limit(pagesize).order_by("user_name")).distinct()

        data = datatime_serialize(result)
        data = uuid_serialize(data)
        return data, total

    async def get(self, request):
        params = request.args_query
        page = params.get("page", 1)
        pagesize = params.get("pagesize", 15)
        search = params.get('search', "")
        spencer = params.get("spencer")
        print(type(params['spencer']), spencer)
        data, total = await self.__fetchData(page, pagesize, search)
        return json({"code": 200, 'msg': 'Success', 'data': data, 'total': total})

    async def post(self, request):
        data = request.json
        print(data)
        # await conn.rpush('name', 'spencer')
        # df = await conn.lrange('name', 0, -1)
        await redis_set('name', 'spencer')
        df = await redis_get('name')
        print('redis数据', df)
        return json({'code': 200, 'status': 'success'})

        await redis_setdict('test', data)
        df = await redis_getdict('test')
        print('redis数据', type(df), df)
        return json({'code': 200, 'status': 'success', 'data': df})

    async def put(self, request):
        params = request.args
        print(params.get('search'))
        # 异步任务方案1
        # arq = await get_arq_obj()
        # await arq.enqueue_job("testdemo")
        # 异步任务方案2
        request.app.add_task(auto_inject)
        return json({'code': 200, 'msg': 'successful'})
