from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .decorators import token_required
from datetime import datetime

from almacenamiento.models import *
from login.general import consulta_contadores, token_required
from login.models import Modules

# Create your views here.
@api_view(['POST'])
@token_required
def crear_bodega(request):
    cod_emp = request.data.get("cod_emp")
    nombre = request.data.get("nombre")
    direccion = request.data.get("direccion")
    ciudad = request.data.get("ciudad")
    departamento = request.data.get("departamento")
    estado = request.data.get("estado")
    observaciones = request.data.get("observaciones")
    status, mensaje, ok = 400, "", False

    if not nombre:
        mensaje = "Debe enviar nombre de bodega"
        return Response({"ok": ok, "mensaje": mensaje}, status=status)

    try:
        bodega = Almacenamiento.objects.create(
            AlNombre=nombre,
            AlDireccion=direccion,
            AlCiudad=ciudad,
            AlDeparta=departamento,
            AlEstado=estado,
            AlCod_emp=cod_emp,
            AlObservaciones=observaciones
        )
        status = 200
        ok = True
        mensaje =  "Bodega creada exitosamente"
        return Response({"ok": ok, "mensaje": mensaje, "bodega_id": bodega.pk}, status= status)


    except Exception as e:
        mensaje = f"Error al crear bodega: {str(e)}"
        return Response({"ok": False, "mensaje": mensaje}, status=status)

# Create your views here.
@api_view(['POST'])
@token_required
def editar_bodega(request, pk):

    data = request.data.get("formulario_usuario")
    qusuarios = request.empleado
    qrol = request.rol
    if qusuarios is None:
        return Response({
            "ok": False,
            "mensaje": "usuario no encontrado",
        }, status=400)
        
    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)

    # GUARDAR
    try:
        qbodega = Almacenamiento.objects.filter(pk=pk).first()
        qbodega.AlNombre = data["nombre"]
        qbodega.AlEstado = data["estado"]
        qbodega.AlDeparta = data["departamento"]
        qbodega.AlCiudad = data["ciudad"]
        qbodega.AlDireccion = data["direccion"]
        qbodega.AlCod_emp = data["cod_emp"]
        qbodega.AlObservaciones = data["observaciones"]
        qbodega.save()
        
        return Response({
            "status": True,
            "mensaje": f"bodega editada correctamente"
        })

    except Exception as e:
        return Response({
            "status": False,
            "mensaje": f"Error editando bodega: {str(e)}"
        }, status=400)

# Create your views here.
@api_view(['POST'])
@token_required
def eliminar_bodega(request, pk):
    qbodega = Almacenamiento.objects.filter(pk=pk).first()
    try:
        qbodega.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"bodega borrada con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando bodega: {str(e)}"
        }, status=400)

# Create your views here.
@api_view(['POST'])
@token_required
def listar_bodega(request):
    cod_emp = request.data.get("cod_emp")
    

    lista_bodegas =[]
    
    qbodegas = Almacenamiento.objects.filter(AlCod_emp=cod_emp).order_by('AlNombre')
    print(qbodegas)
    
    try:

        if qbodegas:
            for bod in qbodegas:
                lista_bodegas.append([bod.pk, bod.AlNombre, bod.AlDireccion, bod.AlEstado, bod.AlObservaciones])
            return Response({
                "ok": True,
                "mensaje": "lista de bodegas",
                "lista_bodegas": lista_bodegas,
            })  
        else:
            return Response({
                "ok": False,
                "mensaje": "error al encontrar las bodegas",
            })
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error listando bodegas: {str(e)}"
        }, status=400)
    
##############bodega equipos ###########################

@api_view(['POST'])
@token_required
def crear_bodega_equipo(request):
    cod_emp = request.data.get("cod_emp")
    nombre = request.data.get("nombre")
    direccion = request.data.get("direccion")
    ciudad = request.data.get("ciudad")
    departamento = request.data.get("departamento")
    estado = request.data.get("estado")
    observaciones = request.data.get("observaciones")
    status, mensaje, ok = 400, "", False

    if not nombre:
        mensaje = "Debe enviar nombre de bodega equipos"
        return Response({"ok": ok, "mensaje": mensaje}, status=status)

    try:
        bodega = AlmacenamientoEquipos.objects.create(
            AleNombre=nombre,
            AleDireccion=direccion,
            AleCiudad=ciudad,
            aleDeparta=departamento,
            AleEstado=estado,
            AleCodemp=cod_emp,
            AleObservaciones=observaciones
        )
        status = 200
        ok = True
        mensaje =  "Bodega equipos creada exitosamente"
        return Response({"ok": ok, "mensaje": mensaje, "bodega_id": bodega.pk}, status= status)


    except Exception as e:
        mensaje = f"Error al crear bodega equipos : {str(e)}"
        return Response({"ok": False, "mensaje": mensaje}, status=status)

