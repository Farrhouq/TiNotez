# from tkinter import N
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('save', views.save, name='save'),
    path('setup/', views.setup, name='setup'),
    path("edit-fc/", views.edit_categories, name='edit')
]