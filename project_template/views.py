from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import numpy as np
from sklearn.metrics.pairwise import distance_metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib2
import csv

# Create your views here.
def index(request):
    output_list = ''
    output=''
    if request.GET.get('search'):
        headers = {"User-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
        search = request.GET.get('search')
        if (search.find('?') == -1):
            search_id = search[search.find('rooms/')+6:]
        else:
            search_id = search[search.find('rooms/')+6:search.find('?')]
        url = 'https://api.airbnb.com/v2/listings/' + search_id + '?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3'
        request = urllib2.Request(url, headers=headers)
        data = json.loads(urllib2.urlopen(request).read())
        input_description = data['listing']['description']
        output_list = find_similar(input_description)
        paginator = Paginator(output_list, 10)
        page = request.GET.get('page')
        try:
            output = paginator.page(page)
        except PageNotAnInteger:
            output = paginator.page(1)
        except EmptyPage:
            output = paginator.page(paginator.num_pages)
        return render_to_response('project_template/index.html', 
                              {'output': output,
                               'magic_url': request.get_full_path(),
                               })