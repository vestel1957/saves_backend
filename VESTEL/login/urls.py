from os import name
from django.urls import path
from .views import *

from login import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Ruta raíz redirige por nombre
    path('WSglLogin', WSglLogin, name='WSglLogin'),  # Ruta con nombre
    path('seleccion_sede', seleccion_sede, name='seleccion_sede'),  
    path('menu_principal', menu_principal, name='menu_principal'),  
    
    # usuarios #######################################
    path('WSgListarUsuario', WSgListarUsuario, name='WSgListarUsuario'),  
    path('WSgCrearUsuario', WSgCrearUsuario, name='WSgCrearUsuario'),  
    path('WSgActualizarUsuario/<int:pk>', WSgActualizarUsuario, name='WSgActualizarUsuario'),  
    path('WSgUsuariosBorrar/<int:pk>', WSgUsuariosBorrar, name='WSgUsuariosBorrar'),  
    # usuarios #######################################
    
    # modales #######################################
    path('modales_lista', modales_lista, name='modales_lista'),  
    path('modales_crear', modales_crear, name='modales_crear'),  
    path('modales_editar/<int:pk>', modales_editar, name='modales_editar'),  
    path('modales_borrar/<int:pk>', modales_borrar, name='modales_borrar'),  
    # modales #######################################
    
    # sedes #######################################
    path('sedes_lista', sedes_lista, name='sedes_lista'),  
    path('sedes_crear', sedes_crear, name='sedes_crear'),  
    path('sedes_editar/<int:pk>', sedes_editar, name='sedes_editar'),  
    path('sedes_borrar/<int:pk>', sedes_borrar, name='sedes_borrar'),  
    # sedes #######################################
    
    
    #comprobar_correo
    path('comprobar_correo', comprobar_correo, name='comprobar_correo'),  
    path('cambio_contra', cambio_contra, name='cambio_contra'),  
    path('verificar_codigo', verificar_codigo, name='verificar_codigo'),  
    path('modulos_accion', modulos_accion, name='modulos_accion'),  
    path('permisos', permisos, name='permisos'),  
    
    # roles #######################################
    path('roles_lista', roles_lista, name='roles_lista'),  
    path('roles_crear', roles_crear, name='roles_crear'),  
    path('roles_editar/<int:pk>', roles_editar, name='roles_editar'),  
    path('roles_borrar/<int:pk>', roles_borrar, name='roles_borrar'),  
    # roles #######################################
    
    path("roles/<int:rol_id>/permisos", roles_ver_permisos),
    path("roles/<int:rol_id>/permisos/asignar", roles_asignar_permisos),    
    
    # path('', views.inicio, name='inicio'),  # Ruta raíz redirige por nombre
    # path('login', login.as_view(), name='login'),  
    # path('select_empresas', select_empresas.as_view(), name='select_empresas'),  
]