import sqlite3
import requests
import hashlib

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a new user
def add_user(username, password):
    connection = sqlite3.connect('book_catalogue.db')
    cursor = connection.cursor()
    
    try:
        cursor.execute('INSERT INTO Users (username, password_hash) VALUES (?, ?);',
                       (username, hash_password(password)))
        connection.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
    finally:
        connection.close()

# Function to authenticate a user
def authenticate_user(username, password):
    connection = sqlite3.connect('book_catalogue.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id, password_hash FROM Users WHERE username = ?;', (username,))
    user = cursor.fetchone()
    
    connection.close()
    
    if user and hash_password(password) == user[1]:  # Hashing the input password for comparison
        return user[0]  # Return user ID if authenticated
    else:
        print("Authentication failed.")
        return None

# Function to search for a book by ISBN using the Google Books API
def search_book_by_isbn(isbn):
    """Search for a book using the Google Books API by ISBN."""
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            # Return the first book's details
            book_info = data['items'][0]['volumeInfo']
            return {
                'isbn': isbn,
                'title': book_info.get('title', 'No title found'),
                'author': ', '.join(book_info.get('authors', ['Unknown author'])),
                'page_count': book_info.get('pageCount', 0),
                'average_rating': book_info.get('averageRating', 0.0),
                'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', '')
            }
        else:
            print("No book found for this ISBN.")
            return None
    else:
        print("Error fetching data from Google Books API.")
        return None

# Function to save book information to the SQLite database
def save_book_to_database(user_id, book):
    """Save the book information to the SQLite database."""
    connection = sqlite3.connect('book_catalogue.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO Books (user_id, isbn, title, author, page_count, average_rating, thumbnail)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (user_id, book['isbn'], book['title'], book['author'],
          book['page_count'], book['average_rating'], book['thumbnail']))

    connection.commit()
    connection.close()
    print(f"Book '{book['title']}' added to the database.")

# Main program logic
def main():
    # User registration (optional)
    register = input("Do you want to register a new user? (yes/no): ").strip().lower()
    if register == 'yes':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        add_user(username, password)

    # User authentication
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    user_id = authenticate_user(username, password)
    
    if user_id:
        print("Welcome!")
        isbn = input("Enter the ISBN of the book to add: ")
        
        # Search for the book using the provided ISBN
        book = search_book_by_isbn(isbn)
        
        # If a book is found, save it to the database
        if book:
            save_book_to_database(user_id, book)

if __name__ == '__main__':
    main()
