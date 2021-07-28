from django.test import TestCase, Client
from django.urls import reverse
from clipboard.models import Word, UserAccount, User

class TestViews(TestCase):

    def setUp(self): 
       self.user = User.objects.create_user('John', 'John@example.com', 'Password') 

       
    # view_words tests

    def test_view_words_POST_authenticated(self):
        client = Client()
        client.login(username = 'John', password = 'Password')

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

    def test_view_words_GET_authenticated_search_contains_0(self):
        client = Client()
        client.login(username='John', password = 'Password')


        response = client.get(reverse('view_words', args = ['0']),{
            'search_query':'2021'
        })

        self.assertEqual(response.context['search_query'], '2021') 

        self.word = Word.objects.create(polish_word = 'polish_word', 
                                        spanish_word = 'spanish_word',
                                        etymology = 'etymology',
                                        notes = 'notes',
                                        date_added = '2021-01-01',
                                        for_deletion=False,
                                        user = response.wsgi_request.user,)

        self.assertEquals(Word.objects.get(date_added__startswith = '2021', user = response.wsgi_request.user, for_deletion = False), self.word )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'clipboard/view_words.html')
    


    

    # add_word tests

    def test_add_word_POST_authenticated(self):
        client = Client()
        client.login(username='John', password = 'Password')

        response = client.post(reverse('add_word'),{
            'polish_word':'polish_word',
            'spanish_word':'spanish_word',
            'etymology':'etymology',
            'notes':'notes'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Word.objects.first().polish_word, 'polish_word')
        self.assertEquals(Word.objects.first().spanish_word, 'spanish_word')
        self.assertEquals(Word.objects.first().etymology, 'etymology')
        self.assertEquals(Word.objects.first().notes, 'notes')
    

    def test_add_word_POST_not_authenticated(self):
        client = Client()
        

        response = client.post(reverse('add_word'),{
            'polish_word':'polish_word2',
            'spanish_word':'spanish_word2',
            'etymology':'etymology2',
            'notes':'notes2'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Word.objects.first(), None)
        
        
        
        