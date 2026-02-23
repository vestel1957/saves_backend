# import os
# from datetime import date
# from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
# from django.urls import reverse_lazy

# from login.general import get_cookie_segura, firmar_cookie, validar_mi_token
# from login.models import empresas, usuarios
# from SUPER_ADMIN.models import *
# from caja.models import historial_caja
# from nomina.models import Employees

# class SeguridadMiddleware:

#     # ---------------------------------------------------------
#     #   MÉTODO PARA VALIDAR COOKIES, TOKEN, USUARIO Y EMPRESA
#     # ---------------------------------------------------------
#     def validar_url(self, request):
#         cod_empresa = get_cookie_segura(request, "CODIGO_EMPRESA")
#         usuario     = get_cookie_segura(request, "USUARIO")
#         token       = get_cookie_segura(request, "TOKEN_USER")

#         qusuario = Employees.objects.filter(email=usuario, active=True).first()

#         # Usuario no existe → sesión expirada
#         if not qusuario:
#             return render(request, "error_permisos.html")

#         # Token inválido
#         token = validar_mi_token(token)
#         if token != True:
#             return render(request, "error_token.html")

#         # Cookies manipuladas
#         if usuario == "Ataque":
#             if request.path != '/select_empresas' and cod_empresa == "Ataque":
#                 return render(request, "error_cookie.html")

#         # Cookies expiradas
#         if usuario == "Expiro":
#             if request.path != '/select_empresas' and cod_empresa == "Expiro":
#                 return render(request, "error_sesion.html")

#         # Guardar información del usuario en el request
#         tipo_usu = qusuario.us_tipo_usuario.ro_nombre
#         request.rol = tipo_usu
#         request.usuario = qusuario.us_nombre
#         request.pk_usuario = qusuario

#         # Logo por defecto
#         logo = "/media/sin_fondo.jpg"

#         # Si no es INICIAR, obtener información de la empresa
#         if tipo_usu != "INICIAR":
#             qempresa = empresas.objects.all().first()

#             if qempresa:
#                 request.empresa_nombre = qempresa.EmRazonSocial

#                 if qempresa.EmLogo and hasattr(qempresa.EmLogo, "path"):
#                     if os.path.isfile(qempresa.EmLogo.path):
#                         logo = qempresa.EmLogo.url

#                 elif qempresa.EmLogo2 and hasattr(qempresa.EmLogo2, "path"):
#                     if os.path.isfile(qempresa.EmLogo2.path):
#                         logo = qempresa.EmLogo2.url

#         request.logo_empresa = logo

#         # Validar permisos según URL
#         url = request.path.lstrip('/')

#         if url != 'menuPrinci':
#             qmodal = sub_modulo.objects.filter(su_url=url).first()

#             if qmodal:
#                 qroles = roles.objects.filter(
#                     ro_modulos=qmodal.su_modulo,
#                     ro_nombre=tipo_usu
#                 )

#                 if not qroles:
#                     return render(request, "error_permisos.html")

#         return None  # Todo OK


#     # ---------------------------------------------------------
#     #   INICIO DEL MIDDLEWARE
#     # ---------------------------------------------------------
#     def __init__(self, get_response):
#         self.get_response = get_response

#     # ---------------------------------------------------------
#     #   EJECUCIÓN PRINCIPAL DEL MIDDLEWARE
#     # ---------------------------------------------------------
#     def __call__(self, request):

#         # Inicializar variables del request
#         request.rol = ""
#         request.usuario = ""
#         request.pk_usuario = ""
#         request.logo_empresa = ""
#         request.empresa_nombre = ""

#         # -----------------------------------
#         # RUTAS LIBRES (NO REQUIEREN LOGIN)
#         # -----------------------------------

#         request.rol = ""
#         request.usuario = ""
#         request.pk_usuario = ""
#         request.logo_empresa = ""
#         request.empresa_nombre = "222222"
#         # Rutas libres sin restricciones
#         if (request.path == '/' or 
#             request.path.startswith(('/login', '/admin/', '/static/', '/media/'))):
#             return self.get_response(request)

#         # Obtener cookies normales
#         usuario = get_cookie_segura(request, "USUARIO")
#         token   = get_cookie_segura(request, "TOKEN_USER")
#         CAJA_HISTORIAL = get_cookie_segura(request, "CAJA_HISTORIAL")
#         cod_emp = get_cookie_segura(request, "CODIGO_EMPRESA")

#         # -----------------------------------
#         # RUTA /select_empresas
#         # -----------------------------------
#         if request.path == '/select_empresas':

#             if usuario == "Ataque" or token == "Ataque":
#                 print("1")
#                 return render(request, "error_cookie.html")
#             elif usuario == "Expiro" or token == "Expiro":
#                 print("2")
                
#                 return render(request, "error_sesion.html")
#             print("3")

#             qusuario = usuarios.objects.filter(us_usuario=usuario).first()
#             if not qusuario:
#                 print("4")
                
#                 return render(request, "error_sesion.html")

#             if qusuario.us_token != token:
#                 print("33")
                
#                 return render(request, "error_token.html")

#             tipo_usu = qusuario.us_tipo_usuario.ro_nombre

#             if tipo_usu not in ["PROGRAMADOR", "ADMIN", "INICIAR"]:
#                 prefijo_sede = qusuario.us_sede
#                 empresa = qusuario.us_prefijo_empresa
#                 año_actual = date.today().year
#                 cod_emp = f"{empresa}{año_actual}-{prefijo_sede}"

#                 response = HttpResponseRedirect(reverse_lazy('menuPrinci'))
#                 firmar_cookie(response, "CODIGO_EMPRESA", cod_emp, 3600)
#                 return response

#             elif tipo_usu == "INICIAR":
#                 return HttpResponseRedirect(reverse_lazy('empresas_crear'))

#         # -----------------------------------
#         # RUTA /caja_pagos
#         # -----------------------------------
#         if request.path == "/caja_pagos":

#             if CAJA_HISTORIAL:

#                 if CAJA_HISTORIAL == "Ataque":
#                     return render(request, "error_token.html")

#                 if CAJA_HISTORIAL == "Expiro":
#                     return render(request, "error_permisos.html")


#                 resp = self.validar_url(request)
#                 if resp: return resp

#             else:
#                 return redirect("caja_apertura")

#         # -----------------------------------
#         # RUTA /caja_apertura
#         # -----------------------------------
#         if request.path == "/caja_apertura":

#             quser = usuarios.objects.filter(us_usuario=usuario).first()

#             qhistorial = historial_caja.objects.filter(
#                 hc_codigo_empresa=cod_emp,
#                 hc_usuario=quser.pk,
#                 hc_estatus="A"
#             ).first()

#             if qhistorial:
#                 response = redirect("caja_pagos")
#                 firmar_cookie(response, "CAJA_HISTORIAL", qhistorial.pk, 9 * 3600)
#                 return response

#             resp = self.validar_url(request)
#             if resp: return resp

#         # -----------------------------------
#         # OTRAS RUTAS (VALIDAR SIEMPRE)
#         # -----------------------------------
#         resp = self.validar_url(request)
#         if resp:
#             return resp

#         # -----------------------------------
#         # CONTINUAR PROCESO NORMAL
#         # -----------------------------------
#         return self.get_response(request)
