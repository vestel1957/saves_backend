from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings

from requests import request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
# from rest_framework_simplejwt.tokens import RefreshToken
from clientes.models import *
from login.choice import DOMINIO_CORREO
from login.general import *
from nomina.models import *
from django.contrib import messages
from rest_framework_simplejwt.tokens import AccessToken
from datetime import date, timedelta
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
import re
from rest_framework.response import Response

def verificar_direccion(nomenclatura, numero_via, adicional_via,via_secundaria, adicional_secundaria, numero_casa):
    partes = []
    # Vía principal
    if nomenclatura and numero_via:
        principal = f"{nomenclatura} {numero_via}"
        if adicional_via:
            principal += f" {adicional_via}"
        partes.append(principal)

    # Vía secundaria
    if via_secundaria:
        secundaria = f"# {via_secundaria}"
        if adicional_secundaria:
            secundaria += f" {adicional_secundaria}"
        partes.append(secundaria)

    # Número de casa
    if numero_casa:
        partes.append(f"- {numero_casa}")

    direccion_completa = " ".join(partes)
    return direccion_completa

# Create your views here.
@api_view(['POST'])
# @token_required
def clientes_crear(request):
    try:
        usuario = request.data.get("usuario")
        cod_emp = request.data.get("cod_emp")
        data = request.data.get("formulario_cliente", {})
        ####validar usuario
        if not Employees.objects.filter(pk=usuario).exists():
            return Response({
                "ok": False,
                "mensaje": "Usuario no válido",
            }, status=400)
        
        qusuario = Employees.objects.filter(pk=usuario).first()

        #datos personales
        nombre = data.get("nombre")
        identificacion = data.get("identificacion")
        # empresa = data.get("empresa")
        celular = data.get("celular")
        celular_adi = data.get("celular_adi")
        correo = data.get("correo")
        fecha_nacimiento = data.get("fecha_nacimiento")
        tipo_clte = data.get("tipo_clte")
        tipo_documento = data.get("tipo_documento")
        estrato = data.get("estrato")
        suscripcion = data.get("suscripcion")

        #datos de residencia
        departamento = data.get("departamento")
        ciudad = data.get("ciudad")
        localidad = data.get("localidad")
        barrio = data.get("barrio")
        # direccion
        nomenclatura = data.get("nomenclatura")
        numero_via = data.get("numero_via")
        adicional_via = data.get("adicional_via")
        via_secundaria = data.get("via_secundaria")
        adicional_secundaria = data.get("adicional_secundaria")
        numero_casa = data.get("numero_casa")

        direccion_completa = verificar_direccion(nomenclatura, numero_via, adicional_via,via_secundaria, adicional_secundaria, numero_casa)
    
        residencia = data.get("residencia")
        referencia = data.get("referencia")
        ###########################

        ########################### diviciones
        division1 = data.get("division1")
        division1_num = data.get("division1_num")
        division2 = data.get("division2")
        division2_num = data.get("division2_num")
        ###########################
        ########################### coordenadas y clausula
        coordenada1 = data.get("coordenada1")
        coordenada2 = data.get("coordenada2")
        direccion_suscriptor = data.get("direccion_suscriptor")
        clausula = data.get("clausula")
        
        # datos de la integracion
        integrar_sistema = data.get("integrar_sistema")
        tecnologia = data.get("tecnologia")
        nombre_equipo = data.get("nombre_equipo")
        contrasena = data.get("contrasena")
        servicio = data.get("servicio")
        perfil = data.get("perfil")
        ip_local = data.get("ip_local")
        ip_remota = data.get("ip_remota")
        comentario = data.get("comentario")

        ##validaciones

        try:
            celular_limpio = validar_numeros(celular, "celular")
            celular_adi_limpio = validar_numeros(celular_adi, "celular adicional")
            identificacion_limpia= validar_numeros(identificacion , "identificacion")
            
            qdepartamento = Departamentos.objects.filter(pk=departamento).first()
            qciudad = Ciudades.objects.filter(pk=ciudad).first()

            if qciudad is None or qdepartamento is None:
                return Response({
                    "ok": False,
                    "mensaje": "departamento o ciudad no validos",
                })
            
            qlocalidad = ""
            if localidad:
                qlocalidad = Localidad.objects.filter(pk=localidad).first()

            qbarrio = ""
            if barrio:
                qbarrio = Barrios.objects.filter(pk=barrio).first()

            nombre_limpio = re.sub(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ ]', '', nombre).strip()
            qcliente = Clientes()
            qcliente.CliNombreTitular = nombre_limpio
            qcliente.CliDocumento = identificacion_limpia
            qcliente.CliCelular = celular_limpio
            qcliente.CliCelular2 = celular_adi_limpio
            qcliente.CliEmail = correo
            qcliente.CliNacimiento = fecha_nacimiento
            qcliente.CliTipoCliente = tipo_clte
            qcliente.CliTipoDocumento = tipo_documento
            qcliente.CliEstrato = estrato
            qcliente.CliSuscripcion = suscripcion
            ########## direccion ##########
            qcliente.CliDepartamento = qdepartamento
            qcliente.CliCiudad = qciudad
            qcliente.CliLocalidad = qlocalidad
            qcliente.CliBarrio = qbarrio
            
            qcliente.CliNomenclatura = nomenclatura
            qcliente.CliNumeroVia = numero_via
            qcliente.CliAdicionalVia = adicional_via
            qcliente.CliViaSecundaria = via_secundaria
            qcliente.CliAdicionalSecundaria = adicional_secundaria
            qcliente.CliNumeroCasa = numero_casa
            qcliente.CliDireccionCompleta = direccion_completa
            qcliente.CliReferencia = referencia
            qcliente.CliTipoResidencia = residencia
            ########## diviciones ##########
            qcliente.CliDivNum1 = division1_num
            qcliente.CliDivicion = division1
            qcliente.CliDivNum2 = division2_num
            qcliente.CliDivicion2 = division2
            ##########
            qcliente.CliCoor1 = coordenada1
            qcliente.CliCoor2 = coordenada2
            qcliente.CliDirsuscriptor = direccion_suscriptor
            qcliente.CliClausula = clausula
            qcliente.CliTecnologiaInstalacion = tecnologia
            qcliente.CliNombreEquipo = nombre_equipo
            qcliente.CliContrasena = encrypt_value(contrasena)
            qcliente.CliServicio = servicio
            qcliente.CliPerfil = perfil
            qcliente.CliIplocal = ip_local
            qcliente.CliIpRemota = ip_remota
            qcliente.CliComentario = comentario
            qcliente.CliCodEmp = cod_emp
            qcliente.save()

            return Response({
                "ok": True,
                "mensaje": "cliente creado con exito",
                "usuario": qusuario.pk,
                "cod_emp": cod_emp,
            })
        
        except Exception as e:
            print("error crear cliente", e)
            print(traceback.format_exc())  # traza completa para ver en qué campo
            return Response({
                "ok": False,
                "mensaje": "error al crear el cliente",
            })
    except Exception as e:
        print("error crear cliente", e)
        print(traceback.format_exc())  # traza completa para ver en qué campo
        return Response({
            "ok": False,
            "mensaje": "error al crear el cliente",
        })

