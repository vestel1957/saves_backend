from django.db import models

from login.models import Sede
# from django_cryptography.fields import encrypt

class Mikroticks(models.Model):
    """
    TABLA: MODULOS PADRES (Ej: INVENTORY, SETTINGS)
    """
    MiNombre = models.CharField("NOMBRE DE la mikro", max_length=100)
    MiIp = models.GenericIPAddressField("Dirección IP")
    MiPuerto = models.IntegerField("Puerto de conexión")
    MiTecnologia = models.CharField("Tecnología", max_length=100, blank=True, null=True)
    MiCodEmp = models.CharField("cod_emp", max_length=10)
    MiUsuario = models.CharField("Usuario", max_length=100)
    MiPassword = models.CharField("Contraseña", max_length=255)
    MiDefecto = models.BooleanField("Router por defecto", default=False)

    MiEstadoConexion = models.CharField("Estado de conexión", max_length=100)
    
    def __str__(self) -> str:
        return self.MiNombre

    class Meta:
        db_table = "Mikroticks"

class Zonas(models.Model):
    ZoNombre = models.CharField("NOMBRE DE A ZONA", max_length=150)
    ZoSede = models.ForeignKey(Sede, on_delete=models.CASCADE,blank=True, null=True)
    ZoEstado = models.CharField("estado",max_length=20, default="A")
    ZoVlan = models.IntegerField("VLAN", default=0,blank=True, null=True)
    ZoCodigoEmp = models.CharField("codigo",max_length=10, default="")
    def __str__(self):
        return f"{self.ZoNombre}"

    class Meta:
        db_table = "Zonas"

class Olt(models.Model):
    OlUrl = models.TextField("URL", blank=True, null=True)
    OlToken = models.TextField("TOKEN",blank=True, null=True)
    OlSede = models.ForeignKey(Sede, on_delete=models.CASCADE,blank=True, null=True)
    OlEstado = models.CharField("estado",max_length=20, default="A")
    OlCodigoEmp = models.CharField("codigo",max_length=10, default="")
    def __str__(self):
        return f"{self.OlUrl} ({self.OlToken})"

    class Meta:
        db_table = "Olt"

class MikrotickOltEmpresa(models.Model):
    MoOlt = models.ForeignKey(Olt, on_delete=models.CASCADE,blank=True, null=True)
    MoSede = models.ForeignKey(Sede, on_delete=models.CASCADE,blank=True, null=True)
    MoMikrotick =models.ForeignKey(Mikroticks, on_delete=models.CASCADE,blank=True, null=True)
    MoZonas =models.ForeignKey(Zonas, on_delete=models.CASCADE,blank=True, null=True)
    MoTipoConfi = models.CharField("TIPO CONFIGURACION", max_length=50)
    MoEstado = models.CharField("estado",max_length=1, default="A")
    MoCodigoEmp = models.CharField("codigo",max_length=10, default="")
    
    def __str__(self):
        return f"{self.MoOlt} ({self.MoMikrotick})"

    class Meta:
        db_table = "MikrotickOltEmpresa"