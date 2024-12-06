from django.contrib import admin
from django.urls import path, include
from pr_lib.library import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('admin/add_book/', views.add_book, name='add_book'),
    path('admin/admin_book_list/', views.admin_book_list, name='admin_book_list'),
    path('admin/edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('admin/delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('admin/add_user/', views.add_user, name='add_user'),
    path('admin/user_list/', views.user_list, name='user_list'),
    path('admin/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('pr_lib.library.urls')),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('library/<int:book_id>/like', views.like_book, name='like_book'),
]