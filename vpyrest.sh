#!/bin/sh

virtualenv pyrest/
cd pyrest
source bin/activate
bin/pip3 install flask

export FLASK_APP=hello.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=8080
