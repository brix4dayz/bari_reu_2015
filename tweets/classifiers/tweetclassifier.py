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
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

# Global field declarations
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Define class to classify tweet relevance
class TweetClassifier(object):
    # Class constructor to initialize classifier
    def __init__(self, paths, cleaner):
        self.cleaner = cleaner
        # Initialize data sets
        self.trainingSet = [] # Labeled tweet training data set
        self.categories = []
        self.tweets = []
        self.labels = []
        self.allTerms = []      
        # Begin functions for classification
        self.initTrainingSet(paths) # Initialize classes
        self.trainClassifier()
        # End func return statement
        return
    # End class constructor
    
    # Function to initialize the feature sets
    def initTrainingSet(self, paths):
        self.categories = paths.keys()
        # Loop through the txt files line by line
        # Assign labels to tweets for sentiments in class paths
        for category in paths.keys():
            with open(current_dir + paths[category], "r") as trainingFile:
                for line in trainingFile:
                    self.tweets.append(line)
                    self.labels.append(self.categories.index(category))
        self.labels = np.array(self.labels)
        # End func return statement
        return
    # End initDictSet
    
    # Function to build classifier pipeline
    # Default multinomial NB using chi sqaured statistics
    def initPipeline(self):
        # Pipeline of transformers with a final estimator
        # The pipeline class behaves like a compound classifier
        # pipeline(steps=[...])

        # Multinomial NB pipeline with TFIDF
        self.pipeline = Pipeline([('tfidf', TfidfTransformer()),
                      ('chi2', SelectKBest(chi2, k=1000)),
                      ('nb', MultinomialNB())])

        #self.pipeline = Pipeline([('chi2', SelectKBest(chi2, k=1000)),
        #              ('nb', MultinomialNB())])
		
		# End func return statement
        return
    # End initPipeline

   # Function to train the classifier using the built pipeline
    def trainClassifier(self):
        # Initialize the pipeline
        self.initPipeline()
        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)
        # End func return statement
        return
    # End trainClassifier

    # Function to classify input tweet  
    def classify(self, tweet_list):
        # Clean the input list of tweets
        for i in range(0,len(tweet_list)):
            tweet_list[i] = self.cleaner(tweet_list[i])

        # Return classified the input tweet text
        return self.classifier.predict(tweet_list)
    # End classify func

    # Function to get the predicted classifiers confusion matrix
    def getConfusionMatrix(self, actual, predicted):
        print(metrics.classification_report(actual, predicted, target_names=self.categories))
        # Return the confusion matrix
        return metrics.confusion_matrix(actual,predicted)
    # End getConfusionMatrix
# End class TweetClassifier

# Sub class to perform linear Multinomial NB tweet classification on transformed data
class TweetClassifierMNB(TweetClassifier):
    # Class constructor
    def __init__(self, paths, cleaner):
        # Call the super class constructor which initializes the classifier
        super(TweetClassifierMNB, self).__init__(paths, cleaner)
        # End func return statement
        return
    # End wrapper class constructor
        
    # Overriding function to build MNB classifier using a pipeline
    def initPipeline(self):
        # Pipeline of transformers with a final estimator
        # In order to make the vectorizer => transformer => classifier easier to work with, 
        # scikit-learn provides a Pipeline class that behaves like a compound classifier
        self.pipeline = Pipeline([('vect', CountVectorizer()), # Create a vector of feature frequencies
                                    ('tfidf', TfidfTransformer()), # Perform tf-idf weighting on features
                                    ('mnb', MultinomialNB())]) # Use the multinomial NB classifier
        # List of (name, transform) tuples (implementing fit/transform) that are chained, 
        # in the order in which they are chained, with the last object an estimator.
        # End func return statement
        return
    # End initPipeline override
	
	# Overriding function to classify input tweet  
    def classify(self, tweet_list):
        # Clean the input list of tweets
        for i in range(0,len(tweet_list)):
            tweet_list[i] = self.cleaner(tweet_list[i])

        # Return classified the input tweet text
        return self.classifier.predict(tweet_list)
    # End classify override
# End TweetClassifierMNB sub class

# Sub class to perform linear support vector machine (SVM) tweet classification
class TweetClassifierSVM(TweetClassifier):
    # Class constructor
    def __init__(self, paths, cleaner):
        # Call the super class constructor which initializes the classifier
        super(TweetClassifierSVM, self).__init__(paths, cleaner)
        # End func return
        return
    # End wrapper class constructor
    
    # Overriding function to build SVM classifier using a pipeline
    def initPipeline(self):
        # Pipeline of transformers with a final estimator
        # In order to make the vectorizer => transformer => classifier easier to work with, 
        # scikit-learn provides a Pipeline class that behaves like a compound classifier
        self.pipeline = Pipeline([('vect', CountVectorizer()), # Create a vector of feature frequencies
                            ('tfidf', TfidfTransformer()), # Perform tf-idf weighting on features
                            ('svm', SGDClassifier())]) # Use the SVM classifier
        # List of (name, transform) tuples (implementing fit/transform) that are chained, 
        # in the order in which they are chained, with the last object an estimator.
        # End of func return statement
        return
    # End initPipeline override
	
	# Overriding function to classify input tweet  
    def classify(self, tweet_list):
        # Clean the input list of tweets
        for i in range(0,len(tweet_list)):
            tweet_list[i] = self.cleaner(tweet_list[i])

        # Return classified the input tweet text
        return self.classifier.predict(tweet_list)
    # End classify override
# End TweetClassifierSVM sub class

# sources:
#   http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html