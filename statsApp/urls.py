from django.urls import path
from .views import *
urlpatterns=[
    path('stats/', StatsView.as_view(), name='stats')

]