# This module accesses data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations.
#
# The API documentation can be accessed here http://api.erg.ic.ac.uk/AirQuality/help
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

def outputPollutantGraph(site_code='MY1', numberOfDays=2):
    """Outputs a text-based graph to the terminal. 
    It takes in a monitoring station site code, collects all pollutant data for the given number of days prior to today and calculates
    the mean average of all the values for each pollutant type at that monitoring station. 
    It then outputs a bar graph scaled to the size of the terminal comparing the average levels of each pollutant at the monitoring station.

    Raises:
        Exception: terminal size is too small
        
    Outputs:
        a text-based graph
        
    Returns:
        True if the function outputs a graph and False otherwise
    """    
    #Check that the number of days input is greater than zero
    if numberOfDays <= 0:
        print("Number of days must be greater than zero.\nFunction Failed!")
        return False
    
    start_date = datetime.date.today() - datetime.timedelta(numberOfDays - 1)  # Stores the date to search from
    
    # Stores the date to search to (adds 1 to the end to include the final day)
    end_date = datetime.date.today() + datetime.timedelta(1)

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/Site/SiteCode={SiteCode}/StartDate={StartDate}/EndDate={EndDate}/Json"

    url = endpoint.format(
        SiteCode=site_code,
        StartDate=start_date,
        EndDate=end_date
    )
    
    #TODO error caused when non-int input

    #Requests data from the API and converts to dictionary format
    pollutantDict = requests.get(url).json()

    #Append each value returned from the api call to a list
    dictOfValues = {} #Stores the pollutant code as a key and each key contains a list of values returned from the api call for that particular pollutant
    for dict in pollutantDict['AirQualityData']['Data']:
        pollutantCode = dict['@SpeciesCode']
        
        #Append value to dictionary if it is not empty if the value is a valid numerical value
        #With dictionary key = pollutantCode
        if(pollutantCode in dictOfValues.keys()):
            try:
                dictOfValues[pollutantCode].append(
                    float(dict['@Value']))
            except:
                False
        else:
            try:
                dictOfValues[pollutantCode] = [float(dict['@Value'])]
            except:
                False
    
    #Check that there are valid values returned from the api call
    if len(dictOfValues.values()) <= 0:
        print("there are no valid values returned from the api call.\nFunction Failed!")
        return False
    
    #Find the mean average of the list of values for each pollutant type
    #Swap the list of values for a single mean value in the dictionary
    for key in dictOfValues.keys():
        dictOfValues[key] = statistics.mean(dictOfValues[key])
        
    #Finds the maximum mean pollutant value in the current data set
    maximumValue = max(dictOfValues.values())
    
    #Get the size of the terminal
    terminalColumns, terminalLines = os.get_terminal_size()
    
    #Scale down the pollutant values if the terminal is too small
    scale = 1
    if terminalLines - 6 < maximumValue:
        scale = (terminalLines - 6)/maximumValue #Calculate the scale factor
        
        #Scale each value in each list of the dictionary down by the correct scale factor
        #Convert to an integer value
        for pollutantCode in dictOfValues.keys():
            dictOfValues[pollutantCode] = int(dictOfValues[pollutantCode]*scale)
            
    #Create an exception if terminal does not have a great enough line length
    if terminalLines - 6 <= 0:
        raise Exception("Terminal size is too small. Make the terminal size larger then try again.")
    
    #TODO implement case where the terminal width is too small

    #Counts down from the maximumValue to zero outputting a graph
    outputArr = []
    print("Scale Factor: " + str("{:.2f}".format(scale)))
    for i in range(int(maximumValue*scale), -1, -1):
        line = ""

        # Unless this is the line with the bottom of the graph, create a line that starts with the graph number followed by the | char
        if (i != 0):
            line += " "*(len(str(int(maximumValue*scale)))-len(str(i))) + str(i) + "|"
            #TODO HERE
            for key in dictOfValues.keys():
                if dictOfValues[key] >= i:
                    line += "\033[1;32m□   \u001b[0m"
                else:
                    line += "    "
            
                    
        else:  # Otherwise output the bottom line of the graph
            line += " "*(len(str(int(maximumValue*scale)))-len(str(i))) + "0" + "+"
            line += "-"*((len(dictOfValues)*4)-3)

        outputArr.append(line)

    # Append the day number at the bottom of the graph if type = 'day'
    

    # Output the array to terminal
    for line in outputArr:
        print(line)

    #Calculate the lines to be output as x-axis labels
    listOfLinesToOutput = []
    for index in range(0,len(max(dictOfValues.keys()))):
        lineToAppend = " "*(len(str(int(maximumValue*scale))) + 1)
        for pollutant in dictOfValues.keys():
            try:
                lineToAppend += pollutant[index] + "   "
            except:
                lineToAppend += "    "
        listOfLinesToOutput.append(lineToAppend)
        
    #Output the x-axis labels to the terminal
    for line in listOfLinesToOutput:
        print(line)
        
    #Allow the user time to read the graph
    time.sleep(3)
    return True
    


