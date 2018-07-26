import subprocess
import sys
import time

impo
import serial

check_rates = [2, 4, 8, 16, 32, 64]
pkt_sizes = [10, 33, 43, 53, 63, 73, 83, 93, 103, 110]

if __name__ == "__main__":

    # get motes
    motes = subprocess.getoutput('ls /dev/tty.usbserial*').split('\n')
    print('mote(s) found:', motes)

    if len(motes) < 2:
        print('need at least 2 motes')
        sys.exit(0)

    check_rates.reverse()
    for check_rate in check_rates:

        print('make clean')
        subprocess.call(['make', 'clean'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # make receiver and upload to mote #1 with given duty cycle
        print('make & upload receiver')
        subprocess.call(['make',
                         'receiver.upload',
                         'MOTES={}'.format(motes[0]),
                         'DEFINES=TEST_DC_CHECK_RATE={}'.format(check_rate)])
                        # stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
                         'MOTES={}'.format(motes[1]),
                         'DEFINES=TEST_DC_CHECK_RATE={}'.format(check_rate)])
                        # stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # open serial to sender
        sender_serial = serial.Serial(port=motes[1], baudrate=115200)
        print("connected to sender")

        # ready for sender to be ready
        while True:
            line = sender_serial.readline().decode()
            if line == 'ready\n':
                print('sender ready')
                break
            else:
                print(line, end='')

        for pkt_size in pkt_sizes:
            # start receiver
            receiver_serial.write('start\n'.encode())
            print(receiver_serial.readline().decode(), end='')

            # start sender
            sender_serial.write('start\n'.encode())
            sender_serial.write((str(pkt_size) + '\n').encode())
            print(sender_serial.readline().decode(), end='')

            # wait for sender to finish sending
            print(sender_serial.readline().decode(), end='')
            sender_result = sender_serial.readline().decode()[0:-1]

            # stop receiver and get receiver result
            receiver_serial.write('stop\n'.encode())
            print(receiver_serial.readline().decode(), end='')
            receiver_result = receiver_serial.readline().decode()[0:-1]

            result = 'check rate: {}Hz\npayload size: {}\n{}\t{}\n'\
                .format(check_rate, pkt_size, sender_result, receiver_result)

            print(result)
            with open('result-duty.txt', 'a') as f:
                f.write(result+'\n')

        # close serial ports
        sender_serial.close()
        receiver_serial.close()

