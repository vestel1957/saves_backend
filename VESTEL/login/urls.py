from os import name
from django.urls import path
from .views import *

from login import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Ruta raíz redirige por nombre
    path('WSglLogin', WSglLogin, name='WSglLogin'),  # Ruta con nombre
    # path('seleccion_sede', seleccion_sede, name='seleccion_sede'),  
    path('menu_principal', menu_principal, name='menu_principal'),  
    
    # usuarios #######################################
    path('WSgListarUsuario', WSgListarUsuario, name='WSgListarUsuario'),  
    path('WSgCrearUsuario', WSgCrearUsuario, name='WSgCrearUsuario'),  
    path('WSgActualizarUsuario/<int:pk>', WSgActualizarUsuario, name='WSgActualizarUsuario'),  
    path('WSgUsuariosBorrar/<int:pk>', WSgUsuariosBorrar, name='WSgUsuariosBorrar'),  
    # usuarios #######################################
    
    # modales #######################################
    path('WCoModalesLista', WCoModalesLista, name='WCoModalesLista'),  
    path('WCoModalesCrear', WCoModalesCrear, name='WCoModalesCrear'),  
    path('WCoModalesEditar/<int:pk>', WCoModalesEditar, name='WCoModalesEditar'),  
    path('WCoModalesBorrar/<int:pk>', WCoModalesBorrar, name='WCoModalesBorrar'),  
    # modales #######################################

    # modales grupo #######################################
    path('WCoModulosGrupoLista', WCoModulosGrupoLista, name='WCoModulosGrupoLista'),  
    path('WCoModulosGrupoCrear', WCoModulosGrupoCrear, name='WCoModulosGrupoCrear'),  
    path('WCoModulosGrupoEditar/<int:pk>', WCoModulosGrupoEditar, name='WCoModulosGrupoEditar'),  
    path('WCoModulosGrupoBorrar/<int:pk>', WCoModulosGrupoBorrar, name='WCoModulosGrupoBorrar'),  
    # modales grupo #######################################
    
    # sedes #######################################
    path('WCoSedesLista', WCoSedesLista, name='WCoSedesLista'),  
    path('WCoSedesCrear', WCoSedesCrear, name='WCoSedesCrear'),  
    path('WCoSedesEditar/<int:pk>', WCoSedesEditar, name='WCoSedesEditar'),  
    path('WCoSedesBorrar/<int:pk>', WCoSedesBorrar, name='WCoSedesBorrar'),  
    # sedes #######################################

     # ACCION #######################################
    path('WCoAccionLista', WCoAccionLista, name='WCoAccionLista'),  
    path('WCoAccionCrear', WCoAccionCrear, name='WCoAccionCrear'),  
    path('WCoAccionEditar/<int:pk>', WCoAccionEditar, name='WCoAccionEditar'),  
    path('WCoAccionBorrar/<int:pk>', WCoAccionBorrar, name='WCoAccionBorrar'),  
    # accion #######################################
    
    
    #WClcomprobar_correo
    path('WClcomprobar_correo', WClcomprobar_correo, name='WClcomprobar_correo'),  
    path('WSgCambioContra', WSgCambioContra, name='WSgCambioContra'),  
    path('WSgVerificarCodigo', WSgVerificarCodigo, name='WSgVerificarCodigo'),  


    path('WSgModulosAccionCrear', WSgModulosAccionCrear, name='WSgModulosAccionCrear'),  
    path('WSgModulosAccionLista', WSgModulosAccionLista, name='WSgModulosAccionLista'),  
    path('WSgModulosAccionBorrar/<int:pk>', WSgModulosAccionBorrar, name='WSgModulosAccionBorrar'),  

    path('WSgPermisos', WSgPermisos, name='WSgPermisos'),  
    
    # roles #######################################
    path('WSgListarRol', views.WSgListarRol, name='WSgListarRol'),
    path('WSgCrearRol', views.WSgCrearRol, name='WSgCrearRol'),
    path('WSgActualizarRol/<int:pk>', views.WSgActualizarRol, name='WSgActualizarRol'),
    path('WSgBorrarRol/<int:pk>', views.WSgBorrarRol, name='WSgBorrarRol'),
    # roles #######################################
    
    path("WSgRolesVerPermisos/<int:rol_id>/permisos", WSgRolesVerPermisos),

    # permisos #######################################
    path('WSgListarPermisos', WSgListarPermisos, name='WSgListarPermisos'),  
    path('WSgPermisosCrear', WSgPermisosCrear, name='WSgPermisosCrear'),  
    path('WSgActualizarPermisos/<int:pk>', WSgActualizarPermisos, name='WSgActualizarPermisos'),  
    path('WSgBorrarPermisos/<int:pk>', WSgBorrarPermisos, name='WSgBorrarPermisos'),  
    # permisos #######################################
    # path("WSgRolesAsignarPermisos/<int:rol_id>/permisos/asignar", WSgRolesAsignarPermisos),    
    
    # path('', views.inicio, name='inicio'),  # Ruta raíz redirige por nombre
    # path('login', login.as_view(), name='login'),  
    # path('select_empresas', select_empresas.as_view(), name='select_empresas'),  
]