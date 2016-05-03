from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Docs
from django.template import loader, RequestContext
from .form import QueryForm
from .test import get_medium_img_url, similarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
import json
import numpy as np
from sklearn.metrics.pairwise import distance_metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib2
import csv
from stop_words import get_stop_words
import string

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
    page_objects = []
    if request.GET.get('AirbnbURL'):
        if not request.GET.get('page_number'):
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
            # get reviews
            listing_reviews = load_reviews(json.loads(urllib2.urlopen(review_request).read()))
            # extract features and construct a vector of these features
            extracted_data = extract_listing_feature(data['listing'])

            # This is the function that returns the final list with all three components combined
            output = similarity(data['listing'], listing_reviews, extracted_data)
            
            orig_listing = {k: data['listing'][k] for k in ('room_type', 'description', 'price', 'bedrooms', 'person_capacity', 'space', 'name','thumbnail_url', 'amenities')}
            orig_listing['price'] = "{0:.2f}".format(float(orig_listing['price']))
            orig_listing['listing_url'] = search
            orig_listing['accommodates'] = orig_listing['person_capacity']
            orig_listing['thumbnail_url'] = get_medium_img_url(orig_listing['thumbnail_url'])

            stop_words = get_stop_words('en')
            stop_words += ['span', 'class', 'highlight', 'more', 'div', 'width', 'style', 'target', 'listing', 'container', 'score', 'meter', 'img', 'text', 'icons', 'spa', 'high', 'light']
            stop_words += ['bed', 'room', 'kitchen', 'we', 'home', 'can', 'one', 'located', 'guests', 'guest', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'just', 'well', 'area', 'two', 'three', 'like', 'stay']

            for listing in output: 
                listing['similar_words'] = list(set(filter(lambda x: x in str(orig_listing['description']).split() and x not in stop_words, str(listing['description'].translate(None, string.punctuation)).split())))

            global paginator 
            paginator = Paginator(output, 10)
            page_objects = paginator.page(1).object_list
            '''
            page_objects_new = []
            # print("OUTPUT: " +output)
            showChar = 300
            for thing in page_objects:
                if(str(thing['room_type']) == 'Entire home/apt'):
                    room_type_icon = '/static/entirehome.png'
                    room_type_text = 'Entire Home/Apt'
                elif (str(thing['room_type']) == 'Private room'):
                    room_type_icon = '/static/private.png'
                    room_type_text = 'Private Room'
                else:
                    room_type_icon = '/static/shared.png'
                    room_type_text = 'Shared Room'
                accom_icon = '/static/accommodates.png'
                accom_text = 'Accomodates: ' + str(thing['accommodates'])
                bedroom_icon = '/static/bedrooms.png'
                bedroom_text = 'Bedrooms: ' + str(thing['bedrooms'])
                html = '<div class = "listing-container"><div class ="listing-score">Similarity Score<div class="meter"><span style="width: '+ str(thing['sim_score']) + '%">' + str(thing['sim_score_rounded']) + '%</span></div></div><div class = "listing-info"><div class="listing-name"><a href="' + str(thing['listing_url']) + '" target="_blank">' + str(thing['name']) + '</a></div><br><div class = "quickinfo"><img src = "' + room_type_icon + '" class="icons"></img><p class="icon_labels">' + room_type_text + '</p></div><div class = "quickinfo"><img src = "' + accom_icon + '" class="icons"></img><p class="icon_labels">' + accom_text + '</p></div><div class = "quickinfo"><img src = "' + bedroom_icon + '" class="icons"></img><p class="icon_labels">' + bedroom_text + '</p></div><div class="quickinfo">' + str(thing['price']) + ' per Night</div></div><div class="listing-img-container"><img src="' + str(thing['thumbnail_url']) + '" /></div><div class="listing-text"><div class = "listing-description">Description: <br><span class="more">' + str(thing['description'])[:showChar] + '<span class="morecontent"><span>' + str(thing['description'])[showChar:len(str(thing['description'])) - showChar] + '</span><a href="" class="morelink">[...]</a></span></span></div><div class = "listing-summary">Summary: <br><span class="more">' + str(thing['summary'])[:showChar] + '<span class="morecontent"><span>' + str(thing['summary'])[showChar:len(str(thing['summary'])) - showChar] + '</span><a href="" class="morelink">[...]</a></span></span></div></div><br></div>'
                page_objects_new += html
                for word in thing['similar_words']:
                    for new_obj in page_objects_new:
                        new_obj.replace(word, '<span class="highlight">' + word + '</span>')
            '''
        else:
            page_number = request.GET.get('page_number');
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                return HttpResponseBadRequest()
            return HttpResponse(json.dumps(page_objects), content_type="application/json")
    return render_to_response('project_template/index.html',{'listing_url':search, 'orig_listing': orig_listing,'output': page_objects,'magic_url': request.get_full_path()})
