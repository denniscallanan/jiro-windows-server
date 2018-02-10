import subprocess, time, os, signal, sys

myprocess = subprocess.Popen([sys.executable, "b.py"])
time.sleep(2)
os.kill(myprocess.pid, signal.CTRL_C_EVENT)
time.sleep(2)
#myprocess.kill()