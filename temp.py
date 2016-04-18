import csv

LISTING_PATH = "data/sf_listings.csv"
REVIEW_PATH = "data/nyc_review.csv"
OUT_LISTING = "data/filtered_sf_listings.csv"
OUT_REVIEWS = "data/filtered_nyc_reviews.csv"

FEATURE_LIST = ["id", "listing_url", "name", "summary", "space", "description", "thumbnail_url",
"host_is_superhost", "host_identity_verified", "neighbourhood_cleansed", 
"neighbourhood_group_cleansed", "zipcode", "room_type", "accommodates", "bedrooms", "beds",
"amenities", "price", "minimum_nights", "review_scores_rating", "review_scores_accuracy",
"review_scores_cleanliness", "review_scores_checkin", "review_scores_communication",
"review_scores_location", "review_scores_value", "instant_bookable", "cancellation_policy"]

in_file = open(LISTING_PATH, "rb")
reader = csv.DictReader(in_file)

with open(OUT_LISTING, "w") as out_file:
	writer = csv.DictWriter(out_file, fieldnames=FEATURE_LIST)
	writer.writeheader()
	for row in reader:
		newrow = {}
		for f in FEATURE_LIST:
			newrow[f] = row[f]
		writer.writerow(newrow)