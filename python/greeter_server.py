# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""
import multiprocessing
import time
from concurrent import futures
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def __init__(self, process_id):
        self.process_id = process_id

    def SayHello(self, request, context):
        time.sleep(0.05)
        #print(f"JEJE {self.process_id}")
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve(num):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2000))#, options=[('grpc.so_reuseport', 1)])
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(num), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print(f"Server {num} started.")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()

    for i in range(6):
        p = multiprocessing.Process(target=serve, args=(i,))
        p.start()
