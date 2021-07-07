from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add_word/', views.add_word, name='add_word'),
    path('edit_word/<int:id>', views.edit_word, name='edit_word'),
    path('view_word/<int:id>', views.view_word, name='view_word'),
    path('view_words/<int:hours>', views.view_words, name='view_words'),
    path('delete_word/<int:id>', views.delete_word, name='delete_word'),
    path('hide_word/<int:id>', views.hide_word, name='hide_word'),
    path('retrive_word/<int:id>', views.retrive_word, name='retrive_word'),
    

    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
    path('account/', views.account_settings, name='account_settings'),
]
