"""seller_perf_tool URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard import views
from django.contrib.auth import views as auth_views
from performance_app import views as perf_views
from feedbacks_app import views as feed_views
from recommendations_app import views as rec_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.login,{'template_name':'login.html'},name='login'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('home/performance/',perf_views.main,name='main'),
    path('home/feedback/',feed_views.main,name='main'),
    path('home/recommendations/',rec_views.main,name='main'),

    path('logout/',auth_views.logout,{'next_page':'/login'},name='logout'),
]