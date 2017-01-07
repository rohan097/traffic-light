import subprocess
from subprocess import Popen
command1 = 'python3 /home/rohan/traffic-light/Vehicle.py "/home/rohan/GDG/video2.avi"'

p = Popen(command1, shell = True, stdout = subprocess.PIPE)

while True:
    ret = p.returncode()

    print (ret)
    if ret < 0 or ret == None:
        break
