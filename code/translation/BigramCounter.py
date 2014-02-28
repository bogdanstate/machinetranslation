import sys

old = ""
count = 0
for line in sys.stdin:
  new = line.strip()
  if old!=new: 
    if old != "":
      print "%s\t%d" % (old, count)
      count = 0
    old = new
  count += 1
