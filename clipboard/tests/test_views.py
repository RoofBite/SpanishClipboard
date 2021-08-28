from django.test import TestCase, Client
from django.urls import reverse
from clipboard.models import Word, UserAccount, User
from django.db.models import Q


class TestViews_view_words(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")


    def test_view_words_POST_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        # If metod POST and authenticated view_words redirects to login_page which is redireting
        # in that sitaution to add_words
        response = client.post(reverse("view_words", args=["1"]), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/add_word.html")

    def test_view_words_POST_not_authenticated(self):
        client = Client()

        response = client.post(reverse("view_words", args=["1"]), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/login.html")

    def test_view_words_GET_not_authenticated(self):
        client = Client()

        response = client.get(reverse("login_page"), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/login.html")

    def test_view_words_GET_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("view_words", args=["1"]), follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/view_words.html")

    def test_view_words_GET_authenticated_search_days_0(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("view_words", args=["0"]))

        self.word = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=False,
            user=response.wsgi_request.user,
        )

        self.assertEquals(Word.objects.first(), self.word)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/view_words.html")

    def test_view_words_GET_authenticated_search_contains_0(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(
            reverse("view_words", args=["0"]), {"search_query": "2021"}
        )

        self.assertEqual(response.context["search_query"], "2021")

        self.word = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=False,
            user=response.wsgi_request.user,
        )

        self.assertEquals(
            Word.objects.get(
                date_added__startswith="2021",
                user=response.wsgi_request.user,
                for_deletion=False,
            ),
            self.word,
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/view_words.html")

    def test_view_words_GET_authenticated_search_without_0(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(
            reverse("view_words", args=["0"]), {"search_query": "Test"}
        )

        self.search_query_text = "Test"
        self.assertEqual(response.context["search_query"], self.search_query_text)

        # Test for polish_word filed lookup
        self.word1 = Word.objects.create(
            polish_word="polish_wordtest",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=False,
            user=response.wsgi_request.user,
        )

        self.search_query1 = Word.objects.get(
            Q(polish_word__icontains=self.search_query_text)
            | Q(date_added__startswith=self.search_query_text)
            | Q(spanish_word__icontains=self.search_query_text)
            | Q(etymology__icontains=self.search_query_text)
            | Q(notes__icontains=self.search_query_text),
            user=response.wsgi_request.user,
            for_deletion=False,
        )

        self.assertEquals(self.search_query1, self.word1)

        self.word1.delete()

        # Test for spanish_word filed lookup
        self.word2 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_wordtest",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=False,
            user=response.wsgi_request.user,
        )

        self.search_query2 = Word.objects.get(
            Q(polish_word__icontains=self.search_query_text)
            | Q(date_added__startswith=self.search_query_text)
            | Q(spanish_word__icontains=self.search_query_text)
            | Q(etymology__icontains=self.search_query_text)
            | Q(notes__icontains=self.search_query_text),
            user=response.wsgi_request.user,
            for_deletion=False,
        )

        self.assertEquals(self.search_query2, self.word2)

        self.word2.delete()

        # Test for etymology filed lookup
        self.word3 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymologytest",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=False,
            user=response.wsgi_request.user,
        )

        self.search_query3 = Word.objects.get(
            Q(polish_word__icontains=self.search_query_text)
            | Q(date_added__startswith=self.search_query_text)
            | Q(spanish_word__icontains=self.search_query_text)
            | Q(etymology__icontains=self.search_query_text)
            | Q(notes__icontains=self.search_query_text),
            user=response.wsgi_request.user,
            for_deletion=False,
        )

        self.assertEquals(self.search_query3, self.word3)

        self.word3.delete()

        # Test for notes filed lookup
        self.word4 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notestest",
            date_added="2021-01-01",
            for_deletion=False,
            user=response.wsgi_request.user,
        )

        self.search_query4 = Word.objects.get(
            Q(polish_word__icontains=self.search_query_text)
            | Q(date_added__startswith=self.search_query_text)
            | Q(spanish_word__icontains=self.search_query_text)
            | Q(etymology__icontains=self.search_query_text)
            | Q(notes__icontains=self.search_query_text),
            user=response.wsgi_request.user,
            for_deletion=False,
        )

        self.assertEquals(self.search_query4, self.word4)

        self.word4.delete()

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/view_words.html")





class TestViews_add_word(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

    def test_add_word_POST_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.post(
            reverse("add_word"),
            {
                "polish_word": "polish_word",
                "spanish_word": "spanish_word",
                "etymology": "etymology",
                "notes": "notes",
            },
        )

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Word.objects.first().polish_word, "polish_word")
        self.assertEquals(Word.objects.first().spanish_word, "spanish_word")
        self.assertEquals(Word.objects.first().etymology, "etymology")
        self.assertEquals(Word.objects.first().notes, "notes")

    def test_add_word_POST_not_authenticated(self):
        client = Client()

        response = client.post(
            reverse("add_word"),
            {
                "polish_word": "polish_word2",
                "spanish_word": "spanish_word2",
                "etymology": "etymology2",
                "notes": "notes2",
            },
        )

        self.assertEquals(response.status_code, 302)


class TestViews_view_deleted_words(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

        self.word1 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=True,
            user=self.user,
        )
        self.word2 = Word.objects.create(
            polish_word="polish_word2",
            spanish_word="spanish_word2",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-02",
            for_deletion=True,
            user=self.user,
        )

    def test_view_deleted_words_GET_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("view_deleted_words"))

        self.assertEquals(Word.objects.first(), self.word1)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "clipboard/deleted_words.html")
    
    def test_view_deleted_words_GET_not_authenticated(self):
        client = Client()

        response = client.get(reverse("view_deleted_words"))

        self.assertEquals(Word.objects.first(), self.word1)

        self.assertEquals(response.status_code, 302)


