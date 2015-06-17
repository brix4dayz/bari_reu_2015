#!/usr/bin/python2.7

import time
import csv

#################### CRITERIA ########################################################################

keywords = ["#bostonmarathon", 
    "#marathonmonday",
    "#patriotsday"
    "marathon",
    "boylston",
    "finish line",
    "#bostonstrong",
    "#bostonpride",
    "#prayforboston",
    "#pray4bos",
    "bomb"
    "explosion",
    "explode",
    "wounded",
    "hostage",
    "watertown",
    "lockdown"]

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

def main():
  dates = {}
  date = []

  with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
    tweets = csv.DictReader(csvfile)
    # for all the tweets the reader finds
    for tweetData in tweets:
      if tweetData['time'] != "":
        date = time.strptime(tweetData['time'], tweet_time_fmt)
        if not date.tm_mday in dates.keys():
          dates[date.tm_mday] = {'AM':0, 'PM':0}
        tweetData['tweet_text'] = tweetData['tweet_text'].lower()
        if tweetContainsKeyWords(tweetData['tweet_text']):
          if date.tm_hour < 12:
            dates[date.tm_mday]['AM'] += 1
          else:
            dates[date.tm_mday]['PM'] += 1

  print "date_hour,number_tweets"
  for d in sorted(dates):
    for h in sorted(dates[d]):
      print str(date.tm_mon) + "/" + str(d) + " - " + h + "," + str(dates[d][h])

if __name__ == "__main__":
  main()

