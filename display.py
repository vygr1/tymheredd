import time
import re
import datetime
from Adafruit_LED_Backpack import AlphaNum4
try:
    import cPickle as pickle
except ImportError:
    import pickle

display = AlphaNum4.AlphaNum4()
delay = 2

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
        temperature = float(tempData[2:])/1000
        return (True, "%.1f" % temperature)
    except:
        return (False, ""%.1f" % 0.0")

def getForecast():
    global forecastData
    try:
        input = open(filename, 'rb')
        forecastData = pickle.load(input)
        input.close()
        return True
    except Exception as e:
        print("Failed to open forecast file:\r\n" + str(e))
        return False

# Initialize the display. Must be called once before using the display.
display.begin()

try:
    while True:

        #display the current time
        display.clear()
        display.print_str("TIME")
        display.write_display()
        time.sleep(delay)
        theTime=('{:%H:%M}'.format(datetime.datetime.now().time()))
        decimalpos=theTime.find(':')
        theTime=re.sub('[:]','',theTime)
        display.print_str(theTime)
        display.set_decimal(decimalpos-1,True)
        display.write_display()
        time.sleep(delay)

        #display the forecast
        if getForecast()
            #display minimum forecast temp
            if (forecastData[0]['minTemp'] == "--"):
                print("No minTemp in forecast file")
            else:
                display.clear()
                display.print_number_str(forecastData[0]['minTemp'])
                display.set_digit(0,"m")
                display.write_display()
                time.sleep(delay)

            #display maximum forecast temp
            if (forecastData[0]['maxTemp'] == "--"):
                print("No maxTemp in forecast file")
            else:
                display.clear()
                display.print_number_str(forecastData[0]['maxTemp'])
                display.set_digit(0,"M")
                display.write_display()
                time.sleep(delay)

            #display probability of precipitation
            if (forecastData[0]['probPrecip'] == "--"):
                print("No probPrecip in forecast file")
            else:
                display.clear()
                display.print_number_str(forecastData[0]['probPrecip'])
                display.set_digit(0,"%")
                display.write_display()
                time.sleep(delay)

        #display inside temp
        (success,value) = getTemp(inside);
        if (success):
            display.clear()
            display.print_str(value)
            display.set_digit(0,"i")
            display.write_display()
            time.sleep(delay)

        #display outside temp
        (success,value) = getTemp(outside);
        if (success):
            display.clear()
            display.print_str(value)
            display.set_digit(0,"o")
            display.write_display()
            time.sleep(delay)

        #display roof temp
        (success,value) = getTemp(roof);
        if (success):
            display.clear()
            display.print_str(value)
            display.set_digit(0,"r")
            display.write_display()
            time.sleep(delay)

except KeyboardInterrupt:
    GPIO.cleanup()
    display.clear()
    display.write_display()
    print("Program Exited Cleanly")

except Exception as e:
    print("Error happens:\r\n" + str(e))
