from django.db import models
import os
from django.conf import settings

# Create your models here.
class Actions(models.Model):
    """
    ACCIONES DISPONIBLES DENTRO DEL SISTEMA
    """
    AcKey = models.CharField("LLAVE DE LA ACCION", max_length=50, default="")
    AcName = models.CharField("NOMBRE DE LA ACCION", max_length=100, default="")
   
    def __str__(self) -> str:
        return f"{self.AcName}"

    class Meta:
        db_table = "Acciones"
        
class ModuleGroup(models.Model):
    """
    TABLA: MODULOS PADRES (Ej: INVENTORY, SETTINGS)
    """
    MgNombre = models.CharField("NOMBRE DEL GRUPO", max_length=100)
    MgIcono = models.CharField("ICONO (FontAwesome)", max_length=50, default="fa-folder", null=True, blank=True)
    MgOrden = models.IntegerField("ORDEN EN EL MENU", unique=True)

    def __str__(self) -> str:
        return self.MgNombre

    class Meta:
        db_table = "ModuleGroup"
        
class Modules(models.Model):
    """
    SUBMODULOS O PANTALLAS REALES (Ej: Traslados, Kardex)
    """
    MdKey = models.CharField("LLAVE DEL MODAL", max_length=100, default="")
    MdName = models.CharField("NOMBRE DEL MODAL", max_length=150, default="")
    MdDateCreated = models.DateField('FECHA CREACION', auto_now_add=True)
    MdUrl = models.CharField("NOMBRE DEL MODAL", max_length=150, default="")
    # Este es el campo clave para crear la jerarquía
    # Relación con el Padre
    MdPadre = models.ForeignKey(ModuleGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='hijos')
    
    def __str__(self) -> str:
        return f"{self.MdName}"

    class Meta:
        db_table = "Modules"
        
class ModuleActions(models.Model):
    """
    ACCIONES DISPONIBLES DENTRO DEL MODULO
    """
    MaModule = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True) 
    MaAction = models.ForeignKey(Actions, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self) -> str:
        return f"{self.MaModule.MdName} - {self.MaAction.AcName}"

    class Meta:
        db_table = "ModuleActions"
        
class Permissions(models.Model):
    """
    PERMISOS QUE TENDRAN LOS USUARIOS
    """
    PeModuleActionId = models.ForeignKey(ModuleActions, on_delete=models.CASCADE, null=True, blank=True) 
    PeKey = models.CharField("LLAVE DE LOS PERMISOS", max_length=100, default="")
    PeName = models.CharField("NOMBRE", max_length=150, default="")

    def __str__(self) -> str:
        return f"{self.PeModuleActionId.MaModule.MdName} - {self.PeModuleActionId.MaAction.AcName}"

    class Meta:
        db_table = "Permissions"
        
class Roles(models.Model):
    RoKey =  models.CharField("LLAVE DEL ROL", max_length=100, default="")
    RoName = models.CharField("NOMBRE DEL ROL", max_length=100, default="")
    RoSystem = models.BooleanField('',default=True)
    RoDateCreated =  models.DateField('FECHA CREACION', auto_now_add=True)
    RoPermissions = models.ManyToManyField(Permissions, related_name="roles", blank=True)
    
    def __str__(self) -> str:
        return f"{self.RoName}"

    class Meta:
        db_table = "Roles"
        
        
def logo_empresa_path(instance, filename):
    """
    Genera la ruta dinámica:
    <BASE_DIR>/informacion_externa/<COD_EMPRESA>/logo/<filename>
    """
    # Carpeta base dentro del proyecto
    base_path = os.path.join(settings.BASE_DIR, "informacion_externa", str(instance.EmCodEempresa), "logo")
    # Crear carpeta si no existe
    os.makedirs(base_path, exist_ok=True)
    
    # Retorna la ruta relativa que Django usará
    return os.path.join("informacion_externa", str(instance.EmCodEempresa), "logo", filename) 

# Create your models here.
class Departamentos(models.Model):

    DeNombreDepartamento = models.CharField("NOMBRE DEL DEPARTAMENTO", max_length=100, default="")
   
    def __str__(self) -> str:
        return f"{self.DeNombreDepartamento}"

    class Meta:
        db_table = "Departamentos"
     
