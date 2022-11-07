from PIL import Image #imports Image from the Pillow module - used to load images into an array of RGB values
import numpy as np
from utils import checkExceptionArray, checkExceptionBool, checkExceptionInteger, checkExceptionString

def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """finds all red pixels in a given image

    Args:
        map_filename (str): The name of the map file that should be read
        upper_threshold (int): Defaults to 100. The lowest (exclusive) red RGB value for the pixel to be considered red
        lower_threshold (int): Defaults to 50. the heighest (exclusive) green/blue RGB value for the pixel to be considered red

    Outputs:
        file: A file map-red-pixels.jpg in the data file
        
    Raised:
        Exception: map_filename is not of type str
        Exception: upper_threshold is not of type int
        Exception: lower_threshold is not of type int
        Exception: upper_threshold is not within the bounds 0, 255 inclusive
        Exception: lower_threshold is not within the bounds 0, 255 inclusive

    Returns:
        array: A 2D numpy array containing RGB data for each pixel in the resultant image
    """    
    ##Check for parameters of incorrect type
    checkExceptionString(map_filename) #Check that map_filename is of type str
    checkExceptionInteger(upper_threshold) #Check that upper_threshold is of type int
    checkExceptionInteger(lower_threshold) #Check that lower_threshold is of type int
    
    ##Check that the upper threshold does not exceed its maximum/minimum values
    if(upper_threshold > 255 or upper_threshold < 0):
        raise Exception("upper_threshold value: "+ upper_threshold + "found, a value between 0 and 255 (inclusive) was expected")
    
    ##Check that the lower threshold does not exceed its maximum/minimum values
    if(lower_threshold > 255 or lower_threshold < 0):
        raise Exception("upper_threshold value: "+ lower_threshold + "found, a value between 0 and 255 (inclusive) was expected")
    
    originalImage = Image.open('data/'+map_filename) #stores the image file as an object
    newImage = Image.new("RGB",(originalImage.width,originalImage.height),(0, 0, 0)) #Create a new RGB mode image with identical width and height to the original image
    
    for column in range(0,originalImage.height): #iterates through each column of pixels stored within the originalImage object
        for row in range(0,originalImage.width): #iterates through each row of pixels stored within the originalImage object
            
            ##unpacks the tuple into seperate variables dependant on if the format is RGB or RGBA
            if (len(originalImage.getpixel((row,column))) == 4):
                red,green,blue,a = originalImage.getpixel((row,column))
            else:
                red,green,blue = originalImage.getpixel((row,column))
                
            ##Checks that the pixel in row,colum is within the threshold to be considered red and if so inserts a white pixel into the new RGB image in the same location
            if (red > upper_threshold and green < lower_threshold and blue < lower_threshold):
                newImage.putpixel((row,column),(255,255,255))
                
    newImage.save('data/map-red-pixels.jpg') #Saves the resultant image as a file map-red-pixels.jpg and stores it inside the data file
    return np.array(newImage) #return the resultant image as a 2D numpy array
        
    ##TODO use numpy to change RGB values as it is much faster

def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """finds all cyan pixels in a given image

    Args:
        map_filename (str): The name of the map file that should be read
        upper_threshold (int): Defaults to 100. The lowest (exclusive) blue RGB value for the pixel to be considered cyan
        lower_threshold (int): Defaults to 50. the heighest (exclusive) green/red RGB value for the pixel to be considered cyan

    Outputs:
        file: A file map-cyan-pixels.jpg in the data file
        
    Raised:
        Exception: map_filename is not of type str
        Exception: upper_threshold is not of type int
        Exception: lower_threshold is not of type int
        Exception: upper_threshold is not within the bounds 0, 255 inclusive
        Exception: lower_threshold is not within the bounds 0, 255 inclusive

    Returns:
        array: A 2D numpy array containing RGB data for each pixel in the resultant image
    """    
    ##Check for parameters of incorrect type
    checkExceptionString(map_filename) #Check that map_filename is of type str
    checkExceptionInteger(upper_threshold) #Check that upper_threshold is of type int
    checkExceptionInteger(lower_threshold) #Check that lower_threshold is of type int
    
    ##Check that the upper threshold does not exceed its maximum/minimum values
    if(upper_threshold > 255 or upper_threshold < 0):
        raise Exception("upper_threshold value: "+ upper_threshold + "found, a value between 0 and 255 (inclusive) was expected")
    
    ##Check that the lower threshold does not exceed its maximum/minimum values
    if(lower_threshold > 255 or lower_threshold < 0):
        raise Exception("upper_threshold value: "+ lower_threshold + "found, a value between 0 and 255 (inclusive) was expected")
    
    originalImage = Image.open('data/'+map_filename) #stores the image file as an object
    newImage = Image.new("RGB",(originalImage.width,originalImage.height),(0, 0, 0)) #Create a new RGB mode image with identical width and height to the original image
    
    for column in range(0,originalImage.height): #iterates through each column of pixels stored within the originalImage object
        for row in range(0,originalImage.width): #iterates through each row of pixels stored within the originalImage object
            
            ##unpacks the tuple into seperate variables dependant on if the format is RGB or RGBA
            if (len(originalImage.getpixel((row,column))) == 4):
                red,green,blue,a = originalImage.getpixel((row,column))
            else:
                red,green,blue = originalImage.getpixel((row,column))
                
            ##Checks that the pixel in row,colum is within the threshold to be considered red and if so inserts a white pixel into the new RGB image in the same location
            if (blue > upper_threshold and green > upper_threshold and red < lower_threshold):
                newImage.putpixel((row,column),(255,255,255))
                
    newImage.save('data/map-cyan-pixels.jpg') #Saves the resultant image as a file map-red-pixels.jpg and stores it inside the data file
    return np.array(newImage) #return the resultant image as a 2D numpy array
        
    ##TODO use numpy to change RGB values as it is much faster


def detect_connected_components(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def detect_connected_components_sorted(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here



find_cyan_pixels('map.png')