

name = raw_input("Enter your name (hayden, jeremy, liz): ")
name = name.lower()

fearful = []
excited = []
angry = []
sad = []
positive = []
calm = []
negative = []
neutral = []

with open(name + "_training.txt", "r") as inFile:
  for tweet in inFile:
    tweet = tweet.rstrip('\n')
    print tweet
    sentiment = ""
    while (sentiment == ""):
      sentiment = raw_input("Enter the tweets sentiment: (c-alm, e-xcited, a-angry, f-earful, s-ad, p-ositive, n-egative, u-neutral, or o-ther (not English)): ")
    sentiment = sentiment.lower()[0]
    if sentiment == 'c':
      calm.append(tweet)
    elif sentiment == 'a':
      angry.append(tweet)
    elif sentiment == 'f':
      fearful.append(tweet)
    elif sentiment == 's':
      sad.append(tweet)
    elif sentiment == 'p':
      positive.append(tweet)
    elif sentiment =='n':
      negative.append(tweet)
    elif sentiment == 'e':
      excited.append(tweet)
    elif sentiment == 'u':
      neutral.append(tweet)

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

with open(name + "_neutral.txt", "w") as out:
  out.write('\n'.join(neutral))