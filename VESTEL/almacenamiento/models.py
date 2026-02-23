from django.db import models

from clientes.models import *
from nomina.models import Employees

class Almacenamiento(models.Model):
    AlNombre = models.CharField('NOMBRE',max_length=200, default="")
    AlDireccion = models.CharField('direccion',max_length=200, default="")
    AlCiudad = models.CharField("Ciudad",max_length=150, default="")
    AlDeparta = models.CharField("Departamento", max_length=150, default="")
    AlEstado = models.CharField('Estado', max_length=20, default="A")
    AlCod_emp = models.CharField('codigo de la empresa',max_length=20, default="")
    AlObservaciones = models.TextField('Observaciones', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.AlNombre}"

    class Meta:
        db_table = "Almacenamiento"

class AlmacenamientoEquipos(models.Model):
    AleNombre = models.CharField('NOMBRE',max_length=200, default="")
    AleDireccion = models.CharField('direccion',max_length=200, default="")
    AleCiudad = models.CharField("Ciudad",max_length=150, default="")
    aleDeparta = models.CharField("Departamento", max_length=150, default="")
    AleEstado = models.CharField('Estado', max_length=20, default="A")
    AleCodemp = models.CharField('codigo de la empresa',max_length=20, default="")
    AleObservaciones = models.TextField('Observaciones', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.AleNombre}"

    class Meta:
        db_table = "AlmacenamientoEquipos"

class Contadores(models.Model):
    CoNombre = models.CharField(max_length=150, unique=True)
    CoPrefijo = models.CharField(max_length=10, blank=True)
    CoUltimoValor = models.PositiveIntegerField(default=0)
    CoNumeroContador = models.IntegerField('NUMERAL CONTADOR', default=0)
    # longitud = models.PositiveIntegerField(default=4)
    # anio = models.PositiveIntegerField(null=True, blank=True)
    CoCodEmp = models.CharField('codigo de la empresa',max_length=20, default="")
    CoActivo = models.BooleanField(default=True)
    # opcional: para multi-sucursal
    # sucursal = models.ForeignKey(Sucursal, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.CoPrefijo}- {self.CoNombre}"
    
    class Meta:
        db_table = "Contadores"

class Equipos(models.Model):
    EqCodigo = models.CharField("codigo", max_length=20, default="")
    EqProveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, null=True, blank=True)
    EqAlmacen = models.ForeignKey(AlmacenamientoEquipos, on_delete=models.CASCADE, null=True, blank=True)
    EqMac = models.CharField("mca", max_length=150, default="")
    EqSerial = models.CharField('serial', max_length=20, default="A")
    EqCodEmp = models.CharField('codigo de la empresa',max_length=20, default="")
    EqFechaLlegada = models.TextField('fecha de llegada', blank=True, null=True)
    EqFechaFinal = models.TextField('fecha de finalizacion', blank=True, null=True)
    EqMarca = models.TextField('marca', blank=True, null=True)
    EqTipoInstalacion = models.TextField('tipo de instalacion', blank=True, null=True)
    EqPuerto = models.TextField('puertos del equipo', blank=True, null=True)
    EqVlan = models.TextField('vlan', blank=True, null=True)
    EqNat = models.TextField('nat', blank=True, null=True)
    EqAsignado = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True)
    EqEstado = models.TextField('estado', blank=True, null=True)
    EqObservaciones = models.TextField('Observaciones', blank=True, null=True)
    EqMaster = models.TextField('master', blank=True, null=True)
    EqAccesorios = models.TextField('accesorios', blank=True, null=True)
    EqIdGenieacs = models.TextField('id_genieacs', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.EqCodigo}"

    class Meta:
        db_table = "Equipos"