# -*- coding: utf-8 -*-
"""
Created on Mon May 25 09:10:50 2020

@author: paula
@see: https://amrbook.com/coding/python/automate-adb-with-python/
"""
""" 
import subprocess

adbShell = ['adb', 'shell']
cmd = subprocess.Popen(adbShell, stdin = subprocess.PIPE)
cmd.communicate(b'top')
"""
import os

import time
#import datetime

#import csv

#import multiprocessing
import threading

import adb_commands as commands


# path to adb (home)
# path = "P:\\adb\\platform-tools"
# path to adb (work)
path = "C:\\bin\\adb\\platform-tools"

# Change the directory to it.

os.chdir(path)

webApp = True

# checking for connected devices

os.popen("adb devices")


print("Waiting for connection ...")

topAll = os.popen("adb shell top -d 1").read().split('host', 1)[1]
print(topAll)

print("--------------------------------------\n Please choose a PID from above:")
pid = input()
if webApp:
    print("chrome id:")
    pid2 = input()
    print("second chrome id:")
    pid3 = input()
print("\n Your report for " + pid + " is being generated")

bat_thread = threading.Thread(target=commands.battery, args=(pid))
top_thread = threading.Thread(target=commands.top, args=(pid))
gpuU_thread = threading.Thread(target=commands.gpuUtilization, args=(pid))
topI_thread = threading.Thread(target=commands.topIndividual, args=(pid))


bat_thread.start()
top_thread.start()
topI_thread.start()
gpuU_thread.start()

if webApp:
    topI_thread2 = threading.Thread(target=commands.topIndividual, args=(pid2))
    topI_thread3 = threading.Thread(target=commands.topIndividual, args=(pid3))
    topI_thread2.start()
    topI_thread3.start()
    topI_thread2.join()
    topI_thread3.join()

bat_thread.join()
top_thread.join()
topI_thread.join()
gpuU_thread.join()  
