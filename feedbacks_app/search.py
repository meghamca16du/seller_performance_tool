from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType,Integer, Text, Date,Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch,helpers
from . import models
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

def search_pid(pid_seller):
    p = Search().filter('match',pid_seller=pid_seller)
    response = p.execute()
    return response

def search_rating(rating_points):
    s = Search().filter('term',rating_points=rating_points)
    response = s.execute()
    return response

