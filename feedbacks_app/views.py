from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType,Integer, Text, Date,Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch,helpers
from . import models
from django.utils import formats
from datetime import datetime
from dashboard.models import Products
from django.shortcuts import render
from tablib import Dataset
from performance_app.feedbacks import *
from .models import *
from .search import *
from .resources import *
import re
import nltk
from nltk.corpus import wordnet
connections.create_connection()

def feedback_load_data():
    feedbacks_resource = FeedbackResource()
    dataset = Dataset()
    feedbacks_resource.import_data(dataset, data = open("Feedback.csv"), encoding = 'utf-8')

def all_seller_products(seller_products,current_sellerid):
    seller_pid = Products.objects.all().filter(sid=current_sellerid).values('id')
    for sellerpid in seller_pid:
        for key,productid in sellerpid.items():
            seller_products[productid] = productid

class SearchFeedbacks:

    def filterAccordingToDate(self,documents,request):
        fromDate = (request.GET['from_date'])
        toDate = (request.GET['to_date'])
        filteredDocuments = documents.filter('range',feedback_date = {'gte': fromDate , 'lte': toDate})
        return filteredDocuments

    def filterAccordingToRating(self,documents,request):
        rating_points = request.GET['rating']
        filteredDocuments = documents.filter('term',rating = rating_points)
        return filteredDocuments

    def filterAccordingToProduct(self,documents,request):
        product_id = request.GET['product']
        filteredDocuments = documents.filter('match',product_id = product_id )
        return filteredDocuments

    def filterAccordingToKeywords(self,documents,request):
        keyword = request.GET['keyword']
        synonyms = []
        for syn in wordnet.synsets(keyword):
            for l in syn.lemmas():
                synonyms.append(l.name())
        #print(synonyms)
        filteredDocuments = documents.filter({"terms": {"feedback":synonyms} })
        return filteredDocuments

    def filterAccordingToNegativeFeedbacks(self,documents,request):
        PolarityObj = polarity()
        feedbacks_date = []
        for doc in documents.scan():
            IsNegative = PolarityObj.negative_feedbacks(doc.feedback)
            if IsNegative == True:
                feedbacks_date.append(doc.feedback_date)
        filteredDocuments = documents.filter('terms',feedback_date = feedbacks_date)
        return filteredDocuments

    def filterAccordingToPositiveFeedbacks(self,documents,request):
        PolarityObj = polarity()
        feedbacks_date = []
        for doc in documents.scan():
            IsPositive = PolarityObj.positive_feedbacks(doc.feedback)
            if IsPositive == True:
                feedbacks_date.append(doc.feedback_date)
        filteredDocuments = documents.filter('terms',feedback_date=feedbacks_date)
        return filteredDocuments

    def create_filtered_result_dictionary(self,documents,filtered_result):
        result = documents.execute()
        for res in documents.scan():
            filtered_result[res.id] = (res.id,res.feedback_date,res.feedback)
        return filtered_result

def main(request):
    current_sellerid = request.user.username
    bulk_indexing(current_sellerid)
    feedback_load_data()
    seller_products = {}
    all_seller_products(seller_products,current_sellerid)
    SearchObj = SearchFeedbacks()
    filtered_result = {}
    checkFilterToApply = { SearchObj.filterAccordingToDate : 0,
                   SearchObj.filterAccordingToRating : 0,
                   SearchObj.filterAccordingToProduct : 0,
                   SearchObj.filterAccordingToKeywords : 0,
                   SearchObj.filterAccordingToPositiveFeedbacks : 0,
                   SearchObj.filterAccordingToNegativeFeedbacks: 0 }

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
        if 'keyword' in request.GET:
            if request.GET['keyword']:
                checkFilterToApply[SearchObj.filterAccordingToKeywords] = 1
        if 'Positive Feedbacks' in request.GET:
            if request.GET['Positive Feedbacks']:
                checkFilterToApply[SearchObj.filterAccordingToPositiveFeedbacks] = 1
        if 'Negative Feedbacks' in request.GET:
            if request.GET['Negative Feedbacks']:
                checkFilterToApply[SearchObj.filterAccordingToNegativeFeedbacks] = 1  
        
        documents = Search()

        for filter,value in checkFilterToApply.items():
            if value == 1 :
                documents = filter(documents,request)
        filtered_result = SearchObj.create_filtered_result_dictionary(documents,filtered_result)
    else:
        documents = Search()
        filtered_result = {}
        filtered_result = SearchObj.create_filtered_result_dictionary(documents,filtered_result)
    return render(request,'feedback.html',{'filtered_result':filtered_result, 'seller_products':seller_products})