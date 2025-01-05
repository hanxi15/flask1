from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Données simulées
books = [
    {"id": 1, "title": "Python for Beginners", "author": "John Doe"},
    {"id": 2, "title": "Flask in Action", "author": "Jane Smith"}
]

# Route d'accueil
@app.route('/')
def home():
    return "Bienvenue dans notre service REST Flask !"

# Route pour obtenir tous les livres
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Route pour obtenir un livre spécifique
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Route pour ajouter un nouveau livre
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    if not new_book.get("title") or not new_book.get("author"):
        return jsonify({"error": "Title and author are required"}), 400
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return jsonify(new_book), 201

# Route pour supprimer un livre
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200

# Route pour mettre à jour un livre
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_data = request.get_json()
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    book.update(updated_data)
    return jsonify(book)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Créez les tables de la base de données après avoir créé le contexte de l'application
with app.app_context():
    db.create_all()

# Route pour ajouter un livre à la base de données
@app.route('/books', methods=['POST'])
def add_book_db():
    new_book = request.get_json()
    if not new_book.get("title") or not new_book.get("author"):
        return jsonify({"error": "Title and author are required"}), 400
    book = Book(title=new_book["title"], author=new_book["author"])
    db.session.add(book)
    db.session.commit()
    return jsonify({"id": book.id, "title": book.title, "author": book.author}), 201

# Lancement du serveur
if __name__ == '__main__':
    app.run(debug=True)
