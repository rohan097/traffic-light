import subprocess
from subprocess import Popen
import shlex
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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
lane1 = [2,3,4]
lane2 = [17,27,22]
lane3= [10,9,11]
lane4= [0,5,6]


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
        initial()
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

def switchLight(temp, colour, state):
	laneDict = {0:lane1, 1:lane2, 2:lane3, 3:lane4 }
	colourDict =  { 'R':0, 'Y':1, 'G':2}
	lane = laneDict[temp]
	if state == "OFF":
		#print lane[colourDict[colour]], "LOW"
		GPIO.output(lane[colourDict[colour]],GPIO.LOW)
	elif state == "ON":
		#print lane[colourDict[colour]], "HIGH"
		GPIO.output(lane[colourDict[colour]],GPIO.HIGH)
	else:
		print("Invalid State")
		exit(1)


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

        switchLight(i,'R',"OFF")
        switchLight(i,'G',"ON")

        time.sleep(readyTime)                       #time for yellow is  6 secs
        #time.sleep(1)   # WE NEED TO REMOVE THIS LINE AND UNCOMMENT THE PREVIOUS LINE

        switchLight(i,'G',"OFF")

        tl[ind[(iter+1)%4]] = 1
        print('YELLOW for' , ind[(iter+1)%4])

        switchLight(i,'G',"OFF")

        print('wait for 6 more seconds...')
        switchLight(ind[(iter+1)%4], 'Y',"ON")
        #switchLight(i,'Y',"ON")

        time.sleep(4)

        switchLight(ind[(iter+1)%4],'Y',"OFF")
        switchLight(i,'R',"ON")

        iter = (iter+1)%4
    cycleCompleted = 1


def initial():
        for i in range(0,4):
                for j in ['Y','G']:
                    switchLight(i,j,"OFF")
                switchLight(i,'R',"ON")

def main():
    for i in lane1+lane2+lane3+lane4:
        GPIO.setup(i,GPIO.OUT)
    run_command()

if __name__ == '__main__':
    main()
