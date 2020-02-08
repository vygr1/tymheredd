#!/usr/bin/python3
#
# Prints data stored in forecast.py's pickle file.
#
# 20180618

import datetime
try:
    import cPickle as pickle
except ImportError:
    import pickle

filename = "forecast.pkl"

def printData(data):
    print(data['date'].strftime('%d %b %Y') + ":")
    print("\tMinimum: " + data['minTemp'])
    print("\tMaximum: " + data['maxTemp'])
    print("\tChance of rain: " + data['probPrecip'])

print("Today: " + str(datetime.date.today().strftime('%d %b %Y')))

try:
    input = open(filename, 'rb')
    data = pickle.load(input)
    input.close()

    printData(data[0])
    printData(data[1])

except IOError as e:
    print("IOError happens: " + str(e))
except Exception as e:
    print("Error happens: " + str(e))
