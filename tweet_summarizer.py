from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import pos_tag
from nltk import wordnet as wn
from nltk.wsd import lesk
import string
import argparse
import operator

# Takes a text as an input, removes stop words and punctuation marks from it 
# and returns a set of stemmed version of the remaining words.
def getStemmedForm(text,stemmer_obj):
	stop = stopwords.words('english')
	for i in string.punctuation:
		stop.append(i)
	remainder = [i for i in word_tokenize(text.lower()) if i not in stop]
	# return remainder
	stemmed_remainder = set()
	for w in remainder:
		x=stemmer_obj.stem(w)
		stemmed_remainder.add(x)
	return stemmed_remainder


# Only selects the features which are Nouns excluding proper nouns, verbs, adverbs & adjectives
# returns a dictionary of feat:pos_tag
def removeUnwantedFeatures(tweet_features):
	featues_tag = ['FW','JJ','JJR','JJS','NN','NNS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ','WRB']
	reduced_features = {}
	for feature in tweet_features:
		token = feature.split(":")
		reduced_features[token[0]] = token[1]
	return reduced_features

def penn_to_wn(tag):
    if tag.startswith('J') or tag.startswith('W'):
        return 'a' #ADJECTIVE are represented as 'a' in WordNet
    elif tag.startswith('N'):
        return 'n' #NOUN are represented as 'n' in WordNet
    elif tag.startswith('R'):
        return 'r' #ADVERB are represented as 'r' in WordNet
    elif tag.startswith('V'): 
        return 'v' #VERB are represented as 'v' in WordNet
    return None

stemmer = PorterStemmer()
parser = argparse.ArgumentParser()
parser.add_argument("cleaned_data")
parser.add_argument("processed_data")
parser.add_argument("write_to")
args = parser.parse_args()
cleaned_data = open( args.cleaned_data, "r+")
processed_data = open( args.processed_data, "r+")
file_write = open(args.write_to, 'w')
index=0
tweet_map = {}
tweet_weights = {}
max_weight = -1
max_tweet = ""
for tweet in cleaned_data:
	tweet = tweet.strip()
	if not tweet:
		processed_data.readline()
		continue 
	else:
		tweet_map[index] = tweet
		weight=0
		tweet_set = getStemmedForm(tweet,stemmer)
		tweet_features_string = processed_data.readline().strip()
		if not tweet_features_string:
			continue
		else:
			tweet_features = eval(tweet_features_string)
			reduced_features = removeUnwantedFeatures(tweet_features)

			for feature,feature_pos_tag in reduced_features.items():
				feature_synset = lesk(tweet, feature, penn_to_wn(feature_pos_tag))
				if feature_synset is not None:
					
					feature_meaning = feature_synset.definition()
					feature_meaning_set = getStemmedForm(feature_meaning,stemmer)

					weight+=len(set.intersection(tweet_set,feature_meaning_set))

		if weight > max_weight:
			max_weight = weight
			max_tweet = tweet
		tweet_weights[index]=weight
		index+=1
sorted_tweet_weights = sorted(tweet_weights.items(), key=operator.itemgetter(1), reverse=True)
count = 0
for items in sorted_tweet_weights:
	file_write.write((tweet_map[items[0]]))
	file_write.write((".\n")) 
	# print(tweet_map[items[0]],".",sep="")
	count+=1
	if(count == 4):
		break;
	file_write.flush()
file_write.close()