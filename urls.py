from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view( ), name='login_view'),
    path('curuser/', views.curuser, name='cur user')
]