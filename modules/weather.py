#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

    Sample weather script using secret openweathermap.org API.

    Also serves as a simple unicode test.

    Based on pyfibot IRC bot http://code.google.com/p/pyfibot/source/browse/trunk/pyfibot/modules/module_openweather.py

"""
from __future__ import absolute_import, division, print_function

import sys
import json
import urllib
from datetime import datetime, timedelta

url = 'http://openweathermap.org/data/2.1/find/name?q=%s'

# XXX?
threshold = 30


def call_weather_api(location):
    """ Call API """

    request = urllib.urlopen(url % location)

    payload = json.loads(request.read())

    if 'cod' in payload and payload['cod'] == '200':
        if 'list' in payload:
            data = payload['list'][0]
            location = data['name']

            if 'dt' in data:
                measured = datetime.utcfromtimestamp(data['dt'])
                if datetime.utcnow() - timedelta(minutes=threshold) > measured:
                    text = '%s (%s UTC): ' % (location, measured.strftime('%Y-%m-%d %H:%M'))
                else:
                    text = '%s: ' % location
            else:
                text = '%s: ' % location

            main = data['main']
            if 'temp' in main:
                temperature = main['temp'] - 273.15  # temperature converted from kelvins to celcius and rounded
                text += 'Temperature: %.1fc' % temperature
            else:
                temperature = None
            if 'wind' in data and 'speed' in data['wind']:
                wind = data['wind']['speed']  # Wind speed in mps (m/s)
            else:
                wind = None
            if temperature and wind:
                feels_like = 13.12 + 0.6215 * temperature - 11.37 * (wind * 3.6) ** 0.16 + 0.3965 * temperature * (wind * 3.6) ** 0.16
                text += ', Feels like: %.1fc' % feels_like
            if wind:
                text += ', Wind: %.1f m/s' % wind
            if 'humidity' in main:
                humidity = main['humidity']  # Humidity in %
                text += ', Humidity: %d%%' % humidity
            if 'pressure' in main:
                pressure = main['pressure']  # Atmospheric pressure in hPa
                text += ', Pressure: %d hPa' % pressure
            if 'clouds' in data and 'all' in data['clouds']:
                cloudiness = data['clouds']['all']  # Cloudiness in %
                text += ', Cloudiness: %d%%' % cloudiness

            if temperature:
                print(text.encode('utf-8'))
            else:
                print('Error: No data.')
    else:
        print('Error: Location %s not found.' % location)


if len(sys.argv) < 2:
    sys.exit("You must give a city")

city = sys.argv[1]

call_weather_api(city)
