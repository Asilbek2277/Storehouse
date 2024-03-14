from django.urls import path
from .views import *
urlpatterns=[
    path('stats/', StatsView.as_view(), name='stats'),
    path('ochirish/<int:pk>/', SotuvDelete.as_view(), name='ochirish'),
    path('tahrirlash/<int:pk>/', Stats_TahrirlashView.as_view(), name='tahrirlash'),

]