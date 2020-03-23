from classes import *
import COVID19Py
import operator

covid19 = COVID19Py.COVID19()

USCases = covid19.getLocationByCountryCode("US")

cities = []
for city in USCases:
    name = city["province"]
    if "," in name:
        virusData = VirusData(city["latest"])
        climate = None
        demographics = None
        city = City(name, demographics, climate, virusData)
        cities.append(city)
