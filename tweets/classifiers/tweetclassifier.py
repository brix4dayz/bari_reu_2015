# Author: Elizabeth Brooks
# File: tweetclassifier.py
# Date Modified: 07/14/2015
# Edited: Hayden Fuss

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
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn import metrics

# Global field declarations
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

##########################################################################################################################

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
        # Initialize the pipeline
        self.initPipeline()
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
		# As other classifiers, SGD has to be fitted with two arrays: 
		#	an array X of size [n_samples, n_features] holding the training samples
		#	and an array Y of size [n_samples] holding the target values (class labels) for the training samples
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
        self.pipeline = Pipeline([('vect', CountVectorizer()), # Create a vector of feature frequencies
                      ('tfidf', TfidfTransformer()), # Perform tf-idf weighting on features
                      ('chi2', SelectKBest(chi2, k=2000)), # Use chi squared statistics to select the 1000 best features
                      ('nb', MultinomialNB())]) # Use the multinomial NB classifier

        #self.pipeline = Pipeline([('chi2', SelectKBest(chi2, k=1000)),
        #              ('nb', MultinomialNB())])
        
        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)

        # End func return statement
        return
    # End initPipeline

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
    
    # Function to perform a grid search for best features
    # http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html
    # GridSearchCV implements a "fit" method and a "predict" method like any classifier 
    #   except that the parameters of the classifier used to predict is optimized by cross-validation.
    def getGridSearch(self):
        # Set the search parameters
        parameters = {'vect__ngram_range': [(1,1),(1,2)], # Try either words or birgrams
                    'vect__max_df': (0.5, 0.75, 1.0),
                    #'vect__max_features': (None, 5000, 10000, 50000),
                    'tfidf__use_idf': (True, False),
                    'tfidf__norm': ('l1', 'l2'),
                    'clf__alpha': (0.00001, 0.000001),
                    'clf__penalty': ('l2', 'elasticnet', 'l1'),
                    'clf__n_iter': (10, 50, 80),
                    'clf__random_state':(0, 42)}
        # Use all cores to create a grid search
        classifierGS = GridSearchCV(self.pipeline, parameters, n_jobs=-1)
        # Fit the CS estimator for use as a classifier
        classifierGS = classifierGS.fit(self.tweets, self.labels)
        # Get the scores using the GS classifier
        bestParam, score, _ = max(classifierGS.grid_scores_, key=lambda x: x[1])
        # Print the parameter values
        for param_name in sorted(parameters.keys()):
            print("%s: %r" % (param_name,bestParam[param_name]))
        # Print the classifier score
        print("Classifier score: " + str(score) + "\n")
        # End of func return statement
        return
    # End getGridSearch 
# End class TweetClassifier

##########################################################################################################################

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
                                    ('clf', MultinomialNB())]) # Use the multinomial NB classifier
        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)
        # End func return statement
        return
    # End initPipeline override
# End TweetClassifierMNB sub class

##########################################################################################################################

# Sub class to perform linear support vector machine (SVM) tweet classification
class TweetClassifierLinearSVM(TweetClassifier):
    # Class constructor
    def __init__(self, paths, cleaner):
        # Call the super class constructor which initializes the classifier
        super(TweetClassifierLinearSVM, self).__init__(paths, cleaner)
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
                            ('clf', SGDClassifier(random_state=42))]) # Use the SVM classifier
        # The SGD estimator implememts regularlized linear models with stochastic gradient descent learning
        # By default, SGD supports a linear support vector machine (SVM) using the default args below
        # SGDClassifier(loss='hinge', penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, n_iter=5, 
        #   shuffle=True, verbose=0, epsilon=0.1, n_jobs=1, random_state=None, learning_rate='optimal', 
        #   eta0=0.0, power_t=0.5, class_weight=None, warm_start=False, average=False)
        # http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html

        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)
        # End of func return statement
        return
    # End initPipeline override
# End TweetClassifierLinearSVM sub class

##########################################################################################################################

