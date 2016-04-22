import json
import numpy as np
from sklearn.metrics.pairwise import distance_metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib2
import csv

# 'https://www.airbnb.com/rooms/825531?s=vJx50hcn'

headers = {"User-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
search = input('Enter url: ')
if (search.find('?') == -1):
    search_id = search[search.find('rooms/')+6:]
else:
    search_id = search[search.find('rooms/')+6:search.find('?')]
url = 'https://api.airbnb.com/v2/listings/' + search_id + '?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3'
request = urllib2.Request(url, headers=headers)
data = json.loads(urllib2.urlopen(request).read())
input_description = data['listing']['description']

#make a dictionary of descriptions: descriptions[listing_id] = description
#make a tf-idf matrix of words by listings
#cosine similarity

#load the data
with open('data/filtered_nyc_listings.csv') as f:
     NYClistings = [{k: v for k, v in row.items()}
          for row in csv.DictReader(f, skipinitialspace=True)]
        
with open('data/filtered_sf_listings.csv') as f:
     SFlistings = [{k: v for k, v in row.items()}
          for row in csv.DictReader(f, skipinitialspace=True)]
    
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
for i in top_ten:
    listing_data = id_to_listing[listing_index_to_id[i]]
    sub_dict = {k: listing_data[k] for k in ('listing_url', 'description', 'price', 'bedrooms', 'accommodates', 
                                       'summary', 'name')}
    top_ten_listings.append(sub_dict)

#get ids of the listings so can look up other information to display
#need to figure out a way to map back from description to id
#descript dict maps the id key to the description value
#is there a faster way to do cosine similarity? can we construct a tf-idf vector from the input description instead
#of adding it to the tf-idf matrix?




