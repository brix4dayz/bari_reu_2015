import tweetclassifier as tc
import os
import numpy as np

currentDir = os.getcwd()

def cleanNothing(tweet):
  return tweet

trainingPaths = {'angry':'/sentimentData/angryTraining_1.txt', 'sad':'/sentimentData/sadTraining_1.txt',
 'calm':'/sentimentData/calmTraining_1.txt', 'fearful':'/sentimentData/fearfulTraining_1.txt', 'positive':'/sentimentData/positiveTraining_1.txt',
 'excited':'/sentimentData/excitedTraining_1.txt', 'negative':'/sentimentData/negativeTraining_1.txt', 'neutral':'/sentimentData/neutralTraining_1.txt'}

categories = trainingPaths.keys()

testPaths = {'angry':'/sentimentData/jeremy_2_angry.txt', 'sad':'/sentimentData/jeremy_2_sad.txt',
 'calm':'/sentimentData/jeremy_2_calm.txt', 'fearful':'/sentimentData/jeremy_2_fearful.txt', 'positive':'/sentimentData/jeremy_2_positive.txt',
 'excited':'/sentimentData/jeremy_2_excited.txt', 'negative':'/sentimentData/jeremy_2_negative.txt', 'neutral':'/sentimentData/jeremy_2_neutral.txt'}

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
  print clssfr.getConfusionMatrix(actual, predicted)
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