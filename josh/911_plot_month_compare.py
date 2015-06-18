#!/usr/bin/python2.7

import time
import csv
import numpy as np
import matplotlib.pyplot as plt

emer_time_fmt = "%m/%d/%Y %H:%M"

years = ['2012', '2013']

year_data = {}

def main():
  for y in years:
    year_data[y] = {}

    with open('2010-14 Full CAD, Jan-Jun ' + y + '.csv') as csvfile:
      emergency = csv.DictReader(csvfile)
      # for all the 911 calls the reader finds
      for e in emergency:
        if e['ENTRY_DT'] != "":
          date = time.strptime(e['ENTRY_DT'], emer_time_fmt)
          if not date.tm_mon in year_data[y].keys():
            year_data[y][date.tm_mon] = 1
          else:
            year_data[y][date.tm_mon] += 1


          
          
    """print f
    print "month,count"
    for m in sorted(year_data[y]):
      print str(m) + "," + str(year_data[y][m])
    print """""

  N=6
  counts_2012=(49141, 46840, 52864, 52632, 55796, 55682)

  ind=np.arange(N)
  width=.25

  fig, ax=plt.subplots()
  rects1=ax.bar(ind, counts_2012, width, color='r')

  counts_2013=(58125, 53011, 59786, 61857, 68041, 69526)

  rects2=ax.bar(width+ind, counts_2013, width, color='y')

  ax.set_ylabel('Count')
  ax.set_title('911 Call Volume by Month and Year')
  ax.set_xticks(ind+width)
  ax.set_xticklabels(('Jan', 'Feb', 'March', 'April', 'May', 'June'))

  ax.legend((rects1[0], rects2[0]), ('2012', '2013'))

  def autolabel(rects):
    # attach some text labels
    for rect in rects:
      height = rect.get_height()
      ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
          ha='center', va='bottom')

  autolabel(rects1)
  autolabel(rects2)

  plt.show()



# source: https://docs.python.org/2/library/csv.html
# uses the csv.DictReader class to parse the data
# because the first line of the file explains each field in a csv
# format, DictReader immediately knows how to parse each line into
# a hash/dictionary with the keys matching the fields specified in 
# the first line of the file

if __name__ == "__main__":
  main()