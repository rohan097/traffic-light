import subprocess
from subprocess import Popen
command1 = 'python3 /home/rohan/GDG/Vehicle_Mark5.py "/home/rohan/GDG/video2.avi"'

p = Popen(command1, shell = True, stdout = subprocess.PIPE)
