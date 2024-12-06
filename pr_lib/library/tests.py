from django.test import TestCase
from unicodedata import category

from pr_lib.library.models import Book, AddBookmark, Bookmark, Recommendation, UserInteraction, UserRegistration, User

class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre='Test Genre',
            description='Test Description',
            category='Test Categoty'
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(self.book.genre, 'Test Genre')
        self.assertEqual(self.book.description, 'Test Description')
        self.assertEqual(self.book.category, 'Test Categoty')

    def test_like_creation(self):
        like = AddBookmark.objects.create(user=self.user, book=self.book)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.book, self.book)


    def test_recommendation_creation(self):
        recommendation = Recommendation.objects.create(user=self.user, book=self.book)
        self.assertEqual(recommendation.user, self.user)
        self.assertEqual(recommendation.book, self.book)


#Тестирование форм
from pr_lib.library.forms import LikeForm, BookSearchForm, RegisterForm, LoginForm

class RegisterFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'username': 'Test username',
            'email': 'email@mail.ru',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())

class LoginFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'username': 'JaneD',
            'password': 'password456'
        }
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'username': '',
            'password': ''
        }
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())

class LikeFormTest(TestCase):
    def test_valid_form(self):
        data = {'book_id': 1}
        form = LikeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'book_id': ''}
        form = LikeForm(data=data)
        self.assertFalse(form.is_valid())




#Тестирование views

from django.test import TestCase, Client
from django.urls import reverse

class BookListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre='Test Genre',
            description='Test Description',
            category = 'Test Categoty'
        )


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre='Test Genre',
            description='Test Description',
            category='Test Categoty'
        )



class LikeBookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre='Test Genre',
            description='Test Description',
            category='Test Categoty'
        )

    def test_like_book_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('like_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)

class SaveBookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre='Test Genre',
            description='Test Description',
            category='Test Categoty'
        )

class ChangeUsernameViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')


class RecommendationsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')

    def test_recommendations_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recommendations'))
        self.assertEqual(response.status_code, 302)


from pr_lib.library.controllers import generate_recommendations



from pr_lib.library.controllers import (
    get_books, get_book, get_user_interactions, get_liked_books,
    get_recommendation, get_saved_books, create_user_interaction,
    generate_recommendations
)

class BookViewsTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', email='test@email.com', password='12345')

        # Create some books
        self.book1 = Book.objects.create(title='Book 1', genre='Fiction', author='Author 1', category='Nagito')
        self.book2 = Book.objects.create(title='Book 2', genre='Non-Fiction', author='Author 2', category='Komaeda')

        # Create likes, recommendations, and saved books
        AddBookmark.objects.create(user=self.user, book=self.book1)
        Recommendation.objects.create(user=self.user, book=self.book2)
        Bookmark.objects.create(user=self.user, book=self.book1)

    def test_get_books(self):
        books = get_books()
        self.assertEqual(books.count(), 2)

    def test_get_book(self):
        book = get_book(self.book1.pk)
        self.assertEqual(book, self.book1)

    def test_get_liked_books(self):
        liked_books = get_liked_books(self.user)
        self.assertEqual(len(liked_books), 1)
        self.assertEqual(liked_books[0], self.book1)

    def test_get_recommendation(self):
        recommendations = get_recommendation(self.user)
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0], self.book2)

    def test_get_saved_books(self):
        saved_books = get_saved_books(self.user)
        self.assertEqual(len(saved_books), 1)
        self.assertEqual(saved_books[0], self.book1)




from django.test import TestCase


