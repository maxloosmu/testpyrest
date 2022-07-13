import os, subprocess, datetime
from pathlib import Path

temp_dir = "/home/maxloo/pyrest/temp/"
uuid = "uuid"
spreadsheetId = "ssid"
sheetId = "sid"

targetFolder = "/home/maxloo/pyrest/temp/workdir/"+uuid+"/"+spreadsheetId+"/"+sheetId+"/"
Path(targetFolder).mkdir(parents=True, exist_ok=True)

uuidssfolder = temp_dir + "workdir/" + uuid + "/" + spreadsheetId + "/" + sheetId
# createFiles = "natural4-exe --workdir=/home/maxloo/pyrest/temp/workdir --uuiddir=" + uuid + "/" + spreadsheetId + "/" + sheetId + " " + "/home/maxloo/pyrest/test.csv"
# nl4exe = os.system(createFiles)
createFiles2 = ["natural4-exe", 
                  "--workdir=/home/maxloo/pyrest/temp/workdir", 
                  "--uuiddir=" + uuid + "/" + spreadsheetId + "/" + sheetId, 
                  "/home/maxloo/pyrest/test.csv"]
nl4exe2 = subprocess.run(createFiles2, check=True, timeout=5, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

v8kargs = ["python", "/home/maxloo/vue-pure-pdpa/bin/v8k", "up",
               "--uuid=" + uuid,
               "--ssid=" + spreadsheetId,
               "--sheetid=" + sheetId,
               uuidssfolder + "/purs/LATEST.purs"]
os.system(" ".join(v8kargs) + " > " + "/home/maxloo/pyrest/v8k.out");

