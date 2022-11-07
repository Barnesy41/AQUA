from PIL import Image #imports Image from the Pillow module - used to load images into an array of RGB values
import numpy as np

def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """finds all red pixels in a given image

    Args:
        map_filename (str): The name of the map file that should be read
        upper_threshold (int): Defaults to 100. The lowest (exclusive) red RGB value for the pixel to be considered red
        lower_threshold (int): Defaults to 50. the heighest (exclusive) green/blue RGB value for the pixel to be considered red

    Outputs:
        file: A file map-red-pixels.jpg in the data file

    Returns:
        array: A 2D numpy array containing RGB data for each pixel in the resultant image
    """    
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
        
    ##TODO What if there is somehow an incorrect RGBA value? e.g. value > 255 or < 0 input as a parameter
    ##TODO use numpy to change RGB values as it is much faster
    ##TODO check for incorrect types when input into function

def find_cyan_pixels(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here


def detect_connected_components(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def detect_connected_components_sorted(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

