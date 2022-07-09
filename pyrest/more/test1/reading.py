#!/usr/bin/env python3

import os, json
from os.path import isfile, join, getmtime
workdir = os.getcwd()

def getjson(pathin):
  with open(pathin, "r") as read_file:
    data = json.load(read_file)
    data['jsonfile'] = pathin
    data['modtime'] = getmtime(pathin)
  return data

def read_all():
  vuedirs = [ getjson(join(workdir,f,"001.json"))
              for f in os.listdir(workdir)
              if not isfile("/".join([workdir,f]))
                 and isfile("/".join([workdir,f,"001.json"]))
             ]
  print ("found vuedirs:"); print (vuedirs)
  vuedict = { js['name']: js for js in vuedirs }
  print ("returning vuedict:"); print (vuedict)
  return vuedict

read_all()
