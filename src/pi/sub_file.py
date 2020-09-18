#!/usr/bin/env python3

from subprocess import Popen, PIPE, DEVNULL
from sys import argv
import signal
import time
from time import sleep
import os

do_work = True

class Subscriber:
    proc = None
    frequency = 0
    measurement_interval_seconds = 1.0
    do_work = True
    def stop(self):
        self.proc.kill()
        self.do_work = False
    def wait(self):
        self.proc.wait()
    def sub_data(self):
        self.proc = Popen(['mosquitto_sub', '-h', '192.168.100.199', '-p', '8883', '-t', 'abc', '--cafile', '../../certs/ca.crt', '--cert', '../../certs/client.crt', '--key', '../../certs/client.key'], stdout = PIPE);
    def calc_frequency(self):
        while self.do_work:
            print('\rfrequency: {} Hz; '.format(self.frequency), end = '')
            mosquitto_cpu_usage = os.popen('''pgrep -x mosquitto | xargs top -bn1 -p | grep mosquitto | awk '{print $9}' ''').readline().rstrip()
            overall_cpu_usage = os.popen('''top -bn1 | grep "Cpu(s)" | sed "s/.*, *\\([0-9.]*\\)%* id.*/\\1/" | awk '{print 100 - $1"%"}' ''').readline().rstrip()
            print('overall cpu usage: {} '.format(overall_cpu_usage), end = '')
            print('; mosquitto cpu usage: {}% '.format(mosquitto_cpu_usage), end = '')
            counter = 0
            start = time.time()
            for i in iter(self.proc.stdout.readline, ''):
                counter += 1
                if (time.time() - start) >= self.measurement_interval_seconds:
                    self.frequency = counter / self.measurement_interval_seconds
                    break

subscriber = Subscriber()

def signal_handler(sig, frame):
    print('stop subscriber')
    subscriber.stop()
    do_work = False
        
def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        subscriber.sub_data()
        subscriber.calc_frequency()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
