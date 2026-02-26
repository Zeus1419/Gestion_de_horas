from django.db import models
from django.conf import settings


class Actividad(models.Model):
    """Model for activities/tasks assigned to professors."""
    
    TIPOS = (
        ('extension', 'Extensión'),
        ('investigacion', 'Investigación'),
        ('docencia', 'Docencia'),
        ('administrativa', 'Administrativa'),
    )
    
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('rechazada', 'Rechazada'),
    )
    
    nombre = models.CharField(max_length=200)
    tipo_actividad = models.CharField(max_length=30, choices=TIPOS)
    cantidad_horas = models.DecimalField(max_digits=6, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actividades'
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    asignado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tareas_asignadas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    # Projection fields
    anio = models.IntegerField(null=True, blank=True, verbose_name='Año')
    periodo = models.CharField(max_length=20, blank=True)
    semestre = models.CharField(max_length=20, blank=True)
    curso = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.profesor.nombre_completo}"


class Evidencia(models.Model):
    """Model for evidence files uploaded by professors."""
    
    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name='evidencias'
    )
    archivo = models.FileField(upload_to='evidencias/')
    nombre_archivo = models.CharField(max_length=200, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='evidencias_subidas'
    )
    
    class Meta:
        verbose_name = 'Evidencia'
        verbose_name_plural = 'Evidencias'
    
    def __str__(self):
        return f"Evidencia: {self.nombre_archivo or self.archivo.name}"
    
    def save(self, *args, **kwargs):
        if not self.nombre_archivo and self.archivo:
            self.nombre_archivo = self.archivo.name
        super().save(*args, **kwargs)


class Novedad(models.Model):
    """Model for news/issues reported by users."""
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='novedades'
    )
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Novedad de {self.usuario.nombre_completo} - {self.fecha.strftime('%Y-%m-%d')}"
