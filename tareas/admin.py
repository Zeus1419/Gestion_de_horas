from django.contrib import admin
from .models import Actividad, Evidencia, Novedad


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_actividad', 'cantidad_horas', 'fecha', 'profesor', 'estado']
    list_filter = ['tipo_actividad', 'estado']
    search_fields = ['nombre', 'profesor__first_name']


@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'actividad', 'subido_por', 'fecha_subida']


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'mensaje', 'fecha', 'leida']
    list_filter = ['leida']
