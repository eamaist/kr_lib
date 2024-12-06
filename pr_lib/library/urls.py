from django.urls import path

from pr_lib.library import views
from pr_lib.library.views import book_detail
from pr_lib.library.views import recommendations
from pr_lib.library.views import book_list

urlpatterns = [
    path('', book_list, name='book_list'),
    path('book_list', book_list, name='book_list'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('recommendations/', recommendations, name='recommendations'),
    path('library/<int:book_id>/like', views.like_book, name='like_book'),
    path('library/bookmarks', views.like_book_list, name='bookmarks'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
]
