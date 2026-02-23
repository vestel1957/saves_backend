# # context_processors.py
# from django.shortcuts import redirect, render
# from login.models import *
# from SUPER_ADMIN.models import *

# def build_subitems(submenu):
#     """Construye recursivamente los hijos de un submenú"""
#     return [
#         {
#             "id": child.id,
#             "su_titulo": child.su_titulo,
#             "su_url": child.su_url,
#             "subitems": build_subitems(child)
#         }
#         for child in submenu.filter
#     ]

# def menu_dinamico(request):
#     modulos = []
#     if request.pk_usuario:
#         pk_usuario = request.pk_usuario
#         qusuario = usuarios.objects.filter(pk=pk_usuario.pk).first()
#         qmodulos = qusuario.us_tipo_usuario.ro_modulos.all().order_by('mo_nombre')
#         # qmodulos = modulo.objects.filter(mo_nombre__in=modulos).order_by("mo_nombre")
#         modulos = []

#         qsubmenu = sub_modulo.objects.all().order_by('su_nivel1','su_nivel2')

#         for modul in qmodulos:
#             modulos_json = {
#                 'id_modulo': modul.pk,
#                 'modulo_titulo': modul.mo_nombre,
#                 'modulo_imagen': modul.mo_imagen,
#                 'modulos': []
#             }

#             qsubmenu2 = qsubmenu.filter(su_modulo=modul.pk, su_nivel2=0)
#             for sub in qsubmenu2:
#                 sub_modulos_json = {
#                     'sub_id': sub.pk,
#                     'sub_titulo': sub.su_titulo,
#                     'sub_modulos2': []
#                 }

#                 qsubmenu3 = qsubmenu.filter(su_modulo=modul.pk, su_nivel1=sub.su_nivel1)
#                 for sub2 in qsubmenu3:
#                     if sub2.su_nivel2 > 0:
#                         sub_modulos_json2 = {
#                             'sub2_id': sub2.pk,
#                             'sub2_titulo': sub2.su_titulo,
#                             'sub2_url': sub2.su_url,
#                         }
#                         sub_modulos_json['sub_modulos2'].append(sub_modulos_json2)

#                 modulos_json['modulos'].append(sub_modulos_json)
#             modulos.append(modulos_json)
#     if request.empresa_nombre is None:
#         request.empresa_nombre = ""

#     return {
#         'rol':request.rol,
#         "json_modulos": modulos,
#         "nombre_modulo": "",
#         "empresa_logo": request.logo_empresa,
#         "usuario": request.usuario,
#         "empresa_nombre": request.empresa_nombre,
#     }
