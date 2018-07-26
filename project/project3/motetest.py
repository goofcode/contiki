
import subprocess
import serial

def get_motes_ports():
    return subprocess.getoutput('ls /dev/tty.usbserial*').split('\n')

def make_clean():
    subprocess.call(['make', 'clean'])

def make_upload(target, port, defines):
    _make(target, port, defines, True)

def _make(target, port, defines, upload):

    make_command = ['make']

    # append target, port
    make_command.append('TARGET=sky')
    make_command.append(target + '.upload' if upload else '')
    make_command.append('MOTES={}'.format(port))

    # append defines
    if defines != [] and defines is not None:
        define_list = ''
        for define in defines:
            define_list += define + ','

        make_command.append('DEFINES=' + define_list[:-1])

    subprocess.call(make_command)


class SkySerial:

    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, baudrate=115200)

    def read_line(self):
        return self.serial.readline().decode()

    def wait_ready(self):
        self.wait_for('ready\n')

    def wait_finished(self):
        self.wait_for('finished\n')

    def write(self, line):
        self.serial.write(line.encode())

    def start(self):
        self.write('start\n')

    def stop(self):
        self.write('stop\n')

    def print_read_line(self):
        print(self.read_line(), end='')

    def wait_for(self, waiting):

        while True:
            line = self.read_line()
            print(line, end='')
            if line == waiting:
                break

    def close(self):
        self.serial.close()

