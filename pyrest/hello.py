from flask import Flask, request, send_from_directory, render_template
import sys, string, os, datetime, glob, shutil
from pathlib import Path

template_dir = "/home/maxloo/pyrest/"
static_dir = "/home/maxloo/pyrest/static/"
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route("/get")
def getCommandList():
  textStr = ""
  with open("/home/maxloo/pyrest/commands.txt", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  return textStr

@app.route("/petri/<uuid>")
def getPetriFile(uuid):
  dirPath = template_dir + "temp/workdir/" + uuid + "/petri/"
  dotPath = dirPath + "LATEST.dot"
  petriFolder = dirPath
  if not os.path.exists(petriFolder):
    Path(petriFolder).mkdir(parents=True, exist_ok=True)
  petriPath = petriFolder + "LATEST.png"
  os.system("dot -Tpng " + dotPath + " -o " + petriPath)
  staticPetri = static_dir + 'petri.png'
  shutil.copy(petriPath, staticPetri)
  return render_template("petri.html")

@app.route("/aasvg/<uuid>")
def getAasvgHtml(uuid):
  aasvgFolder = template_dir + "temp/workdir/" + uuid + "/aasvg/LATEST/"
  aasvgHtml = aasvgFolder + "index.html"
  shutil.copy(aasvgHtml, template_dir + 'aasvg.html')
  return render_template("aasvg.html")

@app.route("/post", methods=['POST'])
def processCsv():
  data = request.form.to_dict()

  target = ""
  if (data['command'].find("native") > -1):
    target = "native/"
  elif (data['command'].find("prolog") > -1):
    target = "prolog/"
  uuid = data['uuid']
  spreadsheetId = data['spreadsheetId']
  sheetId = data['sheetId']
  targetFolder = "/home/maxloo/pyrest/temp/"+uuid+"/"+spreadsheetId+"/"+sheetId+"/"+target
  targetFile = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ") + ".csv"
  targetPath = targetFolder + targetFile
  if not os.path.exists(targetFolder):
    Path(targetFolder).mkdir(parents=True, exist_ok=True)

  command = data['command']+" "+targetPath+" > /home/maxloo/pyrest/temp/output.txt"
  textStr = ""
  with open(targetPath, "w") as fout:
    fout.write(data['csvString'])
  os.system(command)
  with open("/home/maxloo/pyrest/temp/output.txt", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line

  os.system("cd /home/maxloo/pyrest/temp/")
  createFiles = "natural4-exe --workdir=/home/maxloo/pyrest/temp/workdir --uuiddir=" + uuid + " --topetri=petri --tojson=json --toaasvg=aasvg --tonative=native --tocorel4=corel4 --tocheckl=checklist  --tots=typescript " + targetPath
  os.system(createFiles)
  return textStr

@app.route("/you/<name>")
def user(name):
  return "Hello, {}!".format(name)

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


