#!/usr/bin/python
#
# Maintains a file with today and tomorrow's temperature data, downloaded from BOM
# IDN10035.xml is the Canberra week ahead forecast product.
# Output is a pickle package file (forecast.pkl) of an array of two dictionaries containing forecast min, max, and probability of rain
#
# 20180618

import ftplib, datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

filename = "forecast.pkl"
today = {'date': datetime.datetime.strptime("2000-01-01T00:00:00", '%Y-%m-%dT%H:%M:%S'), 'minTemp': "--", 'maxTemp': "--", 'probPrecip': "--"}
tomorrow = {'date': datetime.datetime.strptime("2000-01-01T00:00:00", '%Y-%m-%dT%H:%M:%S'), 'minTemp': "--", 'maxTemp': "--", 'probPrecip': "--"}

# Function to download and parse the latest forecast from BOM
#  Updates global today and tomorrow dictionaries with the forecast data
def downloadForecast():
    global today
    global tomorrow

    try:
        ftp = ftplib.FTP('ftp.bom.gov.au','anonymous','emailAddress')
        ftp.cwd("/anon/gen/fwo")
        gFile = open("IDN10035.xml", "wb")
        ftp.retrbinary('RETR IDN10035.xml', gFile.write)
        gFile.close()
        ftp.quit()
    except Exception as e:
        print("Error happens: we couldn't access ftp.bom.gov.au\n" + str(e))
        return False

    tree = ET.parse("IDN10035.xml")

    date0 = datetime.datetime.strptime("2000-01-01T00:00:00", '%Y-%m-%dT%H:%M:%S')
    minTemp0 = "--"
    maxTemp0 = "--"
    probPrecip0 = "--"
    date1 = datetime.datetime.strptime("2000-01-01T00:00:00", '%Y-%m-%dT%H:%M:%S')
    minTemp1 = "--"
    maxTemp1 = "--"
    probPrecip1 = "--"

    #Extract data for today
    for elem in tree.findall('forecast/area[@aac="NSW_PT027"]/forecast-period[@index="0"]'):
        date0 = datetime.datetime.strptime(elem.attrib['start-time-local'], '%Y-%m-%dT%H:%M:%S+10:00')
        for child in elem:
            if (str(child.attrib['type']) == "air_temperature_minimum"):
                minTemp0 = child.text
            if (str(child.attrib['type']) == "air_temperature_maximum"):
                maxTemp0 = child.text
            if (str(child.attrib['type']) == "probability_of_precipitation"):
                probPrecip0 = child.text

    #Extract data for tomorrow
    for elem in tree.findall('forecast/area[@aac="NSW_PT027"]/forecast-period[@index="1"]'):
        date1 = datetime.datetime.strptime(elem.attrib['start-time-local'], '%Y-%m-%dT%H:%M:%S+10:00')
        for child in elem:
            if (str(child.attrib['type']) == "air_temperature_minimum"):
                minTemp1 = child.text
            if (str(child.attrib['type']) == "air_temperature_maximum"):
                maxTemp1 = child.text
            if (str(child.attrib['type']) == "probability_of_precipitation"):
                probPrecip1 = child.text

    today = {'date': date0, 'minTemp': minTemp0, 'maxTemp': maxTemp0, 'probPrecip': probPrecip0}
    tomorrow = {'date': date1, 'minTemp': minTemp1, 'maxTemp': maxTemp1, 'probPrecip': probPrecip1}

print(str(datetime.datetime.now()) + ": Starting...")

try:
    input = open(filename, 'rb')
    data = pickle.load(input)
    input.close()

    # Check the pickle file to see if tomorrow's data is already in it
    if data[1]['date'].date() == (datetime.date.today() + datetime.timedelta(days=1)):
        # If it is, we don't need to do anything.
        print("Data is already in the file, not adding")
    else:
        print("Data is currently:")
        print(data)
        print("Data is not most current, downloading forecast file...")
        # If it isn't, update the file
        downloadForecast()

        print("Adding tomorrow's forecast to data")
        #Append the new forecast and delete the old
        data.append(tomorrow)
        data.pop(0)

        #update today with the latest data, if it was in the latest XML file
        if (today['minTemp'] != "--"):
            data[0]['minTemp'] = today['minTemp']
        if (today['maxTemp'] != "--"):
            data[0]['maxTemp'] = today['maxTemp']
        if (today['probPrecip'] != "--"):
            data[0]['probPrecip'] = today['probPrecip']

        print("Data is updated... now is:")
        print(data)

        #write the data back to file
        output = open(filename, 'wb')
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
        output.close()



# If we got an IOError, it is probably because the file doeesn't exist (first file access is read)
except IOError:
    print("Error happens: file doesn't exist. Creating with what's available from BOM")
    downloadForecast()

    data = [today,tomorrow]
    print(data)

    output = open(filename, 'wb')
    pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
    output.close()
except Exception as e:
    print("Error happens, we couldn't open/save the datas: " + str(e))
