#!/usr/bin/env python3

from subprocess import Popen, PIPE, DEVNULL
import signal
from sys import argv

class Publisher:
    gnss_pub_proc = None
    sonar_pub_proc = None
    orientation_pub_proc = None
    def stop(self):
        self.gnss_pub_proc.kill()
        self.sonar_pub_proc.kill()
        self.orientation_pub_proc.kill()
    def publish(self):
        self.pub_gnss_data('10')
        self.pub_sonar_data('7')
        self.pub_orirentation_data('20')
    def pub_gnss_data(self, frequency):
        self.gnss_pub_proc = Popen(['./pub_file.py', 'gnss.data', frequency], stdout = DEVNULL)

    def pub_sonar_data(self, frequency):
        self.sonar_pub_proc = Popen(['./pub_file.py', 'sonar.data', frequency], stdout = DEVNULL)

    def pub_orirentation_data(self, frequency):
        self.orientation_pub_proc = Popen(['./pub_file.py', 'orientation.data', frequency], stdout = DEVNULL)

    def wait(self):
        self.gnss_pub_proc.wait()
        self.sonar_pub_proc.wait()
        self.orientation_pub_proc.wait()

publishers = []

def signal_handler(sig, frame):
    for i, publisher in enumerate(publishers):
        print('stop publisher #{}'.format(i))
        publisher.stop()

class Args:
    number_of_publishers = 1
    usage = f'usage:\n\t {argv[0]} NUMBER_OF_PUBLISHERS'
    def __init__(self, argv):
        if len(argv) > 1:
            if argv[1].isdigit() == False:
                raise RuntimeError(f'bad number of publishers "{argv[1]}"')
            else:
                self.number_of_publishers = int(argv[1])
        
def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        arg = Args(argv)
        for i in range(0, arg.number_of_publishers):
            print('create publisher #{}'.format(i))
            publishers.append(Publisher())
        for publisher in publishers:
            publisher.publish()
        for publisher in publishers:
            publisher.wait()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
