
import sys
from project.motetest import *

check_rates = [2, 4, 8, 16, 32, 64]
pkt_sizes = [10, 33, 43, 53, 63, 73, 83, 93, 103, 110]

if __name__ == "__main__":

    # get motes
    motes = get_motes_ports()
    print('mote(s) found:', motes)

    if len(motes) < 2:
        print('need at least 2 motes')
        sys.exit(0)

    # test for every check rate
    for check_rate in check_rates:

        make_clean()

        # upload receiver & connect serial, wait for ready
        make_upload('receiver', motes[0], ['TEST_DC_CHECK_RATE={}'.format(check_rate)])
        receiver_serial = SkySerial(motes[0])
        receiver_serial.wait_ready()
        print('connected to receiver')

        # upload sender & connect serial, wait for ready
        make_upload('sender', motes[1], ['TEST_DC_CHECK_RATE={}'.format(check_rate)])
        sender_serial = SkySerial(motes[1])
        sender_serial.wait_ready()
        print('connected to sender')

        # test for every packet size
        for pkt_size in pkt_sizes:

            # start receiver and sender (with packet size)
            receiver_serial.start()
            sender_serial.start()
            sender_serial.write('{}\n'.format(pkt_size))

            # wait for sender to finish sending
            sender_serial.wait_finished()
            sender_result = sender_serial.read_line()[:-1]

            # stop receiver and get receiver result
            receiver_serial.stop()
            receiver_result = receiver_serial.read_line()[:-1]

            result = 'check rate: {}Hz\tpayload size: {}\n{}\t{}\n' \
                .format(check_rate, pkt_size, sender_result, receiver_result)

            print(result)
            with open('result-duty.txt', 'a') as f:
                f.write(result+'\n')

        # close serial ports
        sender_serial.close()
        receiver_serial.close()

