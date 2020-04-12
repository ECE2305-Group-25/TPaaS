##
#

import flask
import json
import util

app = flask.Flask(__name__)

@app.route('/api/status')
@util.apiwrap
def api_status():
    return {
        "success": True,
        "data": {
            "yeet": "yoot",
            "neet": "noot"
        }
    }

@app.route('/test/missing_param')
@util.apiwrap
def test_missingparam():
    return {
        "success": True
    }

@app.route('/test/extra_param')
@util.apiwrap
def test_extraparam():
    return {
        "success": True,
        "data": {
            "foo": "bar"
        },
        "extra": 3
    }