from django.core.signing import Signer, BadSignature

## biblioteca del envio de correo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
import os
import traceback
import base64

from almacenamiento.models import Contadores
from login.models import Users
from nomina.models import Employees


signer = Signer()
def consulta_contadores(nombre, prefijo, tipo,cod_emp):
    serial_entrada = 0
    qcontadores = Contadores.objects.filter(CoNombre=nombre).last()
    print("qcontadores",qcontadores)
    if qcontadores:
        if tipo == "consulta":
            contador = qcontadores.CoNumeroContador
        else:
            contador = qcontadores.CoNumeroContador + 1
        serial_entrada = contador
    else:
        serial_entrada += 1
        qcontadores = Contadores()
        qcontadores.CoNombre = nombre
        qcontadores.CoPrefijo = prefijo
        qcontadores.CoCodEmp = f"{cod_emp[:4]}-{cod_emp[-1:]}"

    qcontadores.CoNumeroContador = serial_entrada
    qcontadores.save()
    return serial_entrada

def get_cookie_segura(request, nombre_cookie: str):
    """
    Devuelve el valor de la cookie ya validado.
    Si la cookie fue alterada, devuelve None.
    """
    valor_firmado = request.COOKIES.get(nombre_cookie)

    if not valor_firmado:
        return "Expiro"  # Cookie no existe

    try:
        return signer.unsign(valor_firmado)  # Devuelve valor original si es válido
    except BadSignature:
        return "Ataque"  # Cookie manipulada → posible ataque
    

def firmar_cookie(response, nombre_cookie: str, valor: str, duracion: int):
    """
    Firma un valor con Django y lo guarda como cookie segura.
    """
    valor_firmado = signer.sign(valor)

    response.set_cookie(
        nombre_cookie,       # <-- NOMBRE FIJO
        valor_firmado,       # <-- VALOR FIRMADO
        max_age=duracion,
        secure=True,         # Solo HTTPS
        # httponly=True,       # No accesible por JavaScript
        samesite='Lax'       # Protección contra CSRF básica
    )

    return response

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

def validar_mi_token(token_recibido):
    try:
        # Esto valida automáticamente la firma y la expiración
        token = AccessToken(token_recibido)
        
        # Acceder a los datos que guardaste
        id_empleado = token['empleado_id']
        rol_usuario = token['rol']
        
        print(f"Usuario {id_empleado} con rol {rol_usuario} validado.")
        return True
    except Exception as e:
        print("Token inválido o expirado")
        return False
    
HTML_CORREOS_FACTURACION = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Código de verificación</title>

<style>
  /* Las llaves del CSS están duplicadas para evitar conflictos con str.format */
  :root {{
    --bg: #f6f7fb;
    --card: #ffffff;
    --primary: #1e66f5;
    --text: #2b2b2b;
    --muted: #6b7280;
    --border: #e5e7eb;
    --warning: #f59e0b;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
  }}

  .wrapper {{
    width: 100%;
    padding: 24px 12px;
    background: var(--bg);
  }}

  .container {{
    max-width: 640px;
    margin: 0 auto;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  }}

  .header {{
    background: linear-gradient(135deg, #1e66f5 0%, #0ea5e9 100%);
    color: #fff;
    padding: 24px 28px;
  }}

  .brand {{
    font-size: 18px;
    font-weight: 700;
    letter-spacing: .3px;
  }}

  .title {{
    margin-top: 8px;
    font-size: 24px;
    font-weight: 700;
  }}

  .content {{
    padding: 28px;
    line-height: 1.6;
  }}

  .greeting {{
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 16px;
  }}

  .note {{
    margin-top: 0;
    margin-bottom: 20px;
    color: var(--muted);
  }}

  .code-box {{
    width: 100%;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    background: #f9fafb;
    margin-bottom: 16px;
  }}

  .code {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 6px;
    color: var(--primary);
  }}

  .expire {{
    font-size: 13px;
    color: var(--muted);
    margin-top: 6px;
  }}

  .warning {{
    margin-top: 16px;
    font-size: 13px;
    color: var(--warning);
  }}

  .footer {{
    padding: 16px 24px 28px 24px;
    text-align: center;
    font-size: 12px;
    color: var(--muted);
  }}

  @media (max-width: 480px) {{
    .content {{ padding: 20px; }}
    .code {{ font-size: 24px; letter-spacing: 4px; }}
  }}
</style>
</head>

