# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def sumvalues(values):
    """Returns the sum of all values in an array
    
    Args:
        values (list): A list of integers
    
    Raises:
        Exception: values is not of type list
        Exception: values contains a value that is not an integer

    Returns:
        int: The sum of all values in an array
    """    
    checkExceptionArray(values) #Checks that the input parameter is an array
    
    sum = 0   
    for item in values: #loop through each value of the array
        checkExceptionInteger(item) #Check that the item is an integer
        sum += item
    
    return sum #Return the sum of all integers in the array



def maxvalue(values):
    """Returns the index of the maximum integer value contained within an array

    Args:
        values (list): A list of integers

    Raises:
        Exception: values is not of type list
        Exception: values contains a value that is not an integer
        Exception: no items found within the array

    Returns:
        int: The index of the maximum integer value
    """    
    checkExceptionArray(values) #Checks that the input parameter is an array
    
    ##Checks that the array input as a parameter has at least one value
    if len(values) == 0:
        raise Exception("Expected at least one value in array. 0 values found.")
    
    max = values[0] #Set the maximum value to the first value in the list
    indexOfMaxValue = 0 #sets the index of the maximum value to be the first index in the array
    currentIndex = 0 #Keeps track of the current index
    
    
    for item in values: #Iterates through each item of the array
        checkExceptionInteger(item) #Checks that the array item is an integer
        
        ##Checks if the current item is greater than the current maximum value
        if item > max: 
            max = item
            indexOfMaxValue = currentIndex
        currentIndex += 1
    
    return indexOfMaxValue #Returns the index of which the maximum value is ocntained within the array
        


def minvalue(values):
    """Returns the index of the minimum integer value contained within an array

    Args:
        values (list): A list of integers

    Raises:
        Exception: values is not of type list
        Exception: values contains a value that is not an integer
        Exception: no items found within the array

    Returns:
        int: The index of the minimum integer value
    """    
    checkExceptionArray(values) #Checks that the input parameter is an array
    
    ##Checks that the array input as a parameter has at least one value
    if len(values) == 0:
        raise Exception("Expected at least one value in array. 0 values found.")
    
    min = values[0] #Set the minimum value to the first value in the list
    indexOfMinValue = 0 #sets the index of the minimum value to be the first index in the array
    currentIndex = 0 #Keeps track of the current index
    
    
    for item in values: #Iterates through each item of the array
        checkExceptionInteger(item) #Checks that the array item is an integer
        
        ##Checks if the current item is greater than the current minimum value
        if item < min: 
            min = item
            indexOfMinValue = currentIndex
        currentIndex += 1
    
    return indexOfMinValue #Returns the index of which the maximum value is ocntained within the array



def meannvalue(values):
    """Returns the mean value of an integer array

    Args:
        values (list): An integer array

    Raise:
        Exception: If input parameter is not of type list
        Exception: If an item within the input array is not of type int
        
    Returns:
        (int,float): The mean of the input array
    """    
    checkExceptionArray(values) #Check that the input parameter is a list
    
    sum = 0
    numItems = 0
    for item in values: #Loop through each item in the list
        checkExceptionInteger(item) #Check that the item in the array is an integer
        sum += item
        numItems+=1 #increment the length of the list
        
    return sum/numItems #Calculate and return the mean
    


def countvalue(values,x):  
    """counts the number of times x appears in the list values

    Args:
        values (list): A list containing values of any type
        x (any): search for this item in the list values
        
    Raise:
        Exception: If values is not of type list

    Returns:
        int: number of times x was found in the list values
    """
    checkExceptionArray(values) #Check that the parameter values is of type list
    counter = 0 #Keeps track of the number of times x has appeared in the list values
    for item in values: #loops through each item in vlaues
        if item == x: #checks if the current item is equal to the item to search for
            counter +=1 #increment the number of times the searched for item was found
    
    return counter #Return the number of times the item was found
 
 
    
def checkExceptionInteger(value):
    """Raises an exception if the value input as a parameter is not an integer

    Args:
        value (any): value to check if type int

    Raises:
        Exception: if parameter is not of type int
    """    
    if(not type(value) is int):
        raise Exception("Value of type: " + str(type(value)) + " found. Value of type: " + str(type(1)) + " expected.")
 
 
    
def checkExceptionString(value):
    """Raises an exception if the value input as a parameter is not a string

    Args:
        value (any): value to check if type str

    Raises:
        Exception: if parameter is not of type str
    """    
    if(not type(value) is str):
        raise Exception("Value of type: " + str(type(value)) + " found. Value of type: " + str(type("1")) + " expected.")
        
        
        
def checkExceptionBool(value):
    """Raises an exception if the value input as a parameter is not a bool

    Args:
        value (any): value to check if type bool

    Raises:
        Exception: if parameter is not of type bool
    """    
    if(not type(value) is bool):
        raise Exception("Value of type: " + str(type(value)) + " found. Value of type: " + str(type(True)) + " expected.")



def checkExceptionArray(value):
    """Raises an exception if the value input as a parameter is not a list

    Args:
        value (any): value to check if type list

    Raises:
        Exception: if parameter is not of type list
    """    
    if(not type(value) is list):
        raise Exception("Value of type: " + str(type(value)) + " found. Value of type: " + str(type([])) + " expected.")