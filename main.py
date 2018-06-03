from concurrent import futures
from logbook import Logger, StreamHandler

import sys
import time
import os
import logbook

import grpc

import arbitrage_pb2
import arbitrage_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

StreamHandler(sys.stdout).push_application()
log = Logger('arbitrage')


class ArbitrageServiceServicer(arbitrage_pb2_grpc.ArbitrageServiceServicer):
    pass


def serve():
    max_worker = os.getenv('MAX_WORKER', 2)
    port = os.getenv('PORT', 50051)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_worker))

    arbitrage_pb2_grpc.add_ArbitrageServiceServicer_to_server(
        ArbitrageServiceServicer(), server)
    server.add_insecure_port('[::]:{port}'.format(port=port))

    log.info('serving at [::]:{port} using max worker {max_worker}'.format(
        port=port, max_worker=max_worker))
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