<body>
  <div class="wrapper">
    <div class="container">

      <div class="header">
        <div class="brand">{empresa}</div>
        <div class="title">Código de verificación</div>
      </div>

      <div class="content">
        <p class="greeting">Hola {usuario},</p>

        <p class="note">
          Has solicitado restablecer tu contraseña.
          Usa el siguiente código para continuar con el proceso.
        </p>

        <div class="code-box">
          <div class="code">{codigo}</div>

        </div>

        <p class="warning">
          ⚠️ Si no solicitaste este cambio, ignora este correo.
        </p>
      </div>

      <div class="footer">
        © {empresa}. Este correo fue generado automáticamente, por favor no respondas a este mensaje.
      </div>

    </div>
  </div>
</body>
</html>
"""

def comprobar_base64(cadena):
    """
    Devuelve True si la cadena parece ser base64 válida, False en caso contrario.
    """
    if not isinstance(cadena, str):
        return False

    # Quitar espacios o saltos de línea
    cadena = cadena.strip()

    # La longitud de una cadena base64 siempre es múltiplo de 4
    if len(cadena) % 4 != 0:
        return False

    try:
        base64.b64decode(cadena, validate=True)
        return True
    except Exception:
        return False
    
def envio_email(receptor,cabeza_mensaje,mensaje,dominio,archivos_adjuntos=None):
    email1 = "smtp." + dominio
    puerto = 587
    email_envio = "danielmahecha43@gmail.com"
    contrasena_envio = "lbex tfxp wbiy zwfp"
    html = HTML_CORREOS_FACTURACION
    try:
        smtp_obj = smtplib.SMTP(email1,puerto)
        smtp_obj.starttls()
        smtp_obj.login(user=email_envio,password=contrasena_envio)

        email_mensaje = MIMEMultipart("alternative")
        email_mensaje["From"] = receptor
        email_mensaje["To"] = str(receptor)
        email_mensaje["Subject"] = Header(cabeza_mensaje)
        body_html = html.format(
                usuario=mensaje["usuario"],
                codigo=mensaje["codigo"],
                empresa=mensaje["empresa"],
            )
        
        # Adjuntar archivos (PDF o cualquier otro)
        if archivos_adjuntos:
            for nombre_archivo, archivo in archivos_adjuntos:
                if comprobar_base64(archivo):
                    # ✅ Si es base64: decodificarlo y adjuntarlo
                    contenido = base64.b64decode(archivo)
                    adjunto = MIMEApplication(contenido, _subtype="pdf")
                    adjunto.add_header("Content-Disposition", "attachment", filename=nombre_archivo)
                else:
                    # ✅ Si no es base64: abrir el archivo desde disco
                    with open(archivo, "rb") as f:
                        contenido = f.read()
                        nombre = os.path.basename(archivo)
                        adjunto = MIMEApplication(contenido, _subtype="pdf")
                        adjunto.add_header("Content-Disposition", "attachment", filename=nombre)

                # Adjuntar el MIME al correo
                email_mensaje.attach(adjunto)

        email_mensaje.attach(MIMEText(body_html, 'html'))
        smtp_obj.send_message(email_mensaje)

        smtp_obj.quit()
        return True
            
    except Exception as e:
        print("eror", e)
        print(traceback.format_exc())  # traza completa para ver en qué campo
        return False
    
import secrets
import string
from functools import wraps
def generar_codigo(longitud=6):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def token_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"ok": False, "mensaje": "Token no proporcionado"}, status=401)

        token_str = auth_header.split(" ")[1]
        try:
            token = AccessToken(token_str)
            empleado_id = token.get('empleado_id')
            empleado = Users.objects.filter(pk=empleado_id).first()

            if not empleado:
                return Response({"ok": False, "mensaje": "Usuario Login no encontrado"}, status=401)

            # Inyectamos todo en request
            request.empleado = empleado
            request.empleado_id = empleado.id
            request.empleado_name = empleado.UsUsername
            request.rol = empleado.UsRoleid

            return func(request, *args, **kwargs)

        except Exception as e:
            print("ERROR TOKEN:", e)
            return Response({"ok": False, "mensaje": "Token inválido o expirado"}, status=401)

    return wrapper

import re
def validar_numeros(numero, texto):
    """
    Sirve para validar numeros como lo son numeros de telefono o de cedula
    Args:
        numero (str): cadena que contiene el numero a validar
    """
    numero_limpio = re.sub(r'[^0-9]', '', numero)
    if numero_limpio.isdigit():
      print("numero válido")
      return numero_limpio
    else:
      return Response({
          "ok": False,
          "mensaje": f"error de {texto}",
      })
    
####### incriptacin contraseñas de equipos y demas #  #### # #
    
from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_KEY)

def encrypt_value(value):
    return fernet.encrypt(value.encode()).decode()

def decrypt_value(value):
    return fernet.decrypt(value.encode()).decode()