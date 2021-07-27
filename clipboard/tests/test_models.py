from django.test import TestCase
from clipboard.models import Word, UserAccount

class TestViews(TestCase):

    
    def test_word_str_method_spanish_and_polish_word(self):
        self.word=Word.objects.create(polish_word='polish_word', spanish_word = 'spanish_word')

        self.assertEquals(str(Word.objects.first()), 'polish_word' + " - " + 'spanish_word')
    
    def test_word_str_method_only_spanish_word(self):
        self.word=Word.objects.create(spanish_word = 'spanish_word')

        self.assertEquals(str(Word.objects.first()), 'spanish_word')

    def test_word_str_method_only_polish_word(self):
        self.word=Word.objects.create(polish_word='polish_word')

        self.assertEquals(str(Word.objects.first()), 'polish_word')

    def test_word_str_method_no_word(self):
        self.word=Word.objects.create(etymology='etymology')

        self.assertEquals(str(Word.objects.first()), 'empty')
        