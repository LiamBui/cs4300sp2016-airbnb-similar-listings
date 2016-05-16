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
from decimal import Decimal

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

	terms = tfidf_vec.get_feature_names()

	listing_index_to_id = desc_tfidf["sf_listing_index_to_id"]

	sim_list = cosine_similarity(listing_by_vocab[0], listing_by_vocab)[0]

	results = {}
	for index, listing_id in listing_index_to_id.iteritems():
		results[listing_id] = sim_list[index+1]

	return (results, listing_by_vocab, terms)


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

def lda_reviews(v):
	reviews_data = urls.lda_data 
	
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
		results[k] = float(len((mset(topics) & mset(v))))/(len(topics)+len(v))

	return results

def similarity(data, reviews, extracted, input_amenities):
	feature_sim = find_similar_features(extracted, data['id'])
	descript_data = find_similar_descript(data['description'] + " " + data['space'])
	descript_sim = descript_data[0]
	lda_results = lda_reviews(reviews)
	min_accom = data['person_capacity']
	#pass in the tf_idf matrix
	tf_idf_matrix = descript_data[1]

	desc_tfidf = urls.desc_tfidf
	combined = {}
	for k, v in feature_sim.iteritems():
		if k != data['id']:
			if k in lda_results:
				combined[k] = (v + descript_sim[k] + lda_results[k])/3

	max_score = max(combined.values())
	
	for k, v in combined.iteritems():
		combined[k] = v / max_score

	ranked_list = sorted(combined.items(), key=operator.itemgetter(1), reverse=True)
	full_data = desc_tfidf['sf']

	top_ten_idx = ranked_list[:200] #first element is the input listing itself
	top_ten_listings = []  #top ten listings and their data

	# BEGIN TFIDF WORDS FOR WORD CLOUD
	k = 15
	n = 25
	terms = descript_data[2]
	tf_idf_matrix = tf_idf_matrix.toarray()
	res = tf_idf_matrix[0]
	orig = tf_idf_matrix[0]
	stop_words = get_stop_words('en')
	stop_words += ['bed', 'room', 'bedroom', 'apartment', 'kitchen', 'we', 'home', 'can', 'one', 'located', 'guests', 'guest','0', '1', '2', '3', '4', '5', '6', '7', '8', '9','100', 'just', 'well', 'area', 'two', 'three', 'like', 'stay', 'will', 'also', 'living', 'll']
	for i,sim in top_ten_idx[1:k]:
	 	list_id = full_data[i]['id']
	 	index = desc_tfidf["sf_id_to_index"][list_id]
	 	#get listing id
	 	t = orig*tf_idf_matrix[index+1]
	 	res = res + t
	indices = np.argsort(res)[::-1]
	counter = 0
	term_scores = {}
	for i in indices:
		if(terms[i] not in stop_words and counter<n):
			term_scores[terms[i]] = res[i]*50
			counter+=1



	# TO LAURA AND LIAM
	# sim here is the actual score, not used yet, but you guys can make it a part of 
	# the result returned
	for (i, sim) in top_ten_idx:
	    listing_data = full_data[i]
	    if min_accom <= int(listing_data['accommodates']):
	    	listing_data["thumbnail_url"] = get_medium_img_url(listing_data["thumbnail_url"])
	    	sub_dict = {k: listing_data[k] for k in ('room_type','listing_url', 'description', 'price', 'bedrooms', 'accommodates', 'space', 'name','thumbnail_url', 'amenities')}
	    	sub_dict['price'] = sub_dict['price'][:sub_dict['price'].find('.')]
	    	sub_dict['sim_score'] = sim*100
	    	sub_dict['sim_score_rounded'] = round(sim*100,2)
	    	sub_dict['amenities'] = sub_dict['amenities'].replace('{','').replace('}','').replace('"','').replace(',',', ')
	    	sim_amenities = list(set(sub_dict['amenities'].split(', ')) & set(input_amenities))
	    	sub_dict['sim_amenities'] = sim_amenities

	    	top_ten_listings.append(sub_dict)
	return top_ten_listings, term_scores





