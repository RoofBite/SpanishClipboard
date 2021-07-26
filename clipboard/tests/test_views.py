from django.test import TestCase, Client
from django.urls import reverse
from clipboard.models import Word, UserAccount, User

class TestViews(TestCase):

    def setUp(self): 
       User.objects.create_user('John', 'John@example.com', 'Password') 


    def test_view_words_POST_authenticated(self):
        client = Client()
        client.login(username='John', password = 'Password')


        # If metod POST and authenticated view_words redirects to login_page which is redireting 
        # in that sitaution to add_words
        response = client.post(reverse('view_words', args = ['1']), follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'clipboard/add_word.html')

    def test_view_words_POST_not_authenticated(self):
        client = Client()

        response = client.post(reverse('view_words', args = ['1']), follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'clipboard/login.html')

    
    def test_view_words_GET_not_authenticated(self):
        client = Client()

        response = client.get(reverse('login_page'), follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'clipboard/login.html')

    def test_view_words_GET_authenticated(self):
        client = Client()
        client.login(username='John', password = 'Password')

        response = client.get(reverse('view_words', args = ['1']), follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'clipboard/view_words.html')