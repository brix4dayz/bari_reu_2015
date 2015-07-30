# author: Hayden Fuss

import numpy as np

sentiments = ['angry', 'calm', 'fearful', 'sad', 'excited', 'positive', 'negative', 'neutral']

for s in sentiments:

  test = []

  tweets = []

  with open(s + 'Training_Uncleaned.txt', 'r') as f:
    for line in f:
      tweets.append(line.rstrip('\n'))

  for i in range(0,30):
    j = np.random.randint(len(tweets))
    test.append(tweets.pop(j))

  with open(s + 'Training.txt', 'w') as f:
    f.write('\n'.join(tweets))

  with open(s + 'Validation.txt', 'w') as f:
    f.write('\n'.join(test))

