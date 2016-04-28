from django.conf.urls import url

from . import views
import csv
import urllib2
import time
import json

amazon_s3 = 'https://s3.amazonaws.com/similairbnb/'


def desc_tfidf_initialization():
	nyc_url = 'https://s3.amazonaws.com/similairbnb/filtered_nyc_listings.csv'
	sf_url = 'https://s3.amazonaws.com/similairbnb/filtered_sf_listings.csv'

	

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

	return {"nyc": nyc, 
    		"sf": sf,
    		"nyc_listing_index_to_id": nyc_listing_index_to_id,
    		"sf_listing_index_to_id": sf_listing_index_to_id,
    		"nyc_descript_arr": nyc_descript_arr,
    		"sf_descript_arr": sf_descript_arr}

def reviews_initialization():
	nyc_url = 'https://s3.amazonaws.com/similairbnb/filtered_nyc_reviews.json'
	sf_url = 'https://s3.amazonaws.com/similairbnb/filtered_sf_reviews.json'
	nyc_reviews = json.load(urllib2.urlopen(nyc_url))
	sf_reviews = json.load(urllib2.urlopen(sf_url))
	return {
		"nyc_reviews": nyc_reviews,
		"sf_reviews": sf_reviews
	}

def feature_initializatoin():
	nyc_index_out = amazon_s3 + 'nyc_index_processed.pickle'
	sf_index_out = amazon_s3 + 'sf_index_processed.pickle'
	nyc_out = amazon_s3 + 'nyc_data_processed.pickle'
	sf_out = amazon_s3 + 'sf_data_processed.pickle'

	nyc_data = pickle.load(open(nyc_out, 'r'))
	sf_data = pickle.load(open(sf_out, 'r'))
	nyc_index = pickle.load(open(nyc_index_out, 'r'))
	sf_index = pickle.load(open(sf_index_out, 'r'))







start = time.time()
desc_tfidf = desc_tfidf_initialization()
reviews_data = reviews_initialization()

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
