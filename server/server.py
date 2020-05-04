##
# Main Server Module.
#
# When invoking Flask, ensure `FLASK_APP` is pointing to this file.

import flask
import json
import util
import hardware
from pin import PIN
import werkzeug
import os

app = flask.Flask(__name__)
pin = PIN()
him = hardware.HIM()

##############
## HANDLERS ##
##############

@app.route('/api/status')
@util.apiwrap
def api_status():
    return {
        "success": True,
        "data": {
            "rolls_remaining": him.get_remaining_rolls()
        }
    }

@app.route('/api/generate_pin')
@util.apiwrap
def api_generatepin():
    success, result = pin.generate_new_pin()
    if not success:
        return {
            "success": False,
            "reason": result
        }
    else:
        him.change_pin(result)
        if os.getenv("TPAAS_DEBUG") == "true":
            return {
                "success": True,
                "data": {
                    "pin": result
                }
            }
        return {
            "success": True
        }

@app.route('/api/dispense')
@util.apiwrap
def api_dispense():
    # Make sure the auth token parameter was given
    if not "auth" in flask.request.args:
        return {
            "success": False,
            "reason": "This endpoint requires authentication"
        }
    # Validate the authentication token
    if not pin.check_pin(flask.request.args.get("auth")):
        return {
            "success": False,
            "reason": "Authentication Failure"
        }
    # Yeet the poo poo paper
    him.dispense()
    return {
        "success": True
    }

@app.route('/')
def static_redirect():
    response = flask.Response()
    response.headers["Location"] = "app/"
    response.status_code = 301
    return response

@app.route('/app/<path:path>')
def static_handler(path):
    print("HANDLER")
    return flask.send_from_directory('static/web-build', path)

####################
## ERROR HANDLERS ##
####################

@app.errorhandler(404)
@util.apiwrap
def handle_bad_request(e):
    return {
        "success": False,
        "reason": str(e)
    }

##################
## TEST METHODS ##
##################

import subprocess

@app.route('/test')
def test_getpage():
    branch = subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True).decode()
    commit = subprocess.check_output('git rev-parse --verify HEAD', shell=True).decode()
    clean = subprocess.Popen('git diff-index --quiet HEAD --', shell=True, stdout=subprocess.PIPE)
    clean.communicate()
    clean = "clean" if clean.returncode == 0 else "dirty"
    return flask.render_template('test.html', branch=branch, commit=commit, clean=clean)

@app.route('/test/missing_param')
@util.apiwrap
def test_missingparam():
    return {
        "success": False
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

@app.route('/test/handle_exception')
@util.apiwrap
def test_handleexception():
    raise Exception("Test Exception!")