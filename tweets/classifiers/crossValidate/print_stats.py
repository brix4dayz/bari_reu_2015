import cPickle as cp

name = raw_input("Enter name of person who did test (hayden, jeremy, liz): ")
name = name.lower()

otherName = raw_input("Enter the name of the person who was tested (hayden, jeremy, liz): ")
otherName = otherName.lower()

f = open(otherName + '_' + name + '.pkl', 'rb')
yourTweets = cp.load(f)
f.close()

incorrect = 0

incorrectCounts = {'calm':0, 'excited':0, 'angry':0, 'fearful':0, 'sad':0, 'positive':0, 'negative':0, 'neutral':0}

f = open(otherName + '.pkl', 'rb')
theirTweets = cp.load(f)
f.close()

for each in yourTweets:
  s = each['sentiment']
  s1 = theirTweets[each['idx']]['sentiment']
  if s != s1:
    incorrect += 1
    incorrectCounts[s1] += 1

print "Percent disagreed: " + str(float(incorrect)/80)
print "Percent disagreed for each sentiment:"
for s in incorrectCounts.keys():
  print s + ": " + str(float(incorrectCounts[s])/10)