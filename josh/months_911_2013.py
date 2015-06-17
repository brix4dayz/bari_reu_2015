#!/usr/bin/python2.7

import time
import csv


emer_time_fmt = "%m/%d/%Y %H:%M"


# source: https://docs.python.org/2/library/csv.html
# uses the csv.DictReader class to parse the data
# because the first line of the file explains each field in a csv
# format, DictReader immediately knows how to parse each line into
# a hash/dictionary with the keys matching the fields specified in 
# the first line of the file

if __name__ == "__main__":
  dates = {}

  with open('2010-14 Full CAD, Jan-Jun 2013.csv') as csvfile:
    emergency = csv.DictReader(csvfile)
    # for all the 911 calls the reader finds
    for e in emergency:
      if e['ENTRY_DT'] != "":
        date = time.strptime(e['ENTRY_DT'], emer_time_fmt)
        if not date.tm_mon in dates.keys():
          dates[date.tm_mon] = {}
        
        if not date.tm_mday in dates[date.tm_mon].keys():
          dates[date.tm_mon][date.tm_mday] = 1
        else:
          dates[date.tm_mon][date.tm_mday] += 1
        

  print "month,day,count"
  for m in sorted(dates):
    for d in sorted(dates[m]):
      print str(m) + "," + str(d) + "," + str(dates[m][d])
