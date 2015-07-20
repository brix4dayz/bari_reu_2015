

name = raw_input("Enter your name (hayden, jeremy, liz): ")
name = name.lower()

fearful = []
excited = []
angry = []
sad = []
positive = []
calm = []
negative = []

with open(name + "_training.txt", "r") as inFile:
  for tweet in inFile:
    tweet = tweet.rstrip('\n')
    print tweet
    sentiment = ""
    while (sentiment == ""):
      sentiment = raw_input("Enter the tweets sentiment: (c-alm, e-xcited, a-angry, f-earful, s-ad, p-ositive, n-egative, or o-ther (not English)): ")
    sentiment = sentiment.lower()[0]
    if sentiment == 'c':
      calm.append(sentiment)
    elif sentiment == 'a':
      angry.append(sentiment)
    elif sentiment == 'f':
      fearful.append(sentiment)
    elif sentiment == 's':
      sad.append(sentiment)
    elif sentiment == 'p':
      positive.append(sentiment)
    elif sentiment =='n':
      negative.append(sentiment)
    elif sentiment == 'e':
      excited.append(sentiment)

with open(name + "_fearful.txt", "w") as out:
  out.write('\n'.join(fearful))


with open(name + "_calm.txt", "w") as out:
  out.write('\n'.join(calm))


with open(name + "_angry.txt", "w") as out:
  out.write('\n'.join(angry))


with open(name + "_excited.txt", "w") as out:
  out.write('\n'.join(excited))


with open(name + "_sad.txt", "w") as out:
  out.write('\n'.join(sad))


with open(name + "_positive.txt", "w") as out:
  out.write('\n'.join(positive))


with open(name + "_negative.txt", "w") as out:
  out.write('\n'.join(negative))