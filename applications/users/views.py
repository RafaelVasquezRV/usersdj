from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.views.generic import (
    View,
    CreateView,
)

from django.views.generic.edit import FormView


from .forms import (
    UserRegisterForm, 
    LoginForm,
)

from .models import User

# Create your views here.

class UserRegisterFormView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):

        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            first_name=form.cleaned_data['first_name'],            
            last_name=form.cleaned_data['last_name'],            
            gender=form.cleaned_data['gender'],            
        )


        return super(UserRegisterFormView, self).form_valid(form)


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