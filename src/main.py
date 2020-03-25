import pandas as pd
from math import isnan
from os import listdir
from os.path import isfile, join, abspath
from latlon_utils import get_climate

STATE_TO_ABBREV = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

STATE_TO_LOCATION = {
    'Alabama': (32.32, -86.9),
    'Alaska': (66.16, -153.37),
    'Arizona': (34.0, -111.09),
    'Arkansas': (34.8, -92.20),
    'California': (36.78, -119.41),
    'Colorado': (39.11, -105.36),
    'Connecticut': (41.59, -72.69),
    'Delaware': (39.0, -75.5),
    'District of Columbia': (38.91, -77.04),
    'Florida': (27.99, -81.76),
    'Georgia': (33.24, -83.44),
    'Hawaii': (19.74, -155.84),
    'Idaho': (44.07, -114.74),
    'Illinois': (40.0, -89.0),
    'Indiana': (40.27, -86.13),
    'Iowa': (42.03, -93.58),
    'Kansas': (38.5, -98.0),
    'Kentucky': (37.83, -84.27),
    'Louisiana': (30.39, -80.79),
    'Maine': (45.37, -68.97),
    'Maryland': (39.05, -76.64),
    'Massachusetts': (42.41, -71.38),
    'Michigan': (44.18, -84.51),
    'Minnesota': (46.39, -94.63),
    'Mississippi': (33.0, -90.0),
    'Missouri': (38.57, -92.60),
    'Montana': (46.96, -109.53),
    'Nebraska': (41.5, -100.0),
    'Nevada': (39.87, -117.22),
    'New Hampshire': (44.0, -71.5),
    'New Jersey': (39.83, -74.87),
    'New Mexico': (34.31, -106.02),
    'New York': (43.0, -75.0),
    'North Carolina': (35.78, -80.79),
    'North Dakota': (47.65, -100.43),
    'Ohio': (40.37, -82.99),
    'Oklahoma': (36.08, -96.92),
    'Oregon': (44.0, -120.5),
    'Pennsylvania': (41.20, -77.19),
    'Puerto Rico': (18.22, -66.59),
    'Rhode Island': (41.7, -71.5),
    'South Carolina': (33.83, -81.16),
    'South Dakota': (44.5, -100.0),
    'Tennessee': (35.86, -86.66),
    'Texas': (31.0, -100.0),
    'Utah': (39.42, -111.95),
    'Vermont': (44.0, -72.69),
    'Virginia': (37.93, -78.02),
    'Washington': (47.75, -120.74),
    'West Virginia': (39, 0, -80, 5),
    'Wisconsin': (44.5, -89.5),
    'Wyoming': (43.08, -107.29),
}

DATE_TO_MONTH = {
    "01": "jan",
    "02": "feb",
    "03": "mar",
    "04": "apr",
    "05": "may",
    "06": "jun",
    "07": "jul",
    "08": "aug",
    "09": "sep",
    "10": "oct",
    "11": "nov",
    "12": "dec"
}


# Converts state abbreviation to full name
def getState(abbrev):
    ABBREV_TO_STATE = dict(map(reversed, STATE_TO_ABBREV.items()))
    return ABBREV_TO_STATE[abbrev]


# Converts the state's full name to its abbreviation
def getAbbrev(state):
    return STATE_TO_ABBREV[state]


# Gets the state's latitude and longitude
def getLocation(state):
    return STATE_TO_LOCATION[state]


# Gets the month from the date
def getMonth(date):
    monthNum = date.split("-")[0]
    return DATE_TO_MONTH[monthNum]


# Combines all the stats for each city in a state
def combineStats(cities, state):
    confirmed = 0
    deaths = 0
    recovered = 0
    for city in cities:
        if not isnan(city["Confirmed"]):
            confirmed += city["Confirmed"]
        if not isnan(city["Deaths"]):
            deaths += city["Deaths"]
        if not isnan(city["Recovered"]):
            recovered = city["Recovered"]
    latitude, longitude = getLocation(state)
    population = statePopulations[state]
    area = stateAreas[state]
    density = stateDensities[state]
    avgTemp = getTemp(latitude, longitude)
    avgPrec = getPrec(latitude, longitude)
    return {
        "State": state,
        "Confirmed": confirmed,
        "Deaths": deaths,
        "Recovered": recovered,
        "Latitude": latitude,
        "Longitude": longitude,
        "Population": population,
        "Area": area,
        "Population Density": density,
        "Average Temperature": avgTemp,
        "Average Precipitation": avgPrec
    }


