from sklearn.feature_extraction import DictVectorizer
import csv
import pickle

# Mostly results from dataset exploration
FEATURE_LIST = ["id", "host_is_superhost", "host_identity_verified", "room_type", "accommodates", "bedrooms", "beds",
"amenities", "price", "review_scores_rating", "review_scores_accuracy",
"review_scores_cleanliness", "review_scores_checkin", "review_scores_communication",
"review_scores_location", "review_scores_value", "instant_bookable", "cancellation_policy"]

STR_FEATURE_LIST = ["cancellation_policy", "room_type", "amenities"]
RANGE_FEATURE_LIST = ["accommodates", "bedrooms", "beds", "review_scores_rating", "price"]
VALUE_FEATURE_LIST = ["review_scores_accuracy",
"review_scores_cleanliness", "review_scores_checkin", "review_scores_communication",
"review_scores_location", "review_scores_value"]
BOOL_FEATURE_LIST = ["instant_bookable", "host_is_superhost", "host_identity_verified"]

CANCEL_POLICY = ['no_refunds', 'super_strict_60', 'strict', 'super_strict_30', 'flexible', 'moderate']
ROOM_TYPE_VALUES = ['Shared room', 'Entire home/apt', 'Private room']
AMENITIES_VALUES =  ['Air Conditioning', 'Buzzer/Wireless Intercom', 'Carbon Monoxide Detector', 'Dryer', 'Essentials', 
'Family/Kid Friendly', 'Free Parking on Premises', 'Heating', 'Kitchen', 'Shampoo', 'Smoke Detector', 'TV', 'Washer', 'Wireless Internet']

ACCOMMODATES_RANGES = [1, 2, 3, 4, 5, 6, 10]
PRICE_RANGES = [50, 100, 200, 300, 500, 1000, 3000]
BEDROOMS_VALUES = [0,1,2,3,4,5,6,7,8,9,10] # COULD BE NONE
BEDS_RANGES = [0, 1, 2, 3, 4, 5, 6, 10] # COULD BE NONE
REVIEW_SCORE_RANGES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
SCORE_VALUES = [0,1,2,3,4,5,6,7,8,9,10] # COULD BE NONE


# host_identity_verified: f, t
# instant_bookable: f, t
# host_is_superhost: f, t

def get_new_value_by_range(f, row):
	if not row[f]:
		return None
	elif f == 'accommodates':
		for v in ACCOMMODATES_RANGES:
			if row[f] <= v:
				return v
	elif f == 'bedrooms':
		for v in BEDROOMS_VALUES:
			if row[f] <= v:
				return v
	elif f == 'beds':
		for v in BEDS_RANGES:
			if row[f] <= v:
				return v
	elif f == 'price':
		for v in PRICE_RANGES:
			price = float(row[f].replace('$', '').replace(',', ''))
			if price <= v:
				return v
	elif f == 'review_scores_rating':
		for v in REVIEW_SCORE_RANGES:
			if row[f] <= v:
				return v

def preprocess(data):
	index_to_id = {}
	for index, k in enumerate(data):
		for f in FEATURE_LIST:
			if f in RANGE_FEATURE_LIST:
				k[f] = str(get_new_value_by_range(f, k))
			elif f == 'amenities':
				new_amenities = set(k['amenities'].replace('\"', '').replace('{', '').replace('}', '').split(','))
				for a in AMENITIES_VALUES:
					if a in new_amenities:
						k[a] = str(1)
					else:
						k[a] = str(0)
				k.pop(f, None)
			elif f in BOOL_FEATURE_LIST:
				k[f] = '1' if k[f] == 't' else '0'
			elif f == 'id':
				index_to_id[index] = k[f]
				k.pop(f, None)
	return {'data':data, 'index_to_id': index_to_id}

nyc_data = []
sf_data = []

with open('../data/filtered_nyc_listings.csv') as f:
   	nyc_data = [{k: v for k, v in row.items() if k in FEATURE_LIST} for row in csv.DictReader(f, skipinitialspace=True)]
        
with open('../data/filtered_sf_listings.csv') as f:
	sf_data = [{k: v for k, v in row.items() if k in FEATURE_LIST} for row in csv.DictReader(f, skipinitialspace=True)]


vec = DictVectorizer()

processed_nyc_all = preprocess(nyc_data)
processed_sf_all = preprocess(sf_data)

processed_nyc = vec.fit_transform(processed_nyc_all['data']).toarray()

processed_sf = vec.fit_transform(processed_sf_all['data']).toarray()

nyc_index_to_id = processed_nyc_all['index_to_id']
sf_index_to_id = processed_sf_all['index_to_id']

nyc_index_out = '../data/nyc_index_processed.pickle'
sf_index_out = '../data/sf_index_processed.pickle'
nyc_out = '../data/nyc_data_processed.pickle'
sf_out = '../data/sf_data_processed.pickle'

nyc_file = open(nyc_out, 'wb')
sf_file = open(sf_out, 'wb')

nyc_index_file = open(nyc_index_out, 'wb')
sf_index_file = open(sf_index_out, 'wb')

pickle.dump(nyc_index_to_id, nyc_index_file)
pickle.dump(sf_index_to_id, sf_index_file)

pickle.dump(processed_nyc, nyc_file)
pickle.dump(processed_sf, sf_file)

nyc_file.close()
sf_file.close()

# LOAD IN PICKLE FILES
# nyc_file_in = open(nyc_out, 'r')
# nyc_data = pickle.load(nyc_file_in)


# Code used to explore dataset
# def get_all_possible_values(feature):
# 	results = set()
# 	for k in nyc_data:
# 		results.add(k[feature])
# 	return sorted(results)

# def get_amenities():
# 	results = set()
# 	for k in nyc_data:
# 		v = set(k['amenities'].replace('\"', '').replace('{', '').replace('}', '').split(','))
# 		# print(v)
# 		if len(results) == 0:
# 			results = v
# 		else:
# 			results.union(v)
# 	return sorted(results)

# def get_max_min_values(feature):
# 	max_v = 0
# 	min_v = 800
# 	for k in nyc_data:
# 		v = float(k[feature].replace('$', '').replace(',', ''))
# 		if v < min_v:
# 			min_v = v
# 		elif v > max_v:
# 			max_v = v
# 	return (max_v, min_v)

# print(get_all_possible_values('review_scores_value'))
# print(get_amenities())
# print(get_max_min_values('price'))
