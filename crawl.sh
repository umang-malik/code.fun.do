#!/bin/bash

#Find trending hashtags
python TrendingHashtags.py >| hashtags.txt

# Downloading the tweets
echo Downloading tweets
rm -rf crawl_tweets
mkdir crawl_tweets
python crawl.py hashtags.txt crawl_tweets/
find crawl_tweets/ -size 0 -type f -delete

#Clean file names
for file in $(ls crawl_tweets); do
    crawl_tweets="crawl_tweets/"
    name=$(echo ${file} | rev | sed -e "s/[^A-Za-z//]/_/g" | cut -d '_' -f 2 | rev)
    mv $crawl_tweets$file $crawl_tweets$name
done
