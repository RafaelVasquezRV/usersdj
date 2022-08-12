from django.shortcuts import render

from django.views.generic import (
    CreateView,
)

from .forms import UserRegisterForm

# Create your views here.

class UserRegisterCreateView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    