def showSpeciesInfo(SpeciesCode:str) -> dict:
    """Displays the information about a given pollutant species in the terminal and returns a dictionary of information about the species

    Parameters:
    SpeciesCode : str
    
    Returns:
        dict: A dictionary of pollutant species information
        False: if the function failed
    """ 
    import requests

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/Species/SpeciesCode={SpeciesCode}/Json"

    url = endpoint.format(
        SpeciesCode=SpeciesCode,
    )

    res = requests.get(url)
    speciesInfoDict = res.json() #Stores the result in a dictionary
    
    #Check that some data was returned for the specific species code
    #Return False if no data was returned
    if len(speciesInfoDict <=0):
        return False
    
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
    
    #Split up each line so that it can be written to the terminal without words being split over two lines
    listToOutput = []
    for line in speciesInfoList:
        
        #Run while the length of a line is greater than the width of the terminal
        while len(line) > terminalColumns:
            indexToSubstrFrom = terminalColumns #The greatest index that can be used to create a sub string from
            
            #Loop through the line backwards starting from the greatest index that can be used to create a sub string,
            #loop through each index in reverse until a space character is found (and therefore a word will not hang over two lines),
            #set the index that the substring of the line to end to be at this index and break the loop
            for count in range(len(line[:terminalColumns]) - 1, -1, -1):
                if line[count] == ' ':
                    indexToSubstrFrom = count
                    break
                
            #Append the substr of the line to the list to output and remove the substring of the line from the line variable  
            listToOutput.append(line[:indexToSubstrFrom])
            line = " "*20 + line[indexToSubstrFrom:]
            
        #Append the remainder of the line to the list of lines to output
        listToOutput.append(line)
        
    #Output each line in the list of lines to output variable,
    #Wait 1 second between outputs to allow the user to read each line
    for item in listToOutput:
        print(item)
        time.sleep(1)
             
    #Return the dictionary of air quality information for the specific monitoring station code
    return res.json()


def showAllSpeciesInfo() -> dict:
    """Displays the information about all common pollutant species in the terminal and returns a dictionary of information about the species
    
    Returns:
        Bool: True if the function has run successfully
    """ 
    #Store the whitelisted pollutants in a list
    whitelistOfPollutants = ['NO2', 'CO', 'O3', 'PM10', 'SO2', 'PM25']
    
    #output the information about all pollutants in the list of whitelisted pollutants
    for item in whitelistOfPollutants:
        showSpeciesInfo(item)
        print("")
        
    #Return True if the function has run successfully
    return True


#TODO box plot function
    
def outputAllMonitoringStations(outputToTerminal = True):
    """Outputs the name and site code of all monitoring stations in London to the terminal. 
    
        Parameters:
        outputToTerminal : bool, optional
            Output the name and site code of all monitoring stations in London to the terminal. Default value is True.
            
        Returns:
            list: a list of tuples with the name of the monitoring station in index 0 and the site code in index 1
    """
    #Validate that the parameter is a boolean value
    if not type(outputToTerminal) == bool:
        raise ValueError("The parameter outputToTerminal must be a boolean value. Function Failed.")
    
    #The url to be used when requesting data from the API
    url = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json"

    #Request the data from the API and store as a dictionary
    result = requests.get(url)
    speciesInfoDict = result.json()
    
    #Loop through each site contained within the returned dictionary of monitoring stations append their site name and site code to
    #A list in the format: (SiteName, SiteCode)
    listOfMonitoringStations = []
    for item in speciesInfoDict['Sites']['Site']:
        listOfMonitoringStations.append((item['@SiteName'], item['@SiteCode']))
        
    #If outputToTerminal == True output to the terminal the site codes and site names
    if outputToTerminal == True:
        for item in listOfMonitoringStations:
            print(item[1] + " | " + item[0])
            time.sleep(0.25)
    
    #Return the list of tuples
    return listOfMonitoringStations
    
