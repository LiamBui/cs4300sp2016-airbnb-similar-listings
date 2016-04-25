from django.conf.urls import url

from . import views
import csv
import urllib2
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def desc_tfidf_initialization():
	nyc_url = 'https://s3.amazonaws.com/similairbnb/filtered_nyc_listings.csv'
	sf_url = 'https://s3.amazonaws.com/similairbnb/filtered_sf_listings.csv'

	start = time.time()

	# Turn data into dicts of id to dict
	nyc = {}
	sf = {}
	for row in csv.DictReader(urllib2.urlopen(nyc_url), skipinitialspace=True):
		nyc[row['id']] = {k: v for k, v in row.items()}

	for row in csv.DictReader(urllib2.urlopen(sf_url), skipinitialspace=True):
		sf[row['id']] = {k: v for k, v in row.items()}
	
	# Take out the descriptions and summaries of listings
	nyc_descript_dict = {}
	sf_descript_dict = {}

	for d in nyc:
		nyc_descript_dict[d] = nyc[d]['description']+" "+nyc[d]['summary']

	for d in sf:
		sf_descript_dict[d] = sf[d]['description']+" "+sf[d]['summary']

	sf_listing_index_to_id = {index:listing_id for index, listing_id in enumerate([d for d in sf_descript_dict])}
	nyc_listing_index_to_id = {index:listing_id for index, listing_id in enumerate([d for d in nyc_descript_dict])}

	nyc_descript_arr = [nyc_descript_dict[d] for d in nyc_descript_dict]
	sf_descript_arr = [sf_descript_dict[d] for d in sf_descript_dict]

	n_feats = 5000
	nyc_listing_by_vocab = np.empty((len(nyc_descript_dict), n_feats))
	sf_listing_by_vocab = np.empty((len(sf_descript_dict), n_feats))

	time_elapsed = time.time() - start
	print("TIME TOOK TO LOAD: " + str(time_elapsed))

	return {"nyc": nyc, 
    		"sf": sf,
    		"nyc_listing_index_to_id": nyc_listing_index_to_id,
    		"sf_listing_index_to_id": sf_listing_index_to_id,
    		"nyc_descript_arr": nyc_descript_arr,
    		"sf_descript_arr": sf_descript_arr}

	
desc_tfidf = desc_tfidf_initialization()

app_name = 'pt'
urlpatterns = [
    url(r'^$', views.index, name='index')
]




# with open('data/filtered_nyc_listings.csv') as f:
#    	nyc = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        
# with open('data/filtered_sf_listings.csv') as f:
# 	sf = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
