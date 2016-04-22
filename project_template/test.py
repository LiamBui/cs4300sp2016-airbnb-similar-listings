from .models import Docs
import os
import Levenshtein
import json
import numpy as np
from sklearn.metrics.pairwise import distance_metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib2
import csv


def read_file(n):
	path = Docs.objects.get(id = n).address;
	file = open(path)
	transcripts = json.load(file)
	return transcripts

def _edit(query, msg):
    return Levenshtein.distance(query.lower(), msg.lower())

#def find_similar(q):
#	transcripts = read_file(1)
#	result = []
#	for transcript in transcripts:
#		for item in transcript:
#			m = item['text']
#			result.append(((_edit(q, m)), m))
#
#	return sorted(result, key=lambda tup: tup[0])

with open('data/filtered_nyc_listings.csv') as f:
   	NYClistings = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        
with open('data/filtered_sf_listings.csv') as f:
	SFlistings = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

def find_similar(input_description):
	
	    
	data = NYClistings + SFlistings

	descript_dict = {}
	for d in data:
	    key = d['id']
	    descript_dict[key]=d['description']

	id_to_listing = {}
	for d in data:
	    id_to_listing[d['id']] = d

	listing_index_to_id = {index:listing_id for index, listing_id in enumerate([d['id'] for d in data])}

	n_feats = 5000
	descriptions = [input_description]+ [descript_dict[d] for d in descript_dict]
	listing_by_vocab = np.empty((len(descriptions), n_feats))

	tfidf_vec = TfidfVectorizer(min_df = 10, max_df = .8, max_features = n_feats, norm='l2', stop_words = 'english')
	listing_by_vocab = tfidf_vec.fit_transform(descriptions)

	ranked_list = np.argsort(cosine_similarity(listing_by_vocab[0:1], listing_by_vocab))[0][::-1]

	top_ten_idx = ranked_list[1:11] #first element is the input listing itself
	top_ten_listings = []  #top ten listings and their data
	for i in top_ten_idx:
	    listing_data = id_to_listing[listing_index_to_id[i]]
	    sub_dict = {k: listing_data[k] for k in ('listing_url', 'description', 'price', 'bedrooms', 'accommodates', 
	                                       'summary', 'name')}
	    top_ten_listings.append(sub_dict)
	return top_ten_listings