def getAirQualityIndexData(AirQualityIndex:int) -> dict:
    """Accepts a value 1-10, gets the air quality band, and health advice for both at risk individuals and general population from an API,
    and returns the results as a dictionary
    
    Parameters:
        int: AirQualityIndex
    
    Exception:
        If the AirQualityIndex input is not between 1 and 10, the advice returned is set to 'Unknown'
        
    Returns:
        dict: a dictionary containing the air quality band, health advice, and population data
    """
    import requests
    import time
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/IndexHealthAdvice/AirQualityIndex={AirQualityIndex}/Json"

    url = endpoint.format(
        AirQualityIndex=AirQualityIndex
    )

    try:
        #Request the air quality index data from the API and store the result in a dictionary
        res = requests.get(url)
        airQualityIndexDict = res.json() 
    
    #If the air quality index input as a parameter is invalid, set the data to 'Unknown'
    except:
        print("\nAn invalid air quality index was input therefore the index health advice is unknown. (values should be 1-10)\n"
              "For accurate advice, please use a valid value.")
        
        #The url used to retrieve data from the API
        url = "https://api.erg.ic.ac.uk/AirQuality/Information/IndexHealthAdvice/AirQualityIndex=1/Json"
        
        #Request data from the api and store as a dictionary
        res = requests.get(url)
        airQualityIndexDict = res.json()
        
        #Set the health advice to unknown as an invalid value was entered
        airQualityIndexDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['@AirQualityBand'] = 'Unknown'
        airQualityIndexDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['@LowerAirQualityIndex'] = str(AirQualityIndex)
        airQualityIndexDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['@UpperAirQualityIndex'] = str(AirQualityIndex)
        airQualityIndexDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['HealthAdvice'][0]['@Advice'] = 'Unknown'
        airQualityIndexDict['AirQualityIndexHealthAdvice']['AirQualityBanding']['HealthAdvice'][1]['@Advice'] = 'Unknown'

    #Return the dictionary of air quality health advice
    return airQualityIndexDict

