import pandas as pd
from latlon_utils import get_climate

us_state_abbrev = {
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
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

virusData = pd.read_csv("03-22-2020.csv")
states = virusData[virusData["Country/Region"]=="US"]

statePopulationData = pd.read_csv("state-population.csv")
statePopulationData = statePopulationData[statePopulationData["ages"] == "total"][statePopulationData["year"] == 2012]
statePopulationData = statePopulationData.drop(["ages", "year"], axis=1)
statePopulationData = pd.DataFrame({"Province/State": [abbrev_us_state[state] for state in statePopulationData["state/region"][:-1]], "Population": statePopulationData["population"][:-1]})

stateAreaData = pd.read_csv("state-areas.csv")
stateAreaData = stateAreaData.rename(columns={"state": "Province/State", "area (sq. mi)": "Area"})

data = states.merge(stateAreaData, on="Province/State").merge(statePopulationData, on="Province/State")

def getPopulationDensity(state):
    return float(state["Population"])/float(state["Area"])

def getTemp(state):
    return get_climate(state["Latitude"], state["Longitude"])["tavg", "mar"]

def getPrec(state):
    return get_climate(state["Latitude"], state["Longitude"])["prec", "mar"]

data["Population Density"] = data.apply(lambda state: getPopulationDensity(state), axis=1)
data["Average Temperature"] = data.apply(lambda state: getTemp(state), axis=1)
data["Average Precipitation"] = data.apply(lambda state: getPrec(state), axis=1)

data.to_csv(r"./data.csv", index=False)
