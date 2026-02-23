from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
# from rest_framework_simplejwt.tokens import RefreshToken
from login.choice import DOMINIO_CORREO
from login.general import comprobarCampos, WClenvio_email, firmar_cookie, WClgenerar_codigo, get_cookie_segura, token_required
from nomina.models import *
from django.contrib import messages
from rest_framework_simplejwt.tokens import AccessToken
from datetime import date, timedelta
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView

from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import AccessToken

from login.models import *

def inicio(request):
    return redirect('login')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(['POST'])
def WSglLogin(request):
    usuario = request.data.get("email")
    password = request.data.get("password")
    print("hola", )

    try:
        # emp = Employees.objects.filter(email=usuario, active=True).first()
        emp = Users.objects.filter(UsEmail=usuario).first()
        if not emp:
            return Response({"ok": False, "mensaje": "Usuario no existe"}, status=401)

    except Users.DoesNotExist:
        return Response({"ok": False, "mensaje": "Usuario no existe"}, status=401)

    if not check_password(password, emp.UsPass):
        return Response({"ok": False, "mensaje": "Contraseña incorrecta"}, status=401)

    if emp and emp.UsRoleid:
        query_permisos = emp.UsRoleid.RoPermissions.all() 
        
        lista_permisos = list(query_permisos.values_list('PeKey', flat=True))
    else:
        lista_permisos = []

    rol = emp.UsRoleid.RoName if emp.UsRoleid else "Sin Rol"
    access = AccessToken()
    access['empleado_id'] = emp.pk
    access['empleado_name'] = emp.UsUsername
    access['rol'] = rol
    access['permisos'] = lista_permisos
    access.set_exp(lifetime=timedelta(hours=2))  # 1<-- usar timedelta

    
    # if emp.UsRole:
    #     rol = emp.UsRole.RoName
    #     if rol == "INICIAR":
    #         print("hola")
    #         return Response({
    #             "status": True,
    #             "access": str(access),
    #             "url": "iniciador",
    #             "empleado": emp.UsUsername,
    #             "empleado_id": emp.pk,
    #             # "rol": emp.UsRole.RoName if emp.UsRole else ""
    #         })

                
    return Response({
        "status": True,
        "access": str(access),
        "empleado": emp.UsUsername,
        "rol": emp.UsRoleid.RoName if emp.UsRoleid else "",
        "empleado_id": emp.pk,
        "lista_permisos": lista_permisos,
    })
    
def WCoListaSedes():
    lista_sedes = []
    qsedes = Sede.objects.all()
    for s in qsedes:
        lista_sedes.append([s.pk, s.SeNombre])
    return lista_sedes

def WCoListaModulos():
    lista_modulos = []
    qmodulo = Modules.objects.all()
    for s in qmodulo:
        lista_modulos.append([s.pk, s.MdName, s.MdUrl])
    return lista_modulos

    
# @api_view(['POST'])
# @token_required
# def WCoSeleccionSede(request):
#     # Ya puedes acceder a request.empleado_name, request.rol, etc.
#     lista_sedes = []
#     print("request.rol", request.rol)
#     if request.rol:
#         lista_sedes = WCoListaSedes()
#         return Response({
#             "ok": True,
#             "empleado": request.empleado_name,
#             "rol": request.rol,
#             "menus": lista_sedes
#         })
    
#     else:
#         return Response({
#             "ok": False,
#             "mensaje": "error de autentificacion",
#         })
        
