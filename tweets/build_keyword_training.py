import csv
import twittercriteria as twc
import time
import numpy as np

twc.loadCriteria()

kw_pattern = twc.getKeywordRegex()
tweet_time_fmt = twc.getTwitterTimeFmt()

twc.clearCriteria()

def containsKeyword(tweet_text):
  return kw_pattern.search(tweet_text) is not None

trueIrrelevants = []

possibleRelevants = []


with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
  tweetData = csv.DictReader(csvfile)
  for tweet in tweetData:
