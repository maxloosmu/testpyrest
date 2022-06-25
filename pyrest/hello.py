from flask import Flask, request
import sys, string, os, datetime
from pathlib import Path

app = Flask(__name__)

@app.route("/get")
def getCommandList():
  textStr = ""
  with open("/home/maxloo/pyrest/temp/commands.txt", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  return textStr

@app.route("/post", methods=['POST'])
def processCSV():
  data = request.form.to_dict()
  
  target = ""
  if data['command'].find("native"): 
    target = "native"
  elif data['command'].find("prolog"): 
    target = "prolog"
  uuid = data['uuid']
  # uuidFolder = "mkdir /home/maxloo/pyrest/temp/" + uuid
  spreadsheetId = data['spreadsheetId']
  # spreadsheetIdFolder = "mkdir /home/maxloo/pyrest/temp/"+uuid+"/"+spreadsheetId
  sheetId = data['sheetId']
  # sheetIdFolder = "mkdir /home/maxloo/pyrest/temp/"+uuid+"/"+spreadsheetId+"/"+sheetId
  targetFolder = "mkdir /home/maxloo/pyrest/temp/"+uuid+"/"+spreadsheetId+"/"+sheetId+"/"+target
  targetFile = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ") + ".csv"
  targetPath = "/home/maxloo/pyrest/temp/"+uuid+"/"+spreadsheetId+"/"+sheetId+"/"+target+"/"+targetFile
  Path(targetFolder).mkdir(parents=True, exist_ok=True)
  # if not os.path.isdir(uuidFolder+"/"):
  #   os.system(uuidFolder)
  # if not os.path.isdir(spreadsheetIdFolder+"/"):
  #   os.system(spreadsheetIdFolder)
  # if not os.path.isdir(sheetIdFolder+"/"):
  #   os.system(sheetIdFolder)
  # if not os.path.isdir(targetFolder+"/"):
  #   os.system(targetFolder)
  command = data['command']+" "+targetPath+" > /home/maxloo/pyrest/temp/output.txt"
  textStr = ""
  with open(targetPath, "w") as fout:
    fout.write(data['csvString'])
  os.system(command)
  with open("/home/maxloo/pyrest/temp/output.txt", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  return textStr

@app.route("/you/<name>")
def user(name):
  return "Hello, {}!".format(name)

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)