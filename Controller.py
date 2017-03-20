import subprocess
from subprocess import Popen
import shlex
import sys
import time

command1 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 1'
command2 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 2'
command3 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 3'
command4 = 'unbuffer python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi" 4'
inc1 = 0
inc2 = 0
inc3 = 0
inc4 = 0
ind = [0,1,2,3]
multifac = 4
tl = [0,0,0,0]
vCount = [4, 2 , 0 , 0]

def run_command():

    process1 = Popen(shlex.split(command1), stdout=subprocess.PIPE, start_new_session = True)
    process2 = Popen(shlex.split(command2), stdout=subprocess.PIPE)
    process3 = Popen(shlex.split(command3), stdout=subprocess.PIPE)
    process4 = Popen(shlex.split(command4), stdout=subprocess.PIPE)

    while True:
        output1 = process1.stdout.readline()
        output2 = process2.stdout.readline()
        output3 = process3.stdout.readline()
        output4 = process4.stdout.readline()

        if output1 or output2 or output3 or output4:
            inc1 = list(map(int, (output1.decode("utf-8")).strip().split()))[0]
            inc2 = list(map(int, (output2.decode("utf-8")).strip().split()))[0]
            inc3 = list(map(int, (output3.decode("utf-8")).strip().split()))[0]
            inc4 = list(map(int, (output4.decode("utf-8")).strip().split()))[0]

        vCount = [inc1, inc2, inc3, inc4]
        print (vCount)
        getCount()
        fillQueue()
        runCycle()

    rc = process1.poll()

def swap( A, x, y ):
    tmp = A[x]
    A[x] = A[y]
    A[y] = tmp

def getCount():
    vCount.append(inc1)
    vCount.append(inc2)
    vCount.append(inc3)
    vCount.append(inc4)

def max(x,y):
    if (x >= y ):
        return(x)
    return (y)

def fillQueue():
    for i in range(len(vCount)):
        for j in range(len(vCount) - 1, i , -1):
            if( vCount[j]  > vCount[j-1]):
                swap( vCount, j, j - 1 )
                swap(ind,j,j-1)

def runCycle():
    cycleCompleted = 0
    print('------------------------------')
    iter = 0
    for i in ind:

        tl[i]  = 2                          #Green
        tl[(i+1)%4] = 0                     #make others red
        tl[(i+2)%4] = 0
        tl[(i+3)%4] = 0

        sleepTime = max(20, multifac*vCount[iter])  #minimum Green time 20 secs
        sleepTime = min(sleepTime, 120)             #max green time 2 minutes
        readyTime = sleepTime  - 6
        print('GREEN for ',i,' RED for others')
        print ('wait for', readyTime ,'seconds...')

        time.sleep(readyTime)                       #time for yellow is  6 secs

        tl[ind[(iter+1)%4]] = 1
        print('YELLOW for' , ind[(iter+1)%4])

        print('wait for 6 more seconds...')
        time.sleep(4)
        iter = (iter+1)%4
    cycleCompleted = 1

def main():
    run_command()

if __name__ == '__main__':
    main()
