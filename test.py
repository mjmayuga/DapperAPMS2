import sqlite3
import time

# Connect to the SQLite3 database
conn = sqlite3.connect('arduinosensors.sqlite3')
cursor = conn.cursor()

# Simulate sensor data generation
ecg_data = [123.45]
temperature_data = [36.5]
respiratory_data = [18]

# Insert data into the database
for index in range(len(ecg_data)):
    time = time.time()
    ecg = ecg_data[index]
    temperature = temperature_data[index]
    respiratory = respiratory_data[index]

    cursor.execute('INSERT INTO arduino1 (time, ecg, temp, respiratory) VALUES (?, ?, ?, ?)', (time, ecg, temperature, respiratory))
    conn.commit()

# Close the connection to the database
conn.close()




