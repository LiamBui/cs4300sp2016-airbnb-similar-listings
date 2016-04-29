from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import get_medium_img_url, similarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import numpy as np
from sklearn.metrics.pairwise import distance_metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib2
import csv

FEATURE_LIST = ["host_is_superhost", "host_identity_verified", "room_type", "accommodates", "bedrooms", "beds",
"amenities", "price", "review_scores_accuracy",
"review_scores_cleanliness", "review_scores_checkin", "review_scores_communication",
"review_scores_location", "review_scores_value", "instant_bookable", "cancellation_policy"]

RANGE_FEATURE_LIST = ["accommodates", "bedrooms", "beds", "price"]
BOOL_FEATURE_LIST = ["instant_bookable", "host_is_superhost", "host_identity_verified"]

AMENITIES_VALUES =  ['Air Conditioning', 'Buzzer/Wireless Intercom', 'Carbon Monoxide Detector', 'Dryer', 'Essentials', 
'Family/Kid Friendly', 'Free Parking on Premises', 'Heating', 'Kitchen', 'Shampoo', 'Smoke Detector', 'TV', 'Washer', 'Wireless Internet']
VALUE_FEATURE_LIST = ["review_scores_accuracy",
"review_scores_cleanliness", "review_scores_checkin", "review_scores_communication",
"review_scores_location", "review_scores_value"]

ACCOMMODATES_RANGES = [1, 2, 3, 4, 5, 6, 10]
PRICE_RANGES = [50, 100, 200, 300, 500, 1000, 3000]
BEDROOMS_VALUES = [0,1,2,3,4,5,6,7,8,9,10] # COULD BE NONE
BEDS_RANGES = [0, 1, 2, 3, 4, 5, 6, 10] # COULD BE NONE
REVIEW_SCORE_RANGES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def load_reviews(data):
    reviews = []
    for r in data['reviews']:
        reviews.append(r['comments'])
    return reviews

def get_new_value_by_range(f, row):
    if f == 'accommodates':
        for v in ACCOMMODATES_RANGES:
            if row['person_capacity'] <= v:
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
            price = row[f]
            if price <= v:
                return v

def extract_listing_feature(k):
    result = {}
    for f in FEATURE_LIST:
        if f in RANGE_FEATURE_LIST:
            result[f] = str(get_new_value_by_range(f, k))
        elif f == 'amenities':
            new_amenities = k['amenities']
            for a in AMENITIES_VALUES:
                if a in new_amenities:
                    result[a] = str(1)
                else:
                    result[a] = str(0)
        elif f in BOOL_FEATURE_LIST:
            if f == "host_is_superhost":
                result[f] = '1' if k['primary_host']['is_superhost'] else '0'
            elif f == "host_identity_verified":
                result[f] = '1' if k['primary_host']['identity_verified'] else '0'
            elif f == "instant_bookable":
                result[f] = '1' if k[f] else '0'
        elif f in VALUE_FEATURE_LIST:
            if f == 'review_scores_value':
                result[f] = k['review_rating_value']
            elif f == 'review_scores_cleanliness':
                result[f] = k['review_rating_cleanliness']
            elif f == 'review_scores_checkin':
                result[f] = k['review_rating_checkin']
            elif f == 'review_scores_location':
                result[f] = k['review_rating_location']
            elif f == 'review_scores_communication':
                result[f] = k['review_rating_communication']
            elif f == 'review_scores_accuracy':
                result[f] = k['review_rating_accuracy']
        else:
            result[f] = k[f]
    return result


# Create your views here.
def index(request):
    output_list = ''
    output = ''
    orig_listing = {}
    search = ''
    if request.GET.get('AirbnbURL'):
        headers = {"User-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
        search = request.GET.get('AirbnbURL')
        if (search.find('?') == -1):
            search_id = search[search.find('rooms/')+6:]
        else:
            search_id = search[search.find('rooms/')+6:search.find('?')]
        url = 'https://api.airbnb.com/v2/listings/' + search_id + '?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3'

        review_url = "https://api.airbnb.com/v2/reviews?client_id=3092nxybyb0otqw18e8nh5nty&listing_id="+search_id+"&role=all"
        
        api_request = urllib2.Request(url, headers=headers)
        review_request = urllib2.Request(review_url, headers=headers)

        data = json.loads(urllib2.urlopen(api_request).read())
        listing_reviews = load_reviews(json.loads(urllib2.urlopen(review_request).read()))
        extracted_data = extract_listing_feature(data['listing'])

        similarity(data['listing'], listing_reviews, extracted_data)

        output = output_list

        orig_listing = {k: data['listing'][k] for k in ('room_type', 'description', 'price', 'bedrooms', 'person_capacity', 'summary', 'name','thumbnail_url')}
        orig_listing['listing_url'] = search
        orig_listing['accommodates'] = orig_listing['person_capacity']
        orig_listing['thumbnail_url'] = get_medium_img_url(orig_listing['thumbnail_url'])
        # paginator = Paginator(output_list, 10)
        # page = request.GET.get('page')
        # try:
        #     output = paginator.page(page)
        # except PageNotAnInteger:
        #     output = paginator.page(1)
        # except EmptyPage:
        #     output = paginator.page(paginator.num_pages)
        # print("OUTPUT: " +output)
    return render_to_response('project_template/index.html',{'listing_url':search, 'orig_listing': orig_listing,'output': output,'magic_url': request.get_full_path()})