@api_view(['POST'])
@token_required
def menu_principal(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    logo_empresa = ""
    sede = request.data.get("sede")
    usuario = request.data.get("usuario")
    año = request.data.get("año")
    
    if usuario is None:
        return Response({
            "ok": False,
            "mensaje": "error de usuario",
        })
    if sede is None:
       return Response({
            "ok": False,
            "mensaje": "error de sede",
        })
        
    if año is None:
        return Response({
            "ok": False,
            "mensaje": "error de año",
        })
        
    
    lista_modulos =[]
    
    qempresa = Empresas.objects.all().first()
    nombre_empresa = qempresa.EmRazonSocial
    logo_empresa = qempresa.EmLogo
    logo_empresa = os.path.join(settings.MEDIA_ROOT, "imagenes", "sin_foto.webp")
    lista_modulos = WCoListaModulos()
    if qempresa.EmLogo:
        logo_empresa = qempresa.EmLogo
    else:
        if qempresa.EmLogo2:
            logo_empresa = qempresa.EmLogo2
        
    ciudad_empresa = qempresa.EmCiudad.MuMunicipio
    cod_empresa = qempresa.EmCodEempresa

    if qempresa:
        return Response({
            "ok": True,
            "mensaje": "bienvenido al menu principal",
            "lista_modulos": lista_modulos,
            "logo_empresa": logo_empresa,
            "ciudad_empresa": ciudad_empresa,
            "cod_empresa": cod_empresa,
            "nombre_empresa": nombre_empresa,
        })  
    else:
        return Response({
            "ok": False,
            "mensaje": "error de autentificacion",
        }) 
        
# usuarios ##############################################################################
        
@api_view(['POST'])
@token_required
def WSgListarUsuario(request):
    """
    T: W (Web), mm: Sg (Seguridad), Accion: Listar, Entidad: Usuario
    """
    # Validamos que el usuario que consulta exista en la data
    if not request.data.get("usuario"):
        return Response({"ok": False, "mensaje": "error de usuario"}, status=400)

    qusuarios = Users.objects.all()
    
    if not qusuarios.exists():
        return Response({"ok": False, "mensaje": "No se encontraron usuarios"}, status=400)

    lista_usuarios = []
    for usu in qusuarios:
        # Nota: Tu modelo no tiene una relación directa con Roles en el código enviado, 
        # se usa UsRoleid directamente.
        lista_usuarios.append([
            usu.pk, 
            usu.UsEmail, 
            usu.UsUsername, 
            usu.UsRoleid, 
            usu.UsDateCreated
        ])

    return Response({
        "ok": True, 
        "mensaje": "lISTA DE USUARIOS", 
        "lista_usuarios": lista_usuarios
    })
    
@api_view(['POST'])
# @token_required
def WSgCrearUsuario(request):
    """
    T: W, mm: Sg, Accion: Crear, Entidad: Usuario
    Procesamiento manual de campos obligatorios sin ciclos.
    """
    data = request.data.get("formulario_usuario")
    terminos_aceptados = []
    
    if not data:
        return Response({"ok": False, "mensaje": "Formulario vacío"}, status=400)

    campos_obligatorios = ["nombre", "email", "password", "rol_id"]
    comprobarCampos(data, campos_obligatorios)

    try:
        # Creamos el registro mapeando el JSON a los campos del Modelo Users
        Users.objects.create(
            UsUsername=data.get("nombre"),
            UsEmail=data.get("email"),
            UsPass=make_password(data.get("password")),
            UsRoleid=data.get("rol_id"),
            # Para 'superadmin' y 'cod_empresa', como no están en tu modelo base,
            # los omitimos o podrías guardarlos en UsSedeAccede si lo requieres.
            UsSedeAccede=data.get("cod_empresa", ""), 
            UsBanned=0,
            UsDateCreated=timezone.now()
        )
        
        return Response({
            "ok": True, 
            "mensaje": "usuario creado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False, 
            "mensaje": f"Error: {str(e)}"
        }, status=400)

@api_view(['POST'])
@token_required
def WSgActualizarUsuario(request, pk):
    """
    T: W, mm: Sg, Accion: Actualizar, Entidad: Usuario.
    Mapeo manual de campos obligatorios para coincidir con la lógica de creación.
    """
    data = request.data.get("formulario_usuario")
    qusuario = Users.objects.filter(pk=pk).first()

    if not qusuario:
        return Response({"ok": False, "mensaje": "usuario no encontrado"}, status=400)
    
    if not data:
        return Response({"ok": False, "mensaje": "formulario vacío"}, status=400)

    try:
        # Actualización de campos base usando las llaves del JSON de creación
        qusuario.UsUsername = data.get("nombre", qusuario.UsUsername)
        qusuario.UsEmail = data.get("email", qusuario.UsEmail)
        qusuario.UsRoleid = data.get("rol_id", qusuario.UsRoleid)
        qusuario.UsSedeAccede = data.get("cod_empresa", qusuario.UsSedeAccede)
        
        # Opcional: Si el JSON trae 'banned' o 'estado', podrías mapearlo aquí
        # qusuario.UsBanned = data.get("banned", qusuario.UsBanned)

        # Solo actualiza la contraseña si viene en el JSON
        if data.get("password"):
            qusuario.UsPass = make_password(data["password"])

        qusuario.save()
        
        return Response({
            "ok": True, 
            "mensaje": "usuario editado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False, 
            "mensaje": f"Error: {str(e)}"
        }, status=400)
    
@api_view(['POST'])
@token_required
def WSgUsuariosBorrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    try:
        qusuarios = Users.objects.filter(pk=pk).first()

        if qusuarios is None:
            return Response({
                "ok": False,
                "mensaje": "usuario no encontrado",
            }, status=400)
        # GUARDAR

        qusuarios.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"usuario borrado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando usuario: {str(e)}"
        }, status=400)
