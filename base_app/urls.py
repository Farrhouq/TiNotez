# from tkinter import N
from django.urls import path
from . import views

app_name = "base_app"

urlpatterns = [
    path('', views.home, name='home'),
    path('save', views.save, name='save')
]