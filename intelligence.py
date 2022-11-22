# from PIL import Image #imports Image from the Pillow module - used to load images into an array of RGB values
import skimage
import skimage.io
import numpy as np
from utils import checkExceptionArray, checkExceptionBool, checkExceptionInteger, checkExceptionString, countvalue





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
    print("finding all red pixels...")  # test
    # Check for parameters of incorrect type
    # Check that map_filename is of type str
    checkExceptionString(map_filename)
    # Check that upper_threshold is of type int
    checkExceptionInteger(upper_threshold)
    # Check that lower_threshold is of type int
    checkExceptionInteger(lower_threshold)

    # Check that the upper threshold does not exceed its maximum/minimum values
    if (upper_threshold > 255 or upper_threshold < 0):
        raise Exception("upper_threshold value: " + upper_threshold +
                        "found, a value between 0 and 255 (inclusive) was expected")

    # Check that the lower threshold does not exceed its maximum/minimum values
    if (lower_threshold > 255 or lower_threshold < 0):
        raise Exception("upper_threshold value: " + lower_threshold +
                        "found, a value between 0 and 255 (inclusive) was expected")

    # stores the image file as an object
    originalImage = skimage.io.imread('data/'+map_filename)

    # TODO what if an empty array is input as a parameter
    # Calculate the height of the image
    height = 0
    for i in originalImage:
        height += 1

    # Calculate the width of the image
    width = 0
    for i in originalImage[0]:
        width += 1

    # Create an empty image
    newImage = []
    newImageRow = []
    while len(newImageRow) < width:
        newImageRow.append((0, 0, 0))

    while len(newImage) < height:
        newImage.append(newImageRow)

    originalImageArr = np.array(originalImage)
    newImageArr = np.array(newImage)

    # iterates through each column of pixels stored within the originalImage object
    for column in range(0, width):
        # iterates through each row of pixels stored within the originalImage object
        for row in range(0, height):

            # unpacks the tuple into seperate variables dependant on if the format is RGB or RGBA
            if (len(originalImageArr[row, column]) == 4):
                red, green, blue, a = originalImageArr[row, column]

                # Checks that the pixel in row,colum is within the threshold to be considered red and if so inserts a white pixel into the new RGB image in the same location
                if (red > upper_threshold and green < lower_threshold and blue < lower_threshold):
                    newImageArr[row, column] = (255, 255, 255)
            else:
                red, green, blue = originalImageArr[row, column]

                # Checks that the pixel in row,colum is within the threshold to be considered red and if so inserts a white pixel into the new RGB image in the same location
                if (red > upper_threshold and green < lower_threshold and blue < lower_threshold):
                    newImageArr[row, column] = (255, 255, 255)

    skimage.io.imsave('data/map-red-pixels.jpg', newImageArr.astype(np.uint8))

    print("finished finding all red pixels! A new file should have appeared in data/map-red-pixels.jpg")  # test
    return newImageArr  # return the resultant image as a 2D numpy array

    # TODO check this works properly as it has been chaged since last test
    # TODO make binary image


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
    # Check for parameters of incorrect type
    # Check that map_filename is of type str
    checkExceptionString(map_filename)
    # Check that upper_threshold is of type int
    checkExceptionInteger(upper_threshold)
    # Check that lower_threshold is of type int
    checkExceptionInteger(lower_threshold)

    # Check that the upper threshold does not exceed its maximum/minimum values
    if (upper_threshold > 255 or upper_threshold < 0):
        raise Exception("upper_threshold value: " + upper_threshold +
                        "found, a value between 0 and 255 (inclusive) was expected")

    # Check that the lower threshold does not exceed its maximum/minimum values
    if (lower_threshold > 255 or lower_threshold < 0):
        raise Exception("upper_threshold value: " + lower_threshold +
                        "found, a value between 0 and 255 (inclusive) was expected")

    # stores the image file as an object
    originalImage = skimage.io.imread('data/'+map_filename)

    # TODO what if an empty array is input as a parameter
    # Calculate the height of the image
    height = 0
    for i in originalImage:
        height += 1

    # Calculate the width of the image
    width = 0
    for i in originalImage[0]:
        width += 1

    # Create an empty image
    newImage = []
    newImageRow = []
    while len(newImageRow) < width:
        newImageRow.append((0, 0, 0))

    while len(newImage) < height:
        newImage.append(newImageRow)

    originalImageArr = np.array(originalImage)
    newImageArr = np.array(newImage)

    # iterates through each column of pixels stored within the originalImage object
    for column in range(0, width):
        # iterates through each row of pixels stored within the originalImage object
        for row in range(0, height):

            # Unpack the rgb values into seperate variables
            red, green, blue, alpha = originalImageArr[row, column]

            # Checks that the pixel in row,colum is within the threshold to be considered red and if so inserts a white pixel into the new RGB image in the same location
            if (blue > upper_threshold and green > upper_threshold and red < lower_threshold):
                # Set the pixel of the same location in the new image to white
                newImageArr[row, column] = (255, 255, 255)

    skimage.io.imsave('data/map-cyan-pixels.jpg', newImageArr.astype(np.uint8))

    return newImageArr  # return the resultant image as a 2D numpy array

    # TODO check this works properly as it has been chaged since last test



