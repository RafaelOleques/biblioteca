from django.urls import path 
from . import views_obra
from . import views_editora
from . import views_genero
from . import views_palavraChave
from . import views_autor
from . import views_subBiblioteca
from . import views_exemplar
from . import views_usuario

urlpatterns = [

    path('', views_usuario.usuario_login, name='usuario_login'),
    path('login/', views_usuario.usuario_login, name='usuario_login'),
    path('login/new/', views_usuario.usuario_add, name='usuario_add'),

    path('usuario/', views_usuario.usuario_detail, name='usuario_detail'),

    #path('', views_obra.obra_list, name='obra_list'),
    path('acervo/', views_obra.obra_list, name='obra_list'),
    path('acervo/obra/', views_obra.obra_redirect, name='obra_redirect'),
    path('acervo/obra/add/', views_obra.obra_add, name='add_Obra'),
    path('acervo/obra/<str:obra_id>/', views_obra.obra_detail, name='obra_detail'),
    path('acervo/obra/edit/<str:obra_id>/', views_obra.obra_edit, name='obra_edit'),
    path('acervo/obra/delete/<str:obra_id>/', views_obra.obra_delete, name='obra_delete'),

    path('acervo/obra/<str:obra_id>/exemplar/add/', views_exemplar.exemplar_add, name='exemplar_add'),
    path('acervo/obra/<str:obra_id>/exemplar/<str:sequencia>/reserva/', views_exemplar.exemplar_reserva, name='exemplar_reserva'),
    path('acervo/obra/<str:obra_id>/exemplar/<str:sequencia>/devolve/', views_exemplar.exemplar_devolucao, name='exemplar_devolucao'),

    path('editora/', views_editora.editora_list, name='editora_list'),
    path('editora/add/', views_editora.editora_add, name='add_Editora'),
    path('editora/<str:editora_id>/', views_editora.editora_detail, name='editora_detail'),
    path('editora/edit/<str:editora_id>/', views_editora.editora_edit, name='editora_edit'),
    path('editora/delete/<str:editora_id>/', views_editora.editora_delete, name='editora_delete'),

    path('genero/', views_genero.genero_list, name='genero_list'),
    path('genero/add/', views_genero.genero_add, name='add_Genero'),
    path('genero/<str:genero_id>/', views_genero.genero_detail, name='genero_detail'),
    path('genero/edit/<str:genero_id>/', views_genero.genero_edit, name='genero_edit'),
    path('genero/delete/<str:genero_id>/', views_genero.genero_delete, name='genero_delete'),

    path('palavraChave/', views_palavraChave.palavraChave_list, name='palavraChave_list'),
    path('palavraChave/add/', views_palavraChave.palavraChave_add, name='add_Palavras_Chaves'),
    path('palavraChave/<str:palavraChave_id>/', views_palavraChave.palavraChave_detail, name='palavraChave_detail'),
    path('palavraChave/edit/<str:palavraChave_id>/', views_palavraChave.palavraChave_edit, name='palavraChave_edit'),
    path('palavraChave/delete/<str:palavraChave_id>/', views_palavraChave.palavraChave_delete, name='palavraChave_delete'),

    path('autor/', views_autor.autor_list, name='autor_list'),
    path('autor/add/', views_autor.autor_add, name='add_Autor'),
    path('autor/<str:autor_id>/', views_autor.autor_detail, name='autor_detail'),
    path('autor/edit/<str:autor_id>/', views_autor.autor_edit, name='autor_edit'),
    path('autor/delete/<str:autor_id>/', views_autor.autor_delete, name='autor_delete'),
    
    path('subBiblioteca/', views_subBiblioteca.subBiblioteca_list, name='subBiblioteca_list'),
    path('subBiblioteca/add/', views_subBiblioteca.subBiblioteca_add, name='add_Sub_Biblioteca'),
    path('subBiblioteca/<str:subBiblioteca_id>/', views_subBiblioteca.subBiblioteca_detail, name='subBiblioteca_detail'),
    path('subBiblioteca/edit/<str:subBiblioteca_id>/', views_subBiblioteca.subBiblioteca_edit, name='subBiblioteca_edit'),
    path('subBiblioteca/delete/<str:subBiblioteca_id>/', views_subBiblioteca.subBiblioteca_delete, name='subBiblioteca_delete'),
]