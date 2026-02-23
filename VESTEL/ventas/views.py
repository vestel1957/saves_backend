from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .decorators import token_required
from datetime import datetime

from login.general import token_required

# Create your views here.
@api_view(['POST'])
@token_required
def apertura_caja(request):
    empleado = request.empleado_name
    rol = request.rol

    # Ejemplo de lógica: abrir caja solo si rol tiene permiso
    if rol not in ['cajero', 'admin']:
        return Response({"ok": False, "mensaje": "No tiene permiso para abrir caja"})

    # Simula apertura de caja
    caja_abierta = {
        "empleado": empleado,
        "fecha_apertura": datetime.now(),
        "estado": "ABIERTA",
    }

    return Response({
        "ok": True,
        "mensaje": "Caja abierta correctamente",
        "caja": caja_abierta
    })

@api_view(['POST'])
@token_required
def nueva_factura(request):
    empleado = request.empleado_name
    rol = request.rol

    # Datos recibidos
    data = request.data
    cliente_id = data.get("cliente_id")
    productos = data.get("productos", [])  # lista de {id, cantidad, precio_unitario}

    # Simula creación de factura
    factura = {
        "numero": "F2026-001",
        "cliente_id": cliente_id,
        "productos": productos,
        "total": sum([p['cantidad'] * p['precio_unitario'] for p in productos]),
        "fecha": datetime.now(),
        "empleado": empleado,
    }

    return Response({
        "ok": True,
        "mensaje": "Factura creada correctamente",
        "factura": factura
    })

@api_view(['POST'])
@token_required
def administrar_factura(request):
    rol = request.rol
    # En un ERP real aquí harías query a la base de datos
    # Por ejemplo, buscar facturas por fecha, cliente, estado, etc.
    filtros = request.data

    # Simulamos respuesta
    facturas = [
        {"numero": "F2026-001", "cliente": "Juan Perez", "total": 1200000, "estado": "PENDIENTE"},
        {"numero": "F2026-002", "cliente": "Maria Gomez", "total": 450000, "estado": "PAGADA"},
    ]

    return Response({
        "ok": True,
        "facturas": facturas,
        "filtros": filtros
    })

@api_view(['POST'])
@token_required
def administrar_cotizaciones(request):
    # Simula listado de cotizaciones
    cotizaciones = [
        {"numero": "COT-001", "cliente": "Empresa XYZ", "total": 2000000, "estado": "PENDIENTE"},
        {"numero": "COT-002", "cliente": "Empresa ABC", "total": 1500000, "estado": "ACEPTADA"},
    ]
    return Response({
        "ok": True,
        "cotizaciones": cotizaciones
    })

@api_view(['POST'])
@token_required
def cierre_caja(request):
    empleado = request.empleado_name
    # Aquí normalmente sumarías todas las ventas del día
    resumen = {
        "total_ventas": 3500000,
        "total_facturas": 5,
        "fecha": datetime.now(),
        "empleado": empleado
    }
    return Response({
        "ok": True,
        "mensaje": "Caja cerrada correctamente",
        "resumen": resumen
    })