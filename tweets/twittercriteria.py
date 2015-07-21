import yaml
import os
import inspect
import re
import time
import string

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

def getHandlesFromTweet(tweet):
  global handle_regex
  return handle_regex.findall(tweet)

def getTweetDate(tweet_time):
  global criteria
  return time.strptime(tweet_time, criteria['time_fmt'])

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

def has_punc(s):
  for i in range(0, len(s)):
    if s[i] in '!,.;#':
      return True
  return

def not_part_of_handle(s):
  return s != 'HANDLE' and s != ' <' and s != '> '

def cleanForSentiment(tweet_text):
  global markup_regex, handle_regex
  temp = markup_regex.sub(r"", tweet_text)
  temp = re.sub(r"\r|\r\n|\n", r" ", temp)
  temp = handle_regex.sub(r"<HANDLE>", temp)
  res = re.split('(\W+)', temp)
  print res
  flag = False
  for i in range(0, len(res)):
    if has_punc(res[i]) or res[i] == 'RT':
      flag = False
    if flag and res[i] != ' ' and not_part_of_handle(res[i]):
      res[i] = 'NOT_' + res[i]
    if res[i] == 'not' or res[i] == 't' or res[i][-2:] == 'nt':
      flag = True
  return ''.join(res)
