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

def find_similar(input_description):
	with open('data/filtered_nyc_listings.csv') as f:
  	NYClistings = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

	with open('data/filtered_sf_listings.csv') as f:
		SFlistings = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
	        
	descript_dict = {}
	for n in NYClistings:
		key = n['id']
		descript_dict[key]=n['description']
	for s in SFlistings:
  	key = s['id']
  	descript_dict[key]=s['description']

  n_feats = 5000
	descriptions = [input_description]+ [descript_dict[d] for d in descript_dict]
	listing_by_vocab = np.empty((len(descriptions), n_feats))

	tfidf_vec = TfidfVectorizer(min_df = 10, max_df = .8, max_features = n_feats, norm='l2', stop_words = 'english')
	listing_by_vocab = tfidf_vec.fit_transform(descriptions)

	ranked_list = np.argsort(cosine_similarity(listing_by_vocab[0:1], listing_by_vocab))[0][::-1]

	top_ten = ranked_list[1:11] #first element is the input listing itself
	top_ten_descriptions = []
	for i in top_ten:
		top_ten_descriptions.append(descriptions[i])

	return top_ten_descriptions