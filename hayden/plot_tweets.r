
tweets <- read.csv(file="tweets_per_day.csv", sep=",", head=TRUE)

hist(rep(tweets$day, tweets$number_tweets), breaks=11:22, main="Tweets Containing Keyword vs. Day", 
  xlab="Day", ylab="Number of Tweets")

axis(side=1, at=seq(11, 22, 1), labels=seq(11, 22, 1))


