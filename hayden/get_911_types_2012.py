#!/usr/bin/python2.7

import csv

# source: https://docs.python.org/2/library/csv.html
# uses the csv.DictReader class to parse the data
# because the first line of the file explains each field in a csv
# format, DictReader immediately knows how to parse each line into
# a hash/dictionary with the keys matching the fields specified in 
# the first line of the file

types = {}

with open('2010-14 Full CAD, Jan-Jun 2012.csv') as csvfile:
  reports = csv.DictReader(csvfile)
  for r in reports:
    if not r['TYPE'] in types.keys():
      types[r['TYPE']] = r['TYPE_DESC']

print "type,description"
for t in sorted(types):
  print t + "," + types[t] 
print "\n"
