# https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/
# https://devcenter.heroku.com/articles/python-pip
# https://devcenter.heroku.com/articles/build-docker-images-heroku-yml

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return "<h1>Hello World</h1>"