# newImage.save('data/map-cyan-pixels.jpg')
# if (blue > upper_threshold and green > upper_threshold and red < lower_threshold):
def detect_connected_components(map_filename):
    print("detecting connected components...")  # test

    image = skimage.io.imread('data/'+map_filename)
    # convert the image to an array of individual pixels
    imageArray = np.array(image)

    # TODO what if an empty array is input as a parameter
    # Calculate the height of the image
    height = 0
    for i in image:
        height += 1

    # Calculate the width of the image
    width = 0
    for i in image[0]:
        width += 1

    # Stores whether each pixel has been visited or not
    visitedArray = [[0]*width]*height
    # Converts the python list to a numpy array
    visitedArray = np.array(visitedArray)

    Queue = []  # initalise the Queue TODO change to numpy

    connectedRegionNumPixels = []  # Stores the number of pixels in each connected region
    numberOfConnectedComponents = 0  # Stores the total number of connected components

    # create the cc-output-2a.txt file if it does not exist, or open the file if it does not already exist
    outputFile = open("cc-output-2a.txt", 'w')
    outputFile.truncate(0)  # Clear the python file if it already exists

    for row in range(0, height):  # iterates through each row of pixels stored within imageArray
        # iterates through each column of pixels stored within imageArray
        for column in range(0, width):

            # Checks if the pixel is white and has not been visited
            if ((imageArray[row][column])[0] >= 128) and ((imageArray[row][column])[1] >= 128) and ((imageArray[row][column])[2] >= 128) and ((visitedArray[row][column]) == 0):
                numPixels = 0
                visitedArray[row][column] = 1  # mark the pixel as visited
                numPixels += 1  # increment the number of pixels in the component
                
                # add the node to the nodes to visit
                Queue.append((row, column))
                
                while len(Queue) != 0:  # loop while the queue contains data
                    item = Queue.pop(0)  # Remove the next item from the queue
                    
                    #initalise a list which can be used to calculate the position of the 8 pixels surrounding the pixel popped from the queue
                    list = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                            (0, 1), (1, -1), (1, 0), (1, 1)]

                    for i in range(0, 8):
                        pixelToCheckRow = item[0]
                        pixelToCheckColumn = item[1]
                        if pixelToCheckRow+(list[i])[0] < height and pixelToCheckRow+(list[i])[0] >= 0 and pixelToCheckColumn + (list[i])[1] < width and pixelToCheckColumn + (list[i])[1] >= 0:
                            rowToCheck = pixelToCheckRow + (list[i])[0]
                            columnToCheck = pixelToCheckColumn + (list[i])[1]
                            
                            if ((imageArray[rowToCheck][columnToCheck])[0] >= 128) and ((imageArray[rowToCheck][columnToCheck])[1] >= 128) and ((imageArray[rowToCheck][columnToCheck])[2] >= 128) and (visitedArray[rowToCheck][columnToCheck] == 0):
                                Queue.append((rowToCheck, columnToCheck))
                                numPixels += 1
                                visitedArray[rowToCheck][columnToCheck] = 1  # mark the pixel as visited
                numberOfConnectedComponents += 1  # Increment the number of connected components
                

                # calculate the size of the new connected region and append to an array
                connectedRegionNumPixels.append(numPixels)
                # Output the connected component number and the number of pixels contained within
                print("Connected Component " + str(numberOfConnectedComponents) +
                      ", number of pixels = " + str(numPixels))
                outputFile.write("Connected Component " + str(
                    numberOfConnectedComponents) + ", number of pixels = " + str(numPixels) + "\n")

    # Calculate the total number of connected particles
    totalNumConnectedParticles = countvalue(visitedArray.flatten(), 1)
    # write the total number of pixels to the end of the output file
    outputFile.write("Total number of connected components = " +
                     str(totalNumConnectedParticles))

    MARK = visitedArray
    return MARK

    # TODO single rather than double for loop? low priority
    # TODO only detect correct nodes as visited not all
    # TODO use numpy ndarray for the Queue
    # TODO make this actually work right


def detect_connected_components_sorted(MARK):
    """Your documentation goes here"""
    # Your code goes here


# TESTING START
detect_connected_components("map-red-pixels.jpg")
find_cyan_pixels("map.png")

'''#test
    f = open('testOutputArray.txt','w')
    f.truncate(0)
    for i in newImageArr:
        for x in i:
            f.write(str(x))
        f.write("\n")
    f.close()
    #test end'''
# test end
