# Author: Elizabeth Brooks
# Date Modified: 07/09/2015

# PreProcessor Directives
import os
import sys
sys.path.append(os.path.realpath('../'))
import csv
import yaml
import re
from nltk.classify import apply_features
import random
# Directives for twc yaml
import twittercriteria as twc

# Define wrapper class
class RelevenceClassifier(object):

    def __init__(self):
        return

    # Global field declarations
    current_dir = os.getcwd()
    # Set the output file path
    resultsPath = current_dir + '/relevantTweetResults.txt'
    # Initialize the training and dev data sets
    trainSet, devSet, labeledTweetDict, featureSet = []
    
    # Function to initialize the feature sets
    def initDictSet(class1_path='relevantTraining.txt', class2_path='irrelevantTraining.txt'):
        # Loop through the txt files line by line
        # Assign labels to tweets
        # Two classes, relevant and irrelevant to the marathon
        self.labeledTweets = []
        with open(current_dir + class1_path, "r") as relevantFile:
            for line in relevantFile:
                self.labeledTweets.append((line.split(), 'relevant'))
        with open(current_dir + class2_path, "r") as irrelevantFile:
            for line in irrelevantFile:
                self.labeledTweets.append((line.split(), 'irrelevant'))
        # Randomize the data
        random.shuffle(self.labeledTweets)
        # Close the files
        relevantTxtFile.close()
        irrelevantTxtFile.close()
    # End initDictSet

    # Function to extract features from tweets
    def extractFeatures(train_file):
        # Iterate through the Twitter data csv files by tweet text
        with open(current_dir + '/../' + train_file + '.csv') as csvfile:  
            tweetIt = csv.DictReader(csvfile)
            # Retrieve terms in tweets
            for twitterData in tweetIt:
                # Send the tweet text to the function for removing unncessary characters
                tweetText = twc.cleanUpTweet(twitterData['tweet_text'])
                # Determine the feature sets
                for word in tweetText.split():
                    featureSet = [(word, relevance) for (word, relevance) in labeledTweetDict]
                # End for
            # End for
        # End with
    # End extractFeatures

    # Function for training the classifier
    def trainClassifier():   
        # Establish the training set
        # Add dev set assignment here
        trainSet = featuresSet

        # Train the Naive Bayes (NB) classifier
        classifierNB = nltk.NaiveBayesClassifier.train(trainSet)
    # End trainClassifyData
    
    # Function to classify input test data, csv file format
    def classifyCSV(test_file):    
        # Classify input test data
        # Create object for writting to a text file
        tweetResultsFile = open(resultsPath, "w")
        # Iterate through the Twitter data csv files by tweet text
        with open(current_dir + '/../' + test_file + '.csv') as csvfile:  
            tweetIt = csv.DictReader(csvfile)
            # Retrieve terms in tweets
            for twitterData in tweetIt:
                # Send the tweet text to the function for removing unncessary characters
                tweetText = twc.cleanUpTweet(twitterData['tweet_text'])
                # Send the results of the classifier to a txt file
                tweetResultsFile.write(classifierNB.classify(tweetText))
            # End for
        # End with
        # Close file
        tweetResultsFile.close()
    # End classifyCSV

    # Function to classify input cleaned tweet txt
    def isRelevant(self, tweet_text):
        # Return the use of the classifier
        return self.classifierNB.classify(twc.cleanUpTweet(tweet_text).split())
    # End isRelevant

    # The main method
    def initClassifier():
        # Request user input of text class files
        inputClassFile1 = raw_input("Enter the first class feature set txt file name...\nEx: relevantTraining.txt")
        inputClassFile2 = raw_input("Enter the second class feature set txt file name...\nEx: irrelevantTraining.txt")

        # Initialize the classifier dictionary based on relevant features
        initDictSet(inputClassFile1, inputClassFile2)

        # Request user input of the file name of train/dev data to be processed
        inputTrainFile = raw_input("Enter training data set csv file name...\nEx: cleaned_geo_tweets_Apr_12_to_22")
        # Request file name of data to be classified
        inputTestFile = raw_input("Enter test data set csv file name...\nEx: cleaned_geo_tweets_Apr_12_to_22")

        # Extract features and train the NB classifier using input training data
        extractFeatures(inputTrainFile)
        trainClassifier()

        # Classify the input test data, csv file format
        classifyCSV(inputTestFile)
    # End initClassifier
# End Wrapper    
# End script