from django.urls import path
from .views import *
urlpatterns=[
    path('bolimlar/', BolimlarVeiw.as_view(), name='bolimlar'),
    path('mahsulotlar/', MahsulotlarView.as_view(), name='mahsulotlar'),
    path('mijozlar/', MijozView.as_view(), name='mijozlar'),
    path('mahsulot_tahrirlash/<int:id>/', MahsulotTahrirlashView.as_view(), name='mahsulot_tahrirlash'),
    path('mahsulot_ochirish/<int:pk>/', mahsulot_ochirish, name='mahsulot_ochirish'),
    path('mijoz_tahrirlash/<int:pk>/', MijozlarniTahrirlashView.as_view(), name='mijoz_tahrirlash'),
    path('mijoz_ochirish/<int:pk>/', mijoz_ochirish, name='mijoz_ochirish'),
]