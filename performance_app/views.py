from django.shortcuts import render
from dashboard.models import *
from django.db.models import Count

def performance(request):
    cancelled = OrderDetails.objects.filter(status = 'C').count()
    total = OrderDetails.objects.filter(sid = 'ank202').count()
    perc = (cancelled/total)*100
    return render(request,'performance.html',{'perc':perc})
