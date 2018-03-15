#!/bin/bash

#Clean the tweets
echo Cleaning tweets
rm -rf clean_tweets
mkdir clean_tweets
python clean.py crawl_tweets/ clean_tweets/

#Tag the tweets.
echo Tagging tweets
rm -rf process_tweets
mkdir process_tweets
python tag.py clean_tweets/ process_tweets/

#Generate the summary of the files.
echo Summarizing tweets
rm -rf summary
mkdir summary
 for i in $(ls clean_tweets/); do
    summary="/summary/"
    working_dir=$(pwd)
    process_tweets="/process_tweets/"
    clean_tweets="/clean_tweets/"
    suffix="_features"
    file="$working_dir$clean_tweets"$i""
    feature="$working_dir$process_tweets"$i"$suffix"
    write_to="$working_dir$summary"$i""
    echo summarizing: "$write_to"
    python tweet_summarizer.py "$file" "$feature" "$write_to"
done

echo DONE!