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

    # Restablecimiento de contraseña por email
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/enviado/', views.password_reset_done, name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/completado/', views.password_reset_complete, name='password_reset_complete'),
]
