from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Actividad, Evidencia, Novedad
from .forms import ActividadForm, EvidenciaForm, NovedadForm, FiltroActividadForm


# ==========================================
# ADMINISTRADOR VIEWS
# ==========================================

@login_required
@role_required('administrador')
def admin_dashboard(request):
    """Admin main dashboard - SISTEMA DE REGISTRO."""
    context = {
        'page_title': 'SISTEMA DE REGISTRO',
        'user_role': 'Vicerrector',
        'user_role_sub': 'Administrador',
        'user_name': request.user.nombre_completo,
        'show_novedades': True,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@role_required('administrador')
def cargar_archivos(request):
    """Admin file upload page."""
    actividades = Actividad.objects.all()
    context = {
        'page_title': 'Cargar Archivos',
        'user_role': 'Vicerrector',
        'user_role_sub': 'Administrador',
        'user_name': request.user.nombre_completo,
        'actividades': actividades,
    }
    return render(request, 'admin_panel/cargar_archivos.html', context)


@login_required
@role_required('administrador')
def visualizar_actividades_admin(request):
    """Admin view activities page."""
    actividades = Actividad.objects.all()
    context = {
        'page_title': 'Visualizar actividades',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'actividades': actividades,
    }
    return render(request, 'admin_panel/visualizar_actividades.html', context)


@login_required
@role_required('administrador')
def proyeccion_admin(request, tipo='preliminar'):
    """Admin projections view."""
    actividades = Actividad.objects.all()
    context = {
        'page_title': f'Proyección {tipo.capitalize()}',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'actividades': actividades,
        'tipo': tipo,
    }
    return render(request, 'admin_panel/visualizar_actividades.html', context)


# ==========================================
# COORDINADOR VIEWS
# ==========================================

@login_required
@role_required('coordinador')
def coordinador_dashboard(request):
    """Coordinador main dashboard."""
    context = {
        'page_title': 'SISTEMA DE REGISTRO',
        'user_role': 'Coordinador',
        'user_name': request.user.nombre_completo,
        'show_novedades': True,
    }
    return render(request, 'coordinador/dashboard.html', context)


@login_required
@role_required('coordinador')
def visualizar_actividades_coordinador(request):
    """Coordinador view activities with filters."""
    form = FiltroActividadForm(request.GET or None)
    actividades = Actividad.objects.all()
    
    if form.is_valid():
        if form.cleaned_data.get('anio'):
            actividades = actividades.filter(anio=form.cleaned_data['anio'])
        if form.cleaned_data.get('periodo'):
            actividades = actividades.filter(periodo__icontains=form.cleaned_data['periodo'])
        if form.cleaned_data.get('semestre'):
            actividades = actividades.filter(semestre__icontains=form.cleaned_data['semestre'])
        if form.cleaned_data.get('curso'):
            actividades = actividades.filter(curso__icontains=form.cleaned_data['curso'])
        if form.cleaned_data.get('codigo_profesor'):
            actividades = actividades.filter(profesor__codigo=form.cleaned_data['codigo_profesor'])
    
    context = {
        'page_title': 'Visualizar Actividades',
        'user_role': 'Coordinador',
        'user_name': request.user.nombre_completo,
        'form': form,
        'actividades': actividades,
    }
    return render(request, 'coordinador/visualizar_actividades.html', context)


@login_required
@role_required('coordinador')
def confirmar_tarea(request, tarea_id):
    """Coordinador confirms task completion."""
    tarea = get_object_or_404(Actividad, id=tarea_id)
    tarea.estado = 'completada'
    tarea.save()
    messages.success(request, f'Tarea "{tarea.nombre}" confirmada como completada.')
    return redirect('visualizar_actividades_coordinador')


# ==========================================
# PROFESOR VIEWS
# ==========================================

@login_required
@role_required('profesor')
def profesor_dashboard(request):
    """Profesor main dashboard - SISTEMA DE PROYECCIÓN DE CURSOS."""
    context = {
        'page_title': 'SISTEMA DE PROYECCIÓN DE CURSOS',
        'user_role': 'Docente',
        'user_name': request.user.nombre_completo,
    }
    return render(request, 'profesor/dashboard.html', context)


@login_required
@role_required('profesor')
def nueva_actividad(request):
    """Profesor creates a new activity with file upload."""
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        evidencia_form = EvidenciaForm(request.POST, request.FILES)
        
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.profesor = request.user
            actividad.save()
            
            # Handle file upload
            if request.FILES.get('archivo'):
                evidencia = Evidencia(
                    actividad=actividad,
                    archivo=request.FILES['archivo'],
                    subido_por=request.user
                )
                evidencia.save()
            
            messages.success(request, 'Actividad registrada exitosamente.')
            return redirect('profesor_dashboard')
    else:
        form = ActividadForm()
        evidencia_form = EvidenciaForm()
    
    context = {
        'page_title': 'Registro de actividad',
        'user_role': 'Docente',
        'user_name': request.user.nombre_completo,
        'form': form,
        'evidencia_form': evidencia_form,
    }
    return render(request, 'profesor/nueva_actividad.html', context)


@login_required
@role_required('profesor')
def visualizar_actividades_profesor(request):
    """Profesor views their assigned activities."""
    actividades = Actividad.objects.filter(profesor=request.user)
    context = {
        'page_title': 'Visualizar actividades',
        'user_role': 'Docente',
        'user_name': request.user.nombre_completo,
        'actividades': actividades,
    }
    return render(request, 'profesor/visualizar_actividades.html', context)


# ==========================================
# SHARED VIEWS
# ==========================================

@login_required
def novedades(request):
    """Novedades page - shared between roles."""
    if request.method == 'POST':
        form = NovedadForm(request.POST)
        if form.is_valid():
            novedad = form.save(commit=False)
            novedad.usuario = request.user
            novedad.save()
            messages.success(request, 'Novedad enviada exitosamente.')
            return redirect('novedades')
    else:
        form = NovedadForm()
    
    context = {
        'page_title': 'Novedades',
        'user_role': request.user.rol_display,
        'user_name': request.user.nombre_completo,
        'form': form,
    }
    return render(request, 'novedades.html', context)
