import os
import django

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vestel.settings') 
django.setup()

# Importamos el modelo (Asegúrate que la app se llame 'login' o cámbialo)
from login.models import Users 
from django.contrib.auth.hashers import make_password
def run():
    print("--- Iniciando Script de Creación ---")
    try:
        # Solo llenamos UsRoleid (obligatorio) y los datos de login
        user, created = Users.objects.get_or_create(
            UsEmail="admin@empresa.com",
            defaults={
                "UsUsername": "Daniel",
                "UsPass": make_password("12345"),  # 👈 Encripta aquí
                "UsRoleid": 1,     # Único campo NOT NULL en tu tabla
                "UsBanned": 0,
                "UsSedeAccede": "SEDE1"
            }
        )

        if created:
            print("✅ Éxito: Usuario 'Daniel' creado correctamente.")
        else:
            print("ℹ️ Aviso: El usuario ya existe, no se realizaron cambios.")
            
    except Exception as e:
        print(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    run()