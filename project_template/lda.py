import json
import urllib2
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim
import time
import pickle

tokenizer = RegexpTokenizer(r'\w+')
lda_tokenizer = RegexpTokenizer(r'\b[a-z]+\b')
en_stopwords = get_stop_words('en')
stemmer = PorterStemmer()

data = {}
with open('../data/filtered_sf_reviews.json', 'r') as in_file:
	data = json.load(in_file)

def lda_reviews(data, isNYC=False):
	reviews_data = data
	results = {}
	start = time.time()
	counter = 0
	for k, v in reviews_data.iteritems():
		print(str(float(counter)/len(data)*100)+"%")
		v = [[stemmer.stem(i) for i in tokenizer.tokenize(r.lower()) if not i in en_stopwords] for r in v]
		dictionary = corpora.Dictionary(v)
		corpus = [dictionary.doc2bow(r) for r in v]
		ldamodel = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=50)
		lda_output = ldamodel.show_topics(num_topics=5, num_words=3)
		
		topics = []
		for i in lda_output:
			topics.extend(lda_tokenizer.tokenize(i[1]))
		# print(topics)
		results[k] = topics
		counter += 1
	
	time_elapsed = time.time() - start
	print("---------------TIME ELAPSED:"+time_elapsed+"-------------")
	return results

out_file = open("../pickles/review_topics.pickle", 'wb')
pickle.dump(lda_reviews(data), out_file)
out_file.close()