

name = raw_input("Enter your name (hayden, jeremy, liz): ")
name = name.lower()

fearful = []
cheerful = []
angry = []
sad = []
objective = []
peaceful = []
undetermined = []

with open(name + "_training.txt", "r") as inFile:
  for tweet in inFile:
    tweet = tweet.rstrip('\n')
    print tweet
    sentiment = ""
    while (sentiment == ""):
      sentiment = raw_input("Enter the tweets sentiment: (c-heerful, a-angry, f-earful, s-ad, p-eaceful, o-bjective, u-ndetermined, or n-one (not English)): ")
    sentiment = sentiment.lower()[0]
    if sentiment == 'c':
      cheerful.append(sentiment)
    elif sentiment == 'a':
      angry.append(sentiment)
    elif sentiment == 'f':
      fearful.append(sentiment)
    elif sentiment == 's':
      sad.append(sentiment)
    elif sentiment == 'p':
      peaceful.append(sentiment)
    elif sentiment =='u':
      undetermined.append(sentiment)
    elif sentiment == 'o':
      objective.append(sentiment)

with open(name + "_fearful.txt", "w") as out:
  out.write('\n'.join(fearful))


with open(name + "_peaceful.txt", "w") as out:
  out.write('\n'.join(peaceful))


with open(name + "_angry.txt", "w") as out:
  out.write('\n'.join(angry))


with open(name + "_cheerful.txt", "w") as out:
  out.write('\n'.join(cheerful))


with open(name + "_sad.txt", "w") as out:
  out.write('\n'.join(sad))


with open(name + "_objective.txt", "w") as out:
  out.write('\n'.join(objective))


with open(name + "_undetermined.txt", "w") as out:
  out.write('\n'.join(undetermined))