# usuarios ##############################################################################

# modales ##############################################################################
        
@api_view(['POST'])
@token_required
def WCoModalesLista(request):
    lista_modales =[]
    qmodales = Modules.objects.all().order_by('MdPadre__MgNombre','MdName')
    
    try:

        if qmodales:
            for mod in qmodales:
                lista_modales.append([mod.pk, mod.MdPadre.MgNombre, mod.MdName, mod.MdUrl])
            return Response({
                "ok": True,
                "mensaje": "lista de modales",
                "lista_modales": lista_modales,
            })  
        else:
            return Response({
                "ok": False,
                "mensaje": "error al encontrar los modulos",
            })
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error Listando Modulos: {str(e)}"
        }, status=400)
    
@api_view(['POST'])
@token_required
def WCoModalesCrear(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("FormularioModulos")

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "Formulario vacío",
        }, status=400)
    campos = ["nombre", "url", "llave", "modalPadre"]
    comprobarCampos(data, campos)
    mensaje, ok, status = "", False, 400
    if ModuleGroup.objects.filter(pk=data["modalPadre"]).first():
        # GUARDAR
        try:
            Modules.objects.create(
                MdName=data["nombre"],
                MdUrl=data["url"],
                MdKey=data["llave"],
                MdPadre_id=data["modalPadre"],
            )
            ok = True
            mensaje = f"modulo creado con exito"
            status = 200

        except Exception as e:
            return Response({
                "ok": False,
                "mensaje": f"Error guardando modulo: {str(e)}"
            }, status=400)
    else:
        mensaje = "modulo padre no encontrado"
    return Response({
                "ok": ok,
                "mensaje": mensaje
            }, status=status)
        
@api_view(['POST'])
@token_required
def WCoModalesEditar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("FormularioModulos")
    print("data",data)
    qmodales = Modules.objects.filter(pk=pk).first()

    if qmodales is None:
        return Response({
            "ok": False,
            "mensaje": "modal no encontrado",
        }, status=400)
        
    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)

    campos = ["nombre", "url", "llave", "modalPadre"]
    comprobarCampos(data, campos)

    # GUARDAR
    try:
        qmodales.MdName=data["nombre"]
        qmodales.MdUrl=data["url"]
        qmodales.MdKey=data["llave"]
        qmodales.MdPadre_id=data["modalPadre"]

        qmodales.save()
        
        return Response({
            "ok": True,
            "mensaje": f"modal editado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error editando modal: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WCoModalesBorrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    qmodales = Modules.objects.filter(pk=pk).first()

    if qmodales is None:
        return Response({
            "ok": False,
            "mensaje": "modal no encontrado",
        }, status=400)
        

    # GUARDAR
    try:
        qmodales.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"modal borrado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando modal: {str(e)}"
        }, status=400)
