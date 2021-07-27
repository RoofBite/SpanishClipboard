from django.test import TestCase
from clipboard.models import Word, UserAccount, User

class TestViews(TestCase):

    def setUp(self): 
       self.user = User.objects.create_user('John', 'John@example.com', 'Password') 

    # Word model tests
    def test_word_str_method_spanish_and_polish_word(self):
        self.word = Word.objects.create(polish_word = 'polish_word', spanish_word = 'spanish_word')

        self.assertEquals(str(Word.objects.first()), 'polish_word' + " - " + 'spanish_word')
    
    def test_word_str_method_only_spanish_word(self):
        self.word = Word.objects.create(spanish_word = 'spanish_word')

        self.assertEquals(str(Word.objects.first()), 'spanish_word')

    def test_word_str_method_only_polish_word(self):
        self.word = Word.objects.create(polish_word = 'polish_word')

        self.assertEquals(str(Word.objects.first()), 'polish_word')

    def test_word_str_method_no_word(self):
        self.word = Word.objects.create(etymology = 'etymology')

        self.assertEquals(str(Word.objects.first()), 'empty')
        
    # UserAccount model tests
    def test_useraccount_str_method(self):
        self.useraccount = UserAccount.objects.create(user = self.user)

        self.assertEquals(str(UserAccount.objects.first()), 'John')