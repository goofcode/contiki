import subprocess
import sys
import time

import serial

pkt_sizes = [10, 33, 43, 53, 63, 73, 83, 93, 103, 110]

if __name__ == "__main__":

    # get motes
    motes = subprocess.getoutput('ls /dev/tty.usbserial*').split('\n')
    print('mote(s) found:', motes)

    if len(motes) < 3:
        print('need at least 3 motes')
        sys.exit(0)

    print('make clean')
    subprocess.call(['make', 'clean'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # make receiver and upload to mote #1 with given duty cycle
    print('make & upload receiver')
    subprocess.call(['make',
                     'receiver.upload',
                     'MOTES={}'.format(motes[0])])

    # open serial to receiver
    receiver_serial = serial.Serial(port=motes[0], baudrate=115200)
    print("connected to receiver")

    # ready for receiver to be ready
    while True:
        line = receiver_serial.readline().decode()
        if line == 'ready\n':
            print('receiver ready')
            break
        else:
            print(line, end='')

    # make sender and upload to mote #2
    print('make & upload sender')
    subprocess.call(['make',
                     'sender.upload',
                     'MOTES={}'.format(motes[1])])

    # open serial to sender
    sender1_serial = serial.Serial(port=motes[1], baudrate=115200)
    print("connected to sender 1")

    # ready for sender to be ready
    while True:
        line = sender1_serial.readline().decode()
        if line == 'ready\n':
            print('sender1 ready')
            break
        else:
            print(line, end='')

    subprocess.call(['make',
                     'sender.upload',
                     'MOTES={}'.format(motes[2])])

    sender2_serial = serial.Serial(port=motes[2], baudrate=115200)
    print("connected to sender 2")

    # ready for sender to be ready
    while True:
        line = sender2_serial.readline().decode()
        if line == 'ready\n':
            print('sender2 ready')
            break
        else:
            print(line, end='')


    for pkt_size in pkt_sizes:
        # start receiver
        receiver_serial.write('start\n'.encode())
        print(receiver_serial.readline().decode(), end='')

        # start sender
        sender1_serial.write('start\n'.encode())
        sender1_serial.write((str(pkt_size) + '\n').encode())
        print(sender1_serial.readline().decode(), end='')

        sender2_serial.write('start\n'.encode())
        sender2_serial.write((str(pkt_size) + '\n').encode())
        print(sender2_serial.readline().decode(), end='')

        # wait for sender to finish sending
        print(sender1_serial.readline().decode(), end='')
        print(sender2_serial.readline().decode(), end='')
        sender1_result = sender1_serial.readline().decode()[0:-1]
        sender2_result = sender2_serial.readline().decode()[0:-1]

        # stop receiver and get receiver result
        receiver_serial.write('stop\n'.encode())
        print(receiver_serial.readline().decode(), end='')
        receiver_result = receiver_serial.readline().decode()[0:-1]

        result = '{}\t{}\t{}\n'\
            .format(sender1_result, sender2_result, receiver_result)

        print(result)
        with open('result-csma-2to1.txt', 'a') as f:
            f.write(result)

    with open('result-csma-2to1.txt', 'a') as f:
        f.write('\n\n')

    # close serial ports
    sender1_serial.close()
    receiver_serial.close()

