import glob, os
from pathlib import Path

# list_of_files = glob.glob('/Users/maxloo/testpyrest/pyrest/more/*') # * means all if need specific format then *.csv
# latest_file = max(list_of_files, key=os.path.getctime)
# latest_file = latest_file[-10:]
# print(latest_file)

# path = '/Users/maxloo/testpyrest/pyrest/'
# newest = max([f for f in os.listdir(path)], key=lambda x: os.stat(os.path.join(path,x)).st_birthtime)
# print(newest)

testDir = '/mnt/c/Users/Max/src/testpyrest/pyrest/images/'
def createHtml(testDir):
  aasvgHtml = testDir + "index.html"
  f = []
  textStr = ""
  for (dirpath, dirnames, filenames) in os.walk(testDir):
    f.extend(filenames)
    break
  print(f)
  for filename in f:
    splitName = filename.split('/')
    if splitName[-1] != "index.html":
      textStr = textStr + '<li> <a href="' + splitName[-1] + '">' + splitName[-1][:-4] + '</a></li>\n'
  with open(aasvgHtml, "w") as fout:
    fout.write(textStr)
  return
# createHtml(testDir)
longPath = '/Users/maxloo/testpyrest/pyrest/more/test1/test2/test3/test4/'
Path(longPath).mkdir(parents=True, exist_ok=True)
os.system('touch ' + longPath + 'final.txt')