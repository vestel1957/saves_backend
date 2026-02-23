from django.db import models
from login.models import *
from django.contrib.auth.hashers import make_password

# class Employees(models.Model):
#     EmRole = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
#     EmName = models.CharField('NOMBRE', max_length=255, default="")
#     EmEmail = models.CharField('EMAIL', max_length=255, unique=True, default="")
#     EmPasswordHash = models.CharField('CONTRASEÑA', max_length=255, default="")
#     EmSuperadmin = models.BooleanField('SUPERADMIN',default=False)
#     EmActive = models.BooleanField('ACTIVACION',default=True)
#     EmDateCreated = models.DateField('FECHA CREACION', auto_now_add=True)
#     EmDateUpdate = models.DateField('FECHA EDICION', auto_now=True)
#     EmCodigoVerificacion = models.CharField('CODIGO DE VERIFICACION', default="")
#     EmCodEmp = models.CharField('CODIGO empresa-año-sede', default="")
    
#     def set_password(self, raw_password):
#         self.password_hash = make_password(raw_password)
    
#     def __str__(self) -> str:
#         return f"{self.EmName} - {self.EmEmail}"

#     class Meta:
#         db_table = "Employees"
        
        
class EmployeesPermission(models.Model):
    EmpEmployees = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True) 
    EmpPermission = models.ForeignKey(Permissions, on_delete=models.CASCADE, null=True, blank=True) 
    EmpAllowed = models.BooleanField('',default=True)

    def __str__(self) -> str:
        return f"{self.EmpEmployees.UsUsername}-{self.EmpPermission.PeName}"

    class Meta:
        db_table = "EmployeesPermission"
