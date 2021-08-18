from flask import request, render_template, redirect, Blueprint, jsonify
from flask_caching import Cache
from .. import app
from web.controller.screener import find_stock
import json


web = Blueprint('web', __name__)
cache = Cache()
cache.init_app(app)

@web.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@web.route('/stocks', methods=['GET'])
@cache.cached(timeout=193)
def stocks():
    region = request.args.get('region')
    driver = request.args.get('driver')
    if driver not in ['Chrome', 'Explorer', 'Edge', 'Opera', 'Firefox']:
        driver = 'Chrome'
    response = json.dumps(find_stock(region, driver))
    return response
