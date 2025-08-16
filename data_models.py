"""Data models
This script creates author and book classes and the related SQL table.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Class for objects who represents an author in the db libary.
    """
    __tablename__ = 'Authors'
    #for more then one argument to guarentee a unipue entry,
    # define __table_args__ with UniqueConstraint
    __table_args__ = (
        db.UniqueConstraint('author_name', 'author_birth_date', name='unique_author'),
    )
    #if only one argument to guarentee a unique entry, use unique=True in Column
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String, nullable=False)
    author_birth_date = db.Column(db.Date, nullable=True)
    author_date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship('Book', backref='author', lazy=True)


    # Attribute names in the constructor should match the column names of the SQL table
    def __init__(self, name, birth_date, date_of_death, author_id=None):
        self.author_id = author_id
        self.author_name = name
        self.author_birth_date = birth_date
        self.author_date_of_death = date_of_death


    def __repr__(self):
        return f'''Author(author_id = {self.author_id}, name = {self.author_name},
        birth_date = {self.author_birth_date}, date_of_death = {self.autor_date_of_death})'''


    def __str__(self):
        return f'''The author {self.author_name} lived from
        {self.author_birth_date} to {self.author_date_of_death}.'''


class Book(db.Model):
    """Class for objects who represents a book in the db libary.
    """
    __tablename__ = 'Books'
    __table_args__ = (
        db.UniqueConstraint('book_title', 'book_isbn', name='unique_book'),
    )

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Authors.author_id'), nullable=False)
    book_isbn = db.Column(db.String, nullable=False)
    book_title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)


    def __init__(self, title, isbn, publication_year, author_id, book_id=None):
        self.book_id = book_id
        self.book_title = title
        self.book_isbn = isbn
        self.publication_year = publication_year
        self.author_id = author_id


    def __repr__(self):
        return f'''Book(book_id = {self.book_id}, book_title = {self.book_title},
        author_id = {self.author_id}, book_isbn = {self.book_isbn},
        publication_year = {self.publication_year})'''


    def __str__(self):
        return f'''The book {self.book_title} with ISBN{self.book_isbn} written by
        {self.author_id} is published in {self.publication_year}.'''