# Gets a dictionary of each state and its population
def getPopulationData():
    statePopulationData = pd.read_csv("state-population.csv")
    statePopulationData = statePopulationData[statePopulationData["ages"]
                                              == "total"][statePopulationData["year"] == 2012]
    statePopulations = {}
    for i, row in statePopulationData.iterrows():
        abbrev = row["state/region"]
        if abbrev != "USA":
            state = getState(abbrev)
            population = row["population"]
            statePopulations[state] = population
    return statePopulations


# Gets a dictionary of each state and its area (sq mi)
def getAreaData():
    stateAreaData = pd.read_csv("state-areas.csv")
    stateAreas = {}
    for i, row in stateAreaData.iterrows():
        state = row["state"]
        area = row["area (sq. mi)"]
        stateAreas[state] = area
    return stateAreas


# Gets a dictionary of each state and its population density
def getDensityData():
    stateDensities = {}
    for state in statePopulations.keys():
        stateDensities[state] = float(
            statePopulations[state]) / float(stateAreas[state])
    return stateDensities


# Gets the average temperature for the given location
def getTemp(latitude, longitude):
    date = file.split("/")[-1]
    month = getMonth(date)
    return get_climate(latitude, longitude)["tavg", month]


# Gets the average precipitation for the given location
def getPrec(latiude, longitude):
    date = file.split("/")[-1]
    month = getMonth(date)
    return get_climate(latiude, longitude)["prec", month]


# Creates new DataFrame from the new rows
def createNewDF(rows):
    df = pd.DataFrame(columns=[
        "State",
        "Confirmed",
        "Deaths",
        "Recovered",
        "Latitude",
        "Longitude",
        "Population",
        "Area",
        "Population Density",
        "Average Temperature",
        "Average Precipitation"
    ])
    for row in rows:
        df = df.append(row, ignore_index=True)
    return df


# Simplifies the data so the DataFrame only shows data for each state
def simplifyDF(df):
    states = {}
    for i, row in df.iterrows():
        cityState = []
        try:
            cityState = row["Province/State"].split(", ")
        except Exception:
            cityState = row["Province_State"].split(", ")
        if len(cityState) == 2:
            state = cityState[1].split(" ")[0]  # Makes sure its a state
            if state != "U.S.":
                state = getState(state)
                if state in states.keys():
                    states[state].append(row)
                else:
                    states[state] = [row]
    newRows = []
    for state in states.keys():
        newRows.append(combineStats(states[state], state))
    df = createNewDF(newRows)
    return df


# Modifies DataFrame to match needed table
def modifyDF(df):
    newRows = []
    for i, row in df.iterrows():
        state = ""
        try:
            state = row["Province/State"]
        except Exception:
            state = row["Province_State"]
        confirmed = row["Confirmed"]
        deaths = row["Deaths"]
        recovered = row["Recovered"]
        if isnan(confirmed):
            confirmed = 0
        if isnan(deaths):
            deaths = 0
        if isnan(recovered):
            recovered = 0
        latitude, longitude = getLocation(row)
        population = statePopulations[state]
        area = stateAreas[state]
        density = stateDensities[state]
        avgTemp = getTemp(latitude, longitude)
        avgPrec = getPrec(latitude, longitude)
        newRow = {
            "State": state,
            "Confirmed": confirmed,
            "Deaths": deaths,
            "Recovered": recovered,
            "Latitude": latitude,
            "Longitude": longitude,
            "Population": population,
            "Area": area,
            "Population Density": density,
            "Average Temperature": avgTemp,
            "Average Precipitation": avgPrec
        }
        newRows.append(newRow)
    df = createNewDF(newRows)
    return df


def getStateData(file):
    try:
        virusData = pd.read_csv(file)
        try:
            virusData = virusData[virusData["Country/Region"] == "US"]
        except Exception:
            virusData = virusData[virusData["Country_Region"] == "US"]
        simiply = False
        for i, row in virusData.iterrows():
            if len(row["Province/State"].split(",")) > 1:
                simiply = True
                break
        if simiply:
            return simplifyDF(virusData)
        else:
            return modifyDF(virusData)
    except Exception as e:
        print(e)
        return None


# Gets all the virus data files
def getFiles(path):
    files = [abspath("./virus_data/" + f)
             for f in listdir(path) if isfile(join(path, f))]
    return files


statePopulations = getPopulationData()
stateAreas = getAreaData()
stateDensities = getDensityData()

path = "/home/akshay/Documents/Projects/coronavirus/src/virus_data/"
files = getFiles(path)

for file in files:
    df = getStateData(file)
    if df is not None:
        newFile = "./generatedCSV/" + file[-14:]
        df.to_csv(newFile, index=False)
