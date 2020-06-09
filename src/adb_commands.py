# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:59:36 2020

@author: paula
"""
import os

import time
import datetime
import csv

import re

# This is for adb shell dumpsys gfxinfo. Records data for the metric "render time"
def gfxinfo(t_end, pid):
    print("\n collecting data for metric 'render time'...")
    lastRow = -1
    
    # read adb for 1 minute
    t_end = time.time() + 50
    
    with open('output_gfx.csv', mode='w') as output:
        csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Flags','IntendedVsync','Vsync','OldestInputEvent','NewestInputEvent','HandleInputStart','AnimationStart','PerformTraversalsStart','DrawStart','SyncQueued','SyncStart','IssueDrawCommandsStart','SwapBuffers','FrameCompleted','DequeueBufferDuration','QueueBufferDuration'])
        
        while time.time() < t_end:
            framestats = os.popen("adb shell dumpsys gfxinfo '" + pid + "' framestats").read().split('---PROFILEDATA---')[1].split('\n')
            for i in framestats[:-2]:
                framestats_split = i.split(',')
                if i != '' and framestats_split[0] != 'Flags' and int(framestats_split[1]) > lastRow:
                    csv_writer.writerow(framestats_split)
                    
            framestats_split = framestats[-2].split(',')
            if i != '' and framestats_split[0] != 'Flags' and int(framestats_split[1]) > lastRow:
                csv_writer.writerow(framestats_split)
            lastRow = int(framestats[-2].split(',')[1])
            #csv_writer.writerow([0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0,0])
     
            
# This is for adb shell dumpsys battery. Records data for the metric "battery usage"
def battery(t_end, pid):
    print("\n collecting data for metric 'battery usage'...")
    
    with open('output_battery.csv', mode='w') as output:
        csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Start','End', 'Difference'])
        
        battery_start = re.search('level: (.*)\n',os.popen("adb shell dumpsys battery | findstr level").read()).group(1)
        time.sleep(5*60)    
        battery_end = re.search('level: (.*)\n',os.popen("adb shell dumpsys battery | findstr level").read()).group(1)
        
        csv_writer.writerow([battery_start, battery_end, int(battery_start)-int(battery_end)])
  
    
# This is for adb shell top. Records data for the metrics "cpu usage" and
# and "memory usage"
def top(t_end, pid):
    print("\n collecting data for metric 'memory usage' and 'cpu usage'...")
    
    # read adb for 1 minute
    t_end = time.time() + 50
    with open('output_top.csv', mode='w') as output:
        csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['time', '%CPU-user', '%CPU-nice', '%CPU-sys', '%MEM'])
        
        topPID = os.popen('adb shell top | findstr "cpu Mem"').read().split(' ')
        topPID_clean = list(filter(None, topPID))
        csv_writer.writerow([time.time(), topPID_clean[10], topPID_clean[11], topPID_clean[12], topPID_clean[3]])
        while time.time() < t_end:
            time.sleep(1)
            topPID = os.popen('adb shell top | findstr "cpu Mem"').read().split(' ')
            topPID_clean = list(filter(None, topPID))
            csv_writer.writerow([time.time(), topPID_clean[10], topPID_clean[11], topPID_clean[12], topPID_clean[3]])


# This is for adb shell dumpsys meminfo. Could be used additionally for the
# metric "memory usage"
def meminfo(t_end, pid):
    print("pss: ")
    while time.time() < t_end:
        time.sleep(1)
        meminfo = os.popen("adb shell dumpsys meminfo " + pid).read()
        ms = int(meminfo.split('Realtime: ')[1].split('\n')[0])
        print(ms)
        time = datetime.datetime.fromtimestamp(ms)
        print(time.strftime("%Y-%m-%d %H:%M:%S") + " --- " + meminfo.split('TOTAL')[1].split(' ')[4])