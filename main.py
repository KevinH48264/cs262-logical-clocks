from multiprocessing import Process, Lock
import os 
import socket 
from _thread import * 
import threading
import time 
from threading import Thread 
import random
from datetime import datetime
 
# server, receives messages
def server(conn, network_queue, network_lock):
    print("server accepted connection" + str(conn)+"\n")

    while True: 
        try:
            data = conn.recv(1024) 
            # print("msg received\n") 
            dataVal = data.decode('ascii') 
            # print("msg received:", dataVal) 

            # hold incoming messages from the client connection
            with network_lock:
                if dataVal:
                    network_queue.append(dataVal)
        except KeyboardInterrupt:
            print("Caught interrupt, shutting down connection")
            conn.close()
            break 
 
# initialize a client, sending messages
def client(portValMachine, portValA, portValB, network_queue, network_lock, test=False, test_client_code=-1): 
    global client_code

    host= "127.0.0.1" 
    portA = int(portValA) 
    portB = int(portValB) 
    s_A = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s_B = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    clock_rate_sleep_val = 1.0 / random.randint(1, 6) # clock rate defined here
    logical_clock = 0

    # for testing
    if test_client_code != -1:
        client_code = test_client_code

    # open log
    with network_lock:
        log_file = open('port_{}_log.txt'.format(portValMachine), 'w')
        log_file.close()
    print("port value: ", portValMachine, "Clock rate: ", clock_rate_sleep_val)

    try: 
        s_A.connect((host,portA))
        print("Client-side connection success to port val:" + str(portValA) + "\n")

        s_B.connect((host,portB))
        print("Client-side connection success to port val:" + str(portValB) + "\n")

        # on each clock cycle
        while True: 
            try:
                # TODO: send messages and edit Log here
                # print("network queue: ", network_queue)
                log_message = ""
                log_file = open('port_{}_log.txt'.format(portValMachine), 'a')

                # there is something in the network queue
                if len(network_queue) > 0:
                    # the virtual machine should take one message off the queue, update the local logical clock, 
                    # and write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time.
                    with network_lock:
                        message = str(network_queue.pop(0))

                    # logical time is the last portion of every message, split by _
                    sender_logical_time = int(message.split("_")[-1])
                    logical_clock = max(sender_logical_time, logical_clock) + 1
                    global_time = str(datetime.time(datetime.now()))
                    # get queue length after popping
                    queue_length = str(len(network_queue))
                    log_file.write("logical clock: " + str(logical_clock) + " | received" + " | global time: " + global_time + " | queue length: " + queue_length + "\n")

                else:
                    # no message in the queue, follow scope and update log

                    # sent message incorporates logical clock time
                    codeVal = str(client_code) + "_" + str(logical_clock)

                    if client_code == 1:
                        s_A.send(codeVal.encode('ascii'))
                        logical_clock += 1
                        global_time = str(datetime.time(datetime.now()))
                        log_file.write("logical clock: " + str(logical_clock) + " | sent: " + str(1) + " | global time: " + global_time + "\n")
                        print("msg sent to one client", codeVal)

                    elif client_code == 2:
                        s_B.send(codeVal.encode('ascii'))
                        logical_clock += 1
                        global_time = str(datetime.time(datetime.now()))
                        log_file.write("logical clock: " + str(logical_clock) + " | sent: " + str(2) + " | global time: " + global_time + "\n")
                        print("msg sent to other client", codeVal)

                    # Do we only update the logical clock once here?
                    elif client_code == 3:
                        s_A.send(codeVal.encode('ascii'))
                        #logical_clock += 1
                        #log_file.write("sent" + "_" + global_time + "_" + str(logical_clock))
                        s_B.send(codeVal.encode('ascii'))
                        logical_clock += 1
                        global_time = str(datetime.time(datetime.now()))
                        log_file.write("logical clock: " + str(logical_clock) + " | sent: " + str(3) + " | global time: " + global_time + "\n")
                        print("msg sent to both clients", codeVal)
                    else:
                        logical_clock += 1
                        global_time = str(datetime.time(datetime.now()))
                        log_file.write("logical clock: " + str(logical_clock) + " | internal event " + "| global time: " + global_time + "\n")
                        print("internal event logged")

                time.sleep(clock_rate_sleep_val)
                log_file.close()

            except KeyboardInterrupt:
                print("Caught interrupt, shutting down client")
                s_A.close()
                s_B.close()
                log_file.close()
                break 

            if test:
                lines = ""
                with open('port_{}_log.txt'.format(portValMachine)) as f:
                    lines = f.readlines()
                    print("LINES", lines)
                return lines

    except socket.error as e: 
        print("Error connecting client: %s" % e)
        log_file.close()

    log_file.close()
 
# initialize a server machine to connect with clients
def init_machine(config, network_queue, network_lock, test=False):
    HOST = str(config[0],)
    PORT = int(config[1])
    print("starting server | port val:", PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    
    original_time = time.time()
    while True: 
        # always accept new connections from other clients and start a server connection between that client and server
        try:
            conn, addr = s.accept()
            start_new_thread(server, (conn, network_queue, network_lock))
        except KeyboardInterrupt:
            print("Caught interrupt, shutting down server")
            s.close()
            break 

        if test and time.time() - original_time > 1:
            break
    return

def machine(config, test=False, client_code_list=[]):
    # get the unique process id of this thread
    config.append(os.getpid())

    global client_code 
    print(config) 

    # create a server thread to listen for messages
    network_queue = []
    network_lock = Lock()

    init_thread = Thread(target=init_machine, args=(config, network_queue, network_lock)) 
    init_thread.daemon = True # allow for threads to exit
    init_thread.start() #add delay to initialize the server-side logic on all processes 

    time.sleep(2) # extensible to multiple producers
    
    # create a client thread to Other Machine A that can send messages
    client_thread = Thread(target=client, args=(config[1], config[2], config[3], network_queue, network_lock)) 
    client_thread.daemon = True
    client_thread.start()
 
    # the random number generator for when there is no message in the queue
    while True:
        try: 
            client_code = random.randint(1, 10)
            client_code_list.append(client_code)
            time.sleep(0.01)
        except KeyboardInterrupt:
            print("Caught interrupt, shutting down machine")
            break

        if test and len(client_code_list) > 5:
            break
    return

localHost= "127.0.0.1"

if __name__ == '__main__':
    # define the three process ports when running on one machine
    port1 = 2056
    port2 = 3056
    port3 = 4056

    # define the config of other machines that should be connected to
    #global p1 
    config1=[localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1,))

    #global p2
    config2=[localHost, port2, port3, port1]
    p2 = Process(target=machine, args=(config2,))

    #global p3
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
    print("Threads all terminated.")
