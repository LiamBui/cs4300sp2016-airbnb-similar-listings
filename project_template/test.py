import os

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import urllib2
import urls
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim
import time
from collections import Counter as mset
import operator
from sklearn.feature_extraction import DictVectorizer

tokenizer = RegexpTokenizer(r'\w+')
en_stopwords = get_stop_words('en')
stemmer = PorterStemmer()
vec = DictVectorizer()
tfidf_transformer = TfidfTransformer(norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
lda_tokenizer = RegexpTokenizer(r'\b[a-z]+\b')



def get_medium_img_url(url):
	if not url:
		url = 'http://assets.fontsinuse.com/static/use-media-items/22/21749/full-2000x1125/5670373c/bnb_billboard_01-2000x1125.jpeg'
	index = url.find('?')
	if index != -1:
		url = url[:index+1]+"aki_policy=medium"
	return url

tfidf_vec = TfidfVectorizer(min_df=10, max_df=.8, max_features=5000, norm='l2', stop_words='english')

def find_similar_descript(input_description):
	desc_tfidf = urls.desc_tfidf

	listing_by_vocab = tfidf_vec.fit_transform([input_description]+desc_tfidf["sf_descript_arr"])

	listing_index_to_id = desc_tfidf["sf_listing_index_to_id"]

	sim_list = cosine_similarity(listing_by_vocab[0], listing_by_vocab)[0]

	results = {}
	for index, listing_id in listing_index_to_id.iteritems():
		results[listing_id] = sim_list[index+1]

	return results

def find_similar_features(data, listing_id):
	sf_data = urls.feature_data
	index_to_id = urls.feature_index
	# add listing data to the matrix
	sf_data.append(data)

	index_to_id[len(sf_data) -1] = listing_id
	feature_matrix = tfidf_transformer.fit_transform(vec.fit_transform(sf_data).toarray())
	sim_list = cosine_similarity(feature_matrix[len(sf_data) -1], feature_matrix)[0]
	
	results = {}
	for index, listing_id in index_to_id.iteritems():
		results[listing_id] = sim_list[index]
	return results

# THIS FUNCTION IS NOT CALLED YET, NEED LDA FILES
def lda_reviews(v):
	reviews_data = {}
	
	v = [[stemmer.stem(i) for i in tokenizer.tokenize(r.lower()) if not i in en_stopwords] for r in v]
	dictionary = corpora.Dictionary(v)
	corpus = [dictionary.doc2bow(r) for r in v]
	ldamodel = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=50)
	lda_output = ldamodel.show_topics(num_topics=5, num_words=3)
		
	topics = []
	for i in lda_output:
		topics.extend(lda_tokenizer.tokenize(i[1]))

	results = {}
	for k, v in reviews_data.iteritems():
		results[k] = len((mset(topics) & mset(v)).elements())/(len(topics)+len(v))

	return results

def similarity(data, reviews, extracted):
	feature_sim = find_similar_features(extracted, data['id'])
	descript_sim = find_similar_descript(data['description'] + " " + data['summary'])
	# lda_results = lda_reviews(reviews)
	desc_tfidf = urls.desc_tfidf
	combined = {}
	for k, v in feature_sim.iteritems():
		if k != data['id']:
			combined[k] = v * descript_sim[k]

	ranked_list = sorted(combined.items(), key=operator.itemgetter(1), reverse=True)
	full_data = desc_tfidf['sf']

	top_ten_idx = ranked_list[:10] #first element is the input listing itself
	top_ten_listings = []  #top ten listings and their data

	# TO LAURA AND LIAM
	# sim here is the actual score, not used yet, but you guys can make it a part of 
	# the result returned
	for (i, sim) in top_ten_idx:
	    listing_data = full_data[i]
	    listing_data["thumbnail_url"] = get_medium_img_url(listing_data["thumbnail_url"])
	    sub_dict = {k: listing_data[k] for k in ('room_type','listing_url', 'description', 'price', 'bedrooms', 'accommodates', 
	                                       'summary', 'name','thumbnail_url')}
	    top_ten_listings.append(sub_dict)
	return top_ten_listings





