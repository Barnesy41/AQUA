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
import turtle
from turtle import *
import statistics
import math
import time
import os
import sys
import random


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
    #Append the species information to a list
    speciesInfoList = ["       Species Name: " + "\033[1m" + speciesInfoDict['AirQualitySpecies']['Species']['@SpeciesName'] + "\033[0m",
                       "       Species Code: " + "\033[1m" + speciesInfoDict['AirQualitySpecies']['Species']['@SpeciesCode'] + "\033[0m",
                       "Species Description: " + "\033[1m" + speciesInfoDict['AirQualitySpecies']['Species']['@Description'] + "\033[0m",
                       "      Health Effect: " + "\033[1m" + speciesInfoDict['AirQualitySpecies']['Species']['@HealthEffect'] + "\033[0m",
                       "  Extra Information: " + "\033[1m" + speciesInfoDict['AirQualitySpecies']['Species']['@Link'] + "\033[0m"]

    #Get the size of the python terminal
    import os
    terminalColumns, terminalLines = os.get_terminal_size()
    listToOutput = []
    for line in speciesInfoList:
        lineList = line.split(' ')
        while len(line) > terminalColumns:
            #Find the last " " character just before substr
            indexToSubstrFrom = terminalColumns
            for count in range(len(line[:terminalColumns]) - 1, -1, -1):
                if line[count] == ' ':
                    indexToSubstrFrom = count
                    break
                
            #Append the substr of the line to the list to output and remove from the current line variable    
            listToOutput.append(line[:indexToSubstrFrom])
            line = " "*20 + line[indexToSubstrFrom:]
        listToOutput.append(line)
        
    for item in listToOutput:
        print(item)
        time.sleep(1)
            
    
    
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
    
def outputAllMonitoringStations(outputToTerminal = True):
    """Outputs the name and site code of all monitoring stations in London to the terminal. 
    
        Parameters:
        outputToTerminal : bool, optional
            Output the name and site code of all monitoring stations in London to the terminal. Default value is True.
            
        Returns:
            list: a list of tuples with the name of the monitoring station in index 0 and the site code in index 1"""
    import requests
    import time
    
    url = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json"

    res = requests.get(url)
    speciesInfoDict = res.json() #Stores the result in a dictionary
    
    listOfMonitoringStations = [] #A list of tuples that all monitoring stations in london and their site code
    
    #Loop through each site contained within the returned dictionary of monitoring stations append their site name and site code to the listOfMonitoringStations
    for item in speciesInfoDict['Sites']['Site']:
        listOfMonitoringStations.append((item['@SiteName'], item['@SiteCode']))
        
    #If outputToTerminal == True output to the terminal the site code and site name
    if outputToTerminal == True:
        for item in listOfMonitoringStations:
            print(item[1] + " | " + item[0])
            time.sleep(0.25)
    
    return listOfMonitoringStations
    
def getAirQualityIndexData(AirQualityIndex):
    """Accepts a value 1-10, gets the air quality band, health advice for both at risk individuals and general population and returns the results as a dictionary"""
    import requests
    import time
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/IndexHealthAdvice/AirQualityIndex={AirQualityIndex}/Json"

    url = endpoint.format(
        AirQualityIndex=AirQualityIndex
    )

    try:
        res = requests.get(url)
        airQualityIndexDict = res.json() #Stores the result in a dictionary
    except: #Use 1 as the default value
        print("\nAn invalid air quality index was input therefore the index health advice is unknown. (values should be 1-10)\n")
        
        url = "https://api.erg.ic.ac.uk/AirQuality/Information/IndexHealthAdvice/AirQualityIndex=1/Json"
        res = requests.get(url)
        airQualityIndexDict = res.json() #Stores the result in a dictionary
        
        #Set the health advice to unknown as an invalid value was entered
        airQualityIndexDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['HealthAdvice'][0]['@Advice'] = 'Unknown'
        airQualityIndexDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['HealthAdvice'][1]['@Advice'] = 'Unknown'

    return airQualityIndexDict
    