# modales ##############################################################################

# modales grupo ##############################################################################
        
@api_view(['POST'])
@token_required
def WCoModulosGrupoLista(request):
    ListaModulosGrupo =[]
    qmodalesGrupo = ModuleGroup.objects.all().order_by('MgOrden')
    mensaje, ok, status = "",False, 400
    try:

        if qmodalesGrupo:
            for mod in qmodalesGrupo:
                ListaModulosGrupo.append([mod.pk, mod.MgNombre, mod.MgIcono, mod.MgOrden])
                ok = True
                mensaje= "lista de modulos"
                status = 200

        else:
            mensaje=  "error al encontrar los modulos"

        return Response({
            "ok": ok,
            "mensaje": mensaje,
            "ListaModulosGrupo":ListaModulosGrupo
        }, status=status)
    except Exception as e:
        return Response({
            "ok": ok,
            "mensaje": f"Error Listando Modulos: {str(e)}"
        }, status=status)
    
@api_view(['POST'])
@token_required
def WCoModulosGrupoCrear(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("EModulosGrupo")

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "Formulario vacío",
        }, status=400)
    
    campos = ["nombre", "icono", "orden"]
    comprobarCampos(data, campos)
        # GUARDAR
    try:
        ModuleGroup.objects.create(
            MgNombre=data["nombre"],
            MgIcono=data["icono"],
            MgOrden=data["orden"],
        )
        return Response({
            "ok": True,
            "mensaje": "modulo guardado"
        }, status=200)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error guardando modulo: {str(e)}"
        }, status=400)

@api_view(['POST'])
@token_required
def WCoModulosGrupoEditar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("EModulosGrupo")
    print("data",data)
    mensaje, ok, status = "", False, 400
    qmodales = ModuleGroup.objects.filter(pk=pk).first()

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)

    campos = ["nombre", "icono", "orden"]
    comprobarCampos(data, campos)

    # GUARDAR
    try:
        if qmodales:
            qmodales.MgNombre=data["nombre"]
            qmodales.MgIcono=data["icono"]
            qmodales.MgOrden=data["orden"]
            qmodales.save()
            mensaje, ok, status = "Modal editado", True, 200
        else:
            mensaje ="modal no encontrado"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje,
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error editando modal: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WCoModulosGrupoBorrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    qmodales = ModuleGroup.objects.filter(pk=pk).first()

    if qmodales is None:
        return Response({
            "ok": False,
            "mensaje": "modal no encontrado",
        }, status=400)
        

    # GUARDAR
    try:
        qmodales.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"modal borrado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando modal: {str(e)}"
        }, status=400)
# modales grupo##############################################################################

# sedes ##############################################################################
        
@api_view(['POST'])
@token_required
def WCoSedesLista(request):
    lista_sedes =[]
    qsedes = Sede.objects.all().order_by('SeNombre')
    
    try:

        if qsedes:
            for sed in qsedes:
                lista_sedes.append([sed.pk, sed.SeLetra, sed.SeNombre, sed.SeMunicipio.CiNombre, sed.SeEstado])
            return Response({
                "ok": True,
                "mensaje": "lista de sedes",
                "lista_sedes": lista_sedes,
            })  
        else:
            return Response({
                "ok": False,
                "mensaje": "error al encontrar los sede",
            })
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando la sede: {str(e)}"
        }, status=400)
    
