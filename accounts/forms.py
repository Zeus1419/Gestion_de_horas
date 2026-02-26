from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingrese su usuario',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingrese su contraseña',
        })
    )


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
        }),
        label='Contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = ['first_name', 'email', 'password', 'programa', 'rol']
        labels = {
            'first_name': 'Nombre',
            'email': 'Correo',
            'programa': 'Programa',
            'rol': 'Rol',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'programa': forms.TextInput(attrs={'class': 'form-input'}),
            'rol': forms.Select(attrs={'class': 'form-input'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email.split('@')[0] if user.email else user.first_name.lower()
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ActualizarPasswordForm(forms.Form):
    nueva_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
        }),
        label='Ingrese Contraseña Nueva'
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
        }),
        label='Confirmar Nueva Contraseña'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        nueva = cleaned_data.get('nueva_password')
        confirmar = cleaned_data.get('confirmar_password')
        if nueva and confirmar and nueva != confirmar:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data
