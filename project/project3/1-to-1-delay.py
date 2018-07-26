import sys

import time
from motetest import *

delays = [0, 1, 2, 3, 4, 5]


if __name__ == "__main__":

    # get motes
    motes = get_motes_ports()
    print(len(motes), 'mote(s) found:', motes)

    if len(motes) < 2:
        print('need at least 2 motes')
        sys.exit(0)

    make_clean()

    # upload receiver & connect serial, wait for ready
    # make_upload('receiver', motes[0], ['TEST_DC_CHECK_RATE={}'.format(check_rate)])
    make_upload('receiver', motes[0], [])
    receiver_serial = SkySerial(motes[0])
    receiver_serial.wait_ready()
    print('connected to receiver')

    # upload sender & connect serial, wait for ready
    # make_upload('sender', motes[1], ['TEST_DC_CHECK_RATE={}'.format(check_rate)])
    make_upload('sender', motes[1], [])
    sender_serial = SkySerial(motes[1])
    sender_serial.wait_ready()
    print('connected to sender')

    # test for every packet size
    for i in range(5):
        for delay in delays:
            # start receiver and sender (with packet size)
            receiver_serial.start()
            print('receiver started')
            time.sleep(0.5)

            sender_serial.start()
            print('sender started')

            sender_serial.write(str(delay) + '\n')

            # wait for sender to finish sending
            sender_serial.wait_finished()
            sender_result = sender_serial.read_line()[:-1]

            time.sleep(0.5)

            # stop receiver and get receiver result
            receiver_serial.stop()
            receiver_result = receiver_serial.read_line()[:-1]

            result = '{}\t{}'.format(sender_result, receiver_result)
            print('delay: {}, result: {}\n'.format(delay, result))

            with open('1-to-1-delay.txt', 'a') as f:
                f.write(result + '\n')

        with open('1-to-1-delay.txt', 'a') as f:
            f.write('\n')

    # close serial ports
    sender_serial.close()
    receiver_serial.close()

