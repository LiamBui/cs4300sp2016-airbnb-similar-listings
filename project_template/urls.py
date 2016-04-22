from django.conf.urls import url

from . import views
import csv
import urllib2

nyc_url = 'https://s3.amazonaws.com/similairbnb/filtered_nyc_listings.csv'
sf_url = 'https://s3.amazonaws.com/similairbnb/filtered_sf_listings.csv'

nyc = [{k: v for k, v in row.items()} for row in csv.DictReader(urllib2.urlopen(nyc_url), skipinitialspace=True)]
sf = [{k: v for k, v in row.items()} for row in csv.DictReader(urllib2.urlopen(sf_url), skipinitialspace=True)]



app_name = 'pt'
urlpatterns = [
    url(r'^$', views.index, name='index')
]



# with open('data/filtered_nyc_listings.csv') as f:
#    	nyc = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        
# with open('data/filtered_sf_listings.csv') as f:
# 	sf = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
