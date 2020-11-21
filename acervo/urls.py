from django.urls import path 
from . import views_obra
from . import views_editora

urlpatterns = [
    path('', views_obra.obra_list, name='obra_list'),
    path('acervo/', views_obra.obra_list, name='obra_list'),
    path('acervo/obra/', views_obra.obra_redirect, name='obra_redirect'),
    path('acervo/obra/add/', views_obra.obra_add, name='add_Obra'),
    path('acervo/obra/<str:obra_id>/', views_obra.obra_detail, name='obra_detail'),
    path('acervo/obra/edit/<str:obra_id>/', views_obra.obra_edit, name='obra_edit'),
    path('acervo/obra/delete/<str:obra_id>/', views_obra.obra_delete, name='obra_delete'),

    path('editora/', views_editora.editora_list, name='editora_list'),
    path('editora/add/', views_editora.editora_add, name='add_Editora'),
    path('editora/<str:editora_id>/', views_editora.editora_detail, name='editora_detail'),
]