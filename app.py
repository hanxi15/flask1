from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from waitress import serve  # Import Waitress

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive les alertes inutiles
db = SQLAlchemy(app)

# Définition du modèle Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Créez les tables de la base de données après avoir créé le contexte de l'application
with app.app_context():
    db.create_all()

# Route d'accueil
@app.route('/')
def home():
    return "Bienvenue dans notre service REST Flask !"

# Route pour obtenir tous les livres
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()  # Récupérer tous les livres depuis la base de données
    books_list = [{"id": book.id, "title": book.title, "author": book.author} for book in books]
    return jsonify(books_list)

# Route pour obtenir un livre spécifique
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)  # Récupérer un livre spécifique
    if book:
        return jsonify({"id": book.id, "title": book.title, "author": book.author})
    else:
        return jsonify({"error": "Book not found"}), 404

# Route pour ajouter un nouveau livre
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    if not new_book.get("title") or not new_book.get("author"):
        return jsonify({"error": "Title and author are required"}), 400
    book = Book(title=new_book["title"], author=new_book["author"])
    db.session.add(book)
    db.session.commit()
    return jsonify({"id": book.id, "title": book.title, "author": book.author}), 201

# Route pour supprimer un livre
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)  # Récupérer un livre spécifique
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

# Route pour mettre à jour un livre
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_data = request.get_json()
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if updated_data.get("title"):
        book.title = updated_data["title"]
    if updated_data.get("author"):
        book.author = updated_data["author"]
    db.session.commit()
    return jsonify({"id": book.id, "title": book.title, "author": book.author})

# Lancement du serveur avec Waitress
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)  # Lancement du serveur Waitress
