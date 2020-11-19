from django.urls import path 
from . import views_obra

urlpatterns = [
    path('', views_obra.obra_list, name='obra_list'),
    path('acervo/', views_obra.obra_list, name='obra_list'),
    path('acervo/obra/', views_obra.obra_redirect, name='obra_redirect'),
    path('acervo/obra/add/', views_obra.obra_add, name='add'),
    path('acervo/obra/<str:obra_titulo>/', views_obra.obra_detail, name='obra_detail'),
]