#!/usr/bin/python3
#
# Used to create an offset for each temp sensor.
# Senors should be co-located for this to be meaningful...
# Logs readings to three decimal places and stores for analysis.
#
# 20200209

import datetime

# Path to 1-wire temperature sensors
inside = "/sys/bus/w1/devices/28-05176050b1ff/w1_slave"
outside = "/sys/bus/w1/devices/28-03176088c7ff/w1_slave"
roof = "/sys/bus/w1/devices/28-0517603ae4ff/w1_slave"

filename = "calibrateTempSensors.csv"

# Function to read a value from a temperature sensor
def getTemp(location):
    try:
        tempStore = open(location)
        data = tempStore.read()
        tempStore.close()
        tempData = data.split("\n")[1].split(" ")[9]
        return str(float(tempData[2:])/1000)
    except:
        return "Err"

# Create the file and add headers if the file doesn't exist
try:
    file = open(filename, "r")
    file.close()
except IOError:
    file = open(filename, "w")
    file.write("timestamp,inside,outside,roof\r\n")
    file.close()

try:
    file = open(filename, "a")
    file.write(str(datetime.datetime.now()) + "," + getTemp(inside) + "," + getTemp(outside) + "," + getTemp(roof) + "\r\n")
    file.close()

except Exception as e:
    print("Error happens: " + str(e))
