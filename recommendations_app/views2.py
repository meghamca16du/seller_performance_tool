from django.shortcuts import render
from math import ceil
from heapq import heappush, heappop, heapify
from django.db.models import Count
from datetime import datetime, date
from django.utils import formats
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
        if l<self.heapsize and self.heap[i][1]>self.heap[l][1]:
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
        self.seller_category_related_subcategory = []
        self.seller_category_related_products = []
        self.final_score = {}
        self.recommendation_list =[]

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
        self.seller_products = Products.objects.all().filter(sid=self.current_sellerid).values('id')

    def search_seller_subcategory(self):
        subcategory = Products.objects.all().filter(id__in=self.seller_product).distinct().values('subcategory_id')
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
        self.sellers_category_related_products = Products.objects.all().filter(
            subcategory_id__in = self.sellers_category_related_subcategory
            ).values('id', 'product_name', 'subcategory_id' , 'product_sale_count' ,
             'subcategory_id__subcategory_sale_count', 'price', 'launch_date' , 'score' , 'inventory')        

    def calculate_score(self):
        for products in self.sellers_category_related_products:
            prod_score = self.calcProductScore(products)
            category_score = self.calcCategoryScore(products)
            date_score = self.calcDateScore(products)
            total_Score = prod_score + category_score + date_score
            Products.objects.all().filter(id=products['id']).update(score=total_Score)
            self.final_score[products['id']] = total_Score
    
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

    def check_inventory():
        low_inventory_products = Products.objects.all().filter(
                                    sid=self.current_sellerid).filter(
                                    inventory__lte=10).values('product_name')
        recommendation = "Inventory level is very low for : \n                  "
        for products in low_inventory_products:
            recommendation + = products.product_name," \n "
        recommendation + = "   to cater Market Demand. Restock "    
        recommendation_list.append(recommendation)

    def initialize_heap(self):
        count = 0
        listOf5products = []
        for productid_score in self.final_score.items():
            if (count != 5):
                listOf5products.append(productid_score)
                count+= 1
            else:
                break
        heapObj = MinHeap(listOf5products)
        heapObj.buildHeap()
        return heapObj
      
    def maintain_heap(self,heapObj):
        for productid_score in self.final_score.items():
            minTrendingProductInHeap = heapObj.heap[0]
            if minTrendingProductInHeap[1] < productid_score[1] :
                heapObj.heap[0] = productid_score
                heapObj.minHeapify(0)

    def checkIfSellerProductIsTrending(self,heapObj):  
        for productid_score in heapObj.heap:
            for seller_product in self.seller_products:
                if not productid_score[0] == seller_product :
                    self.sellerProductIsNotTrending(productid_score)
                    break

    def sellerProductIsNotTrending(self,productid_score):
        trendingProductObj = Products.objects.all().filter(id = productid_score[0])
        category = trendingProductObj.values('sub_categoryid__cname')
        subcategory = trendingProductObj.values('sub_cid')
        trendingProductPrice = trendingProductObj.values('price')
        for cat in category:
            for key,value in cat.items():
                trending_category_name = value   
        for subcat in subcategory:
            for key,value in subcat.items():
                trending_subcat_id = value 
        for trendProductPrice in trendingProductPrice :
            for product,price in trendProductPrice.items() : 
                trend_product_price=price
        if trending_subcat_id in self.sellerSubCategoryList :
            seller_price = ProductMain.objects.filter(
                                sid='ank202'
                                ).filter(
                                sub_cid=trending_subcat_id
                                ).values(
                                'price')
            for sellerprice in seller_price :
                for key,price in sellerprice.items() :
                    sellerPrice=price

            if trend_product_price < sellerPrice:
                recommendationString = 'Decrease your price. Or you can add a deal on this product.'
                self.recommendationList.append(recommendationString)
        else:
            recommendationString = 'Keep ',value, 'category also for increasing sales.'
            self.recommendationList.append(recommendationString)

def main(request):
    current_sellerid = request.user.username
    obj = ProvideTrendRecommendations(current_sellerid)
    obj.template()
    return render(request,'recommendation.html',{})