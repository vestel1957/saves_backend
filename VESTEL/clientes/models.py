from django.db import models
from login.models import *
# from django_cryptography.fields import encrypt

class GrupoCliente(models.Model):
    """
    TABLA: MODULOS PADRES (Ej: INVENTORY, SETTINGS)
    """
    GcNombre = models.CharField("NOMBRE DEL GRUPO", max_length=100)
    GcDescripcion = models.CharField("DESCRIPCION DEL GRUPO", max_length=150)
    GtDir = models.CharField("direccion", max_length=100)
    GtCodEmp = models.CharField("codigo empresa", max_length=20, default="")

    def __str__(self) -> str:
        return self.GcNombre

    class Meta:
        db_table = "GrupoCliente"

# Create your models here.
class Clientes(models.Model):
    # Fechas
    CliNacimiento = models.DateField(null=True, blank=True) ##########
    CliFechaContrato = models.DateField(null=True, blank=True)
    CliFechaIngreso = models.DateField(auto_now_add=True,null=True, blank=True)
    CliFechaGeneraEstadoUser = models.DateField(null=True, blank=True)
    CliFechaCambio = models.DateTimeField(auto_now=True,null=True, blank=True)
    CliCodEmp = models.CharField('CODIGO empresa-año-sede', default="")

    # Valores numéricos
    CliBalance = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    CliAbonado = models.IntegerField(null=True, blank=True)
    CliClausula = models.IntegerField(default=0) ##########
    CliCheckedSeleccionado = models.IntegerField(default=0)
    CliNumero3 = models.BigIntegerField(null=True, blank=True)
    CliGid = models.IntegerField(default=1)

    # Textos largos
    CliCompany = models.TextField(null=True, blank=True)
    CliTipoCliente = models.TextField("si es natural juridico",null=True, blank=True) ##########
    CliTipoDocumento = models.TextField("si es cc etc",null=True, blank=True) ##########
    CliUsuEstado = models.TextField(null=True, blank=True)

    # Flags
    CliFacturarElectronicamente = models.BooleanField(null=True, blank=True)
    CliServicioInstalacion = models.BooleanField("TELEVISION O INTERNET",null=True, blank=True)
    CliFElecPuntos = models.BooleanField(null=True, blank=True)
    CliFirmaDigital = models.BooleanField(null=True, blank=True)

    # Datos personales
    CliNombreTitular = models.CharField(max_length=20) ############
    CliDocumento = models.CharField(max_length=100, null=True, blank=True, unique=True) ###########
    CliEmail = models.CharField(max_length=60, null=True, blank=True) ###########
    CliEstrato = models.CharField(max_length=30, null=True, blank=True) ##########
 
    # Contacto
    CliCelular = models.CharField(max_length=20, null=True, blank=True) ###############
    CliCelular2 = models.CharField("telefono adi",max_length=20, null=True, blank=True) ###############

    # Dirección
    CliDepartamento = models.ForeignKey(
        Departamentos,
        on_delete=models.PROTECT,
        related_name="clientes",
        null=True,
        blank=True
    )

    CliCiudad = models.ForeignKey(
        Ciudades,
        on_delete=models.PROTECT,
        related_name="clientes",
        null=True,
        blank=True
    )

    CliLocalidad = models.ForeignKey(
        Localidad,
        on_delete=models.PROTECT,
        related_name="clientes",
        null=True,
        blank=True
    )

    CliBarrio = models.ForeignKey(
        Barrios,
        on_delete=models.PROTECT,
        related_name="clientes",
        null=True,
        blank=True
    )

    CliGrupoCliente = models.ForeignKey(
        GrupoCliente,
        on_delete=models.PROTECT,
        related_name="grupo_clientes",
        null=True,
        blank=True
    )

    CliNomenclatura = models.CharField("carrera, calle",max_length=50, null=True, blank=True) # Calle / Carrera / Diagonal
    CliNumeroVia = models.CharField(max_length=10, default='NULL') ##########
    CliAdicionalVia = models.CharField(max_length=10, default='NULL') ##########
    CliViaSecundaria = models.CharField(max_length=20, default='NULL') ##########
    CliAdicionalSecundaria = models.CharField(max_length=10, default='NULL') ##########
    CliNumeroCasa = models.CharField(max_length=10, default='NULL') ##########
    CliTipoResidencia = models.CharField(max_length=50, default='NULL') ##########
    CliReferencia = models.CharField("referencia de la direccion",max_length=50, null=True, blank=True) ##########

    CliDireccionCompleta = models.TextField("direccion completa", null=True, blank=True) ##########

    CliDirsuscriptor = models.CharField(max_length=100, null=True, blank=True) ##########
    CliDivNum1 = models.IntegerField(null=True, blank=True) ##########
    CliDivNum2 = models.IntegerField(null=True, blank=True) ##########
    CliDivicion = models.CharField(max_length=15, null=True, blank=True) # #########
    CliDivicion2 = models.CharField(max_length=15, null=True, blank=True)##########

    # Técnicos
    CliServicio = models.CharField(max_length=100, null=True, blank=True) ##########
    CliPerfil = models.CharField(max_length=100, null=True, blank=True) ##########
    CliIplocal = models.CharField(max_length=100, null=True, blank=True) ##########
    CliIpRemota = models.CharField(max_length=20, null=True, blank=True) ##########
    CliMacEquipo = models.CharField(max_length=100, default='0') 
    CliTecnologiaInstalacion = models.CharField(max_length=25, null=True, blank=True) ##########
    CliNombreEquipo = models.CharField(max_length=105, null=True, blank=True) ##########
    CliContrasena = models.TextField(default='0', null=True, blank=True) ##########
    CliComentario = models.CharField(max_length=50, null=True, blank=True) ##########

    # Otros
    CliSuscripcion = models.CharField(max_length=15, null=True, blank=True) ##########
    CliPicture = models.CharField(max_length=100, default='example.png')
    CliUltimoEstado = models.CharField(max_length=50, null=True, blank=True)
    CliDatsLastReport = models.CharField(max_length=2000, null=True, blank=True)

    # Coordenadas
    CliCoor1 = models.CharField(max_length=50, null=True, blank=True) ##########
    CliCoor2 = models.CharField(max_length=50, null=True, blank=True) ##########

    # Contabilidad
    CliDebit = models.CharField(max_length=250, null=True, blank=True)
    CliCredit = models.CharField(max_length=250, null=True, blank=True)
    CliIdsTransaccionesRp = models.CharField(max_length=170, null=True, blank=True)

    class Meta:
        db_table = "Clientes"

    def __str__(self):
        return f"{self.CliNombreTitular}".strip()
    
