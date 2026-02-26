from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Modelo de usuario personalizado con acceso basado en roles."""
    
    ROLES = (
        ('administrador', 'Administrador'),
        ('coordinador', 'Coordinador'),
        ('profesor', 'Profesor'),
    )
    
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='profesor')
    programa = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=20, blank=True, null=True, unique=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_rol_display()}"
    
    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username
    
    @property
    def rol_display(self):
        return self.get_rol_display()
