from flask import Flask

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['CACHE_TYPE'] = 'simple'

from web.view.index import web
app.register_blueprint(web)