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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging
import multiprocessing
import threading
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


class RequestThread(threading.Thread):
    def __init__(self, stub):
        threading.Thread.__init__(self)
        self.stub = stub

    def run(self):
        self.stub.SayHello(helloworld_pb2.HelloRequest(name='you'))


def run(count):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)

    threads = []
    start = time.time()

    for i in range(count):
        threads.append(RequestThread(stub))
        threads[i].start()

    for t in threads:
        t.join()

    end = time.time()

    req_per_sec = 1 * count / (end - start)
    # print("Greeter client received: " + response.message)
    print(f"{req_per_sec} req/sec")


if __name__ == '__main__':
    logging.basicConfig()

    start = time.time()
    processes = []
    num_processes = 6
    count = 2000
    for i in range(num_processes):
        processes.append(multiprocessing.Process(target=run, args=(count,)))
        processes[i].start()

    for p in processes:
        p.join()

    end = time.time()

    req_per_sec = 1 * count * num_processes / (end - start)
    print(f"{req_per_sec} req/sec")