def outputAirQualityIndexDataForSpecificSite(SiteCode: str) -> bool:
    """Outputs the air quality index information for a specific monitoring site along with health advice. Returns False if no information was found and returns True if information is found

    Args:
        SiteCode (str): The SiteCode for any monitoring station

    Returns:
        bool: Returns True if information is found and False if information is not found
    """    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Hourly/MonitoringIndex/SiteCode={SiteCode}/Json"
    
    url = endpoint.format(
        SiteCode=SiteCode
    )

    res = requests.get(url)
    returnedDict = res.json() #Stores the result in a dictionary
    
    if returnedDict == None:
        print("There is no data for the requested site.")
        return None
    
    #Retrieve required data from the dictionary
    SiteName = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['@SiteName']
    
    #Output the information
    def outputHealthAdvice(SpeciesName, SpeciesCode, AirQualityIndex, AirQualityBand):
        import time
        #Get health advice information
        healthAdviceDict = getAirQualityIndexData(AirQualityIndex)
        generalPopulationAdvice = healthAdviceDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['HealthAdvice'][0]['@Advice']
        atRiskPopulationAdvice = healthAdviceDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['HealthAdvice'][1]['@Advice']
        
        #Output data to the terminal
        print(SiteCode + "  | " + SiteName)
        time.sleep(1)
        print(SpeciesCode + " | " + SpeciesName)
        time.sleep(1)
        print("Air Quality Index:", AirQualityIndex)
        time.sleep(1)
        print("Air Quality Band:", AirQualityBand)
        time.sleep(1)
        print("\nGeneral Population Health Advice: ", generalPopulationAdvice)
        time.sleep(1.5)
        print("At Risk Population Health Advice: ", atRiskPopulationAdvice)
        print("")
        time.sleep(1.5)
    
    try: #If there is only one type of pollutant at the site do this
        SpeciesName = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@SpeciesName']
        SpeciesCode = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@SpeciesCode']
        AirQualityIndex = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@AirQualityIndex']
        AirQualityBand = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@AirQualityBand']
        outputHealthAdvice(SpeciesName, SpeciesCode, AirQualityIndex, AirQualityBand)
    except: #Otherwise do this
        for index in range(0, len(returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'])):
            SpeciesName = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@SpeciesName']
            SpeciesCode = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@SpeciesCode']
            AirQualityIndex = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@AirQualityIndex']
            AirQualityBand = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@AirQualityBand']
            outputHealthAdvice(SpeciesName, SpeciesCode, AirQualityIndex, AirQualityBand)
    
    return True #Return True because data was found
    


def validateDate(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    
def validateTime(time):
    try:
        datetime.datetime.strptime(time, '%H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect data format, should be HH:MM:SS")

def inputSiteCode():
    """gets input from the user until a valid monitoring station is entered or the user requests to quit the menu
       returns the user's input if the monitoring station entered is valid, returns 'Q' if the user requests to quit"""
    while True:
        userInput = input(
            "Enter a site code. If you would like to exit, input 'Q'").upper()

        #If the user requests to quit return "Q"
        if userInput == "Q":
            return "Q"
                
        # Check that the site code input by the user is valid
        listOfMonitoringStations = outputAllMonitoringStations(False) # Returns a list of all monitoring stations and their site codes
        for item in listOfMonitoringStations:
            if item[1] == userInput:
                return userInput
            
        print("Invalid input.")
        
def drawPollutantPieChart():
    '''Outputs a pie chart using the turtle module. Displays the average percentage of each pollutant at a specific monitoring station
       in different average formats (mean,median,mode) then also sums up the values and creates a chart.
       Returns True if the pie chart has been drawn, False otherwise.
       
       Inputs:
       1. The site code of the monitoring station
       2. The date to start the pollutant data set from
       3. The date to end the pollutant data set at
       
       Outputs:
       1. A pie chart showing the average percentage of each pollutant at a specific monitoring station
       
       Returns:
       1. True if the pie chart has been drawn, False otherwise
    '''
       
    import datetime
    from datetime import datetime
    
    #Get the pollutant data from a specific monitoring station
    siteCode = inputSiteCode()
    
    if siteCode != 'Q':
        #Enter the start and end date of the data set to retrieve from the API
        startDate = input("enter the date you would like to receive data from (YYYY-MM-DD): ")
        validateDate(startDate) #Validates that the date is in the correct format
        endDate = input("enter the final date you would like to receive data to (YYYY-MM-DD): ")
        validateDate(endDate) #Validates that the date is in the correct format
        
        #Validate the start and end date
        while startDate >= endDate:
            print("The start date must be before the end date.")
            
            #Enter the start and end date of the data set to retrieve from the API
            startDate = input("enter the date you would like to receive data from (YYYY-MM-DD): ")
            validateDate(startDate) #Validates that the date is in the correct format
            endDate = input("enter the final date you would like to receive data to (YYYY-MM-DD): ")
            validateDate(endDate) #Validates that the date is in the correct format
        
        #Get the string for todays date
        import datetime
        dateToday = datetime.date.today()
        dateToday = dateToday.strftime('%Y-%m-%d') #Format datetime object to string
            
        #Validate the date and time
        while startDate >= dateToday or endDate > dateToday:
            print("The start date must be before today's date, and the end date must be before or equal to today's date.")
            
            #Enter the start and end date of the data set to retrieve from the API
            startDate = input("enter the date you would like to receive data from (YYYY-MM-DD): ")
            validateDate(startDate) #Validates that the date is in the correct format
            endDate = input("enter the final date you would like to receive data to (YYYY-MM-DD): ")
            validateDate(endDate) #Validates that the date is in the correct format
        
        #Get the pollutant data for the monitoring station
        import requests
        endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/Site/SiteCode={SiteCode}/StartDate={StartDate}/EndDate={EndDate}/Json"


        url = endpoint.format(
            SiteCode=siteCode,
            StartDate=startDate,
            EndDate=endDate
        )

        result = requests.get(url)
        pollutantDict = result.json()
        
        #Add each pollutant type to a dictionary of its pollutant type as a key and then a list of its values
        pollutantValuesDict = dict()
        for item in pollutantDict['AirQualityData']['Data']:
            #Only add data to the data set if data exists for that specific date and time
            if item['@Value'] != '':
                pollutantType = item['@SpeciesCode']
                
                #If the pollutant key does not already exist, create the key
                #and append the pollutant value to a list within that dictionary key 
                # otherwise append to the list within the dictionary
                if pollutantType not in pollutantValuesDict.keys():
                    pollutantValuesDict[pollutantType] = [float(item['@Value'])]
                else:
                    pollutantValuesDict[pollutantType].append(float(item['@Value']))

        #If there is no valid data for that specific date, return False
        if len(pollutantValuesDict) == 0:
            print("No pollutant data found.")
            return False
        
        
        #Create dictionaries for the different average types:
        meanValueDict = dict()
        medianValueDict = dict()
        modeValueDict = dict()
        sumValueDict = dict()
        
        import math
        import statistics
        #Calculate the value to add to each dictionary and add as a key value pair where key = pollutant name
        for key in pollutantValuesDict.keys():
            meanValueDict[key] = statistics.mean(pollutantValuesDict[key]) #Calculate the mean average
            medianValueDict[key] = statistics.median(pollutantValuesDict[key]) #Calculate the median
            modeValueDict[key] = statistics.mode(pollutantValuesDict[key]) #Calculate the mode
            sumValueDict[key] = sum(pollutantValuesDict[key]) #Calculate the sum of the values

        
        #Instantiate the turtle object
        pieChartTurtle = turtle.Turtle()
        pieChartTurtle.hideturtle()

        #Set the radius of the pie chart
        pieChartRadius = 200

        #Define the colors for the pie chart
        colors = ['red', 'green', 'blue', 'yellow','magenta'] #Black is kept for use with labels
        
        #Define the labels for the pie chart
        listOfChartTypesToDraw = ['mean','median','mode','sum']
        
        #Tell the user they need to open another window
        print("Open the python turtle window")
            
        #For each chart type to draw
        for chartType in listOfChartTypesToDraw:
            #Set the screensize
            Screen().setup(800,800)
            
            #Give the chart a title
            pieChartTurtle.pencolor('black')
            pieChartTurtle.hideturtle()
            pieChartTurtle.penup()
            pieChartTurtle.goto(0,300)
            pieChartTurtle.pendown()
            pieChartTurtle.write("This Pie Chart shows the average percentage of each pollutant detected at a specific monitoring station", align='center', font=("Arial",12,'normal'))
            
            #Label the pie chart
            pieChartTurtle.pencolor('black')
            pieChartTurtle.penup()
            pieChartTurtle.goto(0,-pieChartRadius - 30)
            pieChartTurtle.pendown()
            pieChartTurtle.write(chartType.upper(), align='center', font=("Arial",10,'normal'))
            
            #Go to the location the circle should start from
            pieChartTurtle.penup()
            pieChartTurtle.goto(0,0)
            pieChartTurtle.pendown()
            
            #a list of tuples in the format: (percentage, key, value)
            percentagesOfCircleToDrawList = []
            
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw is the mean 
            # pollutant pie chart
            if chartType == 'mean':
                #Get the sum of all of the mean values
                sumOfAllMeanValues = 0
                for value in meanValueDict.values():
                    sumOfAllMeanValues += value
                
                #Append values to the list of percentage values
                for key in meanValueDict:
                    value = meanValueDict[key]
                    percentage = (360/sumOfAllMeanValues) * value
                    percentagesOfCircleToDrawList.append((percentage,key,value))
                    
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw is the
            # median pollutant pie chart   
            if chartType == 'median':
                #Get the sum of all of the mean values
                sumOfAllMedianValues = 0
                for value in medianValueDict.values():
                    sumOfAllMedianValues += value
                
                #Append values to the list of percentage values
                for key in medianValueDict:
                    value = medianValueDict[key]
                    percentage = (360/sumOfAllMedianValues) * value
                    percentagesOfCircleToDrawList.append((percentage,key,value))
                    
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw is the
            #mode pollutant pie chart   
            if chartType == 'mode':
                #Get the sum of all of the mean values
                sumOfAllModeValues = 0
                for value in modeValueDict.values():
                    sumOfAllModeValues += value
                
                #Append values to the list of percentage values
                for key in modeValueDict:
                    value = modeValueDict[key]
                    percentage = (360/sumOfAllModeValues) * value
                    percentagesOfCircleToDrawList.append((percentage,key,value))
                    
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw is the
            # median pollutant pie chart   
            if chartType == 'sum':
                #Get the sum of all of the mean values
                sumOfAllSumValues = 0
                for value in sumValueDict.values():
                    sumOfAllSumValues += value
                
                #Append values to the list of percentage values
                for key in sumValueDict:
                    value = sumValueDict[key]
                    percentage = (360/sumOfAllSumValues) * value
                    percentagesOfCircleToDrawList.append((percentage,key,value))
                    
            #Draw the pie chart
            currentPenColour = 'cyan'
            for item in percentagesOfCircleToDrawList:
                
                #Change the colour of the pen
                newPenColour = currentPenColour
                while newPenColour == currentPenColour:
                    
                    #Select a random colour from the list of colours
                    if item != percentagesOfCircleToDrawList[0]:
                        newPenColour = colors[random.randint(0,len(colors) - 1)] #Select a random colour from the list of available colours
                    
                    #Always select the same first pen colour so that there is no clash between colours in the chart
                    else:
                        break
                currentPenColour = newPenColour
                pieChartTurtle.fillcolor(currentPenColour)
                pieChartTurtle.pencolor(currentPenColour)
                
                
                #Draw the sector then fill with the corresponding colour
                pieChartTurtle.begin_fill()
                pieChartTurtle.right(90)
                pieChartTurtle.forward(pieChartRadius)
                pieChartTurtle.left(90)
                pieChartTurtle.circle(pieChartRadius, item[0]) #Draw the % of the pie chart that represents that pollutant
                pieChartTurtle.left(90)
                pieChartTurtle.forward(pieChartRadius)
                pieChartTurtle.right(90)
                pieChartTurtle.end_fill()
                
                #Get the coordinates of the turtle
                turtleX = pieChartTurtle.xcor()
                turtleY = pieChartTurtle.ycor()
                
                #Write the pollutant type in the centre of the sector
                pieChartTurtle.penup()
                pieChartTurtle.right(90)
                pieChartTurtle.right(item[0]/2)
                pieChartTurtle.forward(pieChartRadius/2)
                pieChartTurtle.pendown()
                pieChartTurtle.pencolor('black')
                pieChartTurtle.write(item[1] + "\n" + str("{:.1f}".format(item[0])) + "%", align='center', font=("Arial",10,'bold')) #Write the pollutant name in the sector
                pieChartTurtle.pencolor(currentPenColour)
                pieChartTurtle.penup()
                pieChartTurtle.setposition(turtleX,turtleY)
                pieChartTurtle.left(item[0]/2)
                pieChartTurtle.left(90)
                pieChartTurtle.pendown()
            
            #Wait so that the finished pie chart can be read
            time.sleep(3)
            
            #Clear the canvas ready for the next chart
            pieChartTurtle.clear()

        turtle.bye()
        return True
    else:
        print("Quitting...")
    return False
    
    
    
#get_live_data_from_api('CTA','NO','2020-12-01')
#drawPollutantPieChart()
#outputAirQualityIndexDataForSpecificSite('CT4')
#print(getAirQualityIndexData(1.1))
#outputAllMonitoringStations()
#outputPollutantGraph()
#showSpeciesInfo('NO2')
#showAllSpeciesInfo()
# end