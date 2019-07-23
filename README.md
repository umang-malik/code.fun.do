# Tweeting Pigeons
This application generates summaries based on the current trending hashtags on Twitter.
Summaries will greatly help the user in understanding “why the topic is trending”. We have proposed an algorithm which automatically generates summaries for trending topics/hashtags based on tweets and it's related news article.

### Code.Fun.Do
This project was done as part of an __online hackathon__ at IIT Kanpur, and deployed over a [website](tweeting-pigeons.azurewebsites.net). The team comprised of first year students (names in alphabetical order, and no special preference):
* Ayush Gupta
* Tanmay Anand
* Umang Malik  

The demo for the application can be found on https://youtu.be/EOZI0QjhI9g

### Requirements: 
```
1. pip install tweepy
2. pip install nltk
3. NodeJS
```
	 
1. `TrendingHashtags.py`
	Collect currently trending hashtags. 
2. `crawl.py`
	Crawls Twitter for the trends in hashtags.txt
3. `clean.py`
	Removes twitter specific stop words from the data
4. `tag.py`
	Pre-process the data
5. `./tweet_summarizer.sh`
	Output: Summary will be generated for the trending topics/hashtags in predicted folder

For automating all this stuff, we have created shell files, which do this for you. You just need to run the files.

We plan to improve the algorithm and create a better structured summary in due course of time.
