"""Book Alchemy
This script generates webpages with flask displaying a book library,
a form to add new authors and books. 
It reads all books and authors from library.sqlite database,
allows the user to create, delete, update.
"""
import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for

from data_models import db, Author, Book


app = Flask(__name__)
#random key only for development
app.secret_key = os.urandom(24)

#set the database URI using an absolute path, after initialized Flask app
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

#connect the Flask app to the flask-sqlalchemy code, after app.config
db.init_app(app)

# create the database, only run once
# with app.app_context():
#    db.create_all()


@app.route("/")
def home():
    """Renders the homepage.
    """
    books = db.session.query(Book).all()
    authors = db.session.query(Author).all()
    return render_template("home.html", books=books, authors=authors)


@app.route("/add_author", methods=['GET', 'POST'])
def add_author():
    """Adds a new author to the library via web form. 
    By 'GET' it shows the form and by 'POST' it sends to the database and 
    shows a successfully sending messange on the web form.
    """
    if request.method == "POST":
        author_name = request.form.get('name')
        birth_str = request.form.get('birth_date')
        death_str = request.form.get('date_of_death')

        birth_date = datetime.strptime(birth_str, "%Y-%m-%d").date() if birth_str else None
        date_of_death = datetime.strptime(death_str, "%Y-%m-%d").date() if death_str else None

        new_author = Author(author_name, birth_date, date_of_death)
        db.session.add(new_author)
        db.session.commit()

        return render_template("add_author.html", author=new_author)

    return render_template("add_author.html", author=None)

@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    """Adds a new book to the library via web form. 
    By 'GET' it shows the form and by 'POST' it sends to the database and 
    shows a successfully sending messange on the web form.
    """
    authors = db.session.query(Author).all()
    if request.method == "POST":
        book_title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year', type=int)
        author_id = request.form.get('author_id', type=int)

        new_book = Book(book_title, isbn, publication_year, author_id)
        db.session.add(new_book)
        db.session.commit()

        return render_template("add_book.html", authors=authors, book=new_book)

    return render_template("add_book.html", authors=authors, book=None)


@app.route("/sorted", methods=['POST'])
def sort():
    """Sorts the books on the webpage by author or title.
    """
    sort_by = request.form.get('sort_by')
    if sort_by == "title":
        books = db.session.query(Book).order_by(Book.book_title).all()
    elif sort_by == "author":
        books = db.session.query(Book).join(Author).order_by(Author.author_name).all()
    else:
        books = db.session.query(Book).all()
    authors = db.session.query(Author).all()
    return render_template("home.html", books=books, authors=authors)


@app.route("/search", methods=['POST'])
def search():
    """Searchs the book table for a word or phrase."""
    search_request = request.form.get('search')
    books = db.session.query(Book).filter(Book.book_title.like(f'%{search_request}%')).all()
    author = db.session.query(Author).all()
    return render_template("home.html", books=books, authors=author)


@app.route("/<book_title>/<int:book_id>/delete", methods=['POST'])
def delete(book_id, book_title):
    """Deletes a book from the library and 
    if a author doesn't have any book in the library it also deletes the author.
    :param book_id: integer id number of the book to be deleted.
    """
    book = Book.query.get(book_id)
    author = book.author
    db.session.delete(book)
    # another delete option
    # db.session.query(Book).filter(Book.book_id==book_id).delete()
    db.session.commit()

    # old version for delet authors without books:
    # authors_without_books = db.session.query(Author).outerjoin(Book)\
    # .filter(Book.book_id == None).all()
    # for author in authors_without_books:
    if not author.books:
        db.session.delete(author)
        db.session.commit()
        flash(f'Book "{book_title}" and Author "{author.author_name}"\
              have been successfully deleted from the library.', 'success')
    else:
        flash(f'Book "{book_title}" has been successfully deleted from the library.', 'success')

    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
