import generics
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pr_lib.library.controllers import get_books, get_book, create_user_interaction, \
    generate_recommendations, \
    get_liked_books, get_saved_books, get_recommendation
from pr_lib.library.forms import RegisterForm, LoginForm, BookSearchForm, BookForm, UserForm
from django.contrib import messages
from pr_lib.library.models import UserRegistration, User, Bookmark, Book, AddBookmark, Recommendation
from django.contrib.auth.decorators import user_passes_test

def book_list(request):
    books = get_books()
    user = request.user
    return render(request, 'library/book_list.html', {'books': books, "user": user})


def book_detail(request, pk):
    book = get_book(pk)
    if request.method == 'POST':
        interaction = create_user_interaction(request.user, book, request.POST.get('action'))
        if interaction:
            return redirect('book_detail', pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def recommendations(request):
    user = request.user
    generate_recommendations(user)
    recommendations = get_recommendation(user)
    return render(request, 'library/recommendation.html', {'user': user, 'recommendations': recommendations})


def book_list(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        search = form.cleaned_data.get('search')
        genre = form.cleaned_data.get('genre')

        if search:
            books = books.filter(category__icontains=search) or books.filter(title__icontains=search) or books.filter(author__icontains=search)

        if genre:
            books = books.filter(genre__icontains=genre)

    return render(request, 'library/book_list.html', {'form': form, 'books': books})

@login_required
def like_book(request, book_id):
    user = request.user
    book = get_book(book_id)
    like, created = AddBookmark.objects.get_or_create(user=request.user, book=book)
    if created:
        generate_recommendations(user)
        messages.success(request, f"You liked {book.title}.")
    else:
        AddBookmark.objects.filter(book_id=book_id).delete()
        generate_recommendations(user)
        messages.info(request, f"Bookmark removed {book.title}.")
    is_bookmarked = AddBookmark.objects.filter(user=request.user, book=book).exists()
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def like_book_list(request):
    user = request.user
    books = get_liked_books(user)
    return render(request, 'library/bookmarks.html', {'books': books, "user": user})





def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/login.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password1']
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            user.is_active = 1
            return redirect('book_list')
        else:
            print("Form is not valid")
            return render(request, 'registration/login.html', {'form': form})
    form = RegisterForm()
    return render(request, 'registration/login.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username = username)
                if user.password == password:
                    login(request, user)
                    user.is_active = 1
                    messages.success(request, f'Hi {username.title()}, welcome back!')
                    return redirect('book_list')
            except Exception as e:
                print(e)
                messages.error(request, f'Invalid username or password')
        return render(request, 'accounts/login.html', {'form': form})
def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('login')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_book_list(request):
    books = get_books()
    return render(request, 'admin/admin_book_list.html', {'books': books})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('admin_book_list')
    else:
        form = BookForm()
    return render(request, 'admin/add_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('admin_book_list')
    return render(request, 'admin/delete_book.html', {'book': book})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'admin/add_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')
    return render(request, 'admin/delete_user.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_book(request, book_id):
    book = get_book(book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)
            messages.success(request, 'User updated successfully.')
            return redirect('admin_book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'admin/edit_book.html', {'form': form, 'book': book})

