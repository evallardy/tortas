from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('cambia_contrasena/', cambia_contrasena, name='cambia_contrasena'),
]