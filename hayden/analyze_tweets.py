#!/usr/bin/python2.7

import time
import csv

#################### CRITERIA ########################################################################

keywords = ["#bostonstrong", "#prayforboston", "police", "cops", "shooting", "bombing", "marathon"]

"""angrySentiments = {}

peacefulSentiments = {}

scaredSentiments = {}

excitedSentiments = {}

angryMin = 0

peacefulMin = 0

scaredMin = 0

excitedMin = 0"""

tweet_time_fmt = "%Y-%m-%d %H:%M:%S"

####################### CLASSES/FUNCTIONS ############################################################

def tweetContainsKeyWords(tweet):
  for kw in keywords:
    if kw in tweet: return True

def angryTweet(tweet):
  return

def peacefulTweet(tweet):
  return

def scaredTweet(tweet):
  return

def excitedTweet(tweet):
  return


####################### MAIN #########################################################################
# source: https://docs.python.org/2/library/csv.html
# uses the csv.DictReader class to parse the data
# because the first line of the file explains each field in a csv
# format, DictReader immediately knows how to parse each line into
# a hash/dictionary with the keys matching the fields specified in 
# the first line of the file

if __name__ == "__main__":
  dates = {}

  with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
    tweets = csv.DictReader(csvfile)
    # for all the tweets the reader finds
    for tweetData in tweets:
      if tweetData['time'] != "":
        date = time.strptime(tweetData['time'], tweet_time_fmt)
        if not date.tm_mday in dates.keys():
          dates[date.tm_mday] = 0
        tweetData['tweet_text'] = tweetData['tweet_text'].lower()
        if tweetContainsKeyWords(tweetData['tweet_text']):
          dates[date.tm_mday] = dates[date.tm_mday] + 1

  print "day,number_tweets"
  for d in sorted(dates):
    print str(d) + "," + str(dates[d])

