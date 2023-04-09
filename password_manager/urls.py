from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth', views.authenticate, name="authenticate"),
    path('add', views.add_password, name='add'),
    path('passwords/<int:line>/', views.password, name='password')
]
