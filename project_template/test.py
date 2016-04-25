from .models import Docs
import os

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import urllib2
import urls

def read_file(n):
	path = Docs.objects.get(id = n).address;
	file = open(path)
	transcripts = json.load(file)
	return transcripts

# def _edit(query, msg):
#     return Levenshtein.distance(query.lower(), msg.lower())

#def find_similar(q):
#	transcripts = read_file(1)
#	result = []
#	for transcript in transcripts:
#		for item in transcript:
#			m = item['text']
#			result.append(((_edit(q, m)), m))
#
#	return sorted(result, key=lambda tup: tup[0])

def get_medium_img_url(url):
	if not url:
		url = 'http://assets.fontsinuse.com/static/use-media-items/22/21749/full-2000x1125/5670373c/bnb_billboard_01-2000x1125.jpeg'
	index = url.find('?')
	if index != -1:
		url = url[:index+1]+"aki_policy=medium"
	return url

tfidf_vec = TfidfVectorizer(min_df=10, max_df=.8, max_features=5000, norm='l2', stop_words='english')

def nyc_find_similar(input_description):
	desc_tfidf = urls.desc_tfidf

	nyc_listing_by_vocab = tfidf_vec.fit_transform([input_description]+desc_tfidf["nyc_descript_arr"])
	
	ranked_list = np.argsort(cosine_similarity(nyc_listing_by_vocab[0], nyc_listing_by_vocab)[0][::-1])

	top_ten_idx = ranked_list[1:11] #first element is the input listing itself
	top_ten_listings = []  #top ten listings and their data
	for i in top_ten_idx:
	    listing_data = desc_tfidf['nyc'][desc_tfidf["nyc_listing_index_to_id"][i]]
	    listing_data["thumbnail_url"] = get_medium_img_url(listing_data["thumbnail_url"])
	    sub_dict = {k: listing_data[k] for k in ('room_type','listing_url', 'description', 'price', 'bedrooms', 'accommodates', 
	                                       'summary', 'name','thumbnail_url')}
	    top_ten_listings.append(sub_dict)
	return top_ten_listings

def sf_find_similar(input_description):
	desc_tfidf = urls.desc_tfidf

	sf_listing_by_vocab = tfidf_vec.fit_transform([input_description]+desc_tfidf["sf_descript_arr"])
	
	ranked_list = np.argsort(cosine_similarity(sf_listing_by_vocab[0], sf_listing_by_vocab)[0][::-1])

	top_ten_idx = ranked_list[1:11] #first element is the input listing itself
	top_ten_listings = []  #top ten listings and their data
	for i in top_ten_idx:
	    listing_data = desc_tfidf['sf'][desc_tfidf["sf_listing_index_to_id"][i]]
	    listing_data["thumbnail_url"] = get_medium_img_url(listing_data["thumbnail_url"])
	    sub_dict = {k: listing_data[k] for k in ('room_type','listing_url', 'description', 'price', 'bedrooms', 'accommodates', 
	                                       'summary', 'name','thumbnail_url')}
	    top_ten_listings.append(sub_dict)
	return top_ten_listings

