
# ## Useful libraries

import time                         # time/date parser
import csv                          # data parser
import numpy as np                  # arrays for plotting
import matplotlib.pyplot as plt     # plotting
import math                         # ceiling for y-max in plots
import twittercriteria as twc       # yaml, re, os

import os
import sys
sys.path.append(os.path.realpath('../census/'))
import bostonmap as bm


# ## Retrieving useful data with our `twitter_criteria` module
# retrieve the time format string from the criteria dictionary in twc
tweet_time_fmt = twc.getTwitterTimeFmt()

### get data

kwTweets = []
currentHour = 14

with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
    # reads first line of csv to determine keys for the tweet hash, tweets 
    # is an iterator through the list of tweet hashes the DictReader makes
    tweets = csv.DictReader(csvfile)
    # for all the tweets the reader finds
    for tweetData in tweets:
        # make sure its not a 'false tweet' from people using newlines in their tweet_text's
        if tweetData['time'] != "":
            # parse date/time into object
            date = time.strptime(tweetData['time'], tweet_time_fmt)
            if date.tm_mday == 15 and twc.tweetContainsKeyword(tweetData['tweet_text']):
                if date.tm_hour == currentHour:
                    kwTweets.append(tweetData)
                elif date.tm_hour == currentHour + 1:
                    currentHour += 1
                    boston = bm.BostonDensity(kwTweets)
                    boston.plotMap(outname='bombingDay_density_'+str(currentHour), 
                        title='Density of Keyword Tweets At ' + str(currentHour-12) + ' PM')
                    boston = bm.BostonScatter(kwTweets)
                    boston.plotMap(outname='bombingDay_scatter_'+str(currentHour),
                        title='Locations of Keyword Tweets At ' + str(currentHour-12) + ' PM')
                    kwTweets.append(tweetData)


currentHour += 1
boston = bm.BostonScatter(kwTweets)
boston.plotMap(outname='bombingDay_scatter_'+str(currentHour),
    title='Locations of Keyword Tweets At ' + str(currentHour-12) + ' PM')

boston = bm.BostonDensity(kwTweets)
del(kwTweets)
boston.plotMap(outname='bombingDay_density_'+str(currentHour), 
    title='Density of Keyword Tweets At ' + str(currentHour-12) + ' PM')

