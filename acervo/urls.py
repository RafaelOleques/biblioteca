from django.urls import path 
from . import views

urlpatterns = [
    path('', views.obra_list, name='obra_list'),
     path('acervo/', views.obra_list, name='obra_list'),
    #path('acervo/obra/<int:pk>/', views.obra_detail, name='obra_detail'),
    path('acervo/obra/add/', views.obra_add, name='add'),
]