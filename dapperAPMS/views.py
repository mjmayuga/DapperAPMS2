from django.http import HttpResponse
from django.shortcuts import render
import serial
import threading
import time
import sqlite3

conn = sqlite3.connect('arduinosensors.sqlite3')
cursor = conn.cursor()

cursor.execute('SELECT * FROM mytable')
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()

def indexpage(request,*args, **kwargs):
    return render(request,"login.html")

def AllPatientspage(request,*args, **kwargs):
    return render(request,"AllPatients.html")

def Collaboratorspage(request,*args, **kwargs):
    return render(request,"Collaborators.html")

def loginpage(request,*args, **kwargs):
    return render(request,"login.html")

def Dashboardpage(request,*args, **kwargs):
    return render(request,"Dashboard.html")

def OnGoingpage(request, *args, **kwargs):
    # Connect to the SQLite3 database
    conn = sqlite3.connect('arduinosensors.sqlite3')
    cursor = conn.cursor()

    # Retrieve sensor data from the database
    sensor_data = cursor.execute('SELECT * FROM arduino1').fetchall()

    # Process sensor data for the timestamps
    timestamps = []
    for row in sensor_data:
        timestamp = row[0]
        timestamps.append(timestamp)

    # Process sensor data for ecgs
    ecgs = []
    for row in sensor_data:
        ecg = row[1]
        ecgs.append(ecg)

    # Process sensor data for temperatures
    temperatures = []
    for row in sensor_data:
        temperature = row[2]
        temperatures.append(temperature)

    # Process sensor data for respiratory rates
    respiratories = []
    for row in sensor_data:
        respiratory = row[3]
        respiratories.append(respiratory)

    # Close the database connection
    conn.close()

    # Pass data to the template
    context = {
        'timestamps': timestamps,
        'ecgs': ecgs,
        'temperatures': temperatures,
        'respiratories': respiratories
    }

    return render(request, 'OnGoing.html', context)

def SettingAlarmpage(request,*args, **kwargs):
    return render(request,"SettingAlarm.html")

def Settingspage(request,*args, **kwargs):
    return render(request,"Settings.html")




