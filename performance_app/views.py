from django.shortcuts import render

def performance(request):
    return render(request,'performance.html',{})
