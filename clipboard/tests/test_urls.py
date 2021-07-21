from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from clipboard.views import view_deleted_words,view_words, account_settings, hard_delete_words, delete_word, \
hide_word, retrive_word, view_word, edit_word, add_word, register, logout_page, login_page
