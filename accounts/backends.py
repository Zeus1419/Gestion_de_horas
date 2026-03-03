from django.contrib.auth.backends import ModelBackend
from .models import Usuario


class EmailBackend(ModelBackend):
    """Backend de autenticación por correo electrónico en lugar de nombre de usuario."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 'username' aquí contiene el email que el usuario ingresó en el formulario
            # iexact para búsqueda insensible a mayúsculas/minúsculas
            user = Usuario.objects.get(email__iexact=username)
        except (Usuario.DoesNotExist, Usuario.MultipleObjectsReturned):
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
