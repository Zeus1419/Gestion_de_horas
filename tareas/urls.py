from django.urls import path
from . import views

urlpatterns = [
    # Administrador
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/cargar-archivos/', views.cargar_archivos, name='cargar_archivos'),
    path('admin/visualizar/', views.visualizar_actividades_admin, name='visualizar_actividades_admin'),
    path('admin/proyeccion/<str:tipo>/', views.proyeccion_admin, name='proyeccion_admin'),
    
    # Coordinador
    path('coordinador/dashboard/', views.coordinador_dashboard, name='coordinador_dashboard'),
    path('coordinador/visualizar/', views.visualizar_actividades_coordinador, name='visualizar_actividades_coordinador'),
    path('coordinador/confirmar/<int:tarea_id>/', views.confirmar_tarea, name='confirmar_tarea'),
    
    # Profesor
    path('profesor/dashboard/', views.profesor_dashboard, name='profesor_dashboard'),
    path('profesor/nueva-actividad/', views.nueva_actividad, name='nueva_actividad'),
    path('profesor/visualizar/', views.visualizar_actividades_profesor, name='visualizar_actividades_profesor'),
    
    # Shared
    path('novedades/', views.novedades, name='novedades'),
]
