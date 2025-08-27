from django.urls import path
from . import views 


urlpatterns =[
    path('', views.home),
    path('sobre/', views.contato),
    path('contato/', views.contato),
    path('base/', views.base),
]