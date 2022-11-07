# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def sumvalues(values):
    """Your documentation goes here""" 
    sum = 0   
    for item in values:
        sum += item
    
    return sum 
    ##TODO raise exception for non-numerical values


def maxvalue(values):
    """Your documentation goes here"""    
    ## Your code goes here


def minvalue(values):
    """Your documentation goes here"""    
    ## Your code goes here


def meannvalue(values):
    """Your documentation goes here"""    
    ## Your code goes here


def countvalue(values,xw):
    """Your documentation goes here"""    
    ## Your code goes here
    
def checkExceptionInteger(value):
    if(not type(value) is int):
        raise Exception("Value of type: " + str(type(value)) + " found. Value of type: " + str(type(1)) + " expected.")
    
def checkExceptionString(value):
    if(not type(value) is str):
        raise Exception("Value of type: " + str(type(value)) + " found. Value of type: " + str(type("1")) + " expected.")
        
def checkExceptionBool(value):
    if(not type(value) is bool):
        raise Exception("Value of type: " + str(type(value)) + " found. Value of type: " + str(type(True)) + " expected.")

