from __future__ import print_function
import logging
import sys
import grpc

import library_pb2
import library_pb2_grpc
from google.protobuf.empty_pb2 import Empty
from PyInquirer import prompt


def add_book():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = library_pb2_grpc.LibraryStub(channel)
        questions = [
            {'type': 'input', 'name': 'title', 'message': 'book title'},
            {'type': 'input', 'name': 'author', 'message': 'book author'},
            {'type': 'input', 'name': 'isbn', 'message': 'book isbn'},
        ]
        answers = prompt(questions)
        response = stub.AddBook(library_pb2.BookRequest(
            title=answers['title'],
            author=answers['author'],
            isbn=answers['isbn'])
        )
        print("Book:\n" + str(response))


def get_book():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = library_pb2_grpc.LibraryStub(channel)
        questions = [
            {'type': 'input', 'name': 'isbn', 'message': 'book isbn'}
        ]
        answers = prompt(questions)
        response = stub.GetBook(library_pb2.BookRequest(isbn=answers['isbn']))
        if response.isbn == answers['isbn']:
            print("Book:\n" + str(response))
        else:
            print(f"no book with ISBN: {answers['isbn']}")


def list_books():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = library_pb2_grpc.LibraryStub(channel)
        response = stub.ListBooks(Empty())
        for item in response.books:
            print("Book:\n" + str(item))


if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) > 1:
        if str(sys.argv[1]) == 'addbook':
            add_book()
        elif str(sys.argv[1]) == 'getbook':
            get_book()
    else:
        list_books()