@api_view(['POST'])
@token_required
def WCoSedesCrear(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("FormularioSedes")
    qempresa = Empresas.objects.all().first()
    # Municipios = empresas.objects.filter(pk=).first()

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "Formulario vacío",
        }, status=400)

    # GUARDAR
    try:
        Sede.objects.create(
            SeEmpresa=qempresa,
            SeLetra=data["letra"],
            SeNombre=data["nombre"],
            SeDireccion=data["direccion"],
            SeMunicipio_id=data["municipio"],
            SeEstado=data["estado"],
            SeTelefono=data["telefono"],
            SeCorreo=data["correo"],
        )
        
        return Response({
            "ok": True,
            "mensaje": f"sede creado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error guardando sede: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WCoSedesEditar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("formulario")
    qsedes = Sede.objects.filter(pk=pk).first()

    if qsedes is None:
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
        qsedes.SeLetra=data["letra"]
        qsedes.SeNombre=data["nombre"]
        qsedes.SeDireccion=data["direccion"]
        qsedes.SeMunicipio_id=data["municipio"]
        qsedes.SeEstado=data["estado"]
        qsedes.SeTelefono=data["telefono"]
        qsedes.SeCorreo=data["correo"]
        qsedes.save()
        
        return Response({
            "ok": True,
            "mensaje": f"sede editado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error editando sede: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WCoSedesBorrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    qsedes = Sede.objects.filter(pk=pk).first()

    if qsedes is None:
        return Response({
            "ok": False,
            "mensaje": "sede no encontrada",
        }, status=400)
        

    # GUARDAR
    try:
        qsedes.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"sede borrado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando la sede: {str(e)}"
        }, status=400)
# sedes ##############################################################################login


# accion ##############################################################################
        
@api_view(['POST'])
@token_required
def WCoAccionLista(request):
    ListaAcciones =[]
    qAcciones = Actions.objects.all().order_by('AcName')
    
    try:

        if qAcciones:
            for acciones in qAcciones:
                ListaAcciones.append([acciones.pk, acciones.AcName, acciones.AcKey])
            return Response({
                "ok": True,
                "mensaje": "lista de Acciones",
                "ListaAcciones": ListaAcciones,
            })  
        else:
            return Response({
                "ok": False,
                "mensaje": "error al encontrar la accion",
            })
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando la accion: {str(e)}"
        }, status=400)
    
