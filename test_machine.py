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
from main import machine

HOST = "127.0.0.1"
PORT = 2056

class TestMachine(unittest.TestCase):
    def setUp(self):
        self.config=[HOST, 2056, 3056, 4056]

    def test_machine(self):
        # Test that client codes are randomly generated
        client_code_list = []
        machine(self.config, True, client_code_list)

        # allowing time for processing
        time.sleep(0.001)
        self.assertTrue( len(set(client_code_list)) != 1)

if __name__ == '__main__':
    unittest.main()