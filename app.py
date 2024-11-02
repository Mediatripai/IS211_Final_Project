from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Connect to the database
def connect_db():
    connection = sqlite3.connect('book_catalogue.db')
    connection.row_factory = sqlite3.Row
    return connection

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get all books for a user
@app.route('/api/books', methods=['GET'])
def get_books():
    user_id = request.args.get('user_id', type=int)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books WHERE user_id = ?", (user_id,))
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(books)

# Route to add a book to the catalog
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO Books (user_id, isbn, title, author, page_count, average_rating, thumbnail)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (data['user_id'], data['isbn'], data['title'], data['author'], data['page_count'], data['average_rating'], data['thumbnail'])
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
