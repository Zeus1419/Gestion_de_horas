from django.urls import path
from . import views

urlpatterns = [
    # Administrador
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/cargar-archivos/', views.cargar_archivos, name='cargar_archivos'),
    path('admin/visualizar/', views.visualizar_actividades_admin, name='visualizar_actividades_admin'),
    path('admin/progreso-docentes/', views.progreso_docentes_admin, name='progreso_docentes_admin'),
    path('admin/asignar-actividad/', views.asignar_actividad, name='asignar_actividad'),
    path('admin/proyeccion/<str:tipo>/', views.proyeccion_admin, name='proyeccion_admin'),

    # Coordinador
    path('coordinador/dashboard/', views.coordinador_dashboard, name='coordinador_dashboard'),
    path('coordinador/progreso-docentes/', views.progreso_docentes_coordinador, name='progreso_docentes_coordinador'),
    path('coordinador/visualizar/', views.visualizar_actividades_coordinador, name='visualizar_actividades_coordinador'),
    path('coordinador/ver-actividades-docente/<int:profesor_id>/', views.ver_actividades_docente, name='ver_actividades_docente'),
    path('coordinador/confirmar/<int:tarea_id>/', views.confirmar_tarea, name='confirmar_tarea'),
    path('coordinador/aprobar-evidencia/<int:evidencia_id>/', views.aprobar_evidencia, name='aprobar_evidencia'),
    path('coordinador/rechazar-evidencia/<int:evidencia_id>/', views.rechazar_evidencia, name='rechazar_evidencia'),

    # Profesor
    path('profesor/dashboard/', views.profesor_dashboard, name='profesor_dashboard'),
    path('profesor/progreso/', views.progreso_profesor, name='progreso_profesor'),
    path('profesor/nueva-actividad/', views.nueva_actividad, name='nueva_actividad'),
    path('profesor/visualizar/', views.visualizar_actividades_profesor, name='visualizar_actividades_profesor'),
    path('profesor/subir-evidencia/<int:actividad_id>/', views.subir_evidencia, name='subir_evidencia'),

    # Shared
    path('novedades/', views.novedades, name='novedades'),
]
