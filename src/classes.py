class Demographics(object):
    """docstring for demographics."""

    def __init__(self, population, area):
        super(Demographics, self).__init__()
        self.population = population
        self.area = area


class Climate(object):
    """docstring for Climate."""

    def __init__(self, avgTemp, avgRain):
        super(Climate, self).__init__()
        self.avgTemp = avgTemp
        self.avgRain = avgRain


class VirusData(object):
    """docstring for VirusData."""

    def __init__(self, data):
        super(VirusData, self).__init__()
        self.cases = data["confirmed"]
        self.deaths = data["deaths"]
        self.recovered = data["recovered"]
        self.activeCases = self.cases - (self.deaths + self.recovered)

    def addDeath(self, newDeaths=1):
        self.deaths += newDeaths
        self.activeCases -= newDeaths

    def addRecovery(self, newRecoveries=1):
        self.recovered += newRecoveries
        self.activeCases -= newRecoveries

    def addCase(self, newCases=1):
        self.cases += newCases
        self.activeCases += newCases


class City(object):
    """docstring for City."""

    def __init__(self, name, demographics, climate, virusData):
        super(City, self).__init__()
        self.name = name
        self.demographics = demographics
        self.climate = climate
        self.virusData = virusData

    def __lt__(self, otherCity):
        return self.virusData.cases < otherCity.virusData.cases

    def addDeath(self, newDeaths=1):
        self.virusData.addDeath(newDeaths=1)

    def addRecovery(self, newRecoveries=1):
        self.virusData.addRecovery(newRecoveries)

    def addCase(self, newCases=1):
        self.virusData.addCase(newCases)

    def display(self):
        print(self.name)
        print(self.virusData.cases)


class Country(object):
    """docstring for Country."""

    def __init__(self, name, demographics, virusData, cities):
        super(Country, self).__init__()
        self.name = name
        self.demographics = demographics
        self.virusData = virusData
        self.cities = cities

    def addDeath(self, newDeaths=1):
        self.virusData.addDeath(newDeaths=1)

    def addRecovery(self, newRecoveries=1):
        self.virusData.addRecovery(newRecoveries)

    def addCase(self, newCases=1):
        self.virusData.addCase(newCases)
