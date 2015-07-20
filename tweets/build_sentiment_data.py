# author: Hayden Fuss

import csv
import numpy as np

ll = (-71.5457, 42.2084)
ur = (-70.8975, 42.4014)

yMax = 0.0

outsideTweets = []

# if ll[0] <= x and ur[0] >= x and ll[1] <= y and ur[1] >= y:

with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
  tweets = csv.DictReader(csvfile)
  for t in tweets:
    if t['time'] != '' and t['lat'] != '':
      x = float(t['lon'])
      y = float(t['lat'])
      check = ll[0] <= x and ur[0] >= x and ll[1] <= y and ur[1] >= y
      if not check:
        outsideTweets.append(t)
        if y > yMax:
          yMax = y

print len(outsideTweets)
print yMax

