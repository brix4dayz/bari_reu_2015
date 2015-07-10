# Author: Elizabeth Brooks
# Date Modified: 07/09/2015

# PreProcessor Directives
import os
import inspect
import sys
sys.path.append(os.path.realpath('../'))
import csv
import yaml
import re
import random
import twittercriteria as twc
# Classification function imports
import nltk
from nltk.classify import apply_features
from nltk.classify import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Global field declarations
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Define wrapper class
class RelevanceClassifier(object):

    def __init__(self, class1_path='/relevantTraining.txt', class2_path='/irrelevantTraining.txt'):
        # Initialize data sets
        self.trainingSet = [] # Labeled tweet training data set 
        self.labeledTweets = [] # Feature set of labeled tweet terms
        self.allTerms = []
		
		# Begin functions for classification
        self.initLabeledSet(class1_path, class2_path)
		self.initTrainingSet()
        self.trainClassifier()
        return
    
    # Function to initialize the feature sets
    def initLabeledSet(self, class1_path, class2_path):
        # Loop through the txt files line by line
        # Assign labels to tweets
        # Two classes, relevant and irrelevant to the marathon
        with open(current_dir + class1_path, "r") as relevantFile:
            for line in relevantFile:
                self.labeledTweets.append((line.split(), 'relevant'))
        with open(current_dir + class2_path, "r") as irrelevantFile:
            for line in irrelevantFile:
                self.labeledTweets.append((line.split(), 'irrelevant'))
        # Randomize the data
        random.shuffle(self.labeledTweets)
    # End initDictSet
	
	# Function for initializing the labeled training data set
    def initTrainingSet(self):
        self.getTweetText()
        self.getTerms()
        # The apply_features func processes a set of labeled tweet strings using the passed extractFeatures func
        self.trainingSet = apply_features(self.extractFeatures, self.labeledTweets)
        return
	# End initTrainingSet
		
	# Function to train the input NB classifier using it's apply_features func
	# this function can be overridden for scikit learn wrapper for multinomialNB
    def trainClassifier(self):
		self.classifierNB = nltk.NaiveBayesClassifier.train(self.trainingSet)
        self.buildClassifier()
        return
    # End trainClassifier
	
    # Function to get relevant tweet terms
    def getTweetText(self):
        for (terms, relevance) in self.labeledTweets:
            self.allTerms.extend(terms)
        # End for
        # Return statement
        return
    # End getTweetText

    # Function to get term features
    def getTerms(self):
        self.allTerms = nltk.FreqDist(self.allTerms)
        self.wordFeatures = self.allTerms.keys()
        # Return statement
        return
    # End getTerms

    # Function to extract features from tweets
    def extractFeatures(self, tweet_terms):
        features = {}
        for word in self.wordFeatures:
            features['contains(%s)' % word] = (word in tweet_terms)
        # End for
        # Return feature set
        return features
    # End extractFeatures
    
    # Function to classify input cleaned tweet txt
    def isRelevant(self, tweet_text):
        # Return the use of the classifier
        return self.classifierNB.classify(self.extractFeatures(twc.cleanUpTweet(tweet_text).split())) == "relevant"
    # End isRelevant
# End Wrapper    

class WeightedRelevanceClassifier(RelevanceClassifier):
    def __init__(self):
        super(WeightedRelevanceClassifier, self).__init__()
        return

    def buildClassifier(self):
        #insert scikit learn
        pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=1000)),
                     ('nb', MultinomialNB())])
        self.classifierNB = SklearnClassifier(pipeline)
        self.classifierNB.train(self.trainingSet)
        return

# End script
