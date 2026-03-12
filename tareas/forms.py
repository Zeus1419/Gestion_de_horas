from django import forms
from .models import Actividad, Evidencia, Novedad
from accounts.models import Usuario


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'tipo_actividad', 'cantidad_horas', 'fecha', 'descripcion']
        labels = {
            'nombre': 'Nombre de la actividad',
            'tipo_actividad': 'Tipo de actividad',
            'cantidad_horas': 'Cantidad de horas',
            'fecha': 'Fecha',
            'descripcion': 'Descripción',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'tipo_actividad': forms.Select(attrs={'class': 'form-input', 'placeholder': 'Extensión'}),
            'cantidad_horas': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'placeholder': 'Ej: 10'}),
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'placeholder': 'Seleccione un semestre'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seleccione un curso'}),
        }


class ActividadAdminForm(forms.ModelForm):
    """Formulario para que el administrador asigne actividades a docentes."""
    profesor = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(rol='profesor', estado='activo'),
        label='Docente',
        widget=forms.Select(attrs={'class': 'form-input'}),
        empty_label='Seleccione un docente'
    )

    class Meta:
        model = Actividad
        fields = ['profesor', 'nombre', 'tipo_actividad', 'cantidad_horas', 'fecha', 'descripcion']
        labels = {
            'nombre': 'Nombre de la actividad',
            'tipo_actividad': 'Tipo de actividad',
            'cantidad_horas': 'Cantidad de horas',
            'fecha': 'Fecha',
            'descripcion': 'Descripción',
        }
        widgets = {
            'profesor': forms.Select(attrs={'class': 'form-input'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
            'tipo_actividad': forms.Select(attrs={'class': 'form-input'}),
            'cantidad_horas': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-input'}),
        }


class EvidenciaForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ['archivo']
        widgets = {
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }


class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ['mensaje']
        labels = {
            'mensaje': '',
        }
        widgets = {
            'mensaje': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Escriba aqui su novedad',
                'rows': 6,
            }),
        }


class FiltroActividadForm(forms.Form):
    anio = forms.CharField(
        required=False,
        label='Año',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seleccione un año',
        })
    )
    periodo = forms.CharField(
        required=False,
        label='Periodo',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seleccione un periodo',
        })
    )
    semestre = forms.CharField(
        required=False,
        label='Semestre',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seleccione un semestre',
        })
    )
    curso = forms.CharField(
        required=False,
        label='Curso',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Seleccione un curso',
        })
    )
    codigo_profesor = forms.CharField(
        required=False,
        label='Código del Profesor',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Filtrar por código del profesor',
        })
    )
