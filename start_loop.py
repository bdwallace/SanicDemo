import asyncio, os, logging
import nest_asyncio
import uvloop
from arq import cron
from arq.connections import RedisSettings
from arq.worker import create_worker
from signal import signal, SIGINT
from httpx import AsyncClient
from sanic import Sanic
from blueprints import bp
from tortoise import Tortoise
from core import redis
from settings import TORTOISE_ORM, REDIS_CONFIG
from sanic_ext import Extend


app = Sanic("Demo")
Extend(app)
app.config.update(REDIS_CONFIG)
redis.init_app(app)

app.blueprint(bp)  # 注册蓝图
# workers = app.config.get('WORKERS')
# app.ctx.debug = app.config.get('DEBUG')
app.config['DEBUG'] = True
nest_asyncio.apply()

async def startup(ctx):
    ctx['arq'] = AsyncClient()
    print("启动arq....")


async def shutdown(ctx):
    await ctx['arq'].aclose()


async def test_task(ctx):
    logging.info('队列任务运行中...')
    await asyncio.sleep(2)

async def dingshi_task(ctx):
    logging.info('定时任务运行中...')
    await asyncio.sleep(2)


class WorkerSettings:
    # 开发环境不配置密码，生产环境自行配置redis密码
    redis_settings = RedisSettings(host=REDIS_CONFIG['REDIS_HOST'],
                                   port=int(REDIS_CONFIG["REDIS_PORT"]),
                                   password=REDIS_CONFIG["REDIS_PASSWORD"])


    # 监听任务函数
    functions = [dingshi_task]

    # 计划任务
    cron_jobs = [
        cron(dingshi_task, hour={13}, minute={14, 15, 16, 17, 18}),
    ]
    on_startup = startup
    on_shutdown = shutdown

@app.listener('before_server_start')
async def before_server_start(app, loop):
    # 连接数据库
    try:
        # print(TORTOISE_ORM['db_url'],TORTOISE_ORM['modules'])
        await Tortoise.init(db_url=TORTOISE_ORM['db_url'], modules=TORTOISE_ORM['modules'], timezone='Asia/Shanghai')
    except Exception as e:
        print('数据库连接失败：', e)
        return 0
    await Tortoise.generate_schemas()  #启动时生成表,第一次部署需要
    print('数据库已连接')
    # 初始化其他配置
    print('Async Server running...')

    # await app.ctx.server.startup()


@app.listener('after_server_start')
async def after_server_start(app, loop):

    print("Async Server started")



@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    print('关闭前关闭redis、mysql连接')
    await Tortoise.close_connections()

@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    print("服务已停止")


def main():

    serv_coro = app.create_server(host="0.0.0.0", port=5000, return_asyncio_server=True, access_log=True)
    # 设置uvloop相关
    asyncio.set_event_loop(uvloop.new_event_loop())
    loop = asyncio.get_event_loop()
    serv_task = asyncio.ensure_future(serv_coro, loop=loop)
    signal(SIGINT, lambda s, f: loop.stop())

    server = loop.run_until_complete(serv_task)
    loop.run_until_complete(server.startup())
    loop.run_until_complete(server.before_start())
    loop.run_until_complete(server.after_start())

    worker = create_worker(WorkerSettings, job_timeout=86400)
    asyncio.run(worker.async_run())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
    finally:
        loop.run_until_complete(server.before_stop())

        # Wait for server to close
        close_task = server.close()
        loop.run_until_complete(close_task)

        # Complete all tasks on the loop
        for connection in server.connections:
            connection.close_if_idle()
        loop.run_until_complete(server.after_stop())


if __name__ == "__main__":
    main()
    # app.run(host="0.0.0.0", port=5000, auto_reload=True, debug=False)