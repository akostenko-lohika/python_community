from __future__ import print_function
import logging

import grpc

import library_pb2
import library_pb2_grpc
from google.protobuf.empty_pb2 import Empty


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = library_pb2_grpc.LibraryStub(channel)
        response = stub.ListBooks(Empty())
        print("Client received: " + response.books)


if __name__ == '__main__':
    logging.basicConfig()
    run()
