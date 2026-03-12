from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import role_required
from accounts.models import Usuario
from .models import Actividad, Evidencia, Novedad
from .forms import ActividadForm, ActividadAdminForm, EvidenciaForm, NovedadForm, FiltroActividadForm


# ==========================================
# ADMINISTRADOR VIEWS
# ==========================================

@login_required
@role_required('administrador')
def admin_dashboard(request):
    """Admin main dashboard - SISTEMA DE REGISTRO."""
    context = {
        'page_title': 'SISTEMA DE REGISTRO',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'show_novedades': True,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@role_required('administrador')
def cargar_archivos(request):
    """Admin file upload page."""
    actividades = Actividad.objects.all()

    if request.method == 'POST':
        actividad_id = request.POST.get('actividad')
        archivo = request.FILES.get('archivo')
        nombre_archivo = request.POST.get('nombre_archivo', '')

        if actividad_id and archivo:
            actividad = get_object_or_404(Actividad, id=actividad_id)
            evidencia = Evidencia(
                actividad=actividad,
                archivo=archivo,
                nombre_archivo=nombre_archivo or archivo.name,
                subido_por=request.user
            )
            evidencia.save()
            messages.success(request, f'Archivo "{archivo.name}" cargado exitosamente.')
            return redirect('cargar_archivos')
        else:
            messages.error(request, 'Debe seleccionar una actividad y un archivo.')

    context = {
        'page_title': 'Cargar Archivos',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'actividades': actividades,
    }
    return render(request, 'admin_panel/cargar_archivos.html', context)


@login_required
@role_required('administrador')
def visualizar_actividades_admin(request):
    """Admin view activities page."""
    actividades = Actividad.objects.all().select_related('profesor').prefetch_related('evidencias')
    context = {
        'page_title': 'Visualizar actividades',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'actividades': actividades,
    }
    return render(request, 'admin_panel/visualizar_actividades.html', context)


@login_required
@role_required('administrador')
def progreso_docentes_admin(request):
    """Vista para que el administrador vea el progreso de todos los docentes."""
    from django.db.models import Count, Q
    
    # Obtener todos los profesores con sus actividades
    profesores = Usuario.objects.filter(rol='profesor').annotate(
        total_actividades=Count('actividades'),
        actividades_completadas=Count('actividades', filter=Q(actividades__estado='completada')),
        actividades_pendientes=Count('actividades', filter=Q(actividades__estado='pendiente')),
        actividades_en_progreso=Count('actividades', filter=Q(actividades__estado='en_progreso')),
        total_evidencias=Count('actividades__evidencias')
    )
    
    # Calcular porcentaje de progreso para cada profesor
    for profesor in profesores:
        if profesor.total_actividades > 0:
            profesor.progreso = int((profesor.actividades_completadas / profesor.total_actividades) * 100)
        else:
            profesor.progreso = 0
    
    context = {
        'page_title': 'Progreso de Docentes',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'profesores': profesores,
    }
    return render(request, 'admin_panel/progreso_docentes.html', context)


@login_required
@role_required('administrador')
def asignar_actividad(request):
    """Vista para que el administrador asigne actividades a docentes."""
    if request.method == 'POST':
        form = ActividadAdminForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.asignado_por = request.user
            actividad.estado = 'pendiente'
            actividad.save()
            messages.success(request, f'Actividad "{actividad.nombre}" asignada exitosamente a {actividad.profesor.nombre_completo}.')
            return redirect('asignar_actividad')
    else:
        form = ActividadAdminForm()

    context = {
        'page_title': 'Asignar Actividad',
        'user_role': 'Administrador',
        'user_name': request.user.nombre_completo,
        'form': form,
    }
    return render(request, 'admin_panel/asignar_actividad.html', context)


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
def progreso_docentes_coordinador(request):
    """Vista para que el coordinador vea el progreso de todos los docentes."""
    from django.db.models import Count, Q
    
    # Obtener todos los profesores con sus actividades
    profesores = Usuario.objects.filter(rol='profesor').annotate(
        total_actividades=Count('actividades'),
        actividades_completadas=Count('actividades', filter=Q(actividades__estado='completada')),
        actividades_pendientes=Count('actividades', filter=Q(actividades__estado='pendiente')),
        actividades_en_progreso=Count('actividades', filter=Q(actividades__estado='en_progreso')),
        total_evidencias=Count('actividades__evidencias')
    )
    
    # Calcular porcentaje de progreso para cada profesor
    for profesor in profesores:
        if profesor.total_actividades > 0:
            profesor.progreso = int((profesor.actividades_completadas / profesor.total_actividades) * 100)
        else:
            profesor.progreso = 0
    
    context = {
        'page_title': 'Progreso de Docentes',
        'user_role': 'Coordinador',
        'user_name': request.user.nombre_completo,
        'profesores': profesores,
    }
    return render(request, 'coordinador/progreso_docentes.html', context)


@login_required
@role_required('coordinador')
def visualizar_actividades_coordinador(request):
    """Coordinador view activities with filters."""
    from django.db.models import Count
    
    form = FiltroActividadForm(request.GET or None)
    actividades = Actividad.objects.all().select_related('profesor').prefetch_related('evidencias')
    
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
    
    # Annotate with evidence count
    actividades = actividades.annotate(evidencias_count=Count('evidencias'))

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


@login_required
@role_required('coordinador')
def aprobar_evidencia(request, evidencia_id):
    """Coordinador aprueba una evidencia individual."""
    evidencia = get_object_or_404(Evidencia, id=evidencia_id)
    evidencia.estado = 'aprobada'
    evidencia.revisado_por = request.user
    evidencia.fecha_revision = timezone.now()
    evidencia.save()
    messages.success(request, f'Evidencia "{evidencia.nombre_archivo}" aprobada exitosamente.')
    
    # Redirigir a la página anterior o a visualizar actividades
    next_url = request.GET.get('next', 'visualizar_actividades_coordinador')
    return redirect(next_url)


@login_required
@role_required('coordinador')
def rechazar_evidencia(request, evidencia_id):
    """Coordinador rechaza una evidencia individual."""
    evidencia = get_object_or_404(Evidencia, id=evidencia_id)
    evidencia.estado = 'rechazada'
    evidencia.revisado_por = request.user
    evidencia.fecha_revision = timezone.now()
    evidencia.save()
    messages.success(request, f'Evidencia "{evidencia.nombre_archivo}" rechazada.')
    
    # Redirigir a la página anterior o a visualizar actividades
    next_url = request.GET.get('next', 'visualizar_actividades_coordinador')
    return redirect(next_url)


@login_required
@role_required('coordinador')
def ver_actividades_docente(request, profesor_id):
    """Coordinador ve las actividades de un docente específico como si fuera el docente."""
    from django.db.models import Count
    
    profesor = get_object_or_404(Usuario, id=profesor_id, rol='profesor')
    
    # Obtener actividades del profesor con sus evidencias
    actividades = Actividad.objects.filter(profesor=profesor).prefetch_related('evidencias').annotate(
        evidencias_count=Count('evidencias')
    )
    
    # Calcular progreso
    total_actividades = actividades.count()
    actividades_completadas = actividades.filter(estado='completada').count()
    actividades_pendientes = actividades.filter(estado='pendiente').count()
    actividades_en_progreso = actividades.filter(estado='en_progreso').count()
    
    if total_actividades > 0:
        progreso = int((actividades_completadas / total_actividades) * 100)
    else:
        progreso = 0
    
    # Calcular valores para el círculo de progreso
    radio = 52
    circunferencia = 2 * 3.1416 * radio
    offset = circunferencia * (100 - progreso) / 100
    
    faltantes = total_actividades - actividades_completadas
    
    context = {
        'page_title': f'Actividades de {profesor.nombre_completo}',
        'user_role': 'Coordinador',
        'user_name': request.user.nombre_completo,
        'profesor': profesor,
        'actividades': actividades,
        'total_actividades': total_actividades,
        'actividades_completadas': actividades_completadas,
        'actividades_pendientes': actividades_pendientes,
        'actividades_en_progreso': actividades_en_progreso,
        'progreso': progreso,
        'faltantes': faltantes,
        'circunferencia': circunferencia,
        'offset': offset,
    }
    return render(request, 'coordinador/ver_actividades_docente.html', context)


# ==========================================
# PROFESOR VIEWS
# ==========================================

@login_required
@role_required('profesor')
def profesor_dashboard(request):
    """Profesor main dashboard - SISTEMA DE PROYECCIÓN DE CURSOS."""
    from django.db.models import Count, Q
    
    # Calcular progreso del docente
    total_actividades = Actividad.objects.filter(profesor=request.user).count()
    actividades_completadas = Actividad.objects.filter(profesor=request.user, estado='completada').count()
    actividades_pendientes = Actividad.objects.filter(profesor=request.user, estado='pendiente').count()
    actividades_en_progreso = Actividad.objects.filter(profesor=request.user, estado='en_progreso').count()
    
    if total_actividades > 0:
        progreso = int((actividades_completadas / total_actividades) * 100)
    else:
        progreso = 0
    
    # Calcular valores para el círculo de progreso
    radio = 52
    circunferencia = 2 * 3.1416 * radio
    offset = circunferencia * (100 - progreso) / 100
    
    context = {
        'page_title': 'SISTEMA DE PROYECCIÓN DE CURSOS',
        'user_role': 'Docente',
        'user_name': request.user.nombre_completo,
        'total_actividades': total_actividades,
        'actividades_completadas': actividades_completadas,
        'actividades_pendientes': actividades_pendientes,
        'actividades_en_progreso': actividades_en_progreso,
        'progreso': progreso,
        'circunferencia': circunferencia,
        'offset': offset,
    }
    return render(request, 'profesor/dashboard.html', context)


@login_required
@role_required('profesor')
def progreso_profesor(request):
    """Vista para que el profesor vea su progreso individual detallado."""
    from django.db.models import Count
    
    # Obtener actividades del profesor
    actividades = Actividad.objects.filter(profesor=request.user).annotate(
        evidencias_count=Count('evidencias')
    )
    
    # Calcular progreso general
    total_actividades = actividades.count()
    actividades_completadas = actividades.filter(estado='completada').count()
    
    if total_actividades > 0:
        progreso = int((actividades_completadas / total_actividades) * 100)
    else:
        progreso = 0
    
    # Calcular valores para el círculo de progreso
    radio = 52
    circunferencia = 2 * 3.1416 * radio
    offset = circunferencia * (100 - progreso) / 100
    
    # Calcular lo que falta
    faltantes = total_actividades - actividades_completadas
    
    context = {
        'page_title': 'Mi Progreso',
        'user_role': 'Docente',
        'user_name': request.user.nombre_completo,
        'actividades': actividades,
        'total_actividades': total_actividades,
        'actividades_completadas': actividades_completadas,
        'progreso': progreso,
        'faltantes': faltantes,
        'circunferencia': circunferencia,
        'offset': offset,
    }
    return render(request, 'profesor/progreso.html', context)


@login_required
@role_required('profesor')
def nueva_actividad(request):
    """Profesor creates a new activity with file upload."""
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.profesor = request.user
            actividad.save()

            # Handle multiple file uploads
            archivos = request.FILES.getlist('archivo')
            for archivo in archivos:
                if archivo:
                    evidencia = Evidencia(
                        actividad=actividad,
                        archivo=archivo,
                        subido_por=request.user
                    )
                    evidencia.save()

            messages.success(request, 'Actividad registrada exitosamente.')
            return redirect('profesor_dashboard')
    else:
        form = ActividadForm()

    context = {
        'page_title': 'Registro de actividad',
        'user_role': 'Docente',
        'user_name': request.user.nombre_completo,
        'form': form,
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


@login_required
@role_required('profesor')
def subir_evidencia(request, actividad_id):
    """Vista para subir evidencias (fotos, documentos) a una actividad."""
    actividad = get_object_or_404(Actividad, id=actividad_id, profesor=request.user)
    
    if request.method == 'POST':
        archivos = request.FILES.getlist('archivos')
        
        if archivos:
            for archivo in archivos:
                evidencia = Evidencia(
                    actividad=actividad,
                    archivo=archivo,
                    subido_por=request.user
                )
                evidencia.save()
            
            messages.success(request, f'Se subieron {len(archivos)} archivo(s) como evidencia.')
            return redirect('visualizar_actividades_profesor')
        else:
            messages.error(request, 'Debe seleccionar al menos un archivo.')
    
    context = {
        'page_title': 'Subir Evidencias',
        'user_role': 'Docente',
        'user_name': request.user.nombre_completo,
        'actividad': actividad,
    }
    return render(request, 'profesor/subir_evidencia.html', context)


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
