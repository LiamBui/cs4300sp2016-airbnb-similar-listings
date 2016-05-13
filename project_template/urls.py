from django.conf.urls import url

from . import views
import csv
import urllib2
import time
import json
import pickle
import sys

amazon_s3 = 'https://s3.amazonaws.com/similairbnb/'


def desc_tfidf_initialization():
	sf_url = 'https://s3.amazonaws.com/similairbnb/filtered_sf_listings.csv'
	# Turn data into dicts of id to dict
	sf = {}
	
	for row in csv.DictReader(urllib2.urlopen(sf_url), skipinitialspace=True):
		sf[row['id']] = {k: v for k, v in row.items()}
	
	# Take out the descriptions and summaries of listings
	sf_descript_dict = {}

	for d in sf:
		sf_descript_dict[d] = sf[d]['description']+" "+sf[d]['space']

	sf_listing_index_to_id = {index:listing_id for index, listing_id in enumerate([d for d in sf_descript_dict])}
	sf_id_to_listing_index = {listing_id:index for index, listing_id in enumerate([d for d in sf_descript_dict])}
	sf_descript_arr = [sf_descript_dict[d] for d in sf_descript_dict]
	sf_descript_arr = [sf_descript_dict[d] for d in sf_descript_dict]

	return {
    		"sf": sf,
    		"sf_listing_index_to_id": sf_listing_index_to_id,
    		"sf_descript_arr": sf_descript_arr,
    		"sf_id_to_index": sf_id_to_listing_index
    	}

def lda_initialization():
	return pickle.load(open('data/final_lda_topics.pickle', 'r'))

def feature_initializatoin():
	sf_data = pickle.load(open('data/sf_data_processed.pickle', 'r'))
	sf_index = pickle.load(open('data/sf_index_processed.pickle', 'r'))
	return (sf_data, sf_index)


start = time.time()
desc_tfidf = desc_tfidf_initialization()
lda_data = lda_initialization()
(feature_data, feature_index) = feature_initializatoin()

time_elapsed = time.time() - start
print("TIME TOOK TO LOAD: " + str(time_elapsed))

app_name = 'pt'
urlpatterns = [
    url(r'^$', views.index, name='index')
]




# with open('data/filtered_nyc_listings.csv') as f:
#    	nyc = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        
# with open('data/filtered_sf_listings.csv') as f:
# 	sf = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
