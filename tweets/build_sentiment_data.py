# author: Hayden Fuss

import csv
import random
import twittercriteria as twc

ll = (-71.5457, 42.2084)
ur = (-70.8975, 42.4014)

def randomIndices(high, size=1500):
  indx = []
  deck = list(range(0, high))
  random.shuffle(deck)
  for i in range(0, size):
    indx.append(deck.pop())
  return indx

yMax = 0.0

outsideTweets = []

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

indices = randomIndices(len(outsideTweets), 2100)

data = {'indices':{}, 'tweets':{}}

data['indices']['hayden'] = indices[:700]

data['indices']['jeremy'] = indices[700:1400]

data['indices']['liz'] = indices[1400:]

for person in data['indices'].keys():
  data['tweets'][person] = []
  for i in data['indices'][person]:
    data['tweets'][person].append(twc.cleanForSentiment(outsideTweets[i]['tweet_text']))
  with open(person + '_training.txt', 'w') as f:
    f.write('\n'.join(data['tweets'][person]))
