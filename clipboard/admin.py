from django.contrib import admin
from .models import Word, UserAccount

# Register your models here.
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "polish_word", "spanish_word", "etymology", "date_added")


admin.site.register(UserAccount)
