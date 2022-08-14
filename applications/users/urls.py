from django.urls import path

from . import views

app_name = 'users_app'

urlpatterns = [
    path('register/', views.UserRegisterFormView.as_view(),
    name = 'user-register'
    ),
    path('login/', views.LoginUserFormView.as_view(),
    name = 'user-login'
    ),
    path('logout/', views.LogoutView.as_view(),
    name = 'user-logout'
    ),
    path('update/', views.UpdatePasswordFormView.as_view(),
    name = 'user-update'
    ),
    path('user-verification/<pk>/', views.CodeVerificationFormView.as_view(),
    name = 'user-verification'
    ),
]