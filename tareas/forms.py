from django import forms
from .models import Actividad, Evidencia, Novedad


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
            'cantidad_horas': forms.Select(attrs={'class': 'form-input', 'placeholder': 'Seleccione una versión'}, choices=[('', 'Seleccione una versión')] + [(i, str(i)) for i in range(1, 41)]),
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'placeholder': 'Seleccione un semestre'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seleccione un curso'}),
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
