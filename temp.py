import csv

LISTING_PATH = "data/nyc_listings.csv"
REVIEW_PATH = "data/nyc_review.csv"
OUT_LISTING = "data/filtered_nyc_listings.csv"
OUT_REVIEWS = "data/filtered_nyc_reviews.csv"

FEATURE_LIST = ["id", "listing_url", "name"]

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