@api_view(['POST'])
# @token_required
def WCoAccionCrear(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("EAccion")

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "Formulario vacío",
        }, status=400)

    # GUARDAR
    try:
        Actions.objects.create(
            AcKey=data["llave"],
            AcName=data["nombre"],
        )
        
        return Response({
            "ok": True,
            "mensaje": f"accion creado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error guardando accion: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WCoAccionEditar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("EAccion")
    qAccion = Actions.objects.filter(pk=pk).first()

    if qAccion is None:
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
        qAccion.AcKey=data["llave"]
        qAccion.AcName=data["nombre"]
        qAccion.save()
        
        return Response({
            "ok": True,
            "mensaje": f"Accion editado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error editando Accion: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WCoAccionBorrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    qAccion = Actions.objects.filter(pk=pk).first()
    ok,status, mensaje = False, 400, ""
    # GUARDAR
    try:
        if qAccion:
            qAccion.delete()
            mensaje = "Accion borrada con exito"
            status = 200
            ok = True
        else:
            mensaje = "Accion no encontrada"
            
        
        return Response({
            "ok": ok,
            "mensaje": mensaje
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando la Accion: {str(e)}"
        }, status=400)
# sedes ##############################################################################login



# contraseña olvidad ########################################
#comprobar correo
@api_view(['POST'])
# @token_required
def WClcomprobar_correo(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    correo = request.data.get("email")
    
    qcorreo = Users.objects.filter(UsEmail=correo).first()
    correo_estado = False
    mensaje_correo = "correo no encontrado"
    correo = ""
    codigo = ""
    status = 400
    print("correo",correo)

    # GUARDAR
    try:
        if qcorreo:
            correo_estado = True
            mensaje_correo = "correo encontrado"
            status = 200
            
            codigo = WClgenerar_codigo()
            mensaje = {
                "usuario": qcorreo.UsUsername,
                "codigo": codigo,
                "empresa": "Saves",
            }
            WClgenerar_codigo()
            correo = qcorreo.UsEmail
            dominio_actual = correo.split('@')[-1]  # "gmail.com"
            # Buscar si el dominio coincide con alguno de la lista
            dominio = next((nombre for dom, nombre in DOMINIO_CORREO if dom == dominio_actual), 'otro')
            WClenvio_email(correo, "Código de verificación - Cambio de contraseña", mensaje, dominio, "")
            
            qcorreo.UsVerificationCode = codigo
            qcorreo.save()
            print("correo",correo)
            print("codigo",codigo)

        
        return Response({
            "ok": correo_estado,
            "correo_estado": correo_estado,
            "correo": correo,
            "codigo": codigo,
            "mensaje": mensaje_correo
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error: {str(e)}"
        }, status=400)
@api_view(['POST'])       
def WSgVerificarCodigo(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    correo = request.data.get("email")
    codigo = request.data.get("codigo")
    
    qusuario = Users.objects.filter(UsEmail=correo, UsVerificationCode=codigo).first()
    estado = False
    status = 400
    print("correo",correo)

    # GUARDAR
    try:
        if qusuario:
            estado = True
            status = 200
        
        return Response({
            "ok": estado,
            "correo": correo,
            "codigo": codigo,
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error: {str(e)}"
        }, status=400)
        
@api_view(['POST'])       
def WSgCambioContra(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    correo = request.data.get("email")
    codigo = request.data.get("codigo")
    contraseña = request.data.get("password")
    
    qusuario = Users.objects.filter(UsEmail=correo, UsVerificationCode=codigo).first()
    estado = False
    status = 400
    print("correo",correo)

    # GUARDAR
    try:
        if qusuario:
            estado = True
            status = 200
            qusuario.UsPass = make_password(contraseña)
            qusuario.save()
        
        return Response({
            "ok": estado,
            "correo": correo,
            "codigo": codigo,
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error: {str(e)}"
        }, status=400)
        
        
        #permisos
        
@token_required      
@api_view(['POST'])       
def WSgModulosAccionCrear(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("EModuloAccion")
    mensaje = ""
    estado = False
    status = 400
    try:
        for item in data["modulos"]:
            qmodulo = Modules.objects.filter(pk=item["modulo"]).first()
            if not qmodulo:
               mensaje = "no existe este modulo"
            
            else:
                permisos = item.get("permisos", {})
                
                for accion, permitido in permisos.items():
                    qaccion = Actions.objects.filter(AcKey=str(accion)).first()
                    if not qaccion:
                        print(f"Error: La acción {accion} no existe en la base de datos")
                        continue
                    print("accion",accion,permitido)
                    qs = ModuleActions.objects.filter(
                        MaModule=qmodulo,
                        MaAction=qaccion
                    )

                    if permitido:
                        # Crear si no existe
                        if not qs.exists():
                            ModuleActions.objects.create(
                                MaModule=qmodulo,
                                MaAction=qaccion
                            )
                    else:
                        # Eliminar si existe
                        qs.delete()
                mensaje = "permisos concedido o quitatdos"
                estado = True
                status = 200
                    
        return Response({
            "ok": estado,
            "mensaje": mensaje,
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error: {str(e)}"
        }, status=400)
    
@token_required      
@api_view(['POST']) 
def WSgModulosAccionLista(request):
    ListaModuloAccion =[]
    qModuleActions = ModuleActions.objects.all().order_by('MaModule__MdName')
    
    try:

        if qModuleActions:
            for mod in qModuleActions:
                ListaModuloAccion.append([mod.pk, mod.MaModule.MdName, mod.MaAction.AcName])
            return Response({
                "ok": True,
                "mensaje": "lista de sedes",
                "ListaModuloAccion": ListaModuloAccion,
            })  
        else:
            return Response({
                "ok": False,
                "mensaje": "error al encontrar los sede",
            })
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando la sede: {str(e)}"
        }, status=400)

###############################################     
@api_view(['POST'])
@token_required
def WSgModulosAccionBorrar(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    qModuleActions = ModuleActions.objects.filter(pk=pk).first()

    if qModuleActions is None:
        return Response({
            "ok": False,
            "mensaje": "Modulo Accion no encontrada",
        }, status=400)
        

    # GUARDAR
    try:
        qModuleActions.delete()
        
        return Response({
            "ok": True,
            "mensaje": f"Modulo Accion borrado con exito"
        })

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando el Modulo Accion: {str(e)}"
        }, status=400)
# sedes ##############################################################################login

@api_view(['POST'])
# @token_required
def WSgPermisos(request):

    llave = request.data.get("llave")
    nombre = request.data.get("nombre")
    modulo_accion = request.data.get("modulo_accion")

    if not llave or not nombre or not modulo_accion:
        return Response({
            "ok": False,
            "mensaje": "Faltan datos obligatorios"
        }, status=400)

    try:
        qpermiso, creado = Permissions.objects.get_or_create(
            PeKey=llave
        )
        
        qmodulo_accion = ModuleActions.objects.filter(pk=modulo_accion).first()

        qpermiso.PeName = nombre
        qpermiso.PeModuleActionId = qmodulo_accion
        qpermiso.save()

        return Response({
            "ok": True,
            "mensaje": "Permiso creado o actualizado"
        }, status=200)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error: {str(e)}"
        }, status=400)
        
# roles ##############################################################################
        
@api_view(['POST'])
@token_required
def WSgListarRol(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    lista_roles =[]
    
    qroles = Roles.objects.all().order_by('RoName')
    print(qroles)
    ok, mensaje, status = False, "", 400
    try:

        if qroles:
            mensaje = "lista de roles"
            ok = True
            status = 200
            for rol in qroles:
                lista_roles.append([rol.pk, rol.RoKey, rol.RoName, rol.RoDateCreated, rol.RoSystem]) 
        else:
            mensaje = "No hay roles registrados"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje,
            "lista_roles": lista_roles
        }, status=status)
    
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error listando roles: {str(e)}"
        }, status=400)
    
