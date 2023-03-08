import unittest
from multiprocessing import Process, Lock
import os 
import socket 
from _thread import * 
import threading
import time 
from threading import Thread 
import random
from datetime import datetime
from main import server, init_machine

HOST = "127.0.0.1"
PORT = 100

class TestServer(unittest.TestCase):
    def setUp(self):
        self.network_queue = []
        self.network_lock = Lock()

    def test_network_queue_updates(self):
        # Test that network queue updates as expected
        init_thread = Thread(target=init_machine, args=([HOST, PORT], self.network_queue, self.network_lock, True)) 
        init_thread.daemon = True # allow for threads to exit
        init_thread.start()
        
        s_A = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s_A.connect((HOST, PORT))
        codeVal = "1_1"
        s_A.send(codeVal.encode('ascii'))
        s_A.close()

        # allowing time for processing
        time.sleep(0.001)
        self.assertTrue(len(self.network_queue) == 1)

    def test_network_lock_works(self):
        init_thread = Thread(target=init_machine, args=([HOST, PORT], self.network_queue, self.network_lock, True)) 
        init_thread.daemon = True # allow for threads to exit
        init_thread.start()

        # Network lock is working correctly
        with self.network_lock:
            s_A = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
            s_A.connect((HOST, PORT))
            codeVal = "1_1X"
            s_A.send(codeVal.encode('ascii'))
            s_A.close()

            # allowing time for processing
            time.sleep(0.001)
            self.assertTrue(len(self.network_queue) == 0)

        # allowing time for processing
        time.sleep(0.001)
        self.assertTrue(len(self.network_queue) == 1)
    

if __name__ == '__main__':
    unittest.main()