# Create your views here.
@api_view(['POST'])
@token_required
def editar_bodega_equipos(request, pk):

    data = request.data.get("formulario_usuario")

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)

    # GUARDAR
    try:
        qbodega = AlmacenamientoEquipos.objects.filter(pk=pk).first()
        qbodega.AleNombre = data["nombre"]
        qbodega.AleEstado = data["estado"]
        qbodega.aleDeparta = data["departamento"]
        qbodega.AleCiudad = data["ciudad"]
        qbodega.AleDireccion = data["direccion"]
        qbodega.AleCodemp = data["cod_emp"]
        qbodega.AleObservaciones = data["observaciones"]
        qbodega.save()
        
        return Response({
            "status": True,
            "mensaje": f"bodega equipos editada correctamente"
        })

    except Exception as e:
        return Response({
            "status": False,
            "mensaje": f"Error editando bodega equipos: {str(e)}"
        }, status=400)

# Create your views here.
@api_view(['POST'])
@token_required
def eliminar_bodega_equipos(request, pk):
    qbodega = AlmacenamientoEquipos.objects.filter(pk=pk).first()
    try:
        qbodega.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"bodega equipos borrada con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando bodega equipos: {str(e)}"
        }, status=400)

# Create your views here.
@api_view(['POST'])
@token_required
def listar_bodega_equipos(request):
    cod_emp = request.data.get("cod_emp")
    
    lista_bodegas_equipos =[]
    
    qbodegas = AlmacenamientoEquipos.objects.filter(AleCodemp=cod_emp).order_by('AleNombre')
    print(qbodegas)
    
    try:

        if qbodegas:
            for bod in qbodegas:
                lista_bodegas_equipos.append([bod.pk, bod.AleNombre, bod.AleDireccion, bod.AleEstado, bod.AleObservaciones])
            return Response({
                "ok": True,
                "mensaje": "lista de bodegas equipos",
                "lista_bodegas_equipos": lista_bodegas_equipos,
            })  
        else:
            return Response({
                "ok": False,
                "mensaje": "error al encontrar las bodegas equipos",
            })
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error listando bodegas equipos: {str(e)}"
        }, status=400)


