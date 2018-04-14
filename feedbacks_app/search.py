from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType,Integer, Text, Date,Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch,helpers
from . import models
from datetime import datetime
from dashboard.models import ProductMain
connections.create_connection()

class Feedbacks_Index(DocType):
    id = Text()
    pid_seller = Text()
    feedbackdate = Date()
    rating_points = Integer()
    feedback_entered = Text()

    class Meta:
        index = 'feedbacks-index'

def bulk_indexing():
    Feedbacks_Index.init()
    es = Elasticsearch()
    productidlist = []
    sellerPid = ProductMain.objects.all().filter(sid='ank202').values('id')
    for sellerpid in sellerPid:
        for key,productid in sellerpid.items():
            productidlist.append(productid)
    bulk(client=es, actions=(b.indexing() for b in models.Feedbacks_table.objects.filter(pid_seller__in = productidlist).iterator()))

'''def search_pid(pid_seller):
    p = h.filter('match',pid_seller=pid_seller)
    response = p.execute()
    response_dict = {}
    for h in p.scan():
        response_dict[h.id] = h.feedback_entered
    return response_dict

def search_rating(rating_points):
    s = Search().filter('term',rating_points=rating_points)
    response = s.execute()
    response_dict = {}
    for h in s.scan():
        response_dict[h.id] = h.feedback_entered
    return response_dict

def search_date(startdate,enddate):
    s = Search().filter('range',feedbackdate = {'gte': startdate , 'lte': enddate})
    response = s.execute()
    response_dict = {}
    for h in s.scan():
        response_dict[h.id] = [h.feedbackdate, h.feedback_entered]
    return response_dict'''

'''def search_many(startdate,enddate,rating_points,pid_seller):
    p = Search().filter('range',feedbackdate = {'gte': startdate , 'lte': enddate}).filter('term',rating_points=rating_points).filter('match',pid_seller=pid_seller)
    response = p.execute()
    response_dict = {}
    for h in p.scan():
        response_dict[h.id] = h.feedback_entered
    return response_dict'''