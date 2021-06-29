from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add_word/', views.add_word, name='add_word'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
]
