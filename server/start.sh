#!/bin/bash

export FLASK_APP=server.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000
export TPAAS_SHIM=true

flask run
