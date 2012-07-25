#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

    Sample weather script using secret Google Weather API.

    See: http://blog.programmableweb.com/2010/02/08/googles-secret-weather-api/

    Also serves as a simple unicode test.

"""

import sys
import urllib
from xml.etree import ElementTree

if len(sys.argv) < 2:
    sys.exit("You must give a city")

city = sys.argv[1]

url = "http://www.google.com/ig/api?weather=" + urllib.quote(city)

request = urllib.urlopen(url)

tree = ElementTree.ElementTree()
root = tree.parse(request)

#print ElementTree.tostring(root)

template = u"""
City: %s
Weather: %s
Temperature: %s °C
"""

place = root.find("weather/forecast_information/city").get("data")
weather = root.find("weather/current_conditions/condition").get("data")
temp = root.find("weather/current_conditions/temp_c").get("data")


output = template % (place, weather, temp)

print output.encode("utf-8")
