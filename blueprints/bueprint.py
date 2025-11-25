import logging, cgi, io

from sanic import json

from utils import redis_get
from .urls import bp


@bp.on_request
async def request_middleware(request):
    # 在视图之前执行
    try:
        token = request.cookies.get("token")

        if not token:
            token = request.headers.Authorization

        result = await redis_get(token)
        # print(result, token)
        # user = await UsersModel.filter(user_name="admin").first()
        # payload = {"user_name": user.user_name, "password": user.password}
        # token = jwt.encode(payload, user.password)

        if "/v1/api/login" not in request.url:
            if not result:
                print('您未登录,请先登录')
                # return json({"code": 401, "msg": "You are unauthorized!"})
        elif request.method != "POST":
            if not result:
                print('您未登录,请先登录')
                # return json({"code": 401, "msg": "You are unauthorized!"})

        if "/v1/api/login" in request.url or 'v1/api/grant' in request.url:
            return

    except Exception as e:
            logging.error('Middleware error:', e)


@bp.on_response
async def response_middleware(request, response):
    # 在视图之后执行
    CORS_HEADERS = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    # print('response body:', response.body)
    response.headers.update(**CORS_HEADERS)


def parse_form_data(body):
    form = cgi.FieldStorage(fp=io.BytesIO(body), environ={'REQUEST_METHOD': 'POST'})
    data = {}
    for field in form.keys():
        values = [form[field].value]
        data[field] = values
    return data