import csv
import twitter_criteria as twc
import time
import matplotlib.pyplot as plt

twc.loadCriteria()
time_fmt = twc.getTwitterTimeFmt()
handle_pattern = twc.getHandleRegex()
twc.clearCriteria()

handles = {}

senders = {}

with open('cleaned_geo_tweets_Apr_12_to_22.csv') as csvfile:
  twitterData = csv.DictReader(csvfile)
  for tweet in twitterData:
    if tweet['time'] != "":
      date = time.strptime(tweet['time'], time_fmt)
      if date.tm_mday > 15 or (date.tm_mday == 15 and date.tm_hour >= 14):
        
        if not tweet['sender_name'] in senders.keys():
          senders[tweet['sender_name']] = 1
        else:
          senders[tweet['sender_name']] += 1

        results = handle_pattern.findall(tweet['tweet_text'])
        for r in results:
          handle = r.strip("@").lower()
          if not handle in handles.keys():
            handles[handle] = 1
          else:
            handles[handle] += 1


fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(121) # 1x2 grid, 1st subplot
ax.axis("off")

colLabs = ['Twitter Handles', 'Frequency']

ax.set_title("Top 25 Most Active Accounts", fontsize=10)

table_data = []

for sender in sorted(senders, key=senders.get, reverse=True)[0:25]:
  table_data.append([sender, senders[sender]])

table = ax.table(loc='center', colLabels=colLabs, cellText=table_data)
table.set_fontsize(12)
table.scale(1.1,1.1)

ax = fig.add_subplot(122)
ax.axis("off")
ax.set_title("Top 25 Most \'Tweeted-At\' Accounts", fontsize=10)
table_data = []

for handle in sorted(handles, key=handles.get, reverse=True)[0:25]:
  table_data.append([handle, handles[handle]])

table = ax.table(loc='center', colLabels=colLabs, cellText=table_data)
table.set_fontsize(12)
table.scale(1.1,1.1)

plt.savefig('twitter_names.png', dpi=96)
plt.show()