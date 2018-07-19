
import subprocess
import os
import sys

import time


check_rates = [2, 8, 32, 128]
pkt_sizes = [10, 33, 43, 53, 63, 73, 83, 93, 103, 110]

clean_cmd = 'make clean > /dev/null'
sender_cmd = 'make sender.upload login MOTE=1 DEFINES=TEST_DC_CHECK_RATE={},PKT_SIZE={} | grep --line-buffered "packets" >> send_result.txt 2>&1'
receiver_cmd = 'make receiver.upload login MOTE=2 DEFINES=TEST_DC_CHECK_RATE={} | grep --line-buffered "packets" >> recv_result.txt 2>&1'


for check_rate in check_rates:

    print(clean_cmd)
    clean = subprocess.Popen(clean_cmd, shell=True)
    clean.wait()

    cur_recv = receiver_cmd.format(check_rate)
    print(cur_recv)
    receiver = subprocess.Popen(cur_recv, shell=True)
    time.sleep(30)

    for pkt_size in pkt_sizes:

        print('check rate: {}, pkt size: {}'.format(check_rate, pkt_size))

        print(clean_cmd)
        clean = subprocess.Popen(clean_cmd, shell=True)
        clean.wait()

        cur_send = sender_cmd.format(check_rate, pkt_size)
        print(cur_send)
        sys.stdout.flush()

        sender = subprocess.Popen(cur_send, shell=True)

        time.sleep(int((1000/check_rate)*1.2))
        subprocess.call(["kill", str(sender.pid)])

        sys.stdout.flush()

    subprocess.call(["kill", receiver.pid])



