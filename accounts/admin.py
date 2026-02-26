from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'email', 'rol', 'programa', 'estado']
    list_filter = ['rol', 'estado']
    search_fields = ['username', 'first_name', 'last_name', 'email']
