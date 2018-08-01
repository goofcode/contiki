import sys
import time
import os
import numpy as np
import csv

from motetest import *

pkt_sizes = [10, 33, 43, 53, 63, 73, 83, 93, 103, 110]

project = 'project4'
test_inputs = pkt_sizes

if __name__ == "__main__":

    # move to project directory
    os.chdir(project)

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

    # test result of tx_count, tx_clock, rx_count, rx_clock
    result = []
    for i in range(len(test_inputs)):
        result.append([])

    # test for every packet size
    for test in range(5):

        for idx, test_input in enumerate(test_inputs):

            # start receiver and sender (with packet size)
            receiver_serial.start()
            print('receiver started')
            time.sleep(0.3)

            for i in range(2):
                sender_serial[i].start()
                sender_serial[i].write(str(test_input) + '\n')
                print('sender {} started'.format(i))

            # wait for sender to finish sending
            sender_result = []
            for i in range(2):
                sender_serial[i].wait_finished()
                sender_result.append(sender_serial[i].read_line()[:-1])

            # stop receiver and get receiver result
            time.sleep(0.5)
            receiver_serial.stop()
            receiver_result = receiver_serial.read_line()[:-1]

            current_result = [int(x) for x
                              in '{}\t{}\t{}'.format(sender_result[0], sender_result[1],receiver_result).split('\t')]
            result[idx].append(current_result)
            print(current_result)

    result = np.mean(result, axis=1).tolist()
    print(result)

    # save result
    with open('result.csv', 'a') as f:
        csv_writer = csv.writer(f)
        for row in result:
            csv_writer.writerow(row)

    # close serial ports
    sender_serial[0].close()
    sender_serial[1].close()
    receiver_serial.close()

