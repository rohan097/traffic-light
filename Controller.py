import shlex
import subprocess
import time
import RPi.GPIO as GPIO
from subprocess import Popen


command1 = ('unbuffer python3 /home/rohan/traffic-light/Vehicle.py ' +
            '"/home/rohan/GDG/video2.avi" 1')
command2 = ('unbuffer python3 /home/rohan/traffic-light/Vehicle.py ' +
            '"/home/rohan/GDG/video2.avi" 2')
command3 = ('unbuffer python3 /home/rohan/traffic-light/Vehicle.py ' +
            '"/home/rohan/GDG/video2.avi" 3')
command4 = ('unbuffer python3 /home/rohan/traffic-light/Vehicle.py ' +
            '"/home/rohan/GDG/video2.avi" 4')

inc1 = 0
inc2 = 0
inc3 = 0
inc4 = 0
ind = [0, 1, 2, 3]
multifac = 4
tl = [0, 0, 0, 0]
v_count = [4, 2, 0, 0]
lane1 = [2, 3, 4]
lane2 = [17, 27, 22]
lane3 = [10, 9, 11]
lane4 = [0, 5, 6]
GPIO.setmode(GPIO.BCM)


def run_command():

    global inc1, inc2, inc3, inc4, v_count
    process1 = Popen(shlex.split(command1),
                     stdout=subprocess.PIPE, start_new_session=True)
    process2 = Popen(shlex.split(command2), stdout=subprocess.PIPE)
    process3 = Popen(shlex.split(command3), stdout=subprocess.PIPE)
    process4 = Popen(shlex.split(command4), stdout=subprocess.PIPE)

    while True:
        output1 = process1.stdout.readline()
        output2 = process2.stdout.readline()
        output3 = process3.stdout.readline()
        output4 = process4.stdout.readline()

        if output1 or output2 or output3 or output4:
            inc1 = list(map(int, (output1.decode('utf-8')).strip().split()))[0]
            inc2 = list(map(int, (output2.decode('utf-8')).strip().split()))[0]
            inc3 = list(map(int, (output3.decode('utf-8')).strip().split()))[0]
            inc4 = list(map(int, (output4.decode('utf-8')).strip().split()))[0]

        v_count = [inc1, inc2, inc3, inc4]
        print(v_count)
        get_count()
        fill_queue()
        initial()
        run_cycle()


def swap(a, x, y):

    tmp = a[x]
    a[x] = a[y]
    a[y] = tmp


def get_count():

    v_count.append(inc1)
    v_count.append(inc2)
    v_count.append(inc3)
    v_count.append(inc4)


def get_max(x, y):

    if x >= y:
        return x
    return y


def fill_queue():

    for i in range(len(v_count)):
        for j in range(len(v_count) - 1, i, -1):
            if v_count[j] > v_count[j - 1]:
                swap(v_count, j, j - 1)
                swap(ind, j, j - 1)


def switch_light(temp, colour, state):

    lane_dict = {0: lane1, 1: lane2, 2: lane3, 3: lane4}
    colour_dict = {'R': 0, 'Y': 1, 'G': 2}
    lane = lane_dict[temp]
    if state == 'OFF':
        # print lane[colour_dict[colour]], "LOW"
        GPIO.output(lane[colour_dict[colour]], GPIO.LOW)
    elif state == 'ON':
        # print lane[colour_dict[colour]], "HIGH"
        GPIO.output(lane[colour_dict[colour]], GPIO.HIGH)
    else:
        print('Invalid State')
        exit(1)


def run_cycle():

    cycle_completed = 0
    print('------------------------------')
    count = 0
    for i in ind:

        tl[i] = 2  # Green
        tl[(i + 1) % 4] = 0  # make others red
        tl[(i + 2) % 4] = 0
        tl[(i + 3) % 4] = 0

        # minimum Green time 20 secs
        sleep_time = get_max(20, multifac * v_count[count])
        sleep_time = min(sleep_time, 120)  # get_max green time 2 minutes
        ready_time = sleep_time - 6
        print('GREEN for ', i, ' RED for others')
        print('wait for', ready_time, 'seconds...')

        switch_light(i, 'R', 'OFF')
        switch_light(i, 'G', 'ON')

        time.sleep(ready_time)  # time for yellow is  6 secs

        switch_light(i, 'G', 'OFF')

        tl[ind[(count + 1) % 4]] = 1
        print('YELLOW for', ind[(count + 1) % 4])

        switch_light(i, 'G', 'OFF')

        print('wait for 6 more seconds...')
        switch_light(ind[(count + 1) % 4], 'Y', 'ON')
        # switch_light(i,'Y',"ON")

        time.sleep(4)

        switch_light(ind[(count + 1) % 4], 'Y', 'OFF')
        switch_light(i, 'R', 'ON')

        count = (count + 1) % 4
    cycle_completed = 1


def initial():

    for i in range(0, 4):
        for j in ['Y', 'G']:
            switch_light(i, j, 'OFF')
        switch_light(i, 'R', 'ON')


def main():

    for i in lane1 + lane2 + lane3 + lane4:
        GPIO.setup(i, GPIO.OUT)
    run_command()


if __name__ == '__main__':

    main()
