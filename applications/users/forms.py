from django import forms
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegisterForm"""
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )

    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )

    )

    class Meta:
        """Meta definition for UserRegisterForm."""

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
        )

    # def clean_password2(self): # Clase 166
    #     if self.cleaned_data['password1'] != self.cleaned_data['password2']:
    #         self.add_error('password2', '¡No coincide con la contraseña que introdujo!')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        espacio=False
        minuscula=False
        mayuscula=False
        numeros=False

        for c in password1:
            if c.isspace():
                espacio=True
            elif c.islower():
                minuscula=True
            elif c.isupper():
                mayuscula=True
            elif c.isdigit():
                numeros=True

        if len(password1) < 5:
            self.add_error('password1', 'La contraseña debe contener al menos 8 caracteres')
        elif password1 != password2:
            self.add_error('password2', '¡No coincide con la contraseña que introdujo!')
        elif espacio==True:
            self.add_error('password2', 'La contraseña no puede contener espacios')
        elif minuscula==False:
            self.add_error('password2', 'La contraseña debe contener al menos una letra mayúscula')
        elif mayuscula==False:
            self.add_error('password2', 'La contraseña debe contener al menos una letra mayúscula')
        elif numeros==False:
            self.add_error('password2', 'La contraseña debe contener al menos un número')
        elif password1.isalnum()==True:
            print('¡Usuario creado exitosamente!')
        else:
            self.add_error('password2', 'La contraseña debe ser alfanumérica')


class LoginForm(forms.Form):
    
    username = forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'style': '{ margin: 10px }',
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    def clean(self):
        # cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('¡Los datos del usuario o contraseña no son correctos!')
        
        return super(LoginForm, self).clean()

class UpdatePasswordForm(forms.Form):
    """UpdatePasswordForm definition."""

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Nueva Contraseña'
            }
        )
    )


class VerificationForm(forms.Form):
    """VerificationForm definition."""

    codregistro = forms.CharField(required=True)
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk

        super(VerificationForm, self).__init__(*args, **kwargs)
    

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # Verificamos si el código y el id de usuario son válidos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('¡El código es incorrecto!')
            
        else:
            raise forms.ValidationError('¡El código es incorrecto!')

