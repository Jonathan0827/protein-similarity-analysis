
import subprocess
while True:
    proc = subprocess.Popen(["python3 res.py"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(out)