@api_view(['POST'])
@token_required
def WSgCrearRol(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("ERol")

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "Formulario vacío",
        }, status=400)
    
    campos_obligatorios = ["llave", "nombre", "estado"]
    comprobarCampos(data, campos_obligatorios)

    # GUARDAR
    try:
        rol = Roles.objects.create(
            RoKey=data["llave"],
            RoName=data["nombre"],
            RoSystem=data["estado"],
        )
        
        if "permisos" in data and data["permisos"]:
            rol.RoPermissions.set(data["permisos"])
        
        return Response({
            "ok": True,
            "mensaje": f"rol creado con exito"
        }, status=200)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error guardando rol: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WSgActualizarRol(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("ERol")
    qroles = Roles.objects.filter(pk=pk).first()

    if qroles is None:
        return Response({
            "ok": False,
            "mensaje": "rol no encontrado",
        }, status=400)
        
    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)
    
    campos_obligatorios = ["llave", "nombre", "estado"]
    comprobarCampos(data, campos_obligatorios)


    # GUARDAR
    try:
        qroles.RoKey=data["llave"]
        qroles.RoName=data["nombre"]
        qroles.RoSystem=data["estado"]
        qroles.save()
        
        return Response({
            "ok": True,
            "mensaje": f"rol editado con exito"
        }, status=200)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error editando rol: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WSgBorrarRol(request, pk):
    qRol = Roles.objects.filter(pk=pk).first()
    ok,status, mensaje = False, 400, ""
    # GUARDAR
    try:
        if qRol:
            qRol.delete()
            mensaje = "Rol borrada con exito"
            status = 200
            ok = True
        else:
            mensaje = "Rol no encontrada"
            
        
        return Response({
            "ok": ok,
            "mensaje": mensaje
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando el Rol: {str(e)}"
        }, status=400)
# roles ##############################################################################

