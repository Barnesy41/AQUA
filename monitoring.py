# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification.
#
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations.
#
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
import requests
import datetime


def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 

    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + \
        datetime.timedelta(days=1) if end_date is None else end_date

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"

    url = endpoint.format(
        site_code=site_code,
        species_code=species_code,
        start_date=start_date,
        end_date=end_date
    )

    res = requests.get(url)
    return res.json()

# print(get_live_data_from_api())


# Accessing data examples
"""
a = get_live_data_from_api()
print(a)
print(a['RawAQData']['Data'][0]['@MeasurementDateGMT'])
print(a['RawAQData']['Data'][0]['@Value'])
"""


def outputPollutantGraph(site_code='MY1', species_code='NO', numberOfDays=1):
    start_date = datetime.date.today() - datetime.timedelta(numberOfDays - 1)  # Stores the date to search from
    # Stores the date to search to (adds 1 to the end to include the final day)
    end_date = datetime.date.today() + datetime.timedelta(1)

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"

    url = endpoint.format(
        site_code=site_code,
        species_code=species_code,
        start_date=start_date,
        end_date=end_date
    )

    dailyPollutantDict = requests.get(url).json()

    listOfValues = [] #Stores the list of values returned from the api call
    indexToAccess = 0

    # TODO the value is not used?
    #Append each value returned from the api call to a list
    for value in dailyPollutantDict['RawAQData']['Data']:
        print(dailyPollutantDict)
        try:
            listOfValues.append(
                float(dailyPollutantDict['RawAQData']['Data'][indexToAccess]['@Value']))
            indexToAccess += 1
        except:
            False

    maximumValue = int(max(listOfValues)) #Stores the largest value contained within the listOfValues

    outputArr = []
    #Counts down from the maximumValue to zero outputting a graph
    for i in range(maximumValue, -1, -1):
        line = ""

        # Unless this is the line with the bottom of the graph, create a line that starts with the graph number followed by the | char
        if (i != 0):
            line += " "*(len(str(maximumValue))-len(str(i))) + str(i) + "|"
            for value in listOfValues:
                if value == i:
                    line += str(value)
                else:
                    line += " "
                    
        else:  # Otherwise output the bottom line of the graph
            line += " "*(len(str(maximumValue))-len(str(i))) + "0" + "-"
            line += "-"*len(listOfValues)

        outputArr.append(line)

    # Append the day number at the bottom of the graph if type = 'day'
    

    # Output the array to terminal
    for line in outputArr:
        print(line)

def testFunc(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + \
        datetime.timedelta(days=1) if end_date is None else end_date

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName={GroupName}/Year={Year}/Json"

    url = endpoint.format(
        site_code=site_code,
        species_code=species_code,
        start_date=start_date,
        end_date=end_date
    )

    res = requests.get(url)
    
    print(res.json())
    return res.json()

#testFunc()

def showSpeciesInfo(SpeciesCode:str) -> dict:
    """Displays the information about a given pollutant species in the terminal and returns a dictionary of information about the species

    Parameters:
    SpeciesCode : str
    
    Returns:
        dict: A dictionary of pollutant species information
    """ 
    import requests

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/Species/SpeciesCode={SpeciesCode}/Json"

    url = endpoint.format(
        SpeciesCode=SpeciesCode,
    )

    res = requests.get(url)
    speciesInfoDict = res.json() #Stores the result in a dictionary
    
    import time 
    #Output the species information to the terminal
    print("       Species Name:", "\033[1m", speciesInfoDict['AirQualitySpecies']['Species']['@SpeciesName'], "\033[0m")
    time.sleep(2)
    print("       Species Code:", "\033[1m", speciesInfoDict['AirQualitySpecies']['Species']['@SpeciesCode'], "\033[0m")
    time.sleep(1.5)
    print("Species Description:", "\033[1m", speciesInfoDict['AirQualitySpecies']['Species']['@Description'], "\033[0m")
    time.sleep(4)
    print("      Health Effect:", "\033[1m", speciesInfoDict['AirQualitySpecies']['Species']['@HealthEffect'], "\033[0m")
    time.sleep(5)
    print("  Extra Information:", "\033[1m", speciesInfoDict['AirQualitySpecies']['Species']['@Link'], "\033[0m")
    time.sleep(2)
    
    return res.json()


def showAllSpeciesInfo() -> dict:
    """Displays the information about all common pollutant species in the terminal and returns a dictionary of information about the species
    
    Returns:
        dict: A dictionary of all common pollutant species information
    """ 
    whitelistOfPollutants = ['NO2', 'CO', 'O3', 'PM10', 'SO2', 'PM25'] #Stores a list of the whitelisted pollutants
    
    #output the information about all pollutants in the list of whitelisted pollutants
    for item in whitelistOfPollutants:
        showSpeciesInfo(item)
        print("") #Print a line break
    
def outputAllMonitoringStations():
    """Outputs the name and site code of all monitoring stations in London to the terminal. 
    
        Returns:
            list: a list of tuples with the name of the monitoring station in index 0 and the site code in index 1"""
    import requests

    url = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json"

    res = requests.get(url)
    speciesInfoDict = res.json() #Stores the result in a dictionary
    
    listOfMonitoringStations = [] #A list of tuples that all monitoring stations in london and their site code
    
    #Loop through each site contained within the returned dictionary of monitoring stations append their site name and site code to the listOfMonitoringStations
    #Output to the terminal the site code and site name
    for item in speciesInfoDict['Sites']['Site']:
        listOfMonitoringStations.append((item['@SiteName'], item['@SiteCode']))
        print(item['@SiteCode'] + " | " + item['@SiteName'])
        
    return listOfMonitoringStations
    
def rm_function_4(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here


# test
#outputAllMonitoringStations()
#outputPollutantGraph()
#showSpeciesInfo('NO2')
#showAllSpeciesInfo()
# end
