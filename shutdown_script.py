'''contains function to run shell script to shutdown raspberry pi'''
from subprocess import call

def shutdown_script():
    '''script used to run shell command to shutdown the raspberry pi'''
    call("sudo shutdown -h now", shell=True)
