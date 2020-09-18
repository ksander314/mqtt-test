#!/usr/bin/env python3

from os import (system, path)
from sys import argv
import signal
from time import sleep

def pub_data_from_file(arg):
    return_code = system(f'mosquitto_pub -h {arg.host} -p {arg.port} -t {arg.topic} -f {arg.file_name}  --cafile ../../certs/ca.crt --cert ../../certs/client.crt --key ../../certs/client.key');
    if return_code != 0:
        print(f'failed to pub data from file {arg.file_name}')

class Args:
    frequency = 1
    file_name = ""
    host = "localhost"
    port = "8883"
    topic = "abc"
    usage = f'usage:\n\t {argv[0]} PATH_TO_FILE FREQUENCY_IN_HZ'
    def __init__(self, argv):
        if len(argv) < 3:
            raise RuntimeError(self.usage)
        self.file_name = argv[1]
        if path.isfile(self.file_name) == False:
            raise RuntimeError(f'file "{self.file_name}" not found')
        if argv[2].isdigit() == False:
            raise RuntimeError(f'bad frequency "{argv[2]}"')
        self.frequency = int(argv[2])

do_work = True
        
def signal_handler(sig, frame):
    do_work = False
        
def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        arg = Args(argv)
        while do_work:
            pub_data_from_file(arg)
            sleep(1 / arg.frequency)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
