from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('redirect/', views.role_redirect, name='role_redirect'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('password/', views.actualizar_password, name='actualizar_password'),
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('modificar-estado/', views.modificar_estado, name='modificar_estado'),
]
