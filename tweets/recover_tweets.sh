#!/bin/bash

# restores database from pgdump file
pg_restore geo_tweets_2013_04_03.dump > geo.sql

# replaces all tabs with commas, making it csv format
sed 's/	/,/g' < geo.sql > geo.csv

rm -rf geo.sql

# removes first 35 lines and last 22 lines
< geo.csv tail -n +35 | tail -r | tail -n +23 | tail -r > temp.csv

# adds csv header to first line
sed '1i\
tweet_id,time,lat,lon,goog_x,goog_y,sender_id,sender_name,source,reply_to_user_id,reply_to_tweet_id,place_id,tweet_text\
' temp.csv > geo.csv

rm -rf temp.csv
