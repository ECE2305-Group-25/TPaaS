##
# Main Server Module.
#
# When invoking Flask, ensure `FLASK_APP` is pointing to this file.

import flask
import json
import util
import hardware
from pin import PIN

app = flask.Flask(__name__)
pin = PIN()

##############
## HANDLERS ##
##############

@app.route('/api/status')
@util.apiwrap
def api_status():
    return {
        "success": True,
        "data": {
            "rolls_remaining": hardware.get_remaining_rolls()
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
        hardware.change_pin(result)
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
    # Dispense
    hardware.yeet_the_poo_poo_paper()
    return {
        "success": True
    }

##########################
## APIWRAP TEST METHODS ##
##########################

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