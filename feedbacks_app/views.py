from django.shortcuts import render
from tablib import Dataset
from .resources import *

def feedback(request):
    #loading data
    feedback_resource = FeedbacksResource()
    dataset = Dataset()
    feedback_resource.import_data(dataset, data = open("Feedbacks.csv"), encoding = 'utf-8')
    return render(request,'feedback.html',{})
