from multiprocessing import Process 
import os 
import socket 
from _thread import * 
import threading 
import time 
from threading import Thread 
import random
 
# server, receives messages
def server(conn, network_queue):
    print("server accepted connection" + str(conn)+"\n")
    sleepVal = 0.900

    while True: 
        try:
            time.sleep(sleepVal) 
            data = conn.recv(1024) 
            print("msg received\n") 
            dataVal = data.decode('ascii') 
            print("msg received:", dataVal) 

            # hold incoming messages from the client connection
            network_queue.append(dataVal)
        except KeyboardInterrupt:
            print("Caught interrupt, shutting down connection")
            conn.close()
            break 
 

# initialize a client, sending messages
def client(portValMachine, portValA, portValB, network_queue): 
    host= "127.0.0.1" 
    portA = int(portValA) 
    portB = int(portValB) 
    s_A = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s_B = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    clock_rate_sleep_val = 1.0 / random.randint(1, 6) # clock rate defined here

    logical_clock = 0

    # open log
    log_file = open('port_{}_log.txt'.format(portValMachine), 'w')

    try: 
        s_A.connect((host,portValA))
        print("Client-side connection success to port val:" + str(portValA) + "\n")

        s_B.connect((host,portValB))
        print("Client-side connection success to port val:" + str(portValB) + "\n")

        # on each clock cycle
        while True: 
            try:
                # TODO: send messages and edit Log here
                print("network queue: ", network_queue)
                log_message = ""

                # there is something in the network queue
                if len(network_queue) > 0:
                    # TODO: update the logical clock and add first item from network queue to log
                    
                    # logical_clock = max(time from network queue, logical_clock) + 1
                    pass
                else:
                    # no message in the queue, follow scope and update log
                    codeVal = str(client_code) 
                    s_A.send(codeVal.encode('ascii'))
                    s_B.send(codeVal.encode('ascii'))
                    print("msg sent", codeVal)

                log_file.write(str(network_queue.pop(0)))

                time.sleep(clock_rate_sleep_val)
            except KeyboardInterrupt:
                print("Caught interrupt, shutting down client")
                s_A.close()
                s_B.send(codeVal.encode('ascii'))
                break 
    except socket.error as e: 
        print("Error connecting client: %s" % e)

    log_file.close()
 
# initialize a server machine to connect with clients
def init_machine(config, network_queue):
    HOST = str(config[0],)
    PORT = int(config[1])
    print("starting server | port val:", PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    
    while True: 
        # always accept new connections from other clients and start a server connection between that client and server
        try:
            conn, addr = s.accept()
            start_new_thread(server, (conn, network_queue))
        except KeyboardInterrupt:
            print("Caught interrupt, shutting down server")
            s.close()
            break 

def machine(config):
    # get the unique process id of this thread
    config.append(os.getpid())

    global client_code 
    print(config) 

    # create a server thread to listen for messages
    network_queue = []
    init_thread = Thread(target=init_machine, args=(config, network_queue)) 
    init_thread.daemon = True # allow for threads to exit
    init_thread.start() #add delay to initialize the server-side logic on all processes 

    time.sleep(2) # extensible to multiple producers
    
    # create a client thread to Other Machine A that can send messages
    client_thread = Thread(target=client, args=(config[1], config[2], config[3], network_queue)) 
    client_thread.daemon = True
    client_thread.start()
 
    # the random number generator for when there is no message in the queue
    try:
        while True: 
            client_code = random.randint(1, 10)
    except KeyboardInterrupt:
        pass

localHost= "127.0.0.1"

if __name__ == '__main__':
    # define the three process ports when running on one machine
    port1 = 2056
    port2 = 3056
    port3 = 4056

    # define the config of other machines that should be connected to
    config1=[localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1,))
    
    config2=[localHost, port2, port3, port1]
    p2 = Process(target=machine, args=(config2,))
    
    config3=[localHost, port3, port1, port2]
    p3 = Process(target=machine, args=(config3,))
    
    # start the processes / threads
    p1.start()
    p2.start()
    p3.start()

    # wait for each process to finish (is this necessary?)
    p1.join()
    p2.join()
    p3.join()