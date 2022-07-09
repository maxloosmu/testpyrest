import argparse

def aaa():
  print("aaa")
  return
def bbb():
  print("bbb")
  return

ap = argparse.ArgumentParser(description='Print functions')
subparsers = ap.add_subparsers(help='Type a or b')
parsea = subparsers.add_parser('a', help='print a')
parseb = subparsers.add_parser('b', help='print b')
parsea.set_defaults(func=aaa)
parseb.set_defaults(func=bbb)

args = ap.parse_args()
if not hasattr(args, 'func'):
  print("python3 aptest.py -h")
else:
  args.func()

