from flask import Flask, request
import sys, string, os


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def helloWorld():
  data = request.form.to_dict()
  textStr = ""
  # joined = "-".join(data.values()) + "\n"
  # print(joined)
  with open("/home/maxloo/pyrest/test.csv", "w") as fout:
    fout.write(data['csvString'])
    # fo.write(joined)
  os.system("bash cgi.sh")
  with open("/home/maxloo/pyrest/output.txt", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  return textStr

# @app.route("/<name>")
# def user(name):
#   return "Hello, {}!".format(name)

# @app.route("/post")
# def posting():
#   with open("/Users/maxloo/dsl/lib/haskell/natural4/test/test.csv", "w") as fo:
#     fo.write("This is Test Data")
#   return "test.csv file transfer success!\n"



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)