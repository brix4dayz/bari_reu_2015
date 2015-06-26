import yaml
import os
import inspect
import re

# author: Hayden Fuss

# uses os and inspect to determine path to module
myDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
filepath = myDir + '/twitter_criteria.yml'

criteria = None

def loadCriteria():
  global criteria
  # open criteria .yml file and load it into dictionary using yaml
  criteria_yml = open(filepath, 'r')
  criteria = yaml.load(criteria_yml)
  criteria_yml.close()
  return

def getTwitterTimeFmt():
  global criteria
  return criteria['time_fmt']

def getKeywords():
  global criteria
  return criteria['keywords']

def getKeywordRegex():
  global criteria
  return re.compile('|'.join(criteria['keywords']))

def getHandleRegex():
  return re.compile(r'@[^ :\xe2\"\)\./\\\?\'!@]+')

def clearCriteria():
  global criteria
  del(criteria)
  return