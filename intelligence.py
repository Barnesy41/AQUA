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
        lower_threshold (int): Defaults to 50. the highest (exclusive) green/blue RGB value for the pixel to be considered red

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

    newImageArr = np.array(newImage)
    originalImageArr = np.array(originalImage)

    # iterates through each column of pixels stored within the originalImage object
    for column in range(0, width):
        # iterates through each row of pixels stored within the originalImage object
        for row in range(0, height):

            # unpacks the tuple into separate variables dependant on if the format is RGB or RGBA
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

    return newImageArr  # return the resultant image as a 2D numpy array

    # TODO check this works properly as it has been changed since last test
    # TODO make binary image


def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """finds all cyan pixels in a given image

    Args:
        map_filename (str): The name of the map file that should be read
        upper_threshold (int): Defaults to 100. The lowest (exclusive) blue RGB value for the pixel to be considered cyan
        lower_threshold (int): Defaults to 50. the highest (exclusive) green/red RGB value for the pixel to be considered cyan

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

            # Unpack the rgb values into separate variables
            red, green, blue, alpha = originalImageArr[row, column]

            # Checks that the pixel in row,colum is within the threshold to be considered red and if so inserts a white pixel into the new RGB image in the same location
            if (blue > upper_threshold and green > upper_threshold and red < lower_threshold):
                # Set the pixel of the same location in the new image to white
                newImageArr[row, column] = (255, 255, 255)

    skimage.io.imsave('data/map-cyan-pixels.jpg', newImageArr.astype(np.uint8))

    return newImageArr  # return the resultant image as a 2D numpy array

    # TODO check this works properly as it has been changed since last test


def detect_connected_components(map_filename):
    """
    reads an image file returned by the functions: find_red_pixels() or find_cyan_pixels(), 
    finds the total number of connected components and the number of pixels contained within each connected component,
    then returns an nd array containing this data

    Args:
        map_filename (str): The file name of the b/w image file to read pixels from. This file should be stored in /data

    Returns:
        nd array: a numpy nd array containing the component number and number of pixels contained within that component
    """

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

    QueueRow = np.array([])  # initialise the Queue
    QueueColumn = np.array([])  # initialise the Queue

    connectedRegionNumPixels = []  # Stores the number of pixels in each connected region
    numberOfConnectedComponents = 0  # Stores the total number of connected components

    # create the cc-output-2a.txt file if it does not exist, or open the file if it does not already exist
    outputFile = open("cc-output-2a.txt", 'w')
    outputFile.truncate(0)  # Clear the python file if it already exists
    startOfQueueIndex = 0
    queueNextPointer = 0  # TODO the queue could get too large and cause a crash?

    for row in range(0, height):  # iterates through each row of pixels stored within imageArray
        # iterates through each column of pixels stored within imageArray
        for column in range(0, width):

            # Checks if the pixel is white and has not been visited
            if ((imageArray[row][column])[0] >= 128) and ((imageArray[row][column])[1] >= 128) and ((imageArray[row][column])[2] >= 128) and ((visitedArray[row][column]) == 0):
                numPixels = 0  # set the number of pixels in the current component to zero
                numPixels += 1  # increment the number of pixels in the component

                # Increment the total number of connected components (this is also the current component number)
                numberOfConnectedComponents += 1
                # mark the pixel as visited with the number set being the component number
                visitedArray[row][column] = numberOfConnectedComponents

                # add the node to the nodes to visit
                QueueRow = np.append(QueueRow, row)
                QueueColumn = np.append(QueueColumn, column)

                while len(QueueRow) != 0:  # loop while the queue contains pixels to visit

                    # Remove the next item from the queue and store in the variable item
                    item = (QueueRow[startOfQueueIndex],
                            QueueColumn[startOfQueueIndex])
                    QueueRow = np.delete(QueueRow, startOfQueueIndex)
                    QueueColumn = np.delete(QueueColumn, startOfQueueIndex)

                    # initialise a list which can be used to calculate the position of the 8 pixels surrounding the pixel popped from the queue
                    list = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                            (0, 1), (1, -1), (1, 0), (1, 1)]

                    for i in range(0, 8):

                        # Store the row and column of the current pixel in two separate variables
                        pixelToCheckRow = int(item[0])
                        pixelToCheckColumn = int(item[1])

                        # Checks if the pixel to check is a valid pixel (the row/column is not out of the bounds of the image)
                        if pixelToCheckRow+(list[i])[0] < height and pixelToCheckRow+(list[i])[0] >= 0 and pixelToCheckColumn + (list[i])[1] < width and pixelToCheckColumn + (list[i])[1] >= 0:
                            rowToCheck = pixelToCheckRow + (list[i])[0]
                            columnToCheck = pixelToCheckColumn + (list[i])[1]

                            # Checks if the pixel is white and if so adds the pixel to the queue of pixels to visit the 8-connected pixels
                            if ((imageArray[rowToCheck][columnToCheck])[0] >= 128) and ((imageArray[rowToCheck][columnToCheck])[1] >= 128) and ((imageArray[rowToCheck][columnToCheck])[2] >= 128) and (visitedArray[rowToCheck][columnToCheck] == 0):
                                QueueRow = np.append(QueueRow, rowToCheck)
                                QueueColumn = np.append(
                                    QueueColumn, columnToCheck)

                                numPixels += 1  # Increment the number of pixels in the current component
                                # mark the pixel as visited with the number set being the component number
                                visitedArray[rowToCheck][columnToCheck] = numberOfConnectedComponents

                # calculate the size of the new connected region and append to an array
                connectedRegionNumPixels.append(numPixels)

                # Output the connected component number and the number of pixels contained within the component
                #print("Connected Component " + str(numberOfConnectedComponents) +
                #      ", number of pixels = " + str(numPixels))

                # Write the connected component number and the number of pixels within the component into a file
                outputFile.write("Connected Component " + str(
                    numberOfConnectedComponents) + ", number of pixels = " + str(numPixels) + "\n")

    # write the total number of pixels to the end of the output file
    outputFile.write("Total number of connected components = " +
                     str(numberOfConnectedComponents))

    # Must be assigned here as MARK is a constant
    MARK = np.array(visitedArray)
    return MARK

    # TODO single rather than double for loop? low priority


def detect_connected_components_sorted(MARK):
    """
    Performs sorting on the connected component region size based on
    the number of pixels and outputs all connected components in descending order. For each connected
    component region, the number of pixels inside it is output, and the number of pixels is written
    into a text file cc-output-2b.txt. In cc-output-2b.txt, the last line should give the total number of
    connected components. Outputs the two largest connected components inside the image cc-top-2.jpg
    
    Outputs
    ----------
        1. The two largest connected components inside the image cc-top-2.jpg
        2. All connected components and the respective number of pixels inside the component to the terminal in descending order
    
    Parameters
    ----------
    MARK (numpy NDarray): a 2D array containing each row of the image. All path pixels are labelled with their respective component number. All other pixels are labelled with 0
    """
    # Your code goes here
    fileToReadFrom = open("cc-output-2a.txt", 'r')

    # Store the connected components in a sorted list
    unsortedComponents = []
    sortedComponents = []
    largestComponentNumber = 0
    for line in fileToReadFrom:
        line = line.rstrip()

        try:  # Ignores blank lines at the bottom of documents
            # Gets the component number from each line in the txt file and store as integer value
            componentNumber = int(line[20:line.index(',')])
            # Gets the number of pixels in each component from each line in the txt file and stores as integer value
            numPixels = int(line[line.index('=')+2:])
            unsortedComponents.append((numPixels, componentNumber))
            
            #get the largest component number
            if largestComponentNumber < componentNumber:
                largestComponentNumber = componentNumber
        except:
            False

    # Sorting Algorithm
    for i in unsortedComponents:
        if len(sortedComponents) == 0:  # Append the first element to the sorted list
            sortedComponents.append(i)
        else:  # Search through all elements in the list until the current number of pixels is greater than the one found then insert into that position
            isComponentInserted = False
            count = 0
            while isComponentInserted == False:
                if ((count == len(sortedComponents))):
                    sortedComponents.append(i)
                    isComponentInserted = True
                elif ((i[0] > sortedComponents[count][0])):
                    sortedComponents.insert(
                        sortedComponents.index(sortedComponents[count]), i)
                    isComponentInserted = True
                count += 1

    # Write results to the output file
    fileToWriteTo = open("cc-output-2b.txt", 'w')
    for item in sortedComponents:
        fileToWriteTo.write("Connected Component " + str(
            item[1]) + ", number of pixels = " + str(item[0]) + "\n")

        print("Connected Component " + str(
            item[1]) + ", number of pixels = " + str(item[0]))  # Output the results to the terminal
    
    #Write the total number of connected components to the output file
    fileToWriteTo.write("Total number of connected components = " + str(largestComponentNumber))
    
    #Output the total number of connected components to the terminal
    print("Total number of connected components = " + str(largestComponentNumber))

    # Create an image containing the 2 largest connected components
    # Get the height and width the image should be
    imageHeight = len(MARK)
    imageWidth = len(MARK[0])

    # Store the values of the top 2 component numbers in 2 separate variables
    top1ComponentNum = sortedComponents[0][1]
    top2ComponentNum = sortedComponents[1][1]

    image = []
    for row in range(0, imageHeight):
        imageRow = []
        for column in range(0, imageWidth):  # Search through each row of the image appending white rgb values to pixels which match the connected component number of the component with the largest 2 number of pixels in the component
            if (MARK[row][column] == top1ComponentNum) or (MARK[row][column] == top2ComponentNum):
                imageRow.append((255, 255, 255))
            else:
                imageRow.append((0, 0, 0))
        image.append(imageRow)  # Append the filled in row to the image

    image = np.array(image)  # Convert the list into an NDarray
    # Save the image as .jpg
    skimage.io.imsave('data/cc-top-2.jpg', image.astype(np.uint8))
