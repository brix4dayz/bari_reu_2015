# Author: Elizabeth Brooks
# Date Modified: 07/12/2015

# PreProcessor Directives
import os
import inspect
import sys
import csv
import yaml
import re
import random
sys.path.append(os.path.realpath('../'))
import twittercriteria as twc
# Classification function imports
import nltk
from nltk.classify import apply_features
from nltk.classify import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer

# Global field declarations
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Size of chi2 sample, can tune for best results with MNB
#chiK = 3000

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
        tweet_terms = set(tweet_terms)
		# Set of unique tweet terms
        tweetFeatures = {}
        for word in self.wordFeatures:
            tweetFeatures['contains(%s)' % word] = (word in tweet_terms)
        # End for
        # Return feature set
        return tweetFeatures
    # End extractFeatures
    
	# Function to train the input NB classifier using it's apply_features func
	# Should be overridden by child classes
    def trainClassifier(self):
        self.classifier = nltk.NaiveBayesClassifier.train(self.trainingSet)
    	# End func return
        return
    # End trainClassifier

    # Function to classify input tweet	
    def classify(self, tweet_text):
        return self.classifier.classify(self.extractFeatures(twc.cleanUpTweet(tweet_text).split()))

    # Determines relevance
    def isRelevant(self, tweet_text):
        # Return the use of the classifier
        return self.classify(tweet_text) == 'relevant'
    # End isRelevant

    def test(self, testSetRel, testSetIrr):
        for each in testSetRel, testSetIrr:
            for i in range(0, len(each)):
                each[i] = self.extractFeatures(twc.cleanUpTweet(each[i]).split())
        rel = np.array(self.classifier.classify_many(testSetRel))
        irr = np.array(self.classifier.classify_many(testSetIrr))   
        self.tp = (rel == 'relevant').sum()
        self.fn = (rel == 'irrelevant').sum()
        self.fp = (irr == 'relevant').sum()
        self.tn = (irr == 'irrelevant').sum()
        return

    def balancedF(self):
        prec = float(self.tp)/(float(self.tp) + float(self.fp))
        recall = float(self.tp)/(float(self.tp) + float(self.fn))
        Fscore = 2*prec*recall/(prec + recall)
        return Fscore

    def confusionMatrix(self):
        print "Confusion matrix:\n%d\t%d\n%d\t%d" % (self.tp, self.fn, self.fp, self.tn)
        return

# End class    

# Sub class to weight term relevance and use Bag-Of-Words (MultinomialNB)
class RelevanceMNB(RelevanceClassifier):
	# Sub class constructor
    def __init__(self, chiK):
		# Call the super class constructor which initializes the classifier
        self.chiK = chiK
        super(RelevanceMNB, self).__init__()
		# End func return
        return
	# End wrapper class constructor
	
	# Function to initialize the classifier pipeline
    def initPipeline(self):
        # Pipeline of transformers with a final estimator
        # The pipeline class behaves like a compound classifier
        # pipeline(steps=[...])

        # Old MNB pipeline with TFIDF
        # self.pipeline = Pipeline([('tfidf', TfidfTransformer()),
        #              ('chi2', SelectKBest(chi2, k=1000)),
        #              ('nb', MultinomialNB())])

        self.pipeline = Pipeline([('chi2', SelectKBest(chi2, k=self.chiK)),
                      ('nb', MultinomialNB())])
		# End func return
        return
	# End initPipeline
		
	# Overriding func to train multinomial NB classifier
    def trainClassifier(self):
        self.initPipeline()
        # Create the multinomial NB classifier
        self.classifier = SklearnClassifier(self.pipeline)
        # Train the classifier
        self.classifier.train(self.trainingSet)
        # End func return
        return
	# End trainClassifier override
# End sub class

