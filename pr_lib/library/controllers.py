from django.shortcuts import get_object_or_404
from pr_lib.library.models import Book, UserInteraction, UserRegistration, AddBookmark, Bookmark, User, Recommendation
from pr_lib.library.forms import UserInteractionForm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pr_lib.library.models import Book

def get_books():
    return Book.objects.all()

def get_book(pk):
    return get_object_or_404(Book, pk=pk)

def get_user_interactions(user):
    return UserInteraction.objects.filter(user=user.userregistration)

def get_liked_books(user):
    books_id = AddBookmark.objects.filter(user=user)
    books = []
    for i in range(len(books_id)):
        books.append(get_book(books_id[i].book_id))
    return books

def get_recommendation(user):
    books_id = Recommendation.objects.filter(user=user)
    books = []
    for i in range(len(books_id)):
        books.append(get_book(books_id[i].book_id))
    return books

def get_saved_books(user):
    books_id = Bookmark.objects.filter(user=user)
    books = []
    for i in range(len(books_id)):
        books.append(get_book(books_id[i].book_id))
    return books

def create_user_interaction(user, book, action):
    form = UserInteractionForm({'action': action})
    if form.is_valid():
        interaction = form.save(commit=False)
        interaction.book = book
        interaction.save()
        return interaction
    return None

def generate_recommendations(user):
    clear_recommendations(user)
    bookmarks = AddBookmark.objects.filter(user=user).values_list('book', flat=True)
    categories = Book.objects.filter(id__in=bookmarks).values_list('category', flat=True)
    recommended_books = Book.objects.filter(category__in=categories).exclude(id__in=bookmarks)
    top_recommendations = recommended_books.distinct()[:10]
    for book in top_recommendations:
        Recommendation.objects.get_or_create(user=user, book=book)

    return top_recommendations

def clear_recommendations(user):
    Recommendation.objects.filter(user=user).delete()