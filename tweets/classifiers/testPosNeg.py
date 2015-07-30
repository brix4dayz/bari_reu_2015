import tweetclassifier2 as tc
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

relClssr = tc.TweetClassifier(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierLinearSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierModifiedSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierQuadraticSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierLogSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierPerceptronSVM(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierLossSquared(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierMaxEnt(trainingPaths, cleanNothing)

testClassifier(relClssr)

relClssr = tc.TweetClassifierBNB(trainingPaths, cleanNothing)

testClassifier(relClssr)