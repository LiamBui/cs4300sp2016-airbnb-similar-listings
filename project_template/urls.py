from django.conf.urls import url
import csv
from . import views

app_name = 'pt'
urlpatterns = [
    url(r'^$', views.index, name='index')
]

nyc = []
sf = []

with open('data/filtered_nyc_listings.csv') as f:
   	nyc = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        
with open('data/filtered_sf_listings.csv') as f:
	sf = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
