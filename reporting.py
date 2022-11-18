from utils import checkExceptionArray, checkExceptionBool, checkExceptionInteger, checkExceptionString, countvalue, checkExceptionDictionary

def readCSV(fileName):
    file = open(fileName)
    dictionary = dict(date=[],name=[],no=[],pm10=[],pm25=[])
    
    
    readHeadings = True
    dateList = []
    nameList = []
    noList = []
    pm10List = []
    pm25List = []
    count=0
    for i in file:
        count += 1
        line = i.rstrip()
        if readHeadings == False:
            lineArr = line.split(",")
            if len(lineArr) == 5:
                dateList.append(lineArr[0])
                nameList.append(lineArr[1])
                noList.append(lineArr[2])
                pm10List.append(lineArr[3])
                pm25List.append(lineArr[4])
        else:
            readHeadings = False
            
    dictionary["date"] = dateList
    dictionary["name"] = nameList
    dictionary["no"] = noList
    dictionary["pm10"] = pm10List
    dictionary["pm25"] = pm25List
    
    return dictionary    

#dict(name1,name2,name3)
#name1(date, name, no, pm10, pm25)

def daily_average(data:dict, monitoring_station:str, pollutant:str) -> list:
    
    #Put in checks e.g. an hour may be fully missing from the data set
    #Check for exceptions
    checkExceptionString(monitoring_station)
    checkExceptionString(pollutant)
    checkExceptionDictionary(data)
    
    #lowercase the parameters to avoid errors in case sensitivity
    monitoring_station = monitoring_station.lower()
    pollutant = pollutant.lower()
    
    #Raise an exception if an unknown monitoring station is entered
    ###not sure if this should be here? I would put this usually but not sure how code testing works, i dont think that this can
    ###be tested with the names of other monitoring stations though
    ###possibly remove? ask about it.
    if monitoring_station != 'harlington':
        if monitoring_station != 'marylebone road':
            if monitoring_station != 'n kensington':
                raise Exception("unexpected parameter! Parameter: monitoring_station: ", monitoring_station, "entered. expected: 'harlington', 'marylebone road', or 'n kensington'")
    
    #Raise an exception if an unknown pollutant is enteredd
    if pollutant != 'no':
        if pollutant != 'pm10':
            if pollutant != 'pm25':
                raise Exception("unexpected paramater! Parameter: pollutant: ", pollutant, "entered. expected: 'no', 'pm10', or 'pm25'")
    

    
    pollutantData = data[monitoring_station.lower()][pollutant]

    dailyAverageList = []
    dailyTotal = float(0.0)
    count = 1
    numDataPoints = 0
    for i in pollutantData:
        if count%24 != 23:
            try:
                dailyTotal = dailyTotal + float(i)
                numDataPoints += 1
            except:
                a = 1
        else:
            if pollutant == 'no':
                dailyAverageList.append(round((dailyTotal/numDataPoints),5))#append to list and round to 5 dp
            elif pollutant == 'pm10':
                dailyAverageList.append(round((dailyTotal/numDataPoints),3))#append to list and round to 3 dp
            elif pollutant == 'pm25':
                dailyAverageList.append(round((dailyTotal/numDataPoints),3))#append to list and round to 3 dp
            dailyTotal = 0
            numDataPoints = 0
        count+=1
        
    return dailyAverageList
        
    

def daily_median(data:dict, monitoring_station:str, pollutant:str) -> list:
    """Your documentation goes here"""
    
    ## Your code goes here
def hourly_average(data:dict, monitoring_station:str, pollutant:str) -> list:
    """Your documentation goes here"""
    
    ## Your code goes here
def monthly_average(data:dict, monitoring_station:str, pollutant:str) -> list:
    """Your documentation goes here"""
    
    ## Your code goes here
def peak_hour_date(data:dict, date:str, monitoring_station:str,pollutant:str) -> list:
    """Your documentation goes here"""
    
    ## Your code goes here

def count_missing_data(data:dict,  monitoring_station:str,pollutant:str) -> list:
    """Your documentation goes here"""
    
    ## Your code goes here

def fill_missing_data(data:dict, new_value:int,  monitoring_station:str,pollutant:str) -> list:
    """Your documentation goes here"""
    
    ## Your code goes here






#main
pollutionDictionary = dict()
pollutionDictionary['harlington'] = readCSV("data/Pollution-London Harlington.csv")
pollutionDictionary['marylebone road'] = readCSV("data/Pollution-London Marylebone Road.csv")
pollutionDictionary['n kensington'] = readCSV("data/Pollution-London N Kensington.csv")

print(daily_average(pollutionDictionary, 'harLington', 'pM25'))


readCSV("data/Pollution-London Harlington.csv")