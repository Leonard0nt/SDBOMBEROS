from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.contrib.auth.hashers import make_password

# Create your models here.

from django.core.exceptions import ValidationError


def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "")
    if not rut[:-1].isdigit():
        return False

    rut, dv = rut[:-1], rut[-1]
    suma = 0
    mul = 2

    for d in reversed(rut):
        suma += int(d) * mul
        mul = (mul + 1) if mul < 7 else 2

    resultado = str((11 - (suma % 11)) % 11)
    return resultado == dv.upper() or (resultado == "K" and dv.upper() == "0")




class cuarteles(models.Model):
    idCuartel = models.IntegerField(null=False, primary_key=True)
    nombre_cuartel = models.CharField(max_length=30)
    direccionCuartel = models.TextField(default="")
    voluntarios_in = models.IntegerField(default=0)
    unidades_in = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.nombre_cuartel
    
class VoluntarioManager(UserManager):
    def create_voluntario(self, rut, passwordLec = None):
        # Crea un voluntario con el rut proporcionado y la contraseña (si se proporciona)
        password = make_password(passwordLec)
        voluntario = self.model(rut=rut)
        voluntario.set_password(password)
        voluntario.save()
        return voluntario
    

    
class voluntarios(AbstractUser):
    rut = models.CharField(validators=[validar_rut],unique=True, null=False, primary_key=True, max_length=12)
    nombres = models.CharField(max_length=40,default='')
    apellidos = models.CharField(max_length=40,default='')
    cargo = models.CharField(max_length=15,default='')
    telefono = models.PositiveBigIntegerField(blank=True,default=0)
    compania = models.CharField(max_length=10,default='')
    numero_registro = models.IntegerField(unique=True,default=0000)
    estado = models.BooleanField(default=False)
    direccion = models.TextField(blank=True,default='')
    conductor = models.BooleanField(default=False)
    unidad_asignada = models.CharField(max_length=4, default=0)

   

    #llaves foraneas
    cuartel_actual_vol = models.ForeignKey(cuarteles ,default=0, on_delete=models.SET_DEFAULT)
    
    # Configura el administrador y el gestor de modelos personalizado
    objects = VoluntarioManager()

    
    def __str__(self) -> str:
        return self.nombres +" "+ self.apellidos



class unidades(models.Model):
    nomenclatura = models.CharField(primary_key=True, null=False, max_length=4)
    patente = models.CharField(max_length=8)
    estado_unidad = models.BooleanField(default=True)
    especialidad = models.CharField(max_length=15)
    comentario = models.TextField()
    cuartel_actual_uni = models.ForeignKey(cuarteles,default=0, on_delete=models.SET_DEFAULT)

    
    def __str__(self) -> str:
        return self.nomenclatura

    


    