class Ciudades(models.Model):

    CiDepartamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, related_name="municipios")
    CiNombre = models.CharField("NOMBRE DEL MUNICIPIOS", max_length=100, default="")
   
    def __str__(self) -> str:
        return f"{self.CiNombre}"

    class Meta:
        db_table = "Ciudades"

class Empresas(models.Model):
    # repre siginifica representante
    EmRazonSocial = models.CharField("RAZON SOCIAL", max_length=200)
    EmNit = models.CharField("NIT", max_length=20, unique=True)
    EmCodEempresa = models.CharField("codigo de la empresa", max_length=20, unique=True, default="")
    EmDireccion = models.CharField("DIRECCION",max_length=255)
    EmTelefono = models.CharField("TELEFONO", max_length=20)
    EmProduccion = models.CharField("PRODUCCION", max_length=1, default="0")
    EmCorreo = models.EmailField("CORREO ELECTRONICO")
    EmCiudad = models.ForeignKey(Ciudades, on_delete=models.CASCADE)
    # Em_departamento = models.CharField("DEPARTAMENTO", max_length=100)
    EmPais = models.CharField("PAIS", max_length=3, default="CO")
    EmLogo = models.ImageField("LOGO", upload_to=logo_empresa_path, blank=True, null=True)
    EmLogo2 = models.ImageField("LOGO2", upload_to=logo_empresa_path, blank=True, null=True)
    EmEstado = models.CharField("ESTADO",max_length=10, default="A")
    EmFechaCreacion = models.DateField("FECHA CREACION",auto_now_add=True)
    EmReprNombre =  models.CharField("Nombre del dueño", max_length=200)
    EmRepreTipoDocumento = models.CharField("TIPO DOCUMENTO",max_length=40)
    EmRepreDocumento = models.CharField("NUMERO DOCUMENTO DEL DUEÑO",max_length=30)
    EmRepreTelefono = models.CharField("TELEFONO DEL DUEÑO",max_length=20,)
    EmRepreDireccion = models.CharField("DIRECCION DEL DUEÑO", max_length=255)

    def __str__(self):
        return f"{self.EmRazonSocial} - {self.EmNit}"

    class Meta:
        db_table = "Empresa"


class Sede(models.Model):
    SeEmpresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    SeLetra = models.CharField(max_length=2)  # Siempre 'A' por defecto
    SeNombre = models.CharField(max_length=100, default='')
    SeDireccion = models.CharField(max_length=255, blank=True, null=True)
    SeMunicipio = models.ForeignKey(Ciudades, on_delete=models.CASCADE)
    SeEstado = models.CharField("estado sede",max_length=1, default="A")
    SeTelefono = models.CharField("TELEFONO", max_length=20)
    SeCorreo = models.EmailField("CORREO ELECTRONICO", default="")
    SeTokenWhatsapp = models.TextField(blank=True, null=True)
    SeIdentificadorWhatsapp = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.SeNombre} - Sede: {self.SeLetra}"


    class Meta:
        db_table = "Sede"

# Create your models here.
class Localidad(models.Model):

    LoCiudad = models.ForeignKey(Ciudades, on_delete=models.CASCADE, related_name="localidades")
    LoNombreLocalidad = models.CharField("NOMBRE DE LA LOCALIDAD", max_length=100, default="")
   
    def __str__(self) -> str:
        return f"{self.LoNombreLocalidad}"

    class Meta:
        db_table = "Localidad"

# Create your models here.
class Barrios(models.Model):
    BaMunicipio = models.ForeignKey(Ciudades, on_delete=models.CASCADE, related_name="barrios")
    BaLocalidad = models.ForeignKey(
        Localidad,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="barrios"
    )
    BaNombreBarrio = models.CharField("NOMBRE DEL BARRIO", max_length=100, default="")
   
    def __str__(self) -> str:
        return f"{self.BaNombreBarrio}"

    class Meta:
        db_table = "Barrios"

from django.db import models