@api_view(["GET"])
def WSgRolesVerPermisos(request, rol_id):
    try:
        rol = Roles.objects.get(pk=rol_id)

        permisos = rol.RoPermissions.all().values(
            "id",
            "PeKey",
            "PeName"
        )

        return Response({
            "ok": True,
            "rol": {
                "id": rol.id,
                "llave": rol.RoKey,
                "nombre": rol.RoName
            },
            "permisos": list(permisos)
        })

    except Roles.DoesNotExist:
        return Response({
            "ok": False,
            "mensaje": "Rol no encontrado"
        }, status=404)
    
# permisos ##############################################################################
        
@api_view(['POST'])
@token_required
def WSgListarPermisos(request):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    ListaPermisos =[]
    
    qpermisos = Permissions.objects.all().order_by('PeName')
    ok, mensaje, status = False, "", 400
    try:

        if qpermisos:
            mensaje = "lista de permisos"
            ok = True
            status = 200
            for permi in qpermisos:
                ListaPermisos.append([permi.pk, permi.PeModuleActionId.MaModule.MdName,permi.PeModuleActionId.MaAction.AcName, permi.PeName, permi.PeKey]) 
        else:
            mensaje = "No hay permisos registrados"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje,
            "ListaPermisos": ListaPermisos
        }, status=status)
    
    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error listando roles: {str(e)}"
        }, status=400)
    
from django.db import transaction       
@api_view(["POST"])
@transaction.atomic
def WSgPermisosCrear(request):
    data = request.data.get("EPermisos")
    qpermiso = Permissions.objects.all().first()

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)
    
    campos_obligatorios = ["ModuloAccion", "llave", "nombre"]
    comprobarCampos(data, campos_obligatorios)
    ok, status, mensaje = False,400,""

    # GUARDAR
    try:
        qmoduloAccion = ModuleActions.objects.filter(pk=data["ModuloAccion"]).first()
        if qmoduloAccion:
            if qpermiso:
                qpermiso.PeModuleActionId=qmoduloAccion
                qpermiso.PeKey=data["llave"]
                qpermiso.PeName=data["nombre"]
                qpermiso.save()
                ok, status, mensaje = True,200,"Permiso Guardado"
            else:
                mensaje = "permiso no registrado"

        else:
            mensaje = "Modulo accion no registrado"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error guardando permiso: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WSgActualizarPermisos(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    data = request.data.get("EPermisos")
    qpermiso = Permissions.objects.filter(pk=pk).first()
    qmodulo = ModuleActions.objects.filter(pk=data["ModuloAccion"]).first()

    if data is None:
        return Response({
            "ok": False,
            "mensaje": "formulario vacío",
        }, status=400)
    
    campos_obligatorios = ["ModuloAccion", "llave", "nombre"]
    comprobarCampos(data, campos_obligatorios)
    ok, status, mensaje = False,400,""

    # GUARDAR
    try:
        if qmodulo:
            if qpermiso:
                qpermiso.PeModuleActionId=qmodulo
                qpermiso.PeKey=data["llave"]
                qpermiso.PeName=data["nombre"]
                qpermiso.save()
                ok, status, mensaje = True,200,"Permiso editado"
            else:
                mensaje = "permiso no registrado"
        else:
            mensaje = "modulo no registrado"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error editando permiso: {str(e)}"
        }, status=400)
        
@api_view(['POST'])
@token_required
def WSgBorrarPermisos(request, pk):
    # Ya puedes acceder a request.empleado_name, request.rol, etc.
    qpermisos = Permissions.objects.filter(pk=pk).first()

    if qpermisos is None:
        return Response({
            "ok": False,
            "mensaje": "rol no encontrado",
        }, status=400)
        

    ok, status, mensaje = False,400,""

    # GUARDAR
    try:
        if qpermisos:
            qpermisos.delete()
            ok, status, mensaje = True,200,"Permiso Borrado con exito"

        else:
            mensaje = "permiso no registrado"
        
        return Response({
            "ok": ok,
            "mensaje": mensaje
        }, status=status)

    except Exception as e:
        return Response({
            "ok": False,
            "mensaje": f"Error borrando Permiso: {str(e)}"
        }, status=400)