# Sub class to perform quadratic support vector machine (SVM) tweet classification
class TweetClassifierQuadraticSVM(TweetClassifier):
    # Class constructor
    def __init__(self, paths, cleaner):
        # Call the super class constructor which initializes the classifier
        super(TweetClassifierQuadraticSVM, self).__init__(paths, cleaner)
        # End func return
        return
    # End wrapper class constructor
    
    # Overriding function to build SVM classifier using a pipeline
    def initPipeline(self):
        # Pipeline of transformers with a final estimator
        # In order to make the vectorizer => transformer => classifier easier to work with, 
        # scikit-learn provides a Pipeline class that behaves like a compound classifier
        self.pipeline = Pipeline([('vect', CountVectorizer(max_df=0.5, ngram_range=(1,1))), # Create a vector of feature frequencies
                            ('tfidf', TfidfTransformer(norm='l2', use_idf=True)), # Perform tf-idf weighting on features
                            ('clf', SGDClassifier(loss='squared_hinge', random_state=42, n_iter=80, penalty='elasticnet', alpha=1e-05))]) # Use the SVM classifier
        # The SGD estimator implememts regularlized linear models with stochastic gradient descent learning
        # By default, SGD supports a linear support vector machine (SVM) using the default args below
        # SGDClassifier(loss='hinge', penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, n_iter=5, 
        #   shuffle=True, verbose=0, epsilon=0.1, n_jobs=1, random_state=None, learning_rate='optimal', 
        #   eta0=0.0, power_t=0.5, class_weight=None, warm_start=False, average=False)
        # http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html
        # 'squared_hinge' is like hinge, which is used for linear SVM, but is quadratically penalized.

        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)
        # End of func return statement
        return
    # End initPipeline override
# End TweetClassifierQuadraticSVM sub class

##########################################################################################################################

# Sub class to perform less sensitive support vector machine (SVM) tweet classification
class TweetClassifierModifiedSVM(TweetClassifier):
    # Class constructor
    def __init__(self, paths, cleaner):
        # Call the super class constructor which initializes the classifier
        super(TweetClassifierModifiedSVM, self).__init__(paths, cleaner)
        # End func return
        return
    # End wrapper class constructor
    
    # Overriding function to build SVM classifier using a pipeline
    def initPipeline(self):
        # Pipeline of transformers with a final estimator
        # In order to make the vectorizer => transformer => classifier easier to work with, 
        # scikit-learn provides a Pipeline class that behaves like a compound classifier
        self.pipeline = Pipeline([('vect', CountVectorizer(ngram_range=(1,1), max_df=0.5)), # Create a vector of feature frequencies
                            ('tfidf', TfidfTransformer(norm='l2', use_idf=True)), # Perform tf-idf weighting on features
                            ('clf', SGDClassifier(loss='modified_huber', random_state=0, penalty='l2', n_iter=80, alpha=1e-05))]) # Use the SVM classifier
        # The SGD estimator implememts regularlized linear models with stochastic gradient descent learning
        # By default, SGD supports a linear support vector machine (SVM) using the default args below
        # SGDClassifier(loss='hinge', penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, n_iter=5, 
        #   shuffle=True, verbose=0, epsilon=0.1, n_jobs=1, random_state=None, learning_rate='optimal', 
        #   eta0=0.0, power_t=0.5, class_weight=None, warm_start=False, average=False)
        # http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html
        # 'modified_huber' is another smooth loss that brings tolerance to outliers as well as probability estimates.
        # The other losses that may be used are designed for regression but can be useful in classification as well.
        # The epsilon arg for 'huber', determines the threshold at which it becomes less important to get 
        #   the prediction exactly right. 

        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)
        # End of func return statement
        return
    # End initPipeline override
# End TweetClassifierModifiedSVM sub class

##########################################################################################################################

class TweetClassifierMaxEnt(TweetClassifier):

    def __init__(self, paths, cleaner):
        super(TweetClassifierMaxEnt, self).__init__(paths, cleaner)
        return

    def initPipeline(self):
        self.pipeline = Pipeline([('vect', CountVectorizer()),
                            ('tfidf', TfidfTransformer()),
                            ('clf', LogisticRegression())])
        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)
        return

##########################################################################################################################

class TweetClassifierBNB(TweetClassifier):

    def __init__(self, paths, cleaner):
        super(TweetClassifierBNB, self).__init__(paths, cleaner)
        return

    def initPipeline(self):
        self.pipeline = Pipeline([('vect', CountVectorizer()),
                            ('tfidf', TfidfTransformer()),
                            ('clf', BernoulliNB())])
        # Fit the created multinomial NB classifier
        self.classifier = self.pipeline.fit(self.tweets, self.labels)
        return

# sources:
#   http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html