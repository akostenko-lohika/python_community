from concurrent import futures
import grpc
import logging

from library_pb2_grpc import LibraryServicer
from library_pb2 import BookList, Book

import library_pb2_grpc


class Servicer(LibraryServicer):
    def ListBooks(self, request, context):
        return BookList(
            books=[
                Book(title="The Dark Tower: The Gunslinger",
                     author="Stephen King", isbn="978-0-937986-50-9"),
                Book(title="The Talisman", author="Stephen King", isbn="978-0-670-69199-9"),
                Book(title="Neverwhere"),
        ])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_LibraryServicer_to_server(Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Starting server on :50051")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()
