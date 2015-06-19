#!/usr/bin/python2.7

import time
import csv
import numpy as np
import matplotlib.pyplot as plt
import math

emer_time_fmt = "%m/%d/%Y %H:%M"

years = ('2012', '2013')

year_data = {}

def main():
  for y in years:
    year_data[y] = {}

    with open('2010-14 Full CAD, Jan-Jun ' + y + '.csv') as csvfile:
      emergency = csv.DictReader(csvfile)
      # for all the 911 calls the reader finds
      for e in emergency:
        date = time.strptime(e['ENTRY_DT'], emer_time_fmt)
        if not date.tm_mon in year_data[y].keys():
          year_data[y][date.tm_mon] = 1
        else:
          year_data[y][date.tm_mon] += 1

  ind=np.arange(len(year_data['2012']))
  width=.35

  counts_2012 = []

  for month in sorted(year_data['2012']):
    counts_2012.append(year_data['2012'][month])

  counts_2013 = []

  for month in sorted(year_data['2013']):
    counts_2013.append(year_data['2013'][month])

  maxCount = int(math.ceil(max(counts_2012 + counts_2013) / 1000.0)) * 1000

  fig = plt.figure()
  ax = fig.add_subplot(111)

  rects1 = ax.bar(ind, counts_2012, width, color='r')

  rects2 = ax.bar(width+ind, counts_2013, width, color='y')

  ax.set_xlim(-width, len(ind) + width)
  ax.set_ylim(0, maxCount)
  ax.set_ylabel('Number of 911 Reports')
  ax.set_title('911 Call Volume per Month')
  ax.set_xticks(ind+width)
  tickNames = ax.set_xticklabels(('Jan', 'Feb', 'March', 'April', 'May', 'June'))
  plt.setp(tickNames, rotation=45, fontsize=10)

  ax.legend((rects1[0], rects2[0]), years)

  def autolabel(rects):
    # attach some text labels
    for rect in rects:
      height = rect.get_height()
      ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
          ha='center', va='bottom')

  #autolabel(rects1)
  #autolabel(rects2)

  plt.savefig("911_per_month.png", dpi=96)



# source: https://docs.python.org/2/library/csv.html
# uses the csv.DictReader class to parse the data
# because the first line of the file explains each field in a csv
# format, DictReader immediately knows how to parse each line into
# a hash/dictionary with the keys matching the fields specified in 
# the first line of the file

if __name__ == "__main__":
  main()