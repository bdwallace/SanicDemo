import asyncio

from sanic import app
from sanic.response import json
from sanic.views import HTTPMethodView
from tortoise.query_utils import Q

from modules.demo import Demo
from utils import datatime_serialize, uuid_serialize
from utils.others import rate_limit
from utils.redis_fun import redis_getdict, redis_setdict, redis_set, redis_get
from core import get_arq_obj


async def testdemo(ctx):
    count = 0
    while True:
        await asyncio.sleep(1)
        print('耗时任务测试')
        count += 1
        if count >= 3:
            print('任务完成')
            break



async def auto_inject(name):
    count = 0
    while True:
        await asyncio.sleep(0.5)
        print('耗时任务测试', name)
        count += 1
        if count >= 3:
            print('任务完成')
            break


class DemoTestView(HTTPMethodView):

    async def __fetchData(self, page=1, pagesize=20, search=""):
        if type(page) == str:
            page = int(page)
        if type(pagesize) == str:
            pagesize = int(pagesize)
        offset_num = (page - 1) * pagesize
        condition = Q(Q(user_name__icontains=search) | Q(email__icontains=search) | Q(login_ip__icontains=search) | Q(login_time__icontains=search))
        total = await Demo.filter(condition).distinct().count()
        result = await (Demo.filter(condition).offset(offset_num).limit(pagesize).order_by("user_name")).distinct().values()

        data = datatime_serialize(result)
        data = uuid_serialize(data)
        return data, total

    @rate_limit(10, 10)  # 限速装饰器
    async def get(self, request):
        params = request.args
        page = params.get("page", 1)
        pagesize = params.get("pagesize", 20)
        search = params.get('search', "")
        spencer = params.get("spencer")
        return json({"code": 200, 'msg': 'Success'})
        # data, total = await self.__fetchData(page, pagesize, search)
        # return json({"code": 200, 'msg': 'Success', 'data': data, 'total': total})

    async def post(self, request):
        data = request.json
        print(data)
        # await conn.rpush('name', 'spencer')
        # df = await conn.lrange('name', 0, -1)
        await redis_set('name', 'spencer')
        df = await redis_get('name')
        print('redis数据', df)
        await Demo.create(user_name="spencer", password="xxxxx", email='spencer@gmail.com')
        return json({'code': 200, 'status': 'success'})

        await redis_setdict('test', data)
        df = await redis_getdict('test')
        print('redis数据', type(df), df)
        await Demo.create(user_name="spencer", password="xxxxx", email='spencer@gmail.com')
        return json({'code': 200, 'status': 'success', 'data': df})

    async def put(self, request):
        params = request.args
        payload = request.json
        print(payload)
        # 异步任务方案1
        # arq = await get_arq_obj()
        # await arq.enqueue_job("testdemo")
        # 异步任务方案2
        for i in range(3):
            request.app.add_task(auto_inject(name=['auto_inject_name']), name=f"task_name{i}")
            # 查看已有的异步任务
            tasks = request.app.get_task(f"task_name{i}")
            print(tasks)
        return json({'code': 200, 'msg': 'successful'})


def test():
    import requests
    import json

    url = "http://192.168.85.10:5000/v1/api/demo?page=1&pagesize=100"

    payload = json.dumps({
        "code": "456745",
        "data": [
            "sdfg",
            "ertuyesdfg",
            "awedf"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJzcGVuY2VyIiwicGFzc3dvcmQiOiJiMGJkYmM3NzBkZGNkYzM2ZTkwY2FhMTY5YmNkYzQ3ZTAyOGVjN2JiIiwibG9naW5fdGltZSI6IjIwMjUtMTEtMTMgMTE6MTk6MzQuODcwNjA0In0.VjRUyp78zvbxiTRxAqoWhvdkeVS1uraZptcFb3-Sqns; user_name=spencer'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

if __name__ == "__main__":
    for i in range(100):
        test()