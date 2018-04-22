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

class Recommendations:

    def __init__(self):
        self.category_set =[]
        self.categoryList = []
        self.subCategoryList = []
        self.productset = []
        self.final_score={}
        self.recommendationList = []
        self.sellerSubCategoryList = []

    def template(self):
        self.search_category()
        self.search_sellerSubCategory()
        self.search_subcategory()
        self.search_products()
        self.calculate_score()
        heapobj = self.initialize_heap()
        self.maintain_heap(heapobj)
        self.checkIfSellerProductIsTrending(heapobj)

    def search_category(self):
        self.category_set = ProductMain.objects.all().filter(
                         sid='ank202'
                         ).values(
                         'sub_cid__cname'
                         ).distinct()
        for category in self.category_set:
            for key,category_name in category.items():
                self.categoryList.append(category_name)

    def search_sellerSubCategory(self):
        Subcategory = ProductMain.objects.all().filter(
                         sid='ank202'
                         ).values(
                         'sub_cid'
                         ).distinct()
        
        for sub_cat in Subcategory:
            for key,sub_cid in sub_cat.items():
                self.sellerSubCategoryList.append(sub_cid)

    def search_subcategory(self):
        for subcategory in self.categoryList:
            q = Category.objects.all().filter(cname=subcategory)
            for value in q:
                self.subCategoryList.append(value.id)

    def search_products(self):
        self.productset = ProductMain.objects.all(
                                ).filter(
                                sub_cid__in = self.subCategoryList).values(
                                'id','sub_cid','prod_count' ,'sub_cid__subCategoryCount','launch_date')
        

    def calculate_score(self):
        for products in self.productset:
            prod_score = self.calcProductScore(products)
            category_score = self.calcCategoryScore(products)
            date_score = self.calcDateScore(products)
            total_Score = prod_score + category_score + date_score
            ProductMain.objects.all().filter(id=products['id']).update(score=total_Score)
            self.final_score[products['id']] = total_Score
    
    def calcProductScore(self,products):
        count = products['prod_count']
        score = 0.5 * count
        return score

    def calcCategoryScore(self,products):
        count = products['sub_cid__subCategoryCount']
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
        seller_product_list = ProductMain.objects.all().filter(sid = 'ank202').values('id')
        for productid_score in heapObj.heap:
            for seller_product in seller_product_list:
                if productid_score[0] == seller_product :
                    self.sellerProductIsTrending(productid_score)
                    print ('his product','\n')
                else:
                    self.sellerProductIsNotTrending(productid_score)    
                    break

    def sellerProductIsTrending(self,productid_score):
        '''recommendationString = 'Keep ',trending_subcat_name, 'sub category also for increasing sales.','\n'
        self.recommendationList.append(recommendationString)'''
        pass

    def sellerProductIsNotTrending(self,productid_score):
        trendingProductObj = ProductMain.objects.all().filter(id = productid_score[0])
        category = trendingProductObj.values('sub_cid__cname')
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
    #recommendationList = []
    obj = Recommendations()
    obj.template()
    return render(request,'recommendation.html',{})