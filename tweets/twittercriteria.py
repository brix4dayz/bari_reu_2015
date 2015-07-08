import yaml
import os
import inspect
import re

# author: Hayden Fuss

# uses os and inspect to determine path to module
myDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
filepath = myDir + '/twitter_criteria.yml'

# open criteria .yml file and load it into dictionary using yaml
criteria_yml = open(filepath, 'r')
criteria = yaml.load(criteria_yml)
criteria_yml.close()

kw_regex = re.compile('|'.join(criteria['keywords']))

handle_regex = re.compile(r'@[^ :\xe2\"\)\./\\\?\'!@]+')

markup_regex = re.compile('|'.join(criteria['twitterMarkup']))

def getTwitterTimeFmt():
  global criteria
  return criteria['time_fmt']

def getKeywords():
  global criteria
  return criteria['keywords']

def getKeywordRegex():
  global kw_regex
  return kw_regex

def getHandleRegex():
  global handle_regex
  return handle_regex

def tweetContainsKeyword(tweet):
  global kw_regex
  return kw_regex.search(tweet) is not None

# Function to clean up tweet strings 
# by manually removing irrelevant data (not words)
def cleanUpTweet(tweet_text):
  global markup_regex
  # Irrelevant characters
  temp = tweet_text.lower()
  # Use regex to create a regular expression 
  # for removing undesired characters
  temp = markup_regex.sub(r"", temp)
  return temp