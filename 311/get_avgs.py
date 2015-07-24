import time                      # time/date parsing
import csv                       # data parsing
import numpy as np               # arrays for plotting
import matplotlib.pyplot as plt  # Plotting
import math                      # ceiling for y-max in plots
import sys
import cPickle as cp
import pandas as pd
from shapely.geometry import Point
from shapely.prepared import prep

import os
sys.path.append(os.path.realpath('../census'))
import bostonmap2 as bm

# time_fmt declares the format for the time data

time_fmt = "%m/%d/%Y"

latents = ['pubd', 'public', 'private', 'other']

for l in latents:
  data = {}
  with open('311_' + l + '_2012_2013.csv') as csvfile:
    reports = csv.DictReader(csvfile)
    for r in reports:
        date = time.strptime(r['OPEN_DT'], time_fmt) # converts string version of date into a date object
        if date.tm_year == 2013:
            dateStr = str(date.tm_mon) + "/" + str(date.tm_mday)
            if not dateStr in data.keys():
                data[dateStr] = []
            r['lon'] = r['X']
            r['lat'] = r['Y']
            if r['lat'] != 'NA':
              data[dateStr].append(r)

  boston = bm.BostonDensity(None)
  boston.loadBasemap()
  boston.mapDF()

  boston.df_map['avg'] = 0
  ttlDays = len(data)
  for d in sorted(data):
    boston.dataPoints = data[d]
    output = {'lon':[], 'lat':[]}
    for p in boston.dataPoints:
      for each in ('lon', 'lat'):
        output[each].append(p[each])
    df = pd.DataFrame(output)
    df[['lon', 'lat']] = df[['lon', 'lat']].astype(float)
    boston.dataPoints = pd.Series(
      [Point(boston.map(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(df['lon'], df['lat'])])
    
    boston.df_map['count'] = boston.df_map['poly'].map(lambda x: int(len(filter(prep(x).contains, boston.dataPoints))))
    boston.df_map['avg'] += boston.df_map['count']

  boston.df_map['avg'] /= ttlDays

  # avgs = {}
  # for i, row in boston.df_map.iterrows():
  #   avgs[row['CT_ID_10']] = row['avg']

  avgs = pd.Series(boston.df_map.avg.values, index=boston.df_map.CT_ID_10).to_dict()

  with open(l + '_avgs.pkl', 'wb') as f:
    cp.dump(avgs, f)

  print "Done with " + l