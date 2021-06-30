from django.contrib import admin
from .models import Word

# Register your models here.
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display=('polish_word','spanish_word','etymology','date_added')