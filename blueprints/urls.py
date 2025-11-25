from sanic.blueprints import Blueprint
from views import *



bp = Blueprint("OSS", url_prefix='/api', version='v1')
bp.add_route(demoTest.as_view(), '/demo', name='demo', methods=['GET', 'POST'])
