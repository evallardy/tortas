from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    celular = models.CharField(max_length=20, blank=True, null=True)
    cliente = models.BooleanField('Cliente', blank=True, null=True, default=False)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        db_table = 'Usuario'
