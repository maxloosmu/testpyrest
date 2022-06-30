import glob
import os

list_of_files = glob.glob('/Users/maxloo/testpyrest/pyrest/more/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
latest_file = latest_file[-10:]
print(latest_file)

path = '/Users/maxloo/testpyrest/pyrest/'
newest = max([f for f in os.listdir(path)], key=lambda x: os.stat(os.path.join(path,x)).st_birthtime)
print(newest)