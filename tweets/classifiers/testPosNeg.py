# Author: Hayden Fuss
# File: testposneg.py
# Date Modified: 07/31/2015
# Edited: Elizabeth Brooks

import posnegclassifier as tc
import os
import numpy as np

currentDir = os.getcwd()

def cleanNothing(tweet):
  return tweet

trainingPaths = {'positive':'/sentimentData/positive.txt', 'neutral':'/sentimentData/neutral.txt', 'negative':'/sentimentData/negative.txt',}

categories = trainingPaths.keys()

testPaths = {'positive':'/sentimentData/positiveTest.txt', 'neutral':'/sentimentData/neutralTest.txt', 'negative':'/sentimentData/negativeTest.txt',}

actual = np.array([])

testTweets = []

for p in testPaths.keys():
  temp = []
  with open(currentDir + testPaths[p], 'r') as f:
    for line in f:
      temp.append(line.rstrip('\n'))
  testTweets.extend(temp)
  temp = np.empty(len(temp))
  temp.fill(categories.index(p))
  actual = np.append(actual, temp)

def testClassifier(clssfr):
  print "Testing " + type(clssfr).__name__ + "..."
  predicted = clssfr.classify(testTweets)
  mat = clssfr.getConfusionMatrix(actual, predicted)
  num = len(mat)
  correct = 0
  total = 0
  for i in range(0, num):
    for j in range(0, num):
      total += mat[i][j]
      if i == j:
        correct += mat[i][j]
  #print correct
  #print total
  print "Accuracy: " + str(float(correct)/total) 
  print mat
  print "...done.\n"

relClssr = tc.PosNegClassifier(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierLinearSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierModifiedSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierQuadraticSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierLogSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierPerceptronSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierLossSquared(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierMaxEnt(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierBNB(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.PosNegClassifierRegression(trainingPaths, cleanNothing)

testClassifier(relClssr)
