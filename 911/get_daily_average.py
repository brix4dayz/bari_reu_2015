import time                      # time/date parsing
import csv                       # data parsing
import numpy as np               # arrays for plotting
import matplotlib.pyplot as plt  # Plotting
import math                      # ceiling for y-max in plots
import sys
import cPickle as cp

import os
sys.path.append(os.path.realpath('../census'))
import bostonmap2 as bm
import pandas as pd

# time_fmt declares the format for the time data

time_fmt = "%m/%d/%Y %H:%M"

latents = ['medical', 'violent', 'petty', 'unsorted']

for l in latents:
  data = {}
  with open('911_' + l + '_2012_2013.csv') as csvfile:
    reports = csv.DictReader(csvfile)
    for r in reports:
        date = time.strptime(r['ENTRY_DT'], time_fmt) # converts string version of date into a date object
        if date.tm_year == 2013:
            dateStr = str(date.tm_mon) + "/" + str(date.tm_mday)
            if not dateStr in data.keys():
                data[dateStr] = []
            if r['CT_ID'] != 'NA':
              data[dateStr].append(r)

  boston = bm.BostonDensityCT(None)
  boston.loadBasemap()
  boston.mapDF()

  boston.df_map['avg'] = 0
  ttlDays = len(data)
  for d in sorted(data):
    boston.dataPoints = data[d]
    temp = []
    for d in boston.dataPoints:
      temp.append(int(d['CT_ID']))

    boston.dataPoints = np.array(temp)

    boston.df_map['count'] = boston.df_map['CT_ID_10'].map(lambda x: int((boston.dataPoints == int(x)).sum()))
    boston.df_map['avg'] += boston.df_map['count']

  boston.df_map['avg'] /= ttlDays

  # avgs = {}
  # for i, row in boston.df_map.iterrows():
  #   avgs[row['CT_ID_10']] = row['avg']

  avgs = pd.Series(boston.df_map.avg.values, index=boston.df_map.CT_ID_10).to_dict()

  with open(l + '_avgs.pkl', 'wb') as f:
    cp.dump(avgs, f)

  print "Done with " + l


