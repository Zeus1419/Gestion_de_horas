from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, RegistroUsuarioForm, ActualizarPasswordForm, PasswordResetRequestForm, SetNewPasswordForm
from .models import Usuario
from .decorators import role_required


def login_view(request):
    """Página de inicio de sesión con diseño dividido."""
    if request.user.is_authenticated:
        return redirect('role_redirect')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.estado == 'inactivo':
                messages.error(request, 'Su cuenta está inactiva. Contacte al administrador.')
                return render(request, 'accounts/login.html', {'form': form})
            login(request, user)
            return redirect('role_redirect')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """vista para cerrar sesion."""
    logout(request)
    return redirect('login')


@login_required
def role_redirect(request):
    """maneja la vista de autentificacion de usuario segun el rol."""
    user = request.user
    if user.rol == 'administrador':
        return redirect('admin_dashboard')
    elif user.rol == 'coordinador':
        return redirect('coordinador_dashboard')
    elif user.rol == 'profesor':
        return redirect('profesor_dashboard')
    else:
        return redirect('login')


@login_required
@role_required('administrador')
def registro_usuario(request):
    """Vista para registrar un nuevo usuario."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('gestion_usuarios')
        else:
            # Mostrar errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = RegistroUsuarioForm()

    context = {
        'form': form,
        'page_title': 'Registro de Usuario',
        'user_role': request.user.rol_display,
        'user_name': request.user.nombre_completo,
    }
    return render(request, 'accounts/registro_usuario.html', context)


@login_required
def actualizar_password(request):
    """vista para actualizar el tipo de usuario."""
    if request.method == 'POST':
        form = ActualizarPasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['nueva_password'])
            request.user.save()
            messages.success(request, 'Contraseña actualizada exitosamente.')
            return redirect('login')
    else:
        form = ActualizarPasswordForm()
    
    context = {
        'form': form,
        'page_title': 'ACTUALIZACION DE CONTRASEÑA',
        'user_role': request.user.rol_display,
        'user_name': request.user.nombre_completo,
    }
    return render(request, 'accounts/actualizar_password.html', context)


@login_required
@role_required('administrador')
def gestion_usuarios(request):
    """Vista para manejar roles y nombres completos de los usuarios, gestion de usuarios."""
    usuarios = Usuario.objects.all().order_by('first_name')
    context = {
        'page_title': 'Gestion de Usuarios',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'usuarios': usuarios,
    }
    return render(request, 'admin_panel/gestion_usuarios.html', context)


@login_required
@role_required('administrador')
def modificar_estado(request):
    """Vista para modificar el usuario."""
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        nuevo_estado = request.POST.get('estado')
        if user_id and nuevo_estado:
            usuario = get_object_or_404(Usuario, id=user_id)
            usuario.estado = nuevo_estado
            usuario.save()
            messages.success(request, f'Estado de {usuario.nombre_completo} actualizado.')
            return redirect('modificar_estado')

    context = {
        'page_title': 'Ver Archivos',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'usuarios': usuarios,
    }
    return render(request, 'accounts/modificar_estado.html', context)


# ========================================
# VISTAS DE RESTABLECIMIENTO DE CONTRASEÑA
# ========================================

def password_reset_request(request):
    """Vista para solicitar restablecimiento de contraseña por email."""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Usuario.objects.get(email__iexact=email)
            except Usuario.DoesNotExist:
                user = None
            
            if user:
                # Generar token y UID
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Construir enlace de restablecimiento
                protocol = 'https' if request.is_secure() else 'http'
                domain = request.get_host()
                reset_url = f"{protocol}://{domain}/accounts/password-reset/{uid}/{token}/"
                
                # Renderizar email
                email_body = render_to_string('accounts/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                    'protocol': protocol,
                    'domain': domain,
                })
                
                # Enviar email
                send_mail(
                    subject='Restablecer Contraseña - Sistema de Gestión de Horas',
                    message=f'Haga clic en el siguiente enlace para restablecer su contraseña: {reset_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=email_body,
                    fail_silently=False,
                )
            
            # Siempre redirigir a "done" para no revelar si el email existe
            return redirect('password_reset_done')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset.html', {'form': form})


def password_reset_done(request):
    """Vista de confirmación de envío del email."""
    return render(request, 'accounts/password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    """Vista para confirmar token y establecer nueva contraseña."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None
    
    # Validar token
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['nueva_password'])
                user.save()
                return redirect('password_reset_complete')
        else:
            form = SetNewPasswordForm()
        
        return render(request, 'accounts/password_reset_confirm.html', {
            'form': form,
            'validlink': True,
        })
    else:
        return render(request, 'accounts/password_reset_confirm.html', {
            'validlink': False,
        })


def password_reset_complete(request):
    """Vista de confirmación final de contraseña restablecida."""
    return render(request, 'accounts/password_reset_complete.html')
