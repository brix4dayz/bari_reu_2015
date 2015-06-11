#!/usr/bin/python2.7

keywords = ["#bostonstrong", "#prayforboston", "police", "cops", "shooting", "bombing", "marathon"]

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

# source: https://docs.python.org/2/library/csv.html
# uses the csv.DictReader class to parse the data
# because the first line of the file explains each field in a csv
# format, DictReader immediately knows how to parse each line into
# a hash/dictionary with the keys matching the fields specified in 
# the first line of the file

numTweetsWithKeywords = 0

import csv
with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
  tweets = csv.DictReader(csvfile)
  ttlNumTweets = 0
  # for all the tweets the reader finds
  for tweetData in tweets:
    ttlNumTweets = ttlNumTweets + 1
    tweetData['tweet_text'] = tweetData['tweet_text'].lower()
    if tweetContainsKeyWords(tweetData['tweet_text']):
      numTweetsWithKeywords = numTweetsWithKeywords + 1

print numTweetsWithKeywords
print float(numTweetsWithKeywords)/ttlNumTweets