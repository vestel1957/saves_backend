from os import name
from django.urls import path
from .views import *

from login import views

urlpatterns = [  
  # clientes #######################################
    path('clientes_crear', clientes_crear, name='clientes_crear'),  
    path('clientes_listar', clientes_listar, name='clientes_listar'), 
    path('clientes_editar/<int:pk>', clientes_editar, name='clientes_editar'),  
    path('clientes_borrar/<int:pk>', clientes_borrar, name='clientes_borrar'),  
    # clientes #######################################

    # grupo_clientes #######################################
    path('grupo_clientes_crear', grupo_clientes_crear, name='grupo_clientes_crear'),  
    path('grupo_clientes_listar', grupo_clientes_listar, name='grupo_clientes_listar'), 
    path('grupo_clientes_editar/<int:pk>', grupo_clientes_editar, name='grupo_clientes_editar'),  
    path('grupo_clientes_borrar/<int:pk>', grupo_clientes_borrar, name='grupo_clientes_borrar'),  
    # grupo_clientes #######################################
]