# ########################### equipos ###########################
@api_view(['POST'])
@token_required
def crear_equipos(request):
    # EqCodigo = request.data.get("codigo")
    proveedores = request.data.get("proveedores")
    almacen = request.data.get("almacen")
    mac = request.data.get("mac")
    serial = request.data.get("serial")
    cod_emp = request.data.get("cod_emp")
    fecha_llegada = request.data.get("fecha_llegada")
    fecha_final = request.data.get("fecha_final")
    marca = request.data.get("marca")
    tipo_instalaciones = request.data.get("tipo_instalaciones")
    puertos = request.data.get("puertos")
    vlan = request.data.get("vlan")
    nat = request.data.get("nat")
    asignado = request.data.get("asignado")
    estado = request.data.get("estado")
    observaciones = request.data.get("observaciones")
    master = request.data.get("master")
    accesorios = request.data.get("accesorios")
    id_genieacs = request.data.get("id_genieacs")
    status, mensaje, ok = 400, "", False

    lista = [
        [proveedores, "proveedores"],
        [almacen, "almacen"],
        [mac, "mac"],
        [serial, "serial"],
        [marca, "marca"],
        [tipo_instalaciones, "tipo_instalaciones"],
        [puertos, "puertos"],
        [vlan, "vlan"],
        [nat, "nat"],
    ]

    for campo, mensaje_campo in lista:
        if campo is None or (isinstance(campo, str) and campo.strip() == ""):
            mensaje = f"Debe enviar {mensaje_campo} del equipo"
            return Response(
                {"ok": ok, "mensaje": mensaje},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    contador = consulta_contadores("EQUIPOS", "EQP", "EQUIPOS", cod_emp)

    try:
        equipo = Equipos.objects.create(
            EqCodigo=contador,
            EqProveedor=proveedores,
            EqAlmacen=almacen,
            EqMac=mac,
            EqSerial=serial,
            EqFechaLlegada=fecha_llegada,
            EqFechaFinal=fecha_final,
            EqMarca=marca,
            EqTipoInstalacion=tipo_instalaciones,
            EqPuerto=puertos,
            EqVlan=vlan,
            EqNat=nat,
            EqAsignado=asignado,
            EqEstado=estado,
            EqCodEmp=cod_emp,
            EqObservaciones=observaciones,
            EqMaster=master,
            EqAccesorios=accesorios,
            EqIdGenieacs=id_genieacs
        )
        status = 200
        ok = True
        mensaje =  "equipo creada exitosamente"
        return Response({"ok": ok, "mensaje": mensaje, "equipo_id": equipo.pk}, status= status)


    except Exception as e:
        mensaje = f"Error al crear equipo: {str(e)}"
        return Response({"ok": False, "mensaje": mensaje}, status=status)

# Create your views here.
@api_view(['POST'])
@token_required
def editar_equipo(request, pk):

    data = request.data.get("formulario_equipo")
    cod_emp = request.data.get("cod_emp")

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)

    contador = consulta_contadores("EQUIPOS", "EQP", "EQUIPOS", cod_emp)
    qproveedores = Proveedores.objects.filter(pk=data["proveedor"]).first()
    qalmacen = Almacenamiento.objects.filter(pk=data["almacen"]).first()
    qasignado = Employees.objects.filter(pk=data["asignado"]).first()

    # GUARDAR
    try:
        qequipo = Equipos.objects.filter(pk=pk).first()
        qequipo.EqCodigo =contador
        qequipo.EqProveedor = qproveedores
        qequipo.EqAlmacen = qalmacen
        qequipo.EqMac = data["mac"]
        qequipo.EqSerial = data["serial"]
        qequipo.EqFechaLlegada = data["fecha_llegada"]
        qequipo.EqFechaFinal = data["fecha_final"]
        qequipo.EqMarca = data["marca"]
        qequipo.EqTipoInstalacion = data["tipo_instalacion"]
        qequipo.EqPuerto = data["puertos"]
        qequipo.EqVlan = data["vlan"]
        qequipo.EqAsignado = qasignado
        qequipo.EqEstado = data["estado"]
        qequipo.EqCodEmp = cod_emp
        qequipo.EqObservaciones = data["observaciones"]
        qequipo.EqMaster = data["master"]
        qequipo.EqAccesorios = data["accesorios"]
        qequipo.EqIdGenieacs = data["id_genieacs"]
        qequipo.save()
        
        return Response({
            "status": True,
            "mensaje": f"equipo editada correctamente"
        })

    except Exception as e:
        return Response({
            "status": False,
            "mensaje": f"Error editando equipo: {str(e)}"
        }, status=400)

# Create your views here.
@api_view(['POST'])
@token_required
def eliminar_equipo(request, pk):
    qequipo = Almacenamiento.objects.filter(pk=pk).first()
    try:
        qequipo.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"equipo borrada con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando equipo: {str(e)}"
        }, status=400)

# Create your views here.
@api_view(['POST'])
@token_required
def listar_equipo(request):
    cod_emp = request.data.get("cod_emp")
    

    lista_equipos =[]
    
    qequipos = Almacenamiento.objects.filter(AlCod_emp=cod_emp).order_by('AlNombre')
    print(qequipos)
    
    try:

        if qequipos:
            for bod in qequipos:
                lista_equipos.append([bod.pk, bod.AlNombre, bod.AlDireccion, bod.AlEstado, bod.AlObservaciones])
            return Response({
                "ok": True,
                "mensaje": "lista de equipos",
                "lista_equipos": lista_equipos,
            })  
        else:
            return Response({
                "ok": False,
                "mensaje": "error al encontrar las equipos",
            })
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error listando equipos: {str(e)}"
        }, status=400)
