from views import csrf_token
import requests
def csrf_protect(request):
    # global csrf_token
    # response = requests.get('http://localhost:8000/library/api/get-csrf-token/')
    # csrf_token = response.json().get('csrf_token')
    
    if csrf_token:
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
        
        # Make a POST request to create a book
        response = requests.post('http://localhost:8000/library/api/books/create/', json=data, headers=headers)
        
        print(response.status_code)
        print(response.json())
        
        return response
    else:
        print("CSRF token retrieval failed.")
        return None  # You might handle this case differently based on your requirements


# Call the function to execute the CSRF protection and book creation
# csrf_protect()