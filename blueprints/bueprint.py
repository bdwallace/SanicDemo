import logging, ast, cgi, io
from sanic.blueprints import Blueprint
from utils import byte2str
from views import demoTest


bp = Blueprint("OSS", url_prefix='/api', version='v1')
bp.add_route(demoTest.as_view(), '/demo', name='demo', methods=['GET', 'POST'])

@bp.on_request
def request_middleware(request):

    try:
        # print(dir(request))
        # print(request.files)
        if type(request.body) == bytes and request.body != b'':
            try:
                request.ctx.json = ast.literal_eval(byte2str(request.body))
            except:
                # request.ctx.json = parse_form_data(request.body)
                pass
        elif type(request.body) == str:
            request.ctx.json = ast.literal_eval(request.body)


        try:
            request.ctx.params = {key: ast.literal_eval(val[0]) for key, val in request.args.items()}
        except:
            request.ctx.params = {key: val[0] for key, val in request.args.items()}
        logging.info(type(request.args), request.args)
    except Exception as e:
        logging.error('Middleware error:', e)


@bp.on_response
def response_middleware(request, response):
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