def outputAirQualityIndexDataForSpecificSite(SiteCode: str) -> bool:
    """Outputs the air quality index information for a specific monitoring site along with health advice.
    Returns False if no information was found and returns True if information is found

    Args:
        SiteCode (str): The SiteCode for a valid monitoring station

    Returns:
        bool: Returns True if information is found and False if information is not found
    """    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Hourly/MonitoringIndex/SiteCode={SiteCode}/Json"
    
    url = endpoint.format(
        SiteCode=SiteCode
    )

    res = requests.get(url)
    returnedDict = res.json() #Stores the result in a dictionary
    
    #If no data was returned by the API, return False
    if returnedDict == None:
        print("There is no data for the requested site.")
        return False
    
    #If no data was returned by the API, return False
    elif len(returnedDict) == 0:
        print("There is no data for the requested site.")
        return False
    
    #Retrieve required data from the dictionary
    SiteName = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['@SiteName']
    
    #A function to output the information
    def outputHealthAdvice(SpeciesName, SpeciesCode, AirQualityIndex, AirQualityBand):
        ''' Outputs the health advice for the pollutants at a specific site code to the terminal
        '''
        #Get health advice information and store the advice for different population types in 2 separate variables
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
        #Unpack the data from the dictionary into multiple variables and call the output to terminal function
        SpeciesName = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@SpeciesName']
        SpeciesCode = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@SpeciesCode']
        AirQualityIndex = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@AirQualityIndex']
        AirQualityBand = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']['@AirQualityBand']
        outputHealthAdvice(SpeciesName, SpeciesCode, AirQualityIndex, AirQualityBand)
    except: #Otherwise do this
        #Unpack the data from the dictionary into multiple variables and call the output to terminal function for each pollutant type
        for index in range(0, len(returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'])):
            SpeciesName = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@SpeciesName']
            SpeciesCode = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@SpeciesCode']
            AirQualityIndex = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@AirQualityIndex']
            AirQualityBand = returnedDict['HourlyAirQualityIndex']['LocalAuthority']['Site']['species'][index]['@AirQualityBand']
            outputHealthAdvice(SpeciesName, SpeciesCode, AirQualityIndex, AirQualityBand)
    
    #Return True because data was found
    return True
    


def validateDateFormat(date:str) -> bool:
    '''Accepts a date in as a parameter. Returns True if the date is in a valid format ('%Y-%m-%d') otherwise raises a value error
    
    Args:
        date (string): The date to validate
        
    Returns:
        bool: True if the date is valid else False
    '''
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True 
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    
def validateTimeFormat(time:str) -> bool:
    '''Accepts a time in as a parameter. Returns True if the time is in a valid format ('%H:%M:%S') otherwise raises a value error
    
    Args:
        date (string): The date to validate
        
    Returns:
        bool: True if the date is valid else False
    '''
    try:
        datetime.datetime.strptime(time, '%H:%M:%S')
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be HH:MM:SS")

def inputSiteCode():
    """gets input from the user until a valid monitoring station is entered or the user requests to quit the menu.
       returns the user's input if the monitoring station entered is valid, returns 'Q' if the user requests to quit
       
       inputs:
            SiteCode (str): The site code for a monitoring station contained within the API
            
        returns:
            str: The user's input once the monitoring station entered is valid, otherwise returns 'Q' if the user requests to quit
    """
    #Keep running until a valid input is entered or the user requests to quit the menu
    while True:
        #Catch exceptions if incorrect type is input
        userInput = ""
        while True:
            try:
                userInput = str(input(
                    "Enter a site code. If you would like to exit, input 'Q'")).upper()
                break
            except TypeError:
                print("Invalid type input.\nPlease input a string.\n")

        #If the user requests to quit return "Q"
        if userInput == "Q":
            return "Q"
                
        # Check that the site code input by the user is valid
        listOfMonitoringStations = outputAllMonitoringStations(False) # Returns a list of all monitoring stations and their site codes
        for item in listOfMonitoringStations:
            if item[1] == userInput:
                return userInput.upper()
            
        #Tell the user their input is invalid (the function will have already returned a value if the input was valid)
        print("Invalid input.\nThe site code you input is not valid.\n")
        
def drawPollutantPieChart():
    ''' Outputs a pie chart using the turtle module. Displays the average percentage of each pollutant at a specific monitoring station
        in different average formats (mean,median,mode) then also sums up the values and creates a chart.
        Returns True if the pie chart has been drawn, False otherwise.
        \n*NOTE* This function can only be successfully run once per run of the program due to the limitations of the python turtle module
       
        Inputs:
            str: The site code of the monitoring station
            str: The date to start the pollutant data set from
            str: The date to end the pollutant data set at
       
        Outputs:
            A pie chart showing the average percentage of each pollutant at a specific monitoring station
       
        Returns:
            bool: True if the pie chart has been drawn, False otherwise
    '''
    
    #Get the pollutant data from a specific monitoring station
    siteCode = inputSiteCode()
    
    if siteCode != 'Q':
        #Enter the start and end date of the data set to retrieve from the API
        startDate = input("enter the date you would like to receive data from (YYYY-MM-DD): ")
        validateDateFormat(startDate) #Validates that the date is in the correct format
        endDate = input("enter the final date you would like to receive data to (YYYY-MM-DD): ")
        validateDateFormat(endDate) #Validates that the date is in the correct format
        
        #Get the string for todays date by reformatting datetime object
        dateToday = datetime.date.today()
        dateToday = dateToday.strftime('%Y-%m-%d')
            
        #Validate the dates input as parameters
        while startDate >= dateToday or endDate > dateToday or startDate >= endDate:
            #If the start date entered is greater than or equal to the date today 
            #Or the end date entered is greater than the date today request new inputs
            if startDate >= dateToday or endDate > dateToday:
                print("The start date must be before today's date, and the end date must be before or equal to today's date.")
                
                #Enter the start and end date of the data set to retrieve from the API
                startDate = input("enter the date you would like to receive data from (YYYY-MM-DD): ")
                validateDateFormat(startDate)
                endDate = input("enter the final date you would like to receive data to (YYYY-MM-DD): ")
                validateDateFormat(endDate)
            
            #If the start date entered is greater than or equal to the end date request new inputs
            if startDate >= endDate:
                print("\nThe start date must be before the end date.")
                
                #Enter the start and end date of the data set to retrieve from the API
                startDate = input("enter the date you would like to receive data from (YYYY-MM-DD): ")
                validateDateFormat(startDate)
                endDate = input("enter the final date you would like to receive data to (YYYY-MM-DD): ")
                validateDateFormat(endDate)
        
        #Get the pollutant data for the monitoring station
        endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/Site/SiteCode={SiteCode}/StartDate={StartDate}/EndDate={EndDate}/Json"

        url = endpoint.format(
            SiteCode=siteCode,
            StartDate=startDate,
            EndDate=endDate
        )

        #Request the data from the API and store as a dictionary
        result = requests.get(url)
        pollutantDict = result.json()
        
        #Create a dictionary with pollutant type as each key and then a list of its values as the values for each key
        pollutantValuesDict = dict()
        for item in pollutantDict['AirQualityData']['Data']:
            #Only add values to the dictionary if data exists for the pollutant at that specific date and time
            if item['@Value'] != '':
                pollutantType = item['@SpeciesCode']
                
                #If the pollutant key does not already exist, create the key
                #and append the pollutant value to a list within that dictionary key 
                # otherwise append to the list within the dictionary
                if pollutantType not in pollutantValuesDict.keys():
                    pollutantValuesDict[pollutantType] = [float(item['@Value'])]
                else:
                    pollutantValuesDict[pollutantType].append(float(item['@Value']))

        #If there is no valid data for the specified time period, return False
        if len(pollutantValuesDict) == 0:
            print("No pollutant data found.")
            return False
        
        #Create dictionaries for the different average types:
        meanValueDict = dict()
        medianValueDict = dict()
        modeValueDict = dict()
        sumValueDict = dict()

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
        colors = ['red', 'green', 'blue', 'yellow','magenta'] #Black is kept for use with labels only
        
        #Define the different labels for the pie chart
        listOfChartTypesToDraw = ['mean','median','mode','sum']
        
        #Tell the user they need to open another window
        print("Open the python turtle window")
            
        #loop for each chart type to draw
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
            
            #contains a list of tuples in the format: (percentage, key, value)
            percentagesOfCircleToDrawList = []
            
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw 
            #is the mean pollutant pie chart
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
                    
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw
            #is the median pollutant pie chart   
            if chartType == 'median':
                #Get the sum of all of the median values
                sumOfAllMedianValues = 0
                for value in medianValueDict.values():
                    sumOfAllMedianValues += value
                
                #Append values to the list of percentage values
                for key in medianValueDict:
                    value = medianValueDict[key]
                    percentage = (360/sumOfAllMedianValues) * value
                    percentagesOfCircleToDrawList.append((percentage,key,value))
                    
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw
            #is the mode pollutant pie chart   
            if chartType == 'mode':
                #Get the sum of all of the modal values
                sumOfAllModeValues = 0
                for value in modeValueDict.values():
                    sumOfAllModeValues += value
                
                #Append values to the list of percentage values
                for key in modeValueDict:
                    value = modeValueDict[key]
                    percentage = (360/sumOfAllModeValues) * value
                    percentagesOfCircleToDrawList.append((percentage,key,value))
                    
            #Append the percentage of the pie chart to draw to the list if the current type of chart to draw
            #is the median pollutant pie chart   
            if chartType == 'sum':
                #Get the sum of all of the sum values
                sumOfAllSumValues = 0
                for value in sumValueDict.values():
                    sumOfAllSumValues += value
                
                #Append values to the list of percentage values
                for key in sumValueDict:
                    value = sumValueDict[key]
                    percentage = (360/sumOfAllSumValues) * value
                    percentagesOfCircleToDrawList.append((percentage,key,value))
                    
            #Draw each sector of the pie chart
            currentPenColour = 'cyan'
            for item in percentagesOfCircleToDrawList:
                
                #Change the colour of the pen to a colour different to the current pen colour
                #If the sector to draw is not the first sector
                newPenColour = currentPenColour
                while newPenColour == currentPenColour:
                    
                    #Select a random colour from the list of colours
                    if item != percentagesOfCircleToDrawList[0]:
                        newPenColour = colors[random.randint(0,len(colors) - 1)]
                    
                    #Always select the same first pen colour so that there is no clash between colours in the chart
                    else:
                        break
                currentPenColour = newPenColour
                pieChartTurtle.fillcolor(currentPenColour)
                pieChartTurtle.pencolor(currentPenColour)
                
                
                #Draw a sector then fill with the corresponding colour
                pieChartTurtle.begin_fill()
                pieChartTurtle.right(90)
                pieChartTurtle.forward(pieChartRadius)
                pieChartTurtle.left(90)
                pieChartTurtle.circle(pieChartRadius, item[0]) #Draw the % of the pie chart that represents that pollutant
                pieChartTurtle.left(90)
                pieChartTurtle.forward(pieChartRadius)
                pieChartTurtle.right(90)
                pieChartTurtle.end_fill()
                
                #Get the current coordinates of the turtle
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
            
            #Wait so that the finished pie chart can be read by the user
            time.sleep(3)
            
            #Clear the canvas ready for the next chart
            pieChartTurtle.clear()

        #Close the turtle window
        turtle.bye()
        
        #The pie chart was complete so return True
        return True
    else:
        #Quit the function and return False as the pie chart was not drawn
        print("Quitting...")
        return False
