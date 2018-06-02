from django.shortcuts import render
from math import ceil
from heapq import heappush, heappop, heapify
from django.db.models import Count
from datetime import datetime, date
from django.utils import formats
import operator

from dashboard.models import *
class MinHeap:

    def __init__(self, listOf5products):
        self.heap = listOf5products
        self.heapsize = 5

    def left(self,i):
        return 2*i + 1

    def right(self,i):
        return 2*i + 2

    def buildHeap(self):
        for i in range (ceil(self.heapsize/2))[::-1]:
            self.minHeapify(i)

    def minHeapify(self,i):
        l = self.left(i)
        r = self.right(i)
        if l < self.heapsize and self.heap[i][1] > self.heap[l][1]:
            smallest = l
        else:
            smallest = i
        if r < self.heapsize and self.heap[smallest][1] > self.heap[r][1] :
            smallest = r
        if smallest != i:
            self.heap[i] , self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.minHeapify(smallest)

    def printHeap(self):
        for h in self.heap:
            print (h[0] , " " , h[1])

class ProvideTrendRecommendations:

    def __init__(self,current_sellerid):
        self.current_sellerid = current_sellerid
        self.seller_category = []
        self.seller_subcategory = []
        self.seller_products = []
        self.seller_products_name=[]
        self.seller_category_related_subcategory = []
        self.seller_category_related_products = []
        self.final_score = {}
        self.recommendation_list = []
        self.recommend_inventory = []
        self.recommend_product = []
        self.recommend_category = []
        self.recommend_lowerprice = []
        self.recommend_othermeasures = []
        self.new_final={}

    def template(self):
        self.search_seller_products()
        self.search_seller_subcategory()
        self.search_seller_category()
        self.search_seller_category_related_subcategory()
        self.search_seller_category_related_products()
        self.calculate_score()
        self.check_inventory()
        heapobj = self.initialize_heap()
        self.maintain_heap(heapobj)
        self.checkIfSellerProductIsTrending(heapobj)

    def search_seller_products(self):
        sellerproducts = Products.objects.all().filter(sid=self.current_sellerid)
        for products in sellerproducts:
            self.seller_products.append(products.id)
            self.seller_products_name.append(products.product_name)

    def search_seller_subcategory(self):
        subcategory = Products.objects.all().filter(id__in=self.seller_products).distinct().values('subcategory_id')
        for sub_cat in subcategory:
            for key,subcategory_id in sub_cat.items():
                self.seller_subcategory.append(subcategory_id)

    def search_seller_category(self):
        category_set = Products.objects.all().filter(sid=self.current_sellerid).values('subcategory_id__category_id').distinct()
        for category in category_set:
            for key,category_id in category.items():
                self.seller_category.append(category_id)
            
    def search_seller_category_related_subcategory(self):
        q = Subcategories.objects.all().filter(category_id__in = self.seller_category)
        for subcategory in q:
            self.seller_category_related_subcategory.append(subcategory.id)

    def search_seller_category_related_products(self):
        self.seller_category_related_products = Products.objects.all().filter(
            subcategory_id__in = self.seller_category_related_subcategory
            ).values('id', 'product_name', 'product_sale_count' , 'subcategory_id__category_id','subcategory_id',
                'subcategory_id__subcategory_name',
             'subcategory_id__subcategory_sale_count', 'price', 'launch_date' , 'score' , 'inventory')       

    def calculate_score(self):  
        for products in self.seller_category_related_products:
            prod_score = self.calcProductScore(products)
            category_score = self.calcCategoryScore(products)
            date_score = self.calcDateScore(products)
            total_Score = prod_score + category_score + date_score
            Products.objects.all().filter(id=products['id']).update(score=total_Score)
            self.final_score[products['id']] = total_Score
        final_score2 = sorted(self.final_score.items(), key=operator.itemgetter(1))
        self.final_score = dict((x,y) for x,y in final_score2)
    
    def calcProductScore(self,products):
        count = products['product_sale_count']
        score = 0.5 * count
        return score

    def calcCategoryScore(self,products):
        count = products['subcategory_id__subcategory_sale_count']
        score = 0.3 * count
        return score

    def calcDateScore(self,products):
        launch_date = products['launch_date']
        present_datetime = datetime.now()
        present_date = present_datetime.date()
        days_difference = present_date - launch_date
        days = days_difference.days
        if days >= 0 and days < 5:
            score = 0.2*30
        elif days >= 5 and days < 10:
            score = 0.2*20
        elif days >= 10 and days < 15:
            score = 0.2*10
        else:
            score = 0
        return score

    def check_inventory(self):
        low_inventory_products = Products.objects.all().filter(
                                    sid=self.current_sellerid).filter(
                                    inventory__lt=10)
        recommendation = "Inventory level is very low for : "+ "\n"
        for products in low_inventory_products:
            recommendation = recommendation + products.product_name + " \n "
        recommendation  = recommendation + "  . Restock to cater Market Demand.  "  
        self.recommend_inventory.append(recommendation)
        self.recommendation_list.append(recommendation)

    def initialize_heap(self):
        count = 0
        product_list=[]
        for final_score in self.final_score.items():
            if (count != 5):
                product_list.append(final_score)
                count+= 1
            else:
                break
        heapObj=MinHeap(product_list)
        heapObj.buildHeap()
        #heapObj.printHeap()
        return heapObj
      
    def maintain_heap(self,heapObj):
        for productid_score in self.final_score.items():   
            min_trending_product=heapObj.heap[0]
            if min_trending_product[1] < productid_score[1]:
                heapObj.heap[0] = productid_score
                heapObj.minHeapify(0)
        #heapObj.printHeap()

    def checkIfSellerProductIsTrending(self,heapObj):  
        for productid_score in heapObj.heap:
            not_seller_product = True
            for seller_product in self.seller_products:
                if productid_score[0] == seller_product :
                    not_seller_product = False
                    break
            if  not_seller_product:
                self.sellerProductIsNotTrending(productid_score)

    def sellerProductIsNotTrending(self,productid_score):
        trendingProductObj = self.seller_category_related_products.filter(id=productid_score[0])

        for value in trendingProductObj:
            trending_product_name = value['product_name']
            trending_product_price = value['price']
            trending_product_subcategory = value['subcategory_id']
            trending_product_subcategory_name = value['subcategory_id__subcategory_name']
            trending_product_category = value['subcategory_id__category_id']

        if trending_product_name in self.seller_products_name:
            seller_product = Products.objects.all().filter(sid=self.current_sellerid).filter(product_name=trending_product_name)
            for product in seller_product:
                seller_product_price = product.price
            if seller_product_price > trend_product_price:
                recommendation = "As per analysis, your competitors are selling " + trending_product_name + " at a cheaper price than you and have better sales. You may reduce your price or add deals" +" for improved sales."
                self.recommend_lowerprice.append(recommendation)                          
            else:
                recommendation = "As per analysis, your competitors are selling " + trending_product_name + "and having better sales. Take necessary actions to improve sales of your product."
                self.recommend_othermeasures.append(recommendation)                    
        else: 
            if trending_product_subcategory in self.seller_subcategory:
                recommendation = trending_product_name + " is Trending. Add this product to your Product Range in order to "+"boost your sales and earn profit."
                self.recommend_product.append(recommendation)                    
            else:
                recommendation = trending_product_subcategory_name + " is Trending. Add this category to your category Range in order to "+"boost your sales and earn profit."
                self.recommend_category.append(recommendation)                    
        self.recommendation_list.append(recommendation)

def main(request):
    current_sellerid = request.user.username
    obj = ProvideTrendRecommendations(current_sellerid)
    obj.template()
    recommendations = obj.recommendation_list
    recommend_inventory = obj.recommend_inventory
    recommend_product = obj.recommend_product
    recommend_category = obj.recommend_category
    recommend_lowerprice = obj.recommend_lowerprice
    recommend_othermeasures = obj.recommend_othermeasures
    return render(request,'recommendation.html',{'recommendations':recommendations,'recommend_inventory':recommend_inventory,'recommend_product':recommend_product,'recommend_category':recommend_category,'recommend_lowerprice':recommend_lowerprice,'recommend_othermeasures':recommend_othermeasures})