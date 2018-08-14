import csv
import sys

import time
import os
import numpy as np
from motetest import *

pkt_sizes = [10, 31, 41, 51, 61, 71, 81, 91, 101, 108]

project = 'project5'
test_inputs = pkt_sizes

if __name__ == "__main__":

    # move to project directory
    os.chdir(project)

    # get motes
    motes = get_motes_ports()
    print(len(motes), 'mote(s) found:', motes)

    if len(motes) < 2:
        print('need at least 2 motes')
        sys.exit(0)

    make_clean()

    # upload receiver & connect serial, wait for ready
    make_upload('receiver', motes[0], [])
    receiver_serial = SkySerial(motes[0])
    receiver_serial.wait_ready()
    print('connected to receiver')
    receiver_addr = receiver_serial.read_line()

    # upload sender & connect serial, wait for ready
    make_upload('sender', motes[1], [])
    sender_serial = SkySerial(motes[1])
    sender_serial.wait_ready()
    print('connected to sender')
    sender_serial.write(receiver_addr)

    time.sleep(0.5)

    # test result of tx_count, tx_clock, rx_count, rx_clock
    result = []
    for i in range(len(test_inputs)):
        result.append([])

    # test for every packet size
    for i in range(5):

        for idx, test_input in enumerate(test_inputs):

            # start receiver and sender (with packet size)
            receiver_serial.start()
            time.sleep(0.3)
            print('receiver started')

            sender_serial.start()
            sender_serial.write(str(test_input) + '\n')
            print('sender started')

            # wait for sender to finish sending
            sender_serial.wait_finished()
            sender_result = sender_serial.read_line()[:-1]

            # stop receiver and get receiver result
            time.sleep(0.5)
            receiver_serial.stop()
            receiver_result = receiver_serial.read_line()[:-1]

            # append result for this test_input
            current_result = [int(x) for x
                              in '{}\t{}'.format(sender_result, receiver_result).split('\t')]
            result[idx].append(current_result)
            print(current_result)
            # print(result)

    result = np.mean(result, axis=1).tolist()
    print(result)

    # save result
    with open('result.csv', 'a') as f:
        csv_writer = csv.writer(f)
        for row in result:
            csv_writer.writerow(row)

    # close serial ports
    sender_serial.close()
    receiver_serial.close()

