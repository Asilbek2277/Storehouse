from django.urls import path

from .views import *

urlpatterns=[
    path('logout/', LoginView.as_view(), name='logout')
]