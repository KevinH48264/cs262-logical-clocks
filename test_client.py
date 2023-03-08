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
from main import client, init_machine

HOST = "127.0.0.1"
PORT = 2056

class TestServer(unittest.TestCase):
    def setUp(self):
        self.network_queue1 = []
        self.network_lock1 = Lock()
        self.network_queue2 = []
        self.network_lock2 = Lock()
        self.network_queue3 = []
        self.network_lock3 = Lock()

    def test_popping_network_queue(self):
        # Network queue > 0, verify log is updated
        self.network_queue1 = ["1_1"]

        init_thread1 = Thread(target=init_machine, args=([HOST, PORT], self.network_queue1, self.network_lock1, True)) 
        init_thread1.daemon = True # allow for threads to exit
        init_thread1.start()

        init_thread2 = Thread(target=init_machine, args=([HOST, 3056], self.network_queue2, self.network_lock2, True)) 
        init_thread2.daemon = True # allow for threads to exit
        init_thread2.start()

        init_thread3 = Thread(target=init_machine, args=([HOST, 4056], self.network_queue3, self.network_lock3, True)) 
        init_thread3.daemon = True # allow for threads to exit
        init_thread3.start()

        lines = client(PORT, 3056, 4056, self.network_queue1, self.network_lock1, True, 1)

        self.assertTrue("received" in lines[0])

    def test_client_code_1(self):
        # Client code = 1, verify log is updated
        time.sleep(2)
        self.network_queue4 = []

        init_thread1 = Thread(target=init_machine, args=([HOST, 1], self.network_queue4, self.network_lock1, True)) 
        init_thread1.daemon = True # allow for threads to exit
        init_thread1.start()

        init_thread2 = Thread(target=init_machine, args=([HOST, 2], self.network_queue2, self.network_lock2, True)) 
        init_thread2.daemon = True # allow for threads to exit
        init_thread2.start()

        init_thread3 = Thread(target=init_machine, args=([HOST, 3], self.network_queue3, self.network_lock3, True)) 
        init_thread3.daemon = True # allow for threads to exit
        init_thread3.start()

        lines = client(1, 2, 3, self.network_queue4, self.network_lock1, True, 1)

        self.assertTrue('sent: 1' in lines[0])

    def test_client_code_2(self):
        # Client code = 2, verify log is updated
        time.sleep(2)
        self.network_queue4 = []

        init_thread1 = Thread(target=init_machine, args=([HOST, 1], self.network_queue4, self.network_lock1, True)) 
        init_thread1.daemon = True # allow for threads to exit
        init_thread1.start()

        init_thread2 = Thread(target=init_machine, args=([HOST, 2], self.network_queue2, self.network_lock2, True)) 
        init_thread2.daemon = True # allow for threads to exit
        init_thread2.start()

        init_thread3 = Thread(target=init_machine, args=([HOST, 3], self.network_queue3, self.network_lock3, True)) 
        init_thread3.daemon = True # allow for threads to exit
        init_thread3.start()

        lines = client(1, 2, 3, self.network_queue4, self.network_lock1, True, 2)

        self.assertTrue('sent: 2' in lines[0])

    def test_client_code_3(self):
        # Client code = 3, verify log is updated
        time.sleep(2)
        self.network_queue4 = []

        init_thread1 = Thread(target=init_machine, args=([HOST, 1], self.network_queue4, self.network_lock1, True)) 
        init_thread1.daemon = True # allow for threads to exit
        init_thread1.start()

        init_thread2 = Thread(target=init_machine, args=([HOST, 2], self.network_queue2, self.network_lock2, True)) 
        init_thread2.daemon = True # allow for threads to exit
        init_thread2.start()

        init_thread3 = Thread(target=init_machine, args=([HOST, 3], self.network_queue3, self.network_lock3, True)) 
        init_thread3.daemon = True # allow for threads to exit
        init_thread3.start()

        lines = client(1, 2, 3, self.network_queue4, self.network_lock1, True, 3)

        self.assertTrue('sent: 3' in lines[0])

    def test_client_code_else(self):
        # Client code not equal to 1, 2, or 3, verify log is updated
        time.sleep(2)
        self.network_queue4 = []

        init_thread1 = Thread(target=init_machine, args=([HOST, 1], self.network_queue4, self.network_lock1, True)) 
        init_thread1.daemon = True # allow for threads to exit
        init_thread1.start()

        init_thread2 = Thread(target=init_machine, args=([HOST, 2], self.network_queue2, self.network_lock2, True)) 
        init_thread2.daemon = True # allow for threads to exit
        init_thread2.start()

        init_thread3 = Thread(target=init_machine, args=([HOST, 3], self.network_queue3, self.network_lock3, True)) 
        init_thread3.daemon = True # allow for threads to exit
        init_thread3.start()

        lines = client(1, 2, 3, self.network_queue4, self.network_lock1, True, 4)

        self.assertTrue('internal event' in lines[0])    

if __name__ == '__main__':
    unittest.main()