@api_view(['POST'])
# @token_required
def clientes_listar(request):
    try:
        usuario = request.data.get("usuario")
        cod_emp = request.data.get("cod_emp")
        ####validar usuario
        if not Employees.objects.filter(pk=usuario).exists():
            return Response({
                "ok": False,
                "mensaje": "Usuario no válido",
            }, status=400)
        
        qusuario = Employees.objects.filter(pk=usuario).first()

        lista_clientes = []
        mensaje, ok, status = "", False, 400
        qclientes = Clientes.objects.filter(CliCodEmp=cod_emp)
        ##validaciones
        if qclientes:
    
            for cli in qclientes:
                lista_clientes.append([
                    cli.pk,
                    cli.CliNombreTitular,
                    cli.CliDocumento,
                    cli.CliCelular,
                    cli.CliEmail,
                ])
            mensaje = "listado exitoso"
            ok = True
            status = 200
        else:
            mensaje = "no hay clientes"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje,
            "usuario": qusuario.pk,
            "cod_emp": cod_emp,
            "lista_clientes": lista_clientes,
        }, status=status)
        
    except Exception as e:
        print("error crear cliente", e)
        print(traceback.format_exc())  # traza completa para ver en qué campo
        return Response({
            "ok": False,
            "mensaje": "error al crear el cliente",
        })
    
