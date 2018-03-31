from django.shortcuts import render
from tablib import Dataset
from .resources import *

def login(request):
    #loading data
    productMain_resource = ProductMainResource()
    dataset = Dataset()
    productMain_resource.import_data(dataset, data = open("productMain.csv"), encoding = 'utf-8')

    category_resource = CategoryResource()
    category_resource.import_data(dataset, data = open("Category2.csv"),encoding='utf-8')
    return render(request,'login.html',{})

def home(request):
    return render(request,'home.html',{})

def profile(request):
    return render(request,'profile.html',{})