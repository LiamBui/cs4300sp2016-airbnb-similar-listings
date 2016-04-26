import os

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import urllib2
import urls
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim
import time

tokenizer = RegexpTokenizer(r'\w+')
en_stopwords = get_stop_words('en')
stemmer = PorterStemmer()

def get_medium_img_url(url):
	if not url:
		url = 'http://assets.fontsinuse.com/static/use-media-items/22/21749/full-2000x1125/5670373c/bnb_billboard_01-2000x1125.jpeg'
	index = url.find('?')
	if index != -1:
		url = url[:index+1]+"aki_policy=medium"
	return url

tfidf_vec = TfidfVectorizer(min_df=10, max_df=.8, max_features=5000, norm='l2', stop_words='english')

def find_similar(input_description, isNYC=True):
	desc_tfidf = urls.desc_tfidf

	listing_by_vocab = None
	data = {}
	listing_index_to_id = {}
	if isNYC:
		listing_by_vocab = tfidf_vec.fit_transform([input_description]+desc_tfidf["nyc_descript_arr"])
		data = desc_tfidf['nyc']
		listing_index_to_id = desc_tfidf["nyc_listing_index_to_id"]
	else:
		listing_by_vocab = tfidf_vec.fit_transform([input_description]+desc_tfidf["sf_descript_arr"])
		data = desc_tfidf['sf']
		listing_index_to_id = desc_tfidf["sf_listing_index_to_id"]

	ranked_list = np.argsort(cosine_similarity(listing_by_vocab[0], listing_by_vocab)[0][::-1])

	top_ten_idx = ranked_list[1:11] #first element is the input listing itself
	top_ten_listings = []  #top ten listings and their data
	for i in top_ten_idx:
	    listing_data = data[listing_index_to_id[i]]
	    listing_data["thumbnail_url"] = get_medium_img_url(listing_data["thumbnail_url"])
	    sub_dict = {k: listing_data[k] for k in ('room_type','listing_url', 'description', 'price', 'bedrooms', 'accommodates', 
	                                       'summary', 'name','thumbnail_url')}
	    top_ten_listings.append(sub_dict)
	return top_ten_listings

def lda_reviews(isNYC=True):
	reviews_data = {}
	start = time.time()
	counter = 0
	if isNYC:
		reviews_data = urls.reviews_data['nyc_reviews']
	else:
		reviews_data = urls.reviews_data['sf_reviews']
	for k, v in reviews_data.iteritems():
		if counter > 50:
			break
		else:
			counter += 1
			v = [[stemmer.stem(i) for i in tokenizer.tokenize(r.lower()) if not i in en_stopwords] for r in v]
			dictionary = corpora.Dictionary(v)
			corpus = [dictionary.doc2bow(r) for r in v]
			ldamodel = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=50)
			# print(ldamodel.print_topics(num_topics=5, num_words=3))
	time_elapsed = time.time() - start
	print("LDA on 50 NYC listings' reviews took "+str(time_elapsed)+" seconds")