class Users(models.Model):
    # --- CAMPOS BASE ---
    UsEmail = models.EmailField("EMAIL", max_length=100, null=True, blank=True)
    UsPass = models.CharField("PASSWORD", max_length=255, null=True, blank=True)
    UsUsername = models.CharField("NOMBRE DE USUARIO", max_length=100, null=True, blank=True)
    UsBanned = models.IntegerField("BANEADO", null=True, blank=True)
    UsLastLogin = models.DateTimeField("ULTIMO LOGIN", null=True, blank=True)
    UsLastActivity = models.DateTimeField("ULTIMA ACTIVIDAD", null=True, blank=True)
    UsDateCreated = models.DateTimeField("FECHA CREACION", null=True, blank=True)
    UsForgotExp = models.TextField("FORGOT EXP", null=True, blank=True)
    UsRememberTime = models.DateTimeField("REMEMBER TIME", null=True, blank=True)
    UsRememberExp = models.TextField("REMEMBER EXP", null=True, blank=True)
    UsVerificationCode = models.TextField("VERIFICATION CODE", null=True, blank=True)
    UsTotpSecret = models.CharField("TOTP SECRET", max_length=16, null=True, blank=True)
    UsIpAddress = models.TextField("IP ADDRESS", null=True, blank=True)
    UsFinicial = models.DateField("FECHA INICIAL", null=True, blank=True)
    UsHinicial = models.TimeField("HORA INICIAL", null=True, blank=True)
    UsFcierre = models.DateField("FECHA CIERRE", null=True, blank=True)
    UsHcierre = models.TimeField("HORA CIERRE", null=True, blank=True)
    UsRoleid = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    UsPicture = models.CharField("PICTURE", max_length=50, null=True, blank=True)
    UsSedeAccede = models.CharField("SEDE ACCEDE", max_length=25, null=True, blank=True)

    # --- PERMISOS Y MODULOS (128 CAMPOS EN TOTAL) ---
    UsCo = models.IntegerField(null=True, blank=True)
    UsCoape = models.IntegerField(null=True, blank=True)
    UsConue = models.IntegerField(null=True, blank=True)
    UsCoadm = models.IntegerField(null=True, blank=True)
    UsCocie = models.IntegerField(null=True, blank=True)
    UsCofa = models.IntegerField(null=True, blank=True)
    UsCofae = models.IntegerField(null=True, blank=True)
    UsConotas = models.IntegerField(null=True, blank=True)
    UsUs = models.IntegerField(null=True, blank=True)
    UsUsnue = models.IntegerField(null=True, blank=True)
    UsUsadm = models.IntegerField(null=True, blank=True)
    UsUsgru = models.IntegerField(null=True, blank=True)
    UsTik = models.IntegerField(null=True, blank=True)
    UsTiknue = models.IntegerField(null=True, blank=True)
    UsTikadm = models.IntegerField(null=True, blank=True)
    UsMo = models.IntegerField(null=True, blank=True)
    UsMonue = models.IntegerField(null=True, blank=True)
    UsMoadm = models.IntegerField(null=True, blank=True)
    UsPro = models.IntegerField(null=True, blank=True)
    UsPronue = models.IntegerField(null=True, blank=True)
    UsProadm = models.IntegerField(null=True, blank=True)
    UsEnc = models.IntegerField(null=True, blank=True)
    UsEncllam = models.IntegerField(null=True, blank=True)
    UsEncnue = models.IntegerField(null=True, blank=True)
    UsEncenc = models.IntegerField(null=True, blank=True)
    UsEncats = models.IntegerField(null=True, blank=True)
    UsEncatslis = models.IntegerField(null=True, blank=True)
    UsProy = models.IntegerField(null=True, blank=True)
    UsProynue = models.IntegerField(null=True, blank=True)
    UsProyadm = models.IntegerField(null=True, blank=True)
    UsCuen = models.IntegerField(null=True, blank=True)
    UsCuenadm = models.IntegerField(null=True, blank=True)
    UsCuennue = models.IntegerField(null=True, blank=True)
    UsCuenbal = models.IntegerField(null=True, blank=True)
    UsCuendec = models.IntegerField(null=True, blank=True)
    UsRed = models.IntegerField(null=True, blank=True)
    UsReding = models.IntegerField(null=True, blank=True)
    UsRedadm = models.IntegerField(null=True, blank=True)
    UsRedbod = models.IntegerField(null=True, blank=True)
    UsRedcon = models.IntegerField(null=True, blank=True)
    UsComp = models.IntegerField(null=True, blank=True)
    UsComnue = models.IntegerField(null=True, blank=True)
    UsComadm = models.IntegerField(null=True, blank=True)
    UsTes = models.IntegerField(null=True, blank=True)
    UsTestran = models.IntegerField(null=True, blank=True)
    UsTesanu = models.IntegerField(null=True, blank=True)
    UsTesnuetransac = models.IntegerField(null=True, blank=True)
    UsTesnuetransfer = models.IntegerField(null=True, blank=True)
    UsTesing = models.IntegerField(null=True, blank=True)
    UsTesgas = models.IntegerField(null=True, blank=True)
    UsTestransfer = models.IntegerField(null=True, blank=True)
    UsDat = models.IntegerField(null=True, blank=True)
    UsDatest = models.IntegerField(null=True, blank=True)
    UsDatdec = models.IntegerField(null=True, blank=True)
    UsDatrep = models.IntegerField(null=True, blank=True)
    UsDatusu = models.IntegerField(null=True, blank=True)
    UsDatpro = models.IntegerField(null=True, blank=True)
    UsDating = models.IntegerField(null=True, blank=True)
    UsDatgas = models.IntegerField(null=True, blank=True)
    UsDattrans = models.IntegerField(null=True, blank=True)
    UsDatimp = models.IntegerField(null=True, blank=True)
    UsDathistorial = models.IntegerField(null=True, blank=True)
    UsDatservicios = models.IntegerField(null=True, blank=True)
    UsNot = models.IntegerField(null=True, blank=True)
    UsCal = models.IntegerField(null=True, blank=True)
    UsDoct = models.IntegerField(null=True, blank=True)
    UsPag = models.IntegerField(null=True, blank=True)
    UsPagconf = models.IntegerField(null=True, blank=True)
    UsPagvia = models.IntegerField(null=True, blank=True)
    UsPagmon = models.IntegerField(null=True, blank=True)
    UsPagcam = models.IntegerField(null=True, blank=True)
    UsPagban = models.IntegerField(null=True, blank=True)
    UsInv = models.IntegerField(null=True, blank=True)
    UsInving = models.IntegerField(null=True, blank=True)
    UsInvadm = models.IntegerField(null=True, blank=True)
    UsInvcat = models.IntegerField(null=True, blank=True)
    UsInvalm = models.IntegerField(null=True, blank=True)
    UsInvtrs = models.IntegerField(null=True, blank=True)
    UsEmp = models.IntegerField(null=True, blank=True)
    UsCom = models.IntegerField(null=True, blank=True)
    UsComprec = models.IntegerField(null=True, blank=True)
    UsCompurl = models.IntegerField(null=True, blank=True)
    UsComptwi = models.IntegerField(null=True, blank=True)
    UsCompcurr = models.IntegerField(null=True, blank=True)
    UsPla = models.IntegerField(null=True, blank=True)
    UsPlacor = models.IntegerField(null=True, blank=True)
    UsPlamen = models.IntegerField(null=True, blank=True)
    UsPlatem = models.IntegerField(null=True, blank=True)
    UsConf = models.IntegerField(null=True, blank=True)
    UsConfemp = models.IntegerField(null=True, blank=True)
    UsConffa = models.IntegerField(null=True, blank=True)
    UsConfmon = models.IntegerField(null=True, blank=True)
    UsConffec = models.IntegerField(null=True, blank=True)
    UsConfcat = models.IntegerField(null=True, blank=True)
    UsConfmet = models.IntegerField(null=True, blank=True)
    UsConfrest = models.IntegerField(null=True, blank=True)
    UsConfcorr = models.IntegerField(null=True, blank=True)
    UsConfterm = models.IntegerField(null=True, blank=True)
    UsConfaut = models.IntegerField(null=True, blank=True)
    UsConfseg = models.IntegerField(null=True, blank=True)
    UsConftem = models.IntegerField(null=True, blank=True)
    UsConfsop = models.IntegerField(null=True, blank=True)
    UsConface = models.IntegerField(null=True, blank=True)
    UsConfupt = models.IntegerField(null=True, blank=True)
    UsConfapi = models.IntegerField(null=True, blank=True)
    UsTar = models.IntegerField(null=True, blank=True)
    UsFechaUltimoEvento = models.DateField("FECHA ULTIMO EVENTO", null=True, blank=True)

    def __str__(self):
        return f"{self.UsUsername} ({self.UsEmail})"

    class Meta:
        db_table = "Users"