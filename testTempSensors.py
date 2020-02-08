#!/usr/bin/python3
#
# Reads the temp from each sensor
#
# 20200208

# Path to 1-wire temperature sensors
inside = "/sys/bus/w1/devices/28-05176050b1ff/w1_slave"
outside = "/sys/bus/w1/devices/28-03176088c7ff/w1_slave"
roof = "/sys/bus/w1/devices/28-0517603ae4ff/w1_slave"

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

print("Inside temp: " + str(getTemp(inside)))
