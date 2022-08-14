from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic import (
    View,
    CreateView,
)

from django.views.generic.edit import FormView


from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm
)

from .models import User

from .functions import code_generator

# Create your views here.

class UserRegisterFormView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        
        # Genemos el código
        codigo = code_generator()

        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            first_name=form.cleaned_data['first_name'],            
            last_name=form.cleaned_data['last_name'],            
            gender=form.cleaned_data['gender'],
            codregistro=codigo            
        )
        # Enviar el código al email del user
        asunto = 'Confirmación de email'
        mensaje = 'Código de verificación: ' + codigo
        email_remitente = 'neunapp.cursos@gmail.com'

        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        # redirgir a pantalla de validación


        return HttpResponseRedirect(            
            reverse(
                'users_app:user-login'
            )
        )


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)

        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    
    def get(self, request, *args, **kwargs):        
        logout(request)
        return HttpResponseRedirect(            
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordFormView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):        
        usuario = self.request.user

        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1'],
        )
        
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        
        logout(self.request)
        
        return super(UpdatePasswordFormView, self).form_valid(form)