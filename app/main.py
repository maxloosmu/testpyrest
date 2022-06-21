# https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return "<h1>Hello World</h1>"

