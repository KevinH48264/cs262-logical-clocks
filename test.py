import time
log_file = open('port_{}_log.txt'.format(1000), 'w')

while True:
    log_file.write("received")
    time.sleep(5)