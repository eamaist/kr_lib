from django import forms
from pr_lib.library.models import User, Book

from .models import UserInteraction, UserRegistration
from django.contrib.auth.forms import UserCreationForm


class UserInteractionForm(forms.ModelForm):
    class Meta:
        model = UserInteraction
        fields = ['action']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'category']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_superuser', 'password']
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class LikeForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())

class SaveBookForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())

class BookSearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False, label='Search by Title, Author or Category')
    genre = forms.ChoiceField(choices=[], required=False, label='Genre')

    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        genres = Book.objects.values_list('genre', flat=True).distinct()
        self.fields['genre'].choices = [('', 'All')] + [(genre, genre) for genre in genres]