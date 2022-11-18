from utils import checkExceptionArray, checkExceptionBool, checkExceptionInteger, checkExceptionString, countvalue, checkExceptionDictionary, checkExceptionDate


def readCSV(fileName):
    file = open(fileName)
    dictionary = dict(date=[], name=[], no=[], pm10=[], pm25=[])

    readHeadings = True
    dateList = []
    timeList = []
    noList = []
    pm10List = []
    pm25List = []
    for i in file:
        line = i.rstrip()
        if readHeadings == False:
            lineArr = line.split(",")
            if len(lineArr) == 5:
                dateList.append(lineArr[0])
                timeList.append(lineArr[1])
                noList.append(lineArr[2])
                pm10List.append(lineArr[3])
                pm25List.append(lineArr[4])
        else:
            readHeadings = False

    dictionary["date"] = dateList
    dictionary["time"] = timeList
    dictionary["no"] = noList
    dictionary["pm10"] = pm10List
    dictionary["pm25"] = pm25List

    return dictionary


def daily_average(data: dict, monitoring_station: str, pollutant: str) -> list:
    """Takes the data from all monitoring stations input as a dictionary with the keys containing lists of data. 
    Returns a list containing the daily average pollutant data for a given pollutant and monitoring station

    Raises:
        Exception: Raises an exception if an invalid monitoring station is input*
        Exception: Raises an exception if an invalid monitoring station is input
        Exception: Raises an exception of the data input as a parameter is not a dictionary
        Exception: Raises an exception if the monitoring_station parameter is not a string
        Exception: Raises an exeption if the pollutant parameter is not a string

    Returns:
        list: a list containing the daily average pollutant data for a given pollutant and monitoring station
    """

    # TODO Put in checks e.g. an hour may be fully missing from the data set which would break the code as I rely on there being
    # exactly 24 pieces of data to calculate the daily average

    # Check for exceptions
    checkExceptionString(monitoring_station)
    checkExceptionString(pollutant)
    checkExceptionDictionary(data)

    # lowercase the parameters to avoid errors in case sensitivity
    monitoring_station = monitoring_station.lower()
    pollutant = pollutant.lower()

    # Raise an exception if an unknown monitoring station is entered
    # TODO not sure if this should be here? I would put this usually but not sure how code testing works, i dont think that this can
    # be tested with the names of other monitoring stations though
    # possibly remove? ask about it.
    if monitoring_station != 'harlington':
        if monitoring_station != 'marylebone road':
            if monitoring_station != 'n kensington':
                raise Exception("unexpected parameter! Parameter: monitoring_station: ", monitoring_station,
                                "entered. expected: 'harlington', 'marylebone road', or 'n kensington'")

    # Raise an exception if an unknown pollutant is enteredd
    if pollutant != 'no':
        if pollutant != 'pm10':
            if pollutant != 'pm25':
                raise Exception("unexpected paramater! Parameter: pollutant: ",
                                pollutant, "entered. expected: 'no', 'pm10', or 'pm25'")

    pollutantData = data[monitoring_station.lower()][pollutant]

    # Find the number of decimal places the data is required to be
    maximumNumDecimalPlaces = 0
    for i in pollutantData:
        try:
            i = float(i)  # Only count data that can be converted to a float

        except:
            a = 1  # ignore other values

        if type(i) == float:

            i = str(i)
            if len(i[i.rfind('.') + 1:]) > maximumNumDecimalPlaces:
                # finds the number of digits after the decimal point
                maximumNumDecimalPlaces = len(i[i.rfind('.') + 1:])

    dailyAverageList = []
    dailyTotal = float(0.0)
    count = 0
    numDataPoints = 0
    for i in pollutantData:
        # Try to increment the daily total, otherwise ignore as it is missing data
        try:
            dailyTotal = dailyTotal + float(i)
            numDataPoints += 1
        except:
            a = 1

        if count % 24 == 23:
            dailyAverageList.append(
                round(dailyTotal/numDataPoints, maximumNumDecimalPlaces))

            dailyTotal = 0
            numDataPoints = 0
        count += 1

    return dailyAverageList


