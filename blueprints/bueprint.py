import logging, cgi, io
from .urls import bp


@bp.on_request
def request_middleware(request):
    # 在视图之前执行
    try:
        pass

    except Exception as e:
        logging.error('Middleware error:', e)


@bp.on_response
def response_middleware(request, response):
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