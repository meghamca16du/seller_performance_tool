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
        filteredDocuments = documents.filter('range',feedbackdate = {'gte': fromDate , 'lte': toDate})
        return filteredDocuments

    def filterAccordingToRating(self,documents,request):
        rating_points = request.GET['rating']
        filteredDocuments = documents.filter('term',rating_points = rating_points)
        return filteredDocuments

    def filterAccordingToProduct(self,documents,request):
        product_id = request.GET['product']
        filteredDocuments = documents.filter('match',pid_seller = product_id )
        return filteredDocuments

    def filterAccordingToKeywords(self,documents,request):
        keyword = request.GET['keyword']
        synonyms = []
        for syn in wordnet.synsets(keyword):
            for l in syn.lemmas():
                synonyms.append(l.name())
        #print(synonyms)
        filteredDocuments = documents.filter({"terms": {"feedback_entered":synonyms} })
        return filteredDocuments

    def filterAccordingToNegativeFeedbacks(self,documents,request):
        PolarityObj = polarity()
        feedbacks_id = []
        product_id = []
        rate = []
        for doc in documents.scan():
            IsNegative = PolarityObj.negative_feedbacks(doc.feedback_entered)
            if IsNegative == True:
                feedbacks_id.append(doc.id)
                product_id.append(doc.pid_seller)
                rate.append(doc.feedbackdate)
        #print(rate)
        #filteredDocuments = documents.filter('terms',feedback_date= rate)
        #filteredDocuments = documents.filter('terms',rating_points = [3,2])
        filteredDocuments = documents.filter('term',id='F08')

        result = filteredDocuments.execute()
        filtered_result = {}
        for res in filteredDocuments.scan():
            filtered_result[res.id] = (res.id,res.feedbackdate,res.feedback_entered)
        #print(filtered_result)

        return filteredDocuments

        '''polarity_obj=polarity()
        fid_list=[]
        for hit in documents.scan():
            if polarity_obj.negative_feedbacks(hit.feedback_entered):
                fid_list.append(hit.id)
        search=documents.filter('terms',id=fid_list)
        filtered_result={}
        result = documents.execute()
        for res in documents.scan():
            filtered_result[res.id] = (res.id,res.feedbackdate,res.feedback_entered)
            print ('\n \n', res.id)
        print ('helooooo   ',filtered_result,'\n \n')
        return search'''

    def filterAccordingToPositiveFeedbacks(self,documents,request):
        PolarityObj = polarity()
        feedbacks_id = []
        for doc in documents.scan():
            IsPositive = PolarityObj.positive_feedbacks(doc.feedback_entered)
            if IsPositive == True:
                feedbacks_id.append(doc.id)
        filteredDocuments = documents.filter({"terms": {"id":feedbacks_id} })
        return filteredDocuments

    def create_filtered_result_dictionary(self,documents,filtered_result):
        result = documents.execute()
        for res in documents.scan():
            filtered_result[res.id] = (res.id,res.feedbackdate,res.feedback_entered)
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



'''
from django.shortcuts import render
from tablib import Dataset
from .resources import *
from .models import *
from .search import *
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from performance_app.feedbacks import polarity
from nltk.corpus import wordnet

class SearchFeedbacks:

    def rating_filter(self,search,request):
        search=search.filter('term',rating_points=request.GET['rating'])
        return search

    def date_filter(self,search,request):
        from_date=request.GET['from_date']
        to_date=request.GET['to_date']
        search=search.filter('range',feedbackdate={'from':from_date,'to':to_date})
        return search

    def product_filter(self,search,request):
        search=search.filter('match',pid_seller=request.GET['product'])
        return search

    def positive_feedbacks_filter(self,search,request):
        polarity_obj=polarity()
        fid_list=[]
        for hit in search.scan():
            if polarity_obj.check_positive_feedbacks(hit.feedback):
                fid_list.append(hit.id)
        search=search.filter('terms',id=fid_list)
        return search

    def negative_feedbacks_filter(self,search,request):
        polarity_obj=polarity()
        fid_list=[]
        for hit in search.scan():
            if polarity_obj.check_negative_feedbacks(hit.feedback):
                fid_list.append(hit.id)
        search=search.filter('terms',id=fid_list)
        return search
            
    def keyword_filter(elf,search,request):
        keyword = request.GET['keyword']
        synonyms = []
        for syn in wordnet.synsets(keyword):
            for l in syn.lemmas():
                synonyms.append(l.name())
        search = search.filter('terms',feedback=synonyms)
        return search       


def create_dict(search):

    filtered_result={}
    response=search.execute()
    for hit in search.scan():
        filtered_result[hit.id]=(hit.feedbackdate,hit.id,hit.feedback_entered)
    #print('Total %d hits found.' % response.hits.total)
    return filtered_result


def search_pid(current_sellerid):
    seller_pid_set = Products.objects.all().filter(sid=current_sellerid).values('id')
    product_id_List=[]
    for products_dict in seller_pid_set:
        for id,pid in products_dict.items():
           product_id_List.append(pid)
    return product_id_List


def main(request):

    #load_data()
    current_sellerid = request.user.username
    #bulk_indexing(current_sellerid)
    obj=SearchFeedbacks()
    filter_dict={ obj.date_filter : 0 , obj.rating_filter : 0 , obj.product_filter : 0 , 
    obj.positive_feedbacks_filter : 0 , obj.negative_feedbacks_filter : 0 ,obj.keyword_filter : 0 }
    
    if request.method == 'GET':

        if 'from_date' in request.GET and 'to_date' in request.GET:
            if request.GET['from_date'] and request.GET['to_date']:
                filter_dict[obj.date_filter]=1

        if 'rating' in request.GET:
            if request.GET['rating'] :
                filter_dict[obj.rating_filter]=1

        if 'product' in request.GET:
            if request.GET['product'] :
                filter_dict[obj.product_filter]=1
                
        if 'positive_feedbacks' in request.GET:
            if request.GET['positive_feedbacks']:
                filter_dict[obj.positive_feedbacks_filter]=1

        if 'negative_feedbacks' in request.GET:
            if request.GET['negative_feedbacks']:
                filter_dict[obj.negative_feedbacks_filter]=1
        
        if 'keyword' in request.GET:
            if request.GET['keyword']:
                filter_dict[obj.keyword_filter]=1


    search=Search()
    seller_products=search_pid(current_sellerid)
    for filter,value in filter_dict.items():
        if value==1:
            search=filter(search,request)
    filtered_result=create_dict(search)
    return render(request,'feedback.html',{'filtered_result' : filtered_result , 'seller_products' : seller_products})
'''