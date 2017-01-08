import subprocess
from subprocess import Popen
import shlex
import sys


command1 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 1'
command2 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 2'
command3 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 3'
command4 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 4'

def run_command(command1):

    process1 = Popen(shlex.split(command1), stdout=subprocess.PIPE, start_new_session = True)
    process2 = Popen(shlex.split(command2), stdout=subprocess.PIPE)
    process3 = Popen(shlex.split(command3), stdout=subprocess.PIPE)
    process4 = Popen(shlex.split(command4), stdout=subprocess.PIPE)

    while True:
        output1 = process1.stdout.readline()
        output2 = process2.stdout.readline()
        output3 = process3.stdout.readline()
        output4 = process4.stdout.readline()

        if (output1 == '' or output2 == '' or output3 == '' or output4 == '') and ((process1.poll() is not None) or (process2.poll() is not None) or(process3.poll() is not None) or(process4.poll() is not None)):
            break
        if output1 or output2 or output3 or output4:
            output1 = list(map(int, (output1.decode("utf-8")).strip().split()))
            output2 = list(map(int, (output2.decode("utf-8")).strip().split()))
            output3 = list(map(int, (output3.decode("utf-8")).strip().split()))
            output4 = list(map(int, (output4.decode("utf-8")).strip().split()))

    rc = process1.poll()
    return rc
    
def main():
    run_command(command1)

if __name__ == '__main__':
    main()
