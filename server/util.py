##
# Stupidly Overcomplicated Utilities that do stuff

import flask
import json
import traceback

##
# Exception Handling Wrapper.
#
# If an exception is raised by the application while handling a web request,
# this decorator will intercept it and convert it into a user friendly response.
# This ensures that all messages sent to the app are properly formatted JSON
# messages, even if the handling of a particular request causes an error.
def exceptionhandler(func):
    
    def func_wrapper(*args):
        try:
            # Attempt to execute subfunction normally
            return func(*args)
        except Exception as e:
            # Build a new response
            obj = {
                "endpoint": str(flask.request.url_rule),
                "method": flask.request.method,
                "success": False,
                "reason": "Server encountered an internal error",
                "data": {
                    "exception_type": type(e).__name__,
                    "exception_msg": str(e),
                    "trace": traceback.format_exc()
                }
            }
            resp = flask.make_response()
            resp.status_code = 500
            resp.status = "Internal Server Error"
            resp.headers['Content-Type'] = 'application/json; charset=utf-8'
            resp.data = json.dumps(obj, indent=4).encode('utf-8')
            return resp

    # Definitely not a dirty hack to circumvent a flask error checker
    func_wrapper.__name__ = func.__name__
    
    return func_wrapper

##
# Malformed response exception.
# This exception is raised if an api handler method generates a response that
# is not compliant with the API specification.
class MalformedResponseException(Exception):

    def __init__(self, detail, offender = None):
        self.detail = detail
        self.offender = offender

##
# API response wrapper.
#
# This decorator ensures that responses generated by calls to the API adhere to
# the specification.
#
# If an api handler generates an invalid resopnse, a MalformedResponseException
# will be raised to the exception handler.
def apiwrap(func):
    def validate_type(obj, key, t):
        if not type(obj[key]) == t:
            raise MalformedResponseException(
                "Illegal parameter type \"{}\" for \"{}\" (expected \"{}\")"
                .format(type(obj[key]), key, t))

    @exceptionhandler
    def func_wrapper(*args):
        # Call the wrapped function
        obj = func(*args)

        # Validate required parameters
        if not "success" in obj.keys():
            raise MalformedResponseException("Missing required parameter \"success\" in response", obj)
        if not "reason" in obj.keys():
            # `reason` can be omitted if success is true
            if obj["success"] == True:
                obj["reason"] = ""
            else:
                raise MalformedResponseException("Missing required parameter \"reason\" in response", obj)
        if not "data" in obj.keys():
            # `data` can be omitted because some requests have no response
            obj["data"] = {}
        # Validate required parameter types
        validate_type(obj, "success", bool)
        validate_type(obj, "reason", str)
        validate_type(obj, "data", dict)
        # Check for extra parameters
        p = list(obj.keys())
        p.remove("success")
        p.remove("reason")
        p.remove("data")
        if len(p) > 0:
            raise MalformedResponseException("Extraneous response parameters found! [{}]".format(",".join(p)))

        # Add info fields
        obj["endpoint"] = str(flask.request.url_rule)
        obj["method"] = flask.request.method

        # Create the response
        resp = flask.make_response()
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        resp.data = json.dumps(obj, indent=4).encode('utf-8')
        return resp

    # Definitely not a dirty hack to circumvent a flask error checker
    func_wrapper.__name__ = func.__name__
    
    return func_wrapper