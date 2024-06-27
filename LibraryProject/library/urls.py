

from django.urls import path
from . import views
from . import token_verify

urlpatterns = [
    path('api/books/', views.get_all_books, name='get_all_books'),
    path('api/books/create/', views.create_book, name='create_book'),
    path('api/books/update/<int:book_id>/', views.update_book, name='update_book'),
    path('api/books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
]
