from concurrent import futures
import grpc
import logging
import sqlite3

import pandas as pd

from library_pb2_grpc import LibraryServicer
from library_pb2 import BookList, Book
from google.protobuf.empty_pb2 import Empty

import library_pb2_grpc


class Servicer(LibraryServicer):
    def ListBooks(self, request, context):
        conn = sqlite3.connect('TestDB.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''SELECT * FROM books''')
        results = c.fetchall()
        return_books = [Book(title=res['title'], author=res['author'], isbn=res['isbn']) for res in results]
        return BookList(books=return_books)

    def GetBook(self, request, context):
        conn = sqlite3.connect('TestDB.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(f'SELECT * FROM books WHERE isbn=\'{request.isbn}\'')
        result = c.fetchone()
        return_book = Book(title=result['title'], author=result['author'], isbn=result['isbn']) if result else Empty()
        return return_book

    def AddBook(self, request, context):
        conn = sqlite3.connect('TestDB.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        query = f'INSERT INTO books (title, author, isbn) VALUES (\'{request.title}\',\'{request.author}\',\'{request.isbn}\');'
        c.execute(query)
        conn.commit()
        return Book(title=request.title, author=request.author, isbn=request.isbn)


def serve():
    create_test_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_LibraryServicer_to_server(Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Starting server on :50051")
    server.wait_for_termination()


def create_test_db():
    conn = sqlite3.connect('TestDB.db')
    read_books = pd.read_csv(r'books_test_data/books.csv')
    try:
        read_books.to_sql('books', conn, if_exists='fail', index=False)
    except ValueError:
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()
