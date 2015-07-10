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

# Define class to classify tweet relevance
class RelevanceClassifier(object):

	# Class constructor to initialize classifier
    def __init__(self, class1_path='/relevantTraining.txt', class2_path='/irrelevantTraining.txt'):
        # Initialize data sets
        self.trainingSet = [] # Labeled tweet training data set 
        self.labeledTweets = [] # Feature set of labeled tweet terms
        self.allTerms = []		
		# Begin functions for classification
        self.initLabeledSet(class1_path, class2_path) # Initialize labeledTweets
		self.initTrainingSet() # Initialize trainingSet
        self.trainClassifier()
		# End func return
        return
	# End class constructor
    
    # Function to initialize the feature sets
    def initLabeledSet(self, class1_path, class2_path):
        # Loop through the txt files line by line
        # Assign labels to tweets
        # Two classes, relevant and irrelevant
        with open(current_dir + class1_path, "r") as relevantFile:
            for line in relevantFile:
                self.labeledTweets.append((line.split(), 'relevant'))
        with open(current_dir + class2_path, "r") as irrelevantFile:
            for line in irrelevantFile:
                self.labeledTweets.append((line.split(), 'irrelevant'))
        # Randomize the data
        random.shuffle(self.labeledTweets)
		# End func return
		return
    # End initDictSet
	
	# Function for initializing the labeled training data set
    def initTrainingSet(self):
        self.getTweetText()
        self.getTerms()
        # The apply_features func processes a set of labeled tweet strings using the passed extractFeatures func
        self.trainingSet = apply_features(self.extractFeatures, self.labeledTweets)
		# End func return
        return
	# End initTrainingSet
	
    # Function to get relevant tweet terms
    def getTweetText(self):
        for (terms, relevance) in self.labeledTweets:
            self.allTerms.extend(terms)
        # End for
		# End func return
        return
    # End getTweetText

    # Function to get term features
    def getTerms(self):
        self.allTerms = nltk.FreqDist(self.allTerms)
        self.wordFeatures = self.allTerms.keys()
		# End func return
        return
    # End getTerms

    # Function to extract features from tweets
    def extractFeatures(self, tweet_terms):
		# Set of unique tweet terms
        tweetFeatures = {}
        for word in self.wordFeatures:
            tweetFeatures['contains(%s)' % word] = (word in tweet_terms)
        # End for
        # Return feature set
        return tweetFeatures
    # End extractFeatures
    
	# Function to train the input NB classifier using it's apply_features func
	# This function is overridden for the scikit learn wrapper for multinomial NB
    def trainClassifier(self):
		self.classifierNB = nltk.NaiveBayesClassifier.train(self.trainingSet)
		# End func return
        return
    # End trainClassifier
	
    # Function to classify input tweet
	# This function is overridden for the scikit learn wrapper for multinomial NB
    def isRelevant(self, tweet_text):
        # Return the use of the classifier
        return self.classifierNB.classify(self.extractFeatures(twc.cleanUpTweet(tweet_text).split())) == "relevant"
    # End isRelevant
# End class    

# Sub class to weight term relevance
class WeightedRelevanceClassifier(RelevanceClassifier):

	# Sub class constructor
    def __init__(self):
		# Call the super class constructor which initializes the classifier
        super(WeightedRelevanceClassifier, self).__init__()
		# End func return
        return
	# End wrapper class constructor
		
	# Overriding func to train multinomial NB classifier
    def trainClassifier(self):
        # Pipeline of transformers with a final estimator
		# pipeline(steps=[...])
        pipeline = Pipeline([('tfidf', TfidfTransformer()), # Perform tf-idf weighting on features
                     ('chi2', SelectKBest(chi2, k=1000)), # Select 1000 greatest chi-squared stats between features
                     ('nb', MultinomialNB())]) # Allows for classification using discrete features, allows tf-idf
        # Create the multinomial NB classifier
		self.classifierMNB = SklearnClassifier(pipeline)
		# Train the classifier
        self.classifierMNB.train(self.trainingSet)
		# End func return
        return
	# End trainClassifier override
	
	# Overriding func to classify input tweet
    def isRelevant(self, tweet_text):
        # Return the use of the classifier
        return self.classifierMNB.classify(self.extractFeatures(twc.cleanUpTweet(tweet_text).split())) == "relevant"
    # End isRelevant override
# End sub class
# End script

