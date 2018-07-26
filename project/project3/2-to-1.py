import sys

import time
from motetest import *

pkt_sizes = [10, 33, 43, 53, 63, 73, 83, 93, 103, 110]

if __name__ == "__main__":

    # get motes
    motes = get_motes_ports()
    print(len(motes), 'mote(s) found:', motes)

    if len(motes) < 3:
        print('need at least 3 motes')
        sys.exit(0)

    make_clean()

    # upload receiver & connect serial, wait for ready
    make_upload('receiver', motes[2], [])
    receiver_serial = SkySerial(motes[2])
    receiver_serial.wait_ready()
    print('connected to receiver')

    # upload sender & connect serial, wait for ready
    sender_serial = []
    for i in range(2):
        make_upload('sender', motes[i], [])
        sender_serial.append(SkySerial(motes[i]))
        sender_serial[i].wait_ready()
        print('connected to sender {}'.format(i))

    # test for every packet size

    for test in range(5):

        for pkt_size in pkt_sizes:

            # start receiver and sender (with packet size)
            receiver_serial.start()
            print('receiver started')
            time.sleep(0.5)

            for i in range(2):
                sender_serial[i].start()
                print('sender {} started'.format(i))
                sender_serial[i].write(str(pkt_size) + '\n')

            # wait for sender to finish sending
            sender_result = []
            for i in range(2):
                sender_serial[i].wait_finished()
                sender_result.append(sender_serial[i].read_line()[:-1])

            time.sleep(0.5)

            # stop receiver and get receiver result
            receiver_serial.stop()
            receiver_result = receiver_serial.read_line()[:-1]

            result = '{}\t{}\t{}'.format(sender_result[0], sender_result[1], receiver_result)
            print('packet size: {}, result: {}\n'.format(pkt_size, result))

            with open('2-to-1.txt', 'a') as f:
                f.write(result + '\n')

        with open('2-to-1.txt', 'a') as f:
            f.write('\n')

    # close serial ports
    sender_serial[0].close()
    sender_serial[1].close()
    receiver_serial.close()

