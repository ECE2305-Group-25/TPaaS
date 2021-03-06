# Application Programming Interface Description

[Basics](#Basics)  
[Responses](#Responses)  
[Authentication](#Authentication)  
[Endpoints](#Endpoints)

[`/api/status`](#apistatus)  
[`/api/dispense`](#apidispense)  
[`/api/openlid`](#apiopenlid)

---

## Basics

There are four basic HTTP request methods, GET, POST, PUT, and DELETE.  To
maintain simplicity, this interface only deals with the first type, the
humble GET request.

A get request is formatted like such

```
GET https://web.site/api/endpoint?param1=value1&param2=value2
```

## Responses

All API calls generate responses in the JSON format. They are formatted like
this:

```
{
    "endpoint": "/api/status",
    "request_type": "GET",
    "success": true,
    "reason": "",
    "data": {
        "rolls_remaining": 4
    }
}
```

In addition to any endpoint-specific information, all requests will contain the
following four fields:

### `endpoint`

The `endpoint` parameter contains the path the initiating request was made to.
If the user makes a request to `web.site/api/foo` this parameter will contain
the string `/api/foo`.

### `request_type`

The `request_type` parameter contains the requesting method used.

### `success` and `reason`

The `success` parameter returns `true` if the request was completed
successfully, and `false` if an error occurred.  If the request was a success,
the `reason` parameter will be empty, but if the request fails this parameter
will contain a human-readable message explaining what went wrong.

## Authentication

Where authentication is required, it will be handled by a GET parameter called
`auth`, containing a **TO BE DETERMINED** authentication string.  A sample
authenticated request is as follows:

```
GET https://web.site/api/secure_endpoint?auth=132435&foo=bar
```

## Endpoints

The following endpoints are defined

### `/api/status`

Authentication Required: No

The `status` endpoint returns the current status of the system, including the
number of rolls of toilet paper remaining, and weather or not the dispenser
hardware is currently connected to the control server.

Sample Request:
```
GET https://web.site/api/status
```

Sample Response:
```json
{
    "endpoint": "/api/status",
    "request_type": "GET",
    "success": true,
    "reason": "",
    "data": {
        "rolls_remaining": 4
    }
}
```

### `/api/dispense`

Authentication Required: Yes

The `dispense` endpoint surprisingly instructs the toilet paper dispenser to
release a roll.  This endpoint requires an authentication token, which will be
provided to the user via the built in displan in the unit.

Sample Request:
```
GET https://web.site/api/dispense?auth=12345
```

Sample Success Response:
```json
{
    "endpoint": "/api/dispense",
    "request_type": "GET",
    "success": true,
    "reason": ""
}
```

Sample Failure Response:
```json
{
    "endpoint": "/api/dispense",
    "request_type": "GET",
    "success": false,
    "reason": "Invalid authentication token"
}
```

### `/api/generate_pin`

Authentication Required: No

The `generate_pin` method instructs the server to invalidate the previously
stored pin and push a new one to the integrated display.  Each pin has a
minimum lifespan, and calls to this method made before the minum lifespan has
elapsed will return an error, but the previously generated pin will not be
affected.

Sample Success Response:
```json
{
    "endpoint": "/api/generate_pin",
    "request_type": "GET",
    "success": true,
    "reason": ""
}
```

Sample Failure Response:
```json
{
    "endpoint": "/api/generate_pin",
    "request_type": "GET",
    "success": false,
    "reason": "Pin changed too recently"
}
```