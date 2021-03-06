#!/usr/bin/python2.7

# author: Hayden Fuss

import csv

# source: https://docs.python.org/2/library/csv.html
# uses the csv.DictReader class to parse the data
# because the first line of the file explains each field in a csv
# format, DictReader immediately knows how to parse each line into
# a hash/dictionary with the keys matching the fields specified in 
# the first line of the file

types2012 = {}

with open('2010-14 Full CAD, Jan-Jun 2012.csv') as csvfile:
  reports = csv.DictReader(csvfile)
  for r in reports:
    if not r['TYPE'] in types2012.keys():
      types2012[r['TYPE']] = r['TYPE_DESC']

types2013 = {}

with open('2010-14 Full CAD, Jan-Jun 2013.csv') as csvfile:
  reports = csv.DictReader(csvfile)
  for r in reports:
    if not r['TYPE'] in types2013.keys():
      types2013[r['TYPE']] = r['TYPE_DESC']

sharedKeys = (set(types2012.keys()) & set(types2013.keys()))
sharedKeys = list(sharedKeys)

other = []

for k in types2012.keys():
  if k in types2013.keys():
    other.append(k)
    if types2012[k] != types2013[k]:
      print "oh no"

for k in sharedKeys:
  if not k in other:
    print "mhmmmmm"

