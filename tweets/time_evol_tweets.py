
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


def getTimeString(currentHour):
    timeStr = ""
    if currentHour != 12 or currentHour != 24:
        timeStr += str(currentHour%12)
    else:
        timeStr += str(12)
    if currentHour < 12:
        timeStr += ' AM'
    else:
        timeStr += ' PM'
    return timeStr

# ## Retrieving useful data with our `twitter_criteria` module
# retrieve the time format string from the criteria dictionary in twc
tweet_time_fmt = twc.getTwitterTimeFmt()

### get data

kwTweets = []
currentHour = 0

with open('recleaned_geo_tweets_12-22.csv') as csvfile:
    # reads first line of csv to determine keys for the tweet hash, tweets 
    # is an iterator through the list of tweet hashes the DictReader makes
    tweets = csv.DictReader(csvfile)
    # for all the tweets the reader finds
    for tweetData in tweets:
        # make sure its not a 'false tweet' from people using newlines in their tweet_text's
        if tweetData['time'] != "":
            # parse date/time into object
            date = time.strptime(tweetData['time'], tweet_time_fmt)
            if date.tm_mday == 19 and twc.tweetContainsKeyword(tweetData['tweet_text']):
                if date.tm_hour == currentHour:
                    kwTweets.append(tweetData)
                elif date.tm_hour == currentHour + 1:
                    currentHour += 1
                    timeStr = getTimeString(currentHour)
                    boston = bm.GreaterBostonDensity(kwTweets)
                    boston.plotMap(outname='manhuntDay_density_'+str(currentHour), 
                        title='Density of Keyword Tweets At ' + timeStr)
                    boston = bm.GreaterBostonScatter(kwTweets)
                    boston.plotMap(outname='manhuntDay_scatter_'+str(currentHour),
                        title='Locations of Keyword Tweets At ' + timeStr)
                    kwTweets.append(tweetData)
                    plt.close('all')


currentHour += 1
timeStr = getTimeString(currentHour)
boston = bm.GreaterBostonScatter(kwTweets)
boston.plotMap(outname='manhuntDay_scatter_'+str(currentHour),
    title='Locations of Keyword Tweets At ' + str(currentHour-12) + ' PM')

boston = bm.GreaterBostonDensity(kwTweets)
del(kwTweets)
boston.plotMap(outname='manhuntDay_density_'+str(currentHour), 
    title='Density of Keyword Tweets At ' + str(currentHour-12) + ' PM')
plt.close('all')

