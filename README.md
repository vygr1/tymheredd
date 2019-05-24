# tymheredd
Recording temperature and logging forecast, in order to display on a four character LED display.

## display.py
Reads temps from a group of [DS18B20 Digital temperature sensors](https://core-electronics.com.au/waterproof-ds18b20-digital-temperature-sensor.html).

Reads temperature forecast data downloaded from bom.gov.au by *forecast.py*.

Outputs to an [Adafruit Quad Alphanumeric Display](https://www.adafruit.com/product/1911).

## forecast.py
Maintains a file with today and tomorrow's temperature data, downloaded from the Australian Bureau of Meteorology.

IDN10035.xml is the Canberra week ahead forecast product.

Output is a pickle package file, *forecast.pkl*, of an array of two dictionaries containing forecast min, max, and probability of rain.

## logTemp.py
[Temperature sensor](https://core-electronics.com.au/waterproof-ds18b20-digital-temperature-sensor.html) logging. Reads the temp <samples> times from each sensor waiting ~1 second between reads. Appends the average of the reads to a file.
