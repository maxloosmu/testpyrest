from flask import Flask, request, send_from_directory, render_template
import sys, string, os, datetime, glob, shutil
from pathlib import Path

template_dir = "/home/maxloo/pyrest/template/"
temp_dir = "/home/maxloo/pyrest/temp/"
static_dir = "/home/maxloo/pyrest/static/"
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route("/get")
def getCommandList():
  textStr = ""
  with open("/home/maxloo/pyrest/commands.txt", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  return textStr

@app.route("/corel4/<uuid>/<ssid>/<sid>")
def getCorel4File(uuid, ssid, sid):
  textStr = ""
  corel4Folder = temp_dir + "workdir/" + uuid + "/" + ssid + "/" + sid + "/corel4/"
  with open(corel4Folder + "LATEST.l4", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  return render_template("corel4.html", data=textStr)

@app.route("/json/<uuid>/<ssid>/<sid>")
def getJsonFile(uuid, ssid, sid):
  textStr = ""
  jsonFolder = temp_dir + "workdir/" + uuid + "/" + ssid + "/" + sid + "/json/"
  with open(jsonFolder + "LATEST.json", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  return render_template("json.html", data=textStr)

@app.route("/petri/<uuid>/<ssid>/<sid>")
def getPetriFile(uuid, ssid, sid):
  petriFolder = temp_dir + "workdir/" + uuid + "/" + ssid + "/" + sid + "/petri/"
  dotPath = petriFolder + "LATEST.dot"
  if not os.path.exists(petriFolder):
    Path(petriFolder).mkdir(parents=True, exist_ok=True)
  petriPath = petriFolder + "LATEST.png"
  os.system("dot -Tpng " + dotPath + " -o " + petriPath)
  staticPetri = static_dir + 'petri.png'
  shutil.copy(petriPath, staticPetri)
  return render_template("petri.html")

@app.route("/aasvg/<uuid>/<ssid>/<sid>/<image>")
def showAasvgImage(uuid, ssid, sid, image):
  aasvgFolder = temp_dir + "workdir/" + uuid + "/" + ssid + "/" + sid + "/aasvg/LATEST/"
  imagePath = aasvgFolder + image
  cutPathToStaticImage = "workdir/" + uuid + "/" + ssid + "/" + sid + "/" + image
  newImagePath = static_dir + cutPathToStaticImage
  newImageFolderPath = static_dir + "workdir/" + uuid + "/" + ssid + "/" + sid + "/"
  Path(newImageFolderPath).mkdir(parents=True, exist_ok=True)
  shutil.copy(imagePath, newImagePath)
  return render_template("aasvg.html", image = cutPathToStaticImage, image_title = image[:-4])

@app.route("/aasvg/<uuid>/<ssid>/<sid>")
def getAasvgHtml(uuid, ssid, sid):
  aasvgFolder = temp_dir + "workdir/" + uuid + "/" + ssid + "/" + sid + "/aasvg/LATEST/"
  aasvgHtml = aasvgFolder + "index.html"
  f = []
  textStr = ""
  for (dirpath, dirnames, filenames) in os.walk(aasvgFolder):
    f.extend(filenames)
    break
  print(f)
  cutPathToIndexDir = "aasvgindexdir/" + uuid + "/" + ssid + "/" + sid + "/"
  Path(template_dir + cutPathToIndexDir).mkdir(parents=True, exist_ok=True)
  cutPathToIndex = cutPathToIndexDir + "aasvg_index.html"
  for fileName in f:
    if (fileName != "index.html") and (fileName[-3:] == 'svg'):
      textStr = textStr + '<li> <a href="/aasvg/' + uuid + '/' + ssid + '/' + sid + '/' + fileName + '">' + fileName[:-4] + '</a></li>\n'
  with open(aasvgHtml, "w") as fout:
    fout.write(textStr)
  shutil.copy(aasvgHtml, template_dir + cutPathToIndex)
  # return render_template(cutPathToIndex)
  return textStr

@app.route("/post", methods=['GET', 'POST'])
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
  targetFolder = "/home/maxloo/pyrest/temp/workdir/"+uuid+"/"+spreadsheetId+"/"+sheetId+"/"+target
  print(targetFolder)
  targetFile = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ") + ".csv"
  targetPath = targetFolder + targetFile
  # if not os.path.exists(targetFolder):
  Path(targetFolder).mkdir(parents=True, exist_ok=True)

  command = data['command']+" "+targetPath+" > /home/maxloo/pyrest/temp/output.txt"
  textStr = ""
  with open(targetPath, "w") as fout:
    fout.write(data['csvString'])
  os.system(command)
  with open("/home/maxloo/pyrest/temp/output.txt", "r") as fin:
    for line in fin.readlines():
      textStr = textStr + line
  # targetPath is for CSV data
  createFiles = "natural4-exe --workdir=/home/maxloo/pyrest/temp/workdir --uuiddir=" + uuid + "/" + spreadsheetId + "/" + sheetId + " " + targetPath
  # createFiles = "natural4-exe --workdir=/home/maxloo/pyrest/temp/workdir --uuiddir=" + uuid + " --topetri=petri --tojson=json --toaasvg=aasvg --tonative=native --tocorel4=corel4 --tocheckl=checklist  --tots=typescript " + targetPath
  os.system(createFiles)
  return textStr

@app.route("/you/<name>")
def user(name):
  return """
      <!DOCTYPE html>
      <html>
      <head><title>Hello</title></head>
      <body><h1>Hello, {name}</h1></body>
      </html>
      """.format(name=name), 200

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, threaded=True, processes=6)


