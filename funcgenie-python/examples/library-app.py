from flask import Flask, jsonify
from funcgenie import phantom, create_genie_flask_routes

app = Flask(__name__)

# Register genie routes
create_genie_flask_routes(app)

books = []

@phantom
def add_book(title: str, author: str):
    """
    A function to add a new book to the library.
    """
    book = {
        "id": len(books) + 1,
        "title": title,
        "author": author
    }
    books.append(book)
    return {"message": "Book added successfully", "book": book}

@phantom
def get_books():
    """
    A function to get a list of all books from the library.
    """
    return books

@app.route('/books', methods=['GET'])
def show_books():
    return jsonify(get_books())

@app.route('/')
def home():
    return "Welcome to the Library Books Management App!"

if __name__ == "__main__":
    app.run(port=5000)