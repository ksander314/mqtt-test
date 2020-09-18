#!/usr/bin/env python3

from subprocess import Popen, PIPE, DEVNULL
from sys import argv
import signal
import time
from time import sleep
import os

do_work = True

class Mosquitto:
    proc = None
    def stop(self):
        self.proc.kill()
    def wait(self):
        self.proc.wait()
    def start(self):
        self.proc = Popen(['mosquitto', '-c', '../../cfg/mosquitto.conf'], stdout = DEVNULL, stderr = DEVNULL);

class Subscriber:
    proc = None
    def stop(self):
        self.proc.kill()
    def wait(self):
        self.proc.wait()
    def start(self):
        self.proc = Popen(['./sub_file.py']);

subscriber = Subscriber()
mosquitto = Mosquitto()

def signal_handler(sig, frame):
    print('stop mosquitto')
    mosquitto.stop()
    print('stop subscriber')
    subscriber.stop()
        
def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        mosquitto.start()
        subscriber.start()
        subscriber.wait()
        mosquitto.wait()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
