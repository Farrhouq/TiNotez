from django.urls import path
from . import views

app_name = "password_manager"

urlpatterns = [
    path('', views.home, name='home'),
    path('auth', views.authenticate, name="authenticate"),
    path('add', views.add_password, name='add'),
    path('generate', views.generate_password, name='generate'),
    path('save', views.save, name='save'),
    path('passwords/<int:line>/', views.password, name='password')
]
