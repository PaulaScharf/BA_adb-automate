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


# checking for connected devices

os.popen("adb devices")


print("Waiting for connection ...")

topAll = os.popen("adb shell top -d 1").read().split('host', 1)[1]
print(topAll)

print("--------------------------------------\n Please choose a PID from above:")
pid = input() 
print("\n Your report for " + pid + " is being generated")



# read adb for 1 minute
t_end = time.time() + 50

#gfx_thread = multiprocessing.Process(target=commands.gfxinfo, args=(t_end,pid,),)
#bat_thread = multiprocessing.Process(target=commands.battery, args=(t_end,pid),)
#top_thread = multiprocessing.Process(target=commands.top, args=(t_end,pid,),)
#mem_thread = multiprocessing.Process(target=commands.meminfo, args=(t_end,pid),)
# ---------------------------
gfx_thread = threading.Thread(target=commands.gfxinfo, args=(t_end,pid))
bat_thread = threading.Thread(target=commands.battery, args=(t_end,pid))
top_thread = threading.Thread(target=commands.top, args=(t_end,pid))
#mem_thread = threading.Thread(target=commands.meminfo, args=(t_end,pid))

gfx_thread.start()
bat_thread.start()
top_thread.start()
#mem_thread.start()

gfx_thread.join()
bat_thread.join()
top_thread.join()
#mem_thread.join()