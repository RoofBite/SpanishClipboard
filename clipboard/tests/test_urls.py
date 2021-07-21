from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from clipboard.views import view_deleted_words,view_words, account_settings, \
        hard_delete_words, delete_word, hide_word, retrive_word, view_word, \
        edit_word, add_word, register, logout_page, login_page

class TestUrls(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('login_page')
        self.assertEquals(resolve(url).func, login_page)
    
    def test_logout_url_resolves(self):
        url = reverse('logout_page')
        self.assertEquals(resolve(url).func, logout_page)
    
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)
    
    def test_add_word_url_resolves(self):
        url = reverse('add_word')
        self.assertEquals(resolve(url).func, add_word)
    
    def test_view_deleted_words_url_resolves(self):
        url = reverse('view_deleted_words')
        self.assertEquals(resolve(url).func, view_deleted_words)
    
    def test_account_settings_url_resolves(self):
        url = reverse('account_settings')
        self.assertEquals(resolve(url).func, account_settings)
    