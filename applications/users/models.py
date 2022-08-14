from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""
    GENDER_CHOICES = (
        ('0', 'Masculino'),
        ('1', 'Femenino'),
        ('2', 'Otros'),
    )

    username = models.CharField('Usuario', max_length=10, unique=True)
    email = models.EmailField('Correo', max_length=100)
    first_name = models.CharField('Nombres', max_length=50, blank=True)
    last_name = models.CharField('Apellidos', max_length=50, blank=True)
    gender = models.CharField('Genero', max_length=1, choices=GENDER_CHOICES, blank=True)
    codregistro = models.CharField(max_length=6, blank=True)

    is_staff = models.BooleanField('Acceso Admin', default=False)
    is_active = models.BooleanField('Usuario Activo', default=False)

    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email',]


    objects = UserManager()

      
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
