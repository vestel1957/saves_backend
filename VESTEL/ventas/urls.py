from django.urls import path
from . import views

urlpatterns = [
    # Ejemplo:
    path('apertura_caja', views.apertura_caja, name='apertura_caja'),
    path('nueva_factura', views.nueva_factura, name='nueva_factura'),
    path('administrar_factura', views.administrar_factura, name='administrar_factura'),
    path('administrar_cotizaiones', views.administrar_cotizaiones, name='administrar_cotizaiones'),
    path('cierre_caja', views.cierre_caja, name='cierre_caja'),
]