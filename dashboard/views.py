from django.shortcuts import render
from tablib import Dataset
from .resources import *
from performance_app.views import *

def login(request):
    #loading data
    productMain_resource = ProductMainResource()
    dataset = Dataset()
    productMain_resource.import_data(dataset, data = open("Products.csv"), encoding = 'utf-8')

    category_resource = CategoryResource()
    category_resource.import_data(dataset, data = open("Category2.csv"),encoding='utf-8')
    return render(request,'login.html',{})

    #new data
    seller_resource = SellerResource()
    dataset = Dataset()
    seller_resource.import_data(dataset, data = open("Seller.csv"), encoding = 'utf-8')

    buyer_resource = BuyerResource()
    dataset = Dataset()
    buyer_resource.import_data(dataset, data = open("Buyer.csv"), encoding = 'utf-8')

    category_resource = CategoriesResource()
    dataset = Dataset()
    category_resource.import_data(dataset, data = open("Category.csv"), encoding = 'utf-8')

    subcategories_resource = SubcategoriesResource()
    dataset = Dataset()
    subcategories_resource.import_data(dataset, data = open("subcategories.csv"), encoding = 'utf-8')

    products_resource = ProductsResource()
    dataset = Dataset()
    products_resource.import_data(dataset, data = open("Products.csv"), encoding = 'utf-8')
    return render(request,'login.html',{})

def home(request):
    print(request.user)
    print(ReturnValueForDashboard())
    return render(request,'home.html',{})

def profile(request):
    return render(request,'profile.html',{})