def daily_median(data: dict, monitoring_station: str, pollutant: str) -> list:
    """Takes the data from all monitoring stations input as a dictionary with the keys containing lists of data. 
    Returns a list containing the daily median pollutant data for a given pollutant and monitoring station

    Raises:
        Exception: Raises an exception if an invalid monitoring station is input*
        Exception: Raises an exception if an invalid monitoring station is input
        Exception: Raises an exception of the data input as a parameter is not a dictionary
        Exception: Raises an exception if the monitoring_station parameter is not a string
        Exception: Raises an exeption if the pollutant parameter is not a string

    Returns:
        list: a list containing the daily median pollutant data for a given pollutant and monitoring station
    """

    # TODO Put in checks e.g. an hour may be fully missing from the data set which would break the code as I rely on there being
    # exactly 24 pieces of data to calculate the daily average

    # Check for exceptions
    checkExceptionString(monitoring_station)
    checkExceptionString(pollutant)
    checkExceptionDictionary(data)

    # lowercase the parameters to avoid errors in case sensitivity
    monitoring_station = monitoring_station.lower()
    pollutant = pollutant.lower()

    # Raise an exception if an unknown monitoring station is entered
    # TODO not sure if this should be here? I would put this usually but not sure how code testing works, i dont think that this can
    # be tested with the names of other monitoring stations though
    # possibly remove? ask about it.
    if monitoring_station != 'harlington':
        if monitoring_station != 'marylebone road':
            if monitoring_station != 'n kensington':
                raise Exception("unexpected parameter! Parameter: monitoring_station: ", monitoring_station,
                                "entered. expected: 'harlington', 'marylebone road', or 'n kensington'")

    # Raise an exception if an unknown pollutant is enteredd
    if pollutant != 'no':
        if pollutant != 'pm10':
            if pollutant != 'pm25':
                raise Exception("unexpected paramater! Parameter: pollutant: ",
                                pollutant, "entered. expected: 'no', 'pm10', or 'pm25'")

    pollutantData = data[monitoring_station.lower()][pollutant]

    # Find the number of decimal places the data is required to be
    maximumNumDecimalPlaces = 0
    for i in pollutantData:
        try:
            i = float(i)  # Only count data that can be converted to a float

        except:
            a = 1  # ignore other values

        if type(i) == float:

            i = str(i)
            if len(i[i.rfind('.') + 1:]) > maximumNumDecimalPlaces:
                # finds the number of digits after the decimal point
                maximumNumDecimalPlaces = len(i[i.rfind('.') + 1:])

    dailyMedianList = []
    count = 0
    dailyPollutantValues = []  # Stores the pollutant data for a given day
    for i in pollutantData:
        # include the data in the median if the data is an integer or floating point value
        try:
            i = float(i)
            dailyPollutantValues.append(i)
        except:
            a = 1  # Ignore any missing data

        if count % 24 == 23:
            dailyPollutantValues.sort()  # Sort the values into order
            medianValue = 0.0

            # Find the centre value
            if len(dailyPollutantValues) % 2 == 0:  # If even length
                medianValue = (dailyPollutantValues[int(len(
                    dailyPollutantValues) / 2)] + dailyPollutantValues[int(len(dailyPollutantValues) / 2) - 1])/2

            else:
                medianValue = dailyPollutantValues[int(
                    len(dailyPollutantValues)//2)]

            dailyMedianList.append(round(medianValue, maximumNumDecimalPlaces))

            dailyPollutantValues = []

        count += 1

    return dailyMedianList


def hourly_average(data: dict, monitoring_station: str, pollutant: str) -> list:
    """returns a list/array with the hourly averages (i.e. 24 values) for a particular pollutant and monitoring station

    Args:
        data (dict): a dictionary containing the data for all monitoring stations
        monitoring_station (str): the name of the monitoring station you would like to recieve pollutant data from
        pollutant (str): the name of the pollutant that you would like to recieve data about

    Returns:
        list: a list containing the values of the average pollutant level for each hour of the day
    """
    # TODO test that the results of this function are correct

    # Check for exceptions
    checkExceptionString(monitoring_station)
    checkExceptionString(pollutant)
    checkExceptionDictionary(data)

    # lowercase the parameters to avoid errors in case sensitivity
    monitoring_station = monitoring_station.lower()
    pollutant = pollutant.lower()

    # Raise an exception if an unknown monitoring station is entered
    # TODO not sure if this should be here? I would put this usually but not sure how code testing works, i dont think that this can
    # be tested with the names of other monitoring stations though
    # possibly remove? ask about it.
    if monitoring_station != 'harlington':
        if monitoring_station != 'marylebone road':
            if monitoring_station != 'n kensington':
                raise Exception("unexpected parameter! Parameter: monitoring_station: ", monitoring_station,
                                "entered. expected: 'harlington', 'marylebone road', or 'n kensington'")

    # Raise an exception if an unknown pollutant is enteredd
    if pollutant != 'no':
        if pollutant != 'pm10':
            if pollutant != 'pm25':
                raise Exception("unexpected paramater! Parameter: pollutant: ",
                                pollutant, "entered. expected: 'no', 'pm10', or 'pm25'")

    # Retrieve the list for the specific monitoring station and pollutant
    pollutantData = data[monitoring_station][pollutant]

    hourlyDict = {}  # A dictionary containing each hour and the values
    count = 0
    for i in pollutantData:
        # Add a new key if the current time is not already a key in the dictionary

        # Gets only the hour from the time in the pollution csv file
        hour = data[monitoring_station]['time'][count][0:2]
        if hour not in hourlyDict.keys():
            # Creates a new dictionary key with an empty list value
            hourlyDict[hour] = []

        # Add the current pollution data being iterated through to the correct hour in the dictionary
        hourlyDict[hour].append(i)

        count += 1

    # Find the number of decimal places the data is required to be
    maximumNumDecimalPlaces = 0
    for i in pollutantData:
        try:
            i = float(i)  # Only count data that can be converted to a float

        except:
            a = 1  # ignore other values

        if type(i) == float:

            i = str(i)
            if len(i[i.rfind('.') + 1:]) > maximumNumDecimalPlaces:
                # finds the number of digits after the decimal point
                maximumNumDecimalPlaces = len(i[i.rfind('.') + 1:])

    hourlyAvgList = []
    average = 0
    for key in hourlyDict:

        total = 0
        numberOfValues = 0
        for i in hourlyDict[key]:
            try:
                total += float(i)
                numberOfValues += 1
            except:
                a = 1  # The value should be excluded

        average = total/numberOfValues
        # Append the average hourly value to a list and round the value to the required number of decimal places
        hourlyAvgList.append(round(average, maximumNumDecimalPlaces))

    return hourlyAvgList  # Returns the list of hourly averages


def monthly_average(data: dict, monitoring_station: str, pollutant: str) -> list:
    """returns a list/array with the monthly averages (i.e. 12 values) for a particular pollutant and monitoring station

    Args:
        data (dict): a dictionary containing the data for all monitoring stations
        monitoring_station (str): the name of the monitoring station you would like to recieve pollutant data from
        pollutant (str): the name of the pollutant that you would like to recieve data about

    Returns:
        list: a list containing the values of the average pollutant level for each month of the year
    """
    # TODO test that the results of this function are correct

    # Check for exceptions
    checkExceptionString(monitoring_station)
    checkExceptionString(pollutant)
    checkExceptionDictionary(data)

    # lowercase the parameters to avoid errors in case sensitivity
    monitoring_station = monitoring_station.lower()
    pollutant = pollutant.lower()

    # Raise an exception if an unknown monitoring station is entered
    # TODO not sure if this should be here? I would put this usually but not sure how code testing works, i dont think that this can
    # be tested with the names of other monitoring stations though
    # possibly remove? ask about it.
    if monitoring_station != 'harlington':
        if monitoring_station != 'marylebone road':
            if monitoring_station != 'n kensington':
                raise Exception("unexpected parameter! Parameter: monitoring_station: ", monitoring_station,
                                "entered. expected: 'harlington', 'marylebone road', or 'n kensington'")

    # Raise an exception if an unknown pollutant is enteredd
    if pollutant != 'no':
        if pollutant != 'pm10':
            if pollutant != 'pm25':
                raise Exception("unexpected paramater! Parameter: pollutant: ",
                                pollutant, "entered. expected: 'no', 'pm10', or 'pm25'")

    # Retrieve the list for the specific monitoring station and pollutant
    pollutantData = data[monitoring_station][pollutant]

    monthlyDict = {}  # A dictionary containing each month as a key and each key contains a list of the data values of a specific pollutant for that month
    count = 0
    for i in pollutantData:
        # Add a new key if the current month is not already a key in the dictionary

        # Gets only the month from the date in the pollution csv file
        month = data[monitoring_station]['date'][count][5:7]
        if month not in monthlyDict.keys():
            # Creates a new dictionary key with an empty list value
            monthlyDict[month] = []

        # Add the current pollution data being iterated through to the correct month in the dictionary
        monthlyDict[month].append(i)

        count += 1

    # Find the number of decimal places the data is required to be
    maximumNumDecimalPlaces = 0
    for i in pollutantData:
        try:
            i = float(i)  # Only count data that can be converted to a float

        except:
            a = 1  # ignore other values

        if type(i) == float:

            i = str(i)
            if len(i[i.rfind('.') + 1:]) > maximumNumDecimalPlaces:
                # finds the number of digits after the decimal point
                maximumNumDecimalPlaces = len(i[i.rfind('.') + 1:])

    monthlyAvgList = []
    average = 0
    for key in monthlyDict:

        total = 0
        numberOfValues = 0
        for i in monthlyDict[key]:
            try:
                total += float(i)
                numberOfValues += 1
            except:
                a = 1  # The value should be excluded

        average = total/numberOfValues
        # Append the average hourly value to a list and round the value to the required number of decimal places
        monthlyAvgList.append(round(average, maximumNumDecimalPlaces))

    return monthlyAvgList  # Returns the list of hourly averages


def peak_hour_date(data: dict, date: str, monitoring_station: str, pollutant: str) -> tuple:
    """For a given date (e.g., 2021-01-01) returns the hour of the day with the highest pollution level and its corresponding value (e.g., (12:00, 14.8)).

    Args:
        data (dict): a dictionary containing the data for all monitoring stations
        date (str): a string containing the date that you would like to search for the peak hourly pollution
        monitoring_station (str): the name of the monitoring station you would like to recieve pollutant data from
        pollutant (str): the name of the pollutant that you would like to recieve data about

    Returns:
        tuple: a tuple containing the hour that the peak pollution level was found and the peak pollution level e.g. (12:00, 14.8)
    """
    # TODO test that the results of this function are correct

    # Check for exceptions
    checkExceptionString(monitoring_station)
    checkExceptionString(pollutant)
    checkExceptionString(date)
    checkExceptionDate(date)
    checkExceptionDictionary(data)

    # lowercase the parameters to avoid errors in case sensitivity
    monitoring_station = monitoring_station.lower()
    pollutant = pollutant.lower()

    # Raise an exception if an unknown monitoring station is entered
    # TODO not sure if this should be here? I would put this usually but not sure how code testing works, i dont think that this can
    # be tested with the names of other monitoring stations though
    # possibly remove? ask about it.
    if monitoring_station != 'harlington':
        if monitoring_station != 'marylebone road':
            if monitoring_station != 'n kensington':
                raise Exception("unexpected parameter! Parameter: monitoring_station: ", monitoring_station,
                                "entered. expected: 'harlington', 'marylebone road', or 'n kensington'")

    # Raise an exception if an unknown pollutant is enteredd
    if pollutant != 'no':
        if pollutant != 'pm10':
            if pollutant != 'pm25':
                raise Exception("unexpected paramater! Parameter: pollutant: ",
                                pollutant, "entered. expected: 'no', 'pm10', or 'pm25'")

    # Retrieve the list for the specific monitoring station and pollutant
    pollutantData = data[monitoring_station][pollutant]

    dateDict = {}  # A dictionary containing each month as a key and each key contains a list of the data values of a specific pollutant for that month
    count = 0
    for i in pollutantData:
        # Add a new key if the current date is not already a key in the dictionary

        # Gets the date from a specific piece of data
        dateToFind = data[monitoring_station]['date'][count][0:10]
        # Gets only the hour from the time in the pollution csv file
        hourToFind = data[monitoring_station]['time'][count][0:]
        if dateToFind not in dateDict.keys():
            # Creates a new dictionary key with an empty list value
            dateDict[dateToFind] = []

        # Add the current pollution data being iterated through to the correct month in the dictionary
        dateDict[dateToFind].append((hourToFind, i))
        count += 1

    # Find the number of decimal places the data is required to be
    maximumNumDecimalPlaces = 0
    for i in pollutantData:
        try:
            i = float(i)  # Only count data that can be converted to a float

        except:
            a = 1  # ignore other values

        if type(i) == float:

            i = str(i)
            if len(i[i.rfind('.') + 1:]) > maximumNumDecimalPlaces:
                # finds the number of digits after the decimal point
                maximumNumDecimalPlaces = len(i[i.rfind('.') + 1:])

    peakValue = ('-1', '-1')
    for item in dateDict[date]:

        try:
            a = float(item[1])  # Check if there is an exception
            if float(item[1]) > float(peakValue[1]):
                peakValue = item

        except:
            a = 1  # Ignore if there is no data for the pollutant

    if peakValue == -1:
        raise Exception(
            "No numeric value found for the specific date searched for. Expected at least one numeric value")

    return peakValue


def count_missing_data(data: dict,  monitoring_station: str, pollutant: str) -> list:
    # Check for exceptions
    checkExceptionString(monitoring_station)
    checkExceptionString(pollutant)
    checkExceptionDictionary(data)

    # lowercase the parameters to avoid errors in case sensitivity
    monitoring_station = monitoring_station.lower()
    pollutant = pollutant.lower()

    # Raise an exception if an unknown monitoring station is entered
    # TODO not sure if this should be here? I would put this usually but not sure how code testing works, i dont think that this can
    # be tested with the names of other monitoring stations though
    # possibly remove? ask about it.
    if monitoring_station != 'harlington':
        if monitoring_station != 'marylebone road':
            if monitoring_station != 'n kensington':
                raise Exception("unexpected parameter! Parameter: monitoring_station: ", monitoring_station,
                                "entered. expected: 'harlington', 'marylebone road', or 'n kensington'")

    # Raise an exception if an unknown pollutant is enteredd
    if pollutant != 'no':
        if pollutant != 'pm10':
            if pollutant != 'pm25':
                raise Exception("unexpected paramater! Parameter: pollutant: ",
                                pollutant, "entered. expected: 'no', 'pm10', or 'pm25'")

    # Retrieve the list for the specific monitoring station and pollutant
    pollutantData = data[monitoring_station][pollutant]
    
    total = 0
    for i in pollutantData:
        if i == 'No data':
            total += 1
    
    return total


def fill_missing_data(data: dict, new_value: int,  monitoring_station: str, pollutant: str) -> list:
    """Your documentation goes here"""

    # Your code goes here


# test start
pollutionDictionary = dict()
pollutionDictionary['harlington'] = readCSV(
    "data/Pollution-London Harlington.csv")
pollutionDictionary['marylebone road'] = readCSV(
    "data/Pollution-London Marylebone Road.csv")
pollutionDictionary['n kensington'] = readCSV(
    "data/Pollution-London N Kensington.csv")

daily_average(pollutionDictionary, 'harLington', 'pM25')


readCSV("data/Pollution-London Harlington.csv")

monthly_average(pollutionDictionary, 'harLington', 'pM25')

peak_hour_date(pollutionDictionary, '2021-11-18', 'harLington', 'pM25')

print(count_missing_data(pollutionDictionary, 'harLington', 'pM25'))

#test end