import time                      # time/date parsing
import csv                       # data parsing
import numpy as np               # arrays for plotting
import matplotlib.pyplot as plt  # Plotting
import math                      # ceiling for y-max in plots
import sys

import os
sys.path.append(os.path.realpath('../census'))
import bostonmap as bm

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
  densities = []
  for d in sorted(data):
    boston.dataPoints = data[d]
    temp = []
    for d in boston.dataPoints:
      temp.append(int(d['CT_ID']))

    boston.dataPoints = np.array(temp)

    boston.df_map['count'] = boston.df_map['land_info'].map(lambda x: (boston.dataPoints == int(x['CT_ID_10'])).sum())
    boston.df_map['density_km'] = boston.df_map['count'] / boston.df_map['area_km']
    boston.df_map.density_km.fillna(0, inplace=True)
    densities.append(list(boston.df_map['density_km']))
    boston.df_map['avg'] += boston.df_map['density_km']
    boston.df_map.drop(['count', 'density_km'], axis=1, inplace=True)

  boston.df_map['avg'] /= ttlDays

  boston.df_map['stdev'] = 0

  densities = np.array(densities)
  tracts = densities.T
  medians = []
  for t in tracts:
    t = np.sort(t)
    a = len(t)/2
    med = 0
    if len(t)%2 == 0:
      med = (t[a] + t[a-1])/2
    else:
      med = t[a]
    medians.append(med)

  boston.df_map['med'] = medians

  for d in densities:
    boston.df_map['density_km'] = d
    boston.df_map['stdev'] += (boston.df_map['avg'] - boston.df_map['density_km'])**2

  boston.df_map['stdev'] = (boston.df_map['stdev']/ttlDays)**0.5

  strings = []
  for i, row in boston.df_map.iterrows():
    temp = row['land_info']['CT_ID_10'] + "," + str(row['avg']) + "," + str(row['stdev']) + "," + str(row['med'])
    strings.append(temp)

  with open(l + '_2013_daily_avg.csv', 'w') as f:
    f.write('CT_ID,AVG,STDDEV,MEDIAN\n')
    f.write('\n'.join(strings))

  print "Done with " + l


