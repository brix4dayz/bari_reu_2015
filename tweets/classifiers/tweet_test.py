import tweetclassifier as tc
import os
import numpy as np

currentDir = os.getcwd()

def cleanNothing(tweet):
  return tweet

trainingPaths = {'angry':'/sentimentData/angryTraining_3.txt', 'sad':'/sentimentData/sadTraining_3.txt',
 'calm':'/sentimentData/calmTraining_3.txt', 'fearful':'/sentimentData/fearfulTraining_3.txt', 'positive':'/sentimentData/positiveTraining_3.txt',
 'excited':'/sentimentData/excitedTraining_3.txt', 'negative':'/sentimentData/negativeTraining_3.txt', 'neutral':'/sentimentData/neutralTraining_3.txt'}

categories = trainingPaths.keys()

testPaths = {'angry':'/sentimentData/hayden_2_angry.txt', 'sad':'/sentimentData/hayden_2_sad.txt',
 'calm':'/sentimentData/hayden_2_calm.txt', 'fearful':'/sentimentData/hayden_2_fearful.txt', 'positive':'/sentimentData/hayden_2_positive.txt',
 'excited':'/sentimentData/hayden_2_excited.txt', 'negative':'/sentimentData/hayden_2_negative.txt', 'neutral':'/sentimentData/hayden_2_neutral.txt'}

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