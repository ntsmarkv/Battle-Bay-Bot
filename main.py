import subprocess

while True:
    """However, you should be careful with the '.wait()'"""
    p = subprocess.Popen(['python3' '1.9.py']).wait()

    if p != 0:
        continue
    else:
        break