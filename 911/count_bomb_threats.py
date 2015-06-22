#!/usr/bin/python2.7

# author: Hayden Fuss

"""
  Counts number of bomb related 911 calls in 2012 and 2013 in Boston.
"""

import csv

numThreats2012 = 0

with open('2010-14 Full CAD, Jan-Jun 2012.csv') as csvfile:
  reports = csv.DictReader(csvfile)
  for r in reports:
    if "BOMB" in r['TYPE']:
      numThreats2012 = numThreats2012 + 1

numThreats2013 = 0

with open('2010-14 Full CAD, Jan-Jun 2013.csv') as csvfile:
  reports = csv.DictReader(csvfile)
  for r in reports:
    if "BOMB" in r['TYPE']:
      numThreats2013 = numThreats2013 + 1

print "Number of bomb calls in 2012: " + str(numThreats2012)

print "Number of bomb calls in 2013: " + str(numThreats2013)