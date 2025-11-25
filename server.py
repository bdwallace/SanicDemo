import asyncio, os, logging
# import uvloop
from arq import cron
from arq.connections import RedisSettings
from arq.worker import create_worker
from httpx import AsyncClient
from sanic import Sanic
from blueprints import bp
from tortoise import Tortoise
from core import redis
from settings import TORTOISE_ORM, REDIS_CONFIG
from views import testdemo

app = Sanic("Demo")


app.config.update(REDIS_CONFIG)
app.config.update({"WORKERS": 5})
redis.init_app(app)

app.blueprint(bp)  # 注册蓝图
app.config['DEBUG'] = True


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
    functions = [dingshi_task, testdemo]

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
    # 设置系统参数

    worker = create_worker(WorkerSettings, job_timeout=86400)
    print('Async arq running')
    try:
        await worker.async_run()
        await worker.close()
    # except asyncio.exceptions.CancelledError as e:
    #     print('arq连接关闭异常', e)
    except Exception as e:
        print('arq连接关闭异常', e)



@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    print('关闭前关闭redis、mysql连接')
    await Tortoise.close_connections()

@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    print("服务已停止")


if __name__ == "__main__":
    # main()
    app.run(host="0.0.0.0", port=5000, auto_reload=True, debug=False, access_log=True)