import csv
from json import dump
from ast import literal_eval

LISTING_PATH = "data/sf_listings.csv"
OUT_LISTING = "data/filtered_sf_listings.csv"

REVIEW_PATH = "data/sf_reviews.csv"
OUT_REVIEWS = "data/filtered_sf_reviews.json"

FEATURE_LIST = ["id", "listing_url", "name", "summary", "space", "description", "thumbnail_url",
"host_is_superhost", "host_identity_verified", "neighbourhood_cleansed", 
"neighbourhood_group_cleansed", "zipcode", "room_type", "accommodates", "bedrooms", "beds",
"amenities", "price", "minimum_nights", "review_scores_rating", "review_scores_accuracy",
"review_scores_cleanliness", "review_scores_checkin", "review_scores_communication",
"review_scores_location", "review_scores_value", "instant_bookable", "cancellation_policy"]

# Preprocessing listing data
# in_file = open(LISTING_PATH, "rb")
# reader = csv.DictReader(in_file)

# with open(OUT_LISTING, "w") as out_file:
# 	writer = csv.DictWriter(out_file, fieldnames=FEATURE_LIST)
# 	writer.writeheader()
# 	for row in reader:
# 		newrow = {}
# 		for f in FEATURE_LIST:
# 			newrow[f] = row[f]
# 		writer.writerow(newrow)

in_file = open(REVIEW_PATH, 'rb')

def read_csv_reviews(file):
	results = {}
	reader = csv.DictReader(in_file)
	previd = 0
	reviews = []
	for row in reader:
		comments = row['comments']
		if not previd:
			previd = row['listing_id']
			reviews = [comments]
		elif row['listing_id'] == previd:
			reviews.append(comments)
		else:
			results[previd] = reviews
			previd = row['listing_id']
			reviews = [comments]
	return results

with open(OUT_REVIEWS, 'w') as out_file:
	dump(read_csv_reviews(in_file)[], out_file, indent=4)

	
	
	

