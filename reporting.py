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