@api_view(['POST'])
# @token_required
def clientes_editar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    usuario = request.data.get("usuario")
    cod_emp = request.data.get("cod_emp")
    data = request.data.get("formulario_cliente", {})
    status, mensaje = False, ""
    try:
        ####validar usuario
        if not Employees.objects.filter(pk=usuario).exists():
            return Response({
                "ok": False,
                "mensaje": "Usuario no válido",
            }, status=400)

        qcliente = Clientes.objects.filter(pk=pk).first()
        if qcliente:

            #datos personales
            nombre = data.get("nombre")
            identificacion = data.get("identificacion")
            # empresa = data.get("empresa")
            celular = data.get("celular")
            celular_adi = data.get("celular_adi")
            correo = data.get("correo")
            fecha_nacimiento = data.get("fecha_nacimiento")
            tipo_clte = data.get("tipo_clte")
            tipo_documento = data.get("tipo_documento")
            estrato = data.get("estrato")
            suscripcion = data.get("suscripcion")

            #datos de residencia
            departamento = data.get("departamento")
            ciudad = data.get("ciudad")
            localidad = data.get("localidad")
            barrio = data.get("barrio")
            # direccion
            nomenclatura = data.get("nomenclatura")
            numero_via = data.get("numero_via")
            adicional_via = data.get("adicional_via")
            via_secundaria = data.get("via_secundaria")
            adicional_secundaria = data.get("adicional_secundaria")
            numero_casa = data.get("numero_casa")

            direccion_completa = verificar_direccion(nomenclatura, numero_via, adicional_via,via_secundaria, adicional_secundaria, numero_casa)

            residencia = data.get("residencia")
            referencia = data.get("referencia")
            ###########################

            ########################### diviciones
            division1 = data.get("division1")
            division1_num = data.get("division1_num")
            division2 = data.get("division2")
            division2_num = data.get("division2_num")
            ###########################
            ########################### coordenadas y clausula
            coordenada1 = data.get("coordenada1")
            coordenada2 = data.get("coordenada2")
            direccion_suscriptor = data.get("direccion_suscriptor")
            clausula = data.get("clausula")
            
            # datos de la integracion
            integrar_sistema = data.get("integrar_sistema")
            tecnologia = data.get("tecnologia")
            nombre_equipo = data.get("nombre_equipo")
            contrasena = data.get("contrasena")
            servicio = data.get("servicio")
            perfil = data.get("perfil")
            ip_local = data.get("ip_local")
            ip_remota = data.get("ip_remota")
            comentario = data.get("comentario")

            celular_limpio = validar_numeros(celular, "celular")
            celular_adi_limpio = validar_numeros(celular_adi, "celular adicional")
            identificacion_limpia= validar_numeros(identificacion , "identificacion")
            
            qdepartamento = Departamentos.objects.filter(pk=departamento).first()
            qciudad = Ciudades.objects.filter(pk=ciudad).first()

            if qciudad is None or qdepartamento is None:
                return Response({
                    "ok": False,
                    "mensaje": "departamento o ciudad no validos",
                }, status=400)
            
            qlocalidad = ""
            if localidad:
                qlocalidad = Localidad.objects.filter(pk=localidad).first()

            qbarrio = ""
            if barrio:
                qbarrio = Barrios.objects.filter(pk=barrio).first()

            nombre_limpio = re.sub(r'[^A-Za-zÁÉÍÓÚáéíóúÑñ ]', '', nombre).strip()
            mensaje, ok, status = "", False, 400
            ### editar cliente
            qcliente.CliNombreTitular = nombre_limpio
            qcliente.CliDocumento = identificacion_limpia
            qcliente.CliCelular = celular_limpio
            qcliente.CliCelular2 = celular_adi_limpio
            qcliente.CliEmail = correo
            qcliente.CliNacimiento = fecha_nacimiento
            qcliente.CliTipoCliente = tipo_clte
            qcliente.CliTipoDocumento = tipo_documento
            qcliente.CliEstrato = estrato
            qcliente.CliSuscripcion = suscripcion
            ########## direccion ##########
            qcliente.CliDepartamento = qdepartamento
            qcliente.CliCiudad = qciudad
            qcliente.CliLocalidad = qlocalidad
            qcliente.CliBarrio = qbarrio
            
            qcliente.CliNomenclatura = nomenclatura
            qcliente.CliNumeroVia = numero_via
            qcliente.CliAdicionalVia = adicional_via
            qcliente.CliViaSecundaria = via_secundaria
            qcliente.CliAdicionalSecundaria = adicional_secundaria
            qcliente.CliNumeroCasa = numero_casa
            qcliente.CliDireccionCompleta = direccion_completa
            qcliente.CliReferencia = referencia
            qcliente.CliTipoResidencia = residencia
            ########## diviciones ##########
            qcliente.CliDivNum1 = division1_num
            qcliente.CliDivicion = division1
            qcliente.CliDivNum2 = division2_num
            qcliente.CliDivicion2 = division2
            ##########
            qcliente.CliCoor1 = coordenada1
            qcliente.CliCoor2 = coordenada2
            qcliente.CliDirsuscriptor = direccion_suscriptor
            qcliente.CliClausula = clausula
            qcliente.CliTecnologiaInstalacion = tecnologia
            qcliente.CliNombreEquipo = nombre_equipo
            qcliente.CliContrasena = encrypt_value(contrasena)
            qcliente.CliServicio = servicio
            qcliente.CliPerfil = perfil
            qcliente.CliIplocal = ip_local
            qcliente.CliIpRemota = ip_remota
            qcliente.CliComentario = comentario
            qcliente.CliCodEmp = cod_emp
            qcliente.save()
            mensaje = "cliente editado con exito"
            status = 200
            ok = True

        return Response({
            "status": ok,
            "mensaje": f"{mensaje}"
        }, status=status)

    except Exception as e:
        return Response({
            "status": False,
            "mensaje": f"Error editando cliente: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
# @token_required
def clientes_borrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    usuario = request.data.get("usuario")
    qusuario = Employees.objects.filter(pk=usuario).first()
    qcliente= Clientes.objects.filter(pk=pk).first()
    mensaje, ok, status = "", False, 400

    if qusuario is None:
        return Response({
            "ok": False,
            "mensaje": "usuario no encontrado",
        }, status=400)
        
    # GUARDAR
    try:
        if qcliente:
            qcliente.delete()
            ok = True
            status = 200
            mensaje = "cliente borrado con exito"

        return Response({
            "ok": ok,
            "mensaje": f"{mensaje}"
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando cliente: {str(e)}"
        }, status=400)
####
######## grupos clientes


@api_view(['POST'])
# @token_required
def grupo_clientes_crear(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("formulario_grupo_clientes")
    cod_emp = request.data.get("cod_emp")

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "Formulario vacío",
        }, status=400)

    # GUARDAR
    try:
        GrupoCliente.objects.create(
            GcNombre=data["nombre"],
            GtDir=data["direccion"],
            GcDescripcion=data["descripcion"],
            GtCodEmp=cod_emp,
        )
        
        return Response({
            "ok": True,
            "mensaje": f"grupo cliente creado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error guardando grupo cliente: {str(e)}"
        }, status=400)
    

@api_view(['POST'])
# @token_required
def grupo_clientes_listar(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    usuario = request.data.get("usuario")
    cod_emp = request.data.get("cod_emp")
    
    if usuario is None:
        return Response({
            "ok": False,
            "mensaje": "error de usuario",
        })

    lista_grupos =[]
    ok, status, mensaje = False, 400,""
    
    qgrupo_cliente = GrupoCliente.objects.filter(GtCodEmp=cod_emp)
    if qgrupo_cliente:
        for cli in qgrupo_cliente:
            
            lista_grupos.append([cli.pk, cli.GcNombre, cli.GcDescripcion, cli.GtDir])
        ok = True
        status = 200
        mensaje = "bienvenido al menu principal"

    return Response({
            "ok": ok,
            "mensaje": mensaje,
            "lista_grupos": lista_grupos,
        }, status=status) 

@api_view(['POST'])
# @token_required
def grupo_clientes_editar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("formulario_grupo_clientes")
    usuario = request.data.get("usuario")
    cod_emp = request.data.get("cod_emp")
    qusuario = Employees.objects.filter(pk=usuario).first()
    

    if qusuario is None:
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
        ok, status, mensaje = False, 400, "Grupo cliente no encontrado"
        qgrupo_clientes = GrupoCliente.objects.filter(pk=pk).first()
        if qgrupo_clientes:
            qgrupo_clientes.GcNombre=data["nombre"]
            qgrupo_clientes.GtDir=data["direccion"]
            qgrupo_clientes.GcDescripcion=data["descripcion"]
            qgrupo_clientes.GtCodEmp=cod_emp
            qgrupo_clientes.save()
            status = 200
            ok = True
            mensaje = "Grupo cliente editado con exito"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error editando grupo cliente: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
# @token_required
def grupo_clientes_borrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    usuario = request.data.get("usuario")
    qusuario = Employees.objects.filter(pk=usuario).first()

    if qusuario is None:
        return Response({
            "ok": False,
            "mensaje": "usuario no encontrado",
        }, status=400)


    # GUARDAR
    try:
        ok, status, mensaje = False, 400, "Grupo cliente no encontrado"
        qgrupo_clientes = GrupoCliente.objects.filter(pk=pk).first()
        if qgrupo_clientes:
            qgrupo_clientes.delete()
            status = 200
            ok = True
            mensaje = "Grupo cliente borrado con exito"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrado grupo cliente: {str(e)}"
        }, status=400)
########################################