// Fetch all books for a user (assuming user_id = 1)
async function fetchBooks() {
    const response = await fetch('/api/books?user_id=1');
    const books = await response.json();
    const bookList = document.getElementById('book-list');
    bookList.innerHTML = '';

    books.forEach(book => {
        const li = document.createElement('li');
        li.className = 'book-item';
        li.textContent = `${book.title} by ${book.author} (ISBN: ${book.isbn})`;
        bookList.appendChild(li);
    });
}

// Add a new book
async function addBook() {
    const isbn = document.getElementById('isbn').value;

    // Make an API call to get book details using the ISBN (you'd normally validate this too)
    const googleApiUrl = `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`;
    const googleApiResponse = await fetch(googleApiUrl);
    const googleData = await googleApiResponse.json();

    if (!googleData.items || googleData.items.length === 0) {
        alert('Book not found.');
        return;
    }

    const book = googleData.items[0].volumeInfo;
    const newBook = {
        user_id: 1, // static user id for demo
        isbn: isbn,
        title: book.title,
        author: book.authors ? book.authors.join(', ') : 'Unknown',
        page_count: book.pageCount || 0,
        average_rating: book.averageRating || 0,
        thumbnail: book.imageLinks ? book.imageLinks.thumbnail : ''
    };

    await fetch('/api/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newBook)
    });

    document.getElementById('isbn').value = '';
    fetchBooks(); // Refresh book list
}

// Fetch books on page load
fetchBooks();
