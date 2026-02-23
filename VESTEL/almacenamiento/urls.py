from django.urls import path
from . import views

urlpatterns = [
    # Ejemplo:
    ### crud de bodega
    path('crear_bodega', views.crear_bodega, name='crear_bodega'),
    path('editar_bodega/<int:pk>', views.editar_bodega, name='editar_bodega'),
    path('eliminar_bodega/<int:pk>', views.eliminar_bodega, name='eliminar_bodega'),
    path('listar_bodega', views.listar_bodega, name='listar_bodega'),

    ### crud de bodega equipos
    path('crear_bodega_equipo', views.crear_bodega_equipo, name='crear_bodega_equipo'),
    path('editar_bodega_equipo/<int:pk>', views.editar_bodega_equipos, name='editar_bodega_equipo'),
    path('eliminar_bodega_equipo/<int:pk>', views.eliminar_bodega_equipos, name='eliminar_bodega_equipo'),
    path('listar_bodega_equipo', views.listar_bodega_equipos, name='listar_bodega_equipo'),

]