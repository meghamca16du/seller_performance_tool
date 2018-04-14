from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType,Integer, Text, Date,Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch,helpers
from . import models
from django.utils import formats
from datetime import datetime
from dashboard.models import ProductMain
from django.shortcuts import render
from tablib import Dataset
from .models import *
from .search import *
from .resources import *
import re
connections.create_connection()

def feedback_load_data():
    feedback_resource = FeedbacksResource()
    dataset = Dataset()
    feedback_resource.import_data(dataset, data = open("Feedbacks.csv"), encoding = 'utf-8')

class SearchFeedbacks:

    def filterAccordingToDate(self,documents,request):
        fromDate = (request.GET['from_date'])
        toDate = (request.GET['to_date'])
        filteredDocuments = documents.filter('range',feedbackdate = {'gte': fromDate , 'lte': toDate})
        return filteredDocuments

    def filterAccordingToRating(self,documents,request):
        rating_points = request.GET['rating']
        filteredDocuments = documents.filter('term',rating_points=rating_points)
        return filteredDocuments

    def filterAccordingToProduct(self,documents,request):
        product_id = request.GET['product']
        filteredDocuments = documents.filter('match',pid_seller=product_id )
        return filteredDocuments

    def create_filtered_result_dictionary(self,documents,filtered_result):
        result = documents.execute()
        for res in documents.scan():
            filtered_result[res.id] = [res.id,res.feedbackdate,res.feedback_entered]
        return filtered_result 


def main(request):
    feedback_load_data()
    SearchObj = SearchFeedbacks()
    filtered_result = {}
    checkFilterToApply = {SearchObj.filterAccordingToDate : 0,
                   SearchObj.filterAccordingToRating : 0,
                   SearchObj.filterAccordingToProduct : 0}

    if request.method == "GET":
        if 'from_date' in request.GET and 'to_date' in request.GET:
            if request.GET['from_date'] and request.GET['to_date']:
                checkFilterToApply[SearchObj.filterAccordingToDate] = 1
        if 'rating' in request.GET:
            if request.GET['rating']:
                checkFilterToApply[SearchObj.filterAccordingToRating] = 1  
        if 'product' in request.GET:
            if request.GET['product']:
                checkFilterToApply[SearchObj.filterAccordingToProduct] = 1
        
        documents = Search()

        for filter,value in checkFilterToApply.items():
            if value == 1 :
                documents = filter(documents,request)

        filtered_result = SearchObj.create_filtered_result_dictionary(documents,filtered_result)
    else:
        documents = Search()
        filtered_result = {}
        filtered_result = SearchObj.create_filtered_result_dictionary(documents,filtered_result)

    return render(request,'feedback.html',{'filtered_result':filtered_result})