class TestViews_hard_delete_words(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

        self.word1 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=True,
            user=self.user,
        )
        self.word2 = Word.objects.create(
            polish_word="polish_word2",
            spanish_word="spanish_word2",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-02",
            for_deletion=True,
            user=self.user,
        )

    def test_hard_delete_words_POST_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.post(reverse("hard_delete_words"), {"delete_all":1, "delete_all_confirm":"delete"})

        self.assertEquals(Word.objects.first(), None)

        self.assertEquals(response.status_code, 302)
        
    
    def test_hard_delete_words_GET_not_authenticated(self):
        client = Client()

        response = client.get(reverse("hard_delete_words"),follow=True)

        self.assertEquals(Word.objects.first(), self.word1)

        self.assertEquals(response.status_code, 200)


class TestViews_delete_word(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

        self.word1 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=True,
            user=self.user,
        )

    def test_delete_word_POST_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.post(reverse("delete_word", args=[1]))
    
        self.assertEquals(Word.objects.first(), None)
        self.assertEquals(response.status_code, 302)
        
    def test_delete_word_GET_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("delete_word", args=[1]))
    
        self.assertEquals(response.status_code, 200)
    
    def test_delete_word_GET_authenticated_no_word(self):
        client = Client()
        client.login(username="John", password="Password")
        self.word1.delete()
        response = client.get(reverse("delete_word", args=[1]))
    
        self.assertEquals(response.status_code, 302)

    def test_delete_word_GET_not_authenticated(self):
        client = Client()
        response = client.get(reverse("delete_word",  args=[0]))

        self.assertEquals(response.status_code, 302)






class TestViews_hide_word(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

        self.word1 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=True,
            user=self.user,
        )

        
    def test_hide_word_GET_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("hide_word", args=[1]))
        self.assertEquals(response.status_code, 302)
    
    def test_hide_word_GET_authenticated_no_word(self):
        client = Client()
        client.login(username="John", password="Password")
        self.word1.delete()
        response = client.get(reverse("hide_word", args=[1]))
    
        self.assertEquals(response.status_code, 302)

    def test_hide_word_GET_not_authenticated(self):
        client = Client()
        response = client.get(reverse("hide_word",  args=[1]))

        self.assertEquals(response.status_code, 302)




class TestViews_retrive_word(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

        self.word1 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=True,
            user=self.user,
        )

        
    def test_hide_word_GET_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("retrive_word", args=[1]))
        self.assertEquals(response.status_code, 302)
    
    def test_hide_word_GET_authenticated_no_word(self):
        client = Client()
        client.login(username="John", password="Password")
        self.word1.delete()
        response = client.get(reverse("retrive_word", args=[1]))
    
        self.assertEquals(response.status_code, 302)

    def test_hide_word_GET_not_authenticated(self):
        client = Client()
        response = client.get(reverse("retrive_word",  args=[1]))

        self.assertEquals(response.status_code, 302)




class TestViews_edit_word(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

        self.word1 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=True,
            user=self.user,
        )

    def test_edit_word_POST_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.post(reverse("edit_word", args=[1]))
    
        self.assertEquals(response.status_code, 302)
    
    def test_edit_word_POST_authenticated_redirect(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.post(reverse("edit_word", args=[1]),{"redirect":"redirect"})
    
        self.assertEquals(response.status_code, 302)
        
    def test_edit_word_GET_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("edit_word", args=[1]))
    
        self.assertEquals(response.status_code, 200)
    
    def test_edit_word_GET_authenticated_no_word(self):
        client = Client()
        client.login(username="John", password="Password")
        self.word1.delete()
        response = client.get(reverse("edit_word", args=[1]))
    
        self.assertEquals(response.status_code, 302)

    def test_edit_word_GET_not_authenticated(self):
        client = Client()
        response = client.get(reverse("edit_word",  args=[0]))

        self.assertEquals(response.status_code, 302)


class TestViews_view_word(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("John", "John@example.com", "Password")

        self.word1 = Word.objects.create(
            polish_word="polish_word",
            spanish_word="spanish_word",
            etymology="etymology",
            notes="notes",
            date_added="2021-01-01",
            for_deletion=True,
            user=self.user,
        )

        
    def test_view_word_GET_authenticated(self):
        client = Client()
        client.login(username="John", password="Password")

        response = client.get(reverse("view_word", args=[1]))
        self.assertEquals(response.status_code, 200)
    
    def test_view_word_GET_authenticated_no_word(self):
        client = Client()
        client.login(username="John", password="Password")
        self.word1.delete()
        response = client.get(reverse("view_word", args=[1]))
    
        self.assertEquals(response.status_code, 302)

    def test_view_word_GET_not_authenticated(self):
        client = Client()
        self.client.logout()
        response = client.get(reverse("view_word",  args=[1]))

        self.assertEquals(response.status_code, 302)