class Proveedores(models.Model):
    """
    TABLA: proveedores
    """
    PrCategoria = models.CharField("categoria", max_length=100)
    PrNombre = models.CharField("nombre", max_length=150, default="")
    PrNit =  models.CharField(max_length=20, null=True, blank=True) ###############
    PrTelefono = models.CharField(max_length=20, null=True, blank=True) ###############
    PrEmail = models.CharField("email", max_length=150, default="")
    PrCorreo = models.CharField("correo", max_length=150, default="")
    PrDireccion = models.CharField("direccion", max_length=250, default="")
    PrCiudad = models.ForeignKey(Ciudades, on_delete=models.SET_NULL, null=True, blank=True)
    PrDepartamento = models.ForeignKey(Departamentos, on_delete=models.SET_NULL, null=True, blank=True)
    PrRegion = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True, blank=True)

    PrPago = models.CharField("con que lo paga", max_length=100, default="")
    PrNumeroCuenta = models.CharField("numero de la cuenta", max_length=50, default="")
    PrTipo = models.CharField("tipo de la cuenta", max_length=20, default="")
    PrBanco = models.CharField("banco", max_length=100, default="")
    PrFoto = models.ImageField("Foto", upload_to="proveedores/", blank=True, null=True)
    PrGid = models.CharField("gid", max_length=20, default="")
    PrCompañia = models.CharField("compañia", max_length=20, default="")
    PrCodEmp = models.CharField("codigo empresa", max_length=20, default="")
    CreatedAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    UpdatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.PrNombre

    class Meta:
        db_table = "Proveedores"