# Sub class to perform linear Multinomial NB tweet classification on transformed data
class RelevanceLinearMNB(RelevanceClassifier):
	# Class constructor
    def __init__(self):
		# Call the super class constructor which initializes the classifier
        super(RelevanceLinearMNB, self).__init__()
		# End func return
        return
	# End wrapper class constructor
		
	# Function to initialize the vectorizer
	def initVector(self):
		# CountVectorizer supports counts of N-grams of words or consecutive characters
		self.countVect = countVectorizer()
		# Learn the vocabulary dictionary and return term-document matrix
		# The index value of a word in the vocabulary is linked to its frequency in the training set
		self.trainCounts = self.countVect.fit_transform(self.trainingSet) # Dictionary of feature indices
		# xTrainCounts.shape
	# End initVector
	
	# Function to initialize TF-iDF transformer
	def initTransformer(self):
		# Fit the estimator to the data
		self.tfTransformer = TfidfTransformer(use_idf=False).fit(self.trainCounts)
		# Transform the count matrix to a TF-iDF representation
		self.trainTF = self.tfTransformer.transform(self.trainCounts)
		# Should math xTrainCounts.shape
		# xTrainTF.shape
	# End initTransformer
		
	# Overriding func to build MNB classifier
    def initPipeline(self):
		# Initialize the term vector
		self.initVector()
		# Initialize the transformer
		self.initTransformer()
        # Pipeline of transformers with a final estimator
        # In order to make the vectorizer => transformer => classifier easier to work with, 
		# scikit-learn provides a Pipeline class that behaves like a compound classifier
        self.pipeline = Pipeline([('vect', CountVectorizer()), # Create a vector of feature frequencies
                            ('tfidf', TfidfTransformer()), # Perform tf-idf weighting on features
                            ('mnb', MultinomialNB())]) # Use the multinomial NB classifier
		# List of (name, transform) tuples (implementing fit/transform) that are chained, 
		# in the order in which they are chained, with the last object an estimator.
        return
	# End initPipeline
	
	# Overriding func to train the MNB classifier
    def trainClassifier(self):
		# Initialize the pipeline
        self.initPipeline()
		# Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.trainingSet)
        # Train the classifier
        self.classifier.train(self.trainingSet)
        # End func return
        return
	# End trainClassifier override
# End RelevanceLinearMNB sub class

# Sub class to perform linear support vector machine (SVM) tweet classification
class RelevanceLinearSVM(RelevanceClassifier):
	# Class constructor
    def __init__(self):
		# Call the super class constructor which initializes the classifier
        super(RelevanceLinearSVM, self).__init__()
		# End func return
        return
	# End wrapper class constructor
	
	# Function to initialize the vectorizer
	def initVector(self):
		# CountVectorizer supports counts of N-grams of words or consecutive characters
		self.countVect = countVectorizer()
		# Learn the vocabulary dictionary and return term-document matrix
		# The index value of a word in the vocabulary is linked to its frequency in the training set
		self.trainCounts = self.countVect.fit_transform(self.trainingSet) # Dictionary of feature indices
		# xTrainCounts.shape
	# End initVector
	
	# Function to initialize TF-iDF transformer
	def initTransformer(self):
		# Fit the estimator to the data
		self.tfTransformer = TfidfTransformer(use_idf=False).fit(self.trainCounts)
		# Transform the count matrix to a TF-iDF representation
		self.trainTF = self.tfTransformer.transform(self.trainCounts)
		# Should math xTrainCounts.shape
		# xTrainTF.shape
	# End initTransformer
	
	# Overriding func to build SVM classifier
    def initPipeline(self):
		# Initialize the term vector
		self.initVector()
		# Initialize the transformer
		self.initTransformer()
        # Pipeline of transformers with a final estimator
        # In order to make the vectorizer => transformer => classifier easier to work with, 
		# scikit-learn provides a Pipeline class that behaves like a compound classifier
        self.pipeline = Pipeline([('vect', CountVectorizer()), # Create a vector of feature frequencies
                            ('tfidf', TfidfTransformer()), # Perform tf-idf weighting on features
                            ('svm', SGDClassifier())]) # Use the SVM classifier
		# List of (name, transform) tuples (implementing fit/transform) that are chained, 
		# in the order in which they are chained, with the last object an estimator.
        return
	# End initPipeline override
	
	# Overriding func to train SVM classifier
    def trainClassifier(self):
		# Initialize the pipeline
        self.initPipeline()
		# Fit the created SVM classifier
        self.classifier = self.pipeline.fit(self.trainingSet)
        # Train the classifier
        self.classifier.train(self.trainingSet)
        return
	# End trainClassifier override
# End RelevanceLinearSVM sub class

# sources:
#   http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
#   http://stackoverflow.com/questions/10098533/implementing-bag-of-words-naive-bayes-classifier-in-nltk
#   http://www.nltk.org/book/ch06.html
#	http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
#	http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
#	http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

# End script

