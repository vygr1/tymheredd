#!/usr/bin/python3
#
# Reads the temp <samples> times from each sensor waiting ~1 second between reads
# Appends the average of the reads to a file
#
# 20180605

import time
import datetime
import math

samples = 10

# Path to 1-wire temperature sensors
inside = "/sys/bus/w1/devices/28-05176050b1ff/w1_slave"
outside = "/sys/bus/w1/devices/28-03176088c7ff/w1_slave"
roof = "/sys/bus/w1/devices/28-0517603ae4ff/w1_slave"

filename = "/home/pi/code/productionCode/" + datetime.date.today().strftime('%Y%m') + "-temperature.csv"

# Function to read a value from a temperature sensor
def getTemp(location):
    try:
        tempStore = open(location)
        data = tempStore.read()
        tempStore.close()
        tempData = data.split("\n")[1].split(" ")[9]
        return float(tempData[2:])/1000
    except:
        return (float(0.0))

# Create the file and add headers if the file doesn't exist
try:
    file = open(filename, "r")
    file.close()
except IOError:
    file = open(filename, "w")
    file.write("timestamp,inside,outside,roof\r\n")
    file.close()


try:
    insideArray = []
    outsideArray = []
    roofArray = []

    # Collect n samples from each temperature sensor
    for _ in range (samples):
        insideArray.append(getTemp(inside))
        outsideArray.append(getTemp(outside))
        roofArray.append(getTemp(roof))
        time.sleep(1)

    # Average the samples
    insideAvg = "%.1f" % (math.fsum(insideArray)/len(insideArray))
    outsideAvg = "%.1f" % (math.fsum(outsideArray)/len(outsideArray))
    roofAvg = "%.1f" % (math.fsum(roofArray)/len(roofArray))

    # Append the timestamp and averages to a file
    file = open(filename, "a")
    file.write(str(datetime.datetime.now()) + "," + insideAvg + "," + outsideAvg + "," + roofAvg + "\r\n")
    file.close()

except Exception as e:
    print("Error happens: " + str(e))
