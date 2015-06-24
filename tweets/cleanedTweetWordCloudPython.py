## A program for generating tweet based word clouds. Specifically in regards to the "cleaned", geo-tagged Twitter data from April 12 to 22 of 2013.
## The program may be easily altered to create any number of word clouds given an input txt file. A csv file may be used as well, the relavent information from which is parsed and saved into a txt file for use by the word cloud function.

# Author: Elizabeth Brooks
# Date Modified: 06/24/2015
​
# PreProcessor Directives
import csv
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud
​
# The main method
def main():
    # Create object for writing to a text file
    tweetFile = open("OutputTweets.txt", "w")
​
    # Iterate through the "cleaned" Twitter data by tweet
    with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvFile:  
      tweetIt = csv.DictReader(csvFile)
      # Retrieve the strings of tweets
      for twitterData in tweetIt:
        # Convert tweets to lower case to pool words of the same spelling
        twitterData['tweet_text'] = twitterData['tweet_text'].lower()
        # Write the selected Twitter data, tweets, to the txt file
        tweetFile.write(twitterData['tweet_text'] + "\n")
​
    # Close the file obj
    tweetFile.close()
    
    # Use the defined function to create the tweet word cloud
    tweetWordCloud()
# End main 

## The above code creates a file object and opens a txt file to store all the strings of tweets contained in the Twitter data from the "cleaned" tweets csv file. The tweet strings are then retrieved from the csv file by iterating through the tweet hashes made by the DictReader. Finally, these strings are converted to lower case. This is because we are interested in looking at the occurances of a given spelling of a word, regardless of case; stemming may be considered in the future to combine the frequencies of all conjugate forms of a words.

# Function for generating a word cloud
def tweetWordCloud():
    db = path.dirname(_file_)
    # Read in the txt file set by the main method
    text = open(path.join(db, 'OutputTweets.txt')).read()
    # Generate the word cloud
    wordcloud = WordCloud().generate(text)
    # Open a plot of the generated word cloud
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
# End tweetWordCloud

## The above function generates a word cloud based on words in the txt file created in the main method.
​## For more info: https://github.com/amueller/word_cloud