from functools import wraps
from django.http import JsonResponse
from django.middleware.csrf import get_token

from LibraryProject.library.token_verify import csrf_protect
from .models import Book
import json
import requests

from functools import wraps


csrf_token = None
def get_csrf_token(request):
    global csrf_token 
    token = get_token(request)
    csrf_token = token.json().get('csrf_token')
    
    # return JsonResponse({'csrf_token': token})
def csrf_protect(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        csrf_token =requests.json().get('csrf_token') # Function to retrieve CSRF token
        if csrf_token:
            headers = {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json'
            }

            # Perform the specific action based on the view function
            if view_func.__name__ == 'create_book':
                data = {
                    "title": "Book Title",
                    "author": "Author Name",
                    "book_code": "123456"
                }
                url = 'http://localhost:8000/library/api/books/create/'
                method = 'POST'
            elif view_func.__name__ == 'get_all_books':
                # Define data and URL for getting all books
                data = None
                url = 'http://localhost:8000/library/api/books/'
                method = 'GET'
                # ... Add more cases for update and delete if needed

            # Make the appropriate request
            response = requests.request(method, url, json=data, headers=headers)

            print(response.status_code)
            print(response.json())

            return JsonResponse({'message': 'Action performed successfully'})

        else:
            print("CSRF token retrieval failed.")
            return JsonResponse({'message': 'CSRF token retrieval failed'}, status=400)

    return wrapper

def create_book(request):
    global csrf_token  # Access the CSRF token defined in the middleware
    if request.method == 'POST':
        headers = {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json'
        }

        # Define the data for creating a book (replace this with your actual data)
        data = {
            "title": "Book Title",
            "author": "Author Name",
            "book_code": "123456"
        }

        response = requests.post('http://localhost:8000/library/api/books/create/', json=data, headers=headers)

        print(response.status_code)
        print(response.json())

        return JsonResponse({'message': 'Book created successfully'})

# @csrf_protect
# def create_book(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         book = Book.objects.create(
#             title=data['title'],
#             author=data['author'],
#             book_code=data['book_code']
#         )
#         return JsonResponse({'message': 'Book created successfully'})

@csrf_protect
def get_all_books(request):
    books = Book.objects.all().values()
    return JsonResponse({'books': list(books)})

@csrf_protect
def update_book(request, book_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            book = Book.objects.get(pk=book_id)
            book.title = data['title']
            book.author = data['author']
            book.book_code = data['book_code']
 
            book.save()
            return JsonResponse({'message': 'Book updated successfully'})
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book does not exist'}, status=404)

@csrf_protect
def delete_book(request, book_id):
    if request.method == 'DELETE':
        try:
            book = Book.objects.get(pk=book_id)
            book.delete()
            return JsonResponse({'message': 'Book deleted successfully'})
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book does not exist'}, status=404)
