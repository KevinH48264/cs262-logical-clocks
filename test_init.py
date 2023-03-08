'''
To run, go to / directory and run 'pytest'
Note: use the prefix "test_" when naming the function so that it is picked up by pytest
'''

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
PORT = 2056

class TestInit(unittest.TestCase):
    def setUp(self):
        self.network_queue = []
        self.network_lock = Lock()

    def test_init_connection(self):
        # Test that sockets can accept new connections
        init_thread = Thread(target=init_machine, args=([HOST, PORT], self.network_queue, self.network_lock, True)) 
        init_thread.daemon = True # allow for threads to exit
        init_thread.start()
        
        s_A = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        res = s_A.connect((HOST, PORT))
        s_A.close()

        # it would throw an error otherwise
        self.assertTrue(res == None)

if __name__ == '__main__':
    unittest.main()