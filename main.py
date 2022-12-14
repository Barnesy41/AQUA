from reporting import readCSV, daily_average, daily_median, hourly_average, monthly_average, peak_hour_date, count_missing_data, fill_missing_data
from intelligence import find_red_pixels, find_cyan_pixels, detect_connected_components, detect_connected_components_sorted
from monitoring import showSpeciesInfo, showAllSpeciesInfo, outputAllMonitoringStations, outputAirQualityIndexDataForSpecificSite
from monitoring import drawPollutantPieChart, outputPollutantGraph, inputSiteCode

def main_menu():
    """shows the main menu of the program"""
    print("R - Access the PR module\n"
          "I - Access the MI module\n"
          "M - Access the RM module\n"
          "A - Print the About text.\n"
          "Q - Quit the application\n")


def outputMonitoringMenuOptions():
    '''Displays the menu options for the monitoring module inside the terminal window'''
    print("\nSSI - Show information about a specific pollutant species\n"
          "SASI - Show the information about all pollutant species\n"
          "OAMS - Outputs all of the monitoring stations and their site codes within London\n"
          "OAQI - Outputs the air quality index for all pollutants at a specific monitoring station.\n"
          "DPPC - Draw a pie chart showcasing the average percentage of each pollutant at a given monitoring station.\n"
          "OPG - Outputs a text-based graph for the mean average value of each pollutant at a given monitoring station.\n")


def inputPollutant():
    """gets input from the user until a valid pollutant is entered or the user requests to quit the menu
       returns the pollutant as a string or 'Q' if the user requests to quit the menu
    """
    whitelistOfPollutants = ['NO2', 'CO', 'O3', 'PM10', 'SO2', 'PM25']
    
    # Asks the user to select the desired pollutant to get information about
    pollutant = input(
        "Enter a species code to show ('NO2', 'CO', 'O3', 'PM10', 'SO2', 'PM25') or 'Q' to quit: ").upper()

    # re-input if an unknown pollutant is entered
    while pollutant not in whitelistOfPollutants:
        # Break the loop if the pollutant == 'Q' (the user would like to quit)
        if pollutant == "Q":
            break

        # Request a new input
        print("Invalid input.")
        pollutant = input(
            "Enter a species code to show ('NO2', 'CO', '03', 'PM10', 'SO2', 'PM25') or 'Q' to quit: ").upper()
    return pollutant

def inputMonitoringStation():
    """gets input from the user until a valid monitoring station is entered or the user requests to quit the menu
       returns the user's input if the monitoring station entered is valid, returns 'Q' if the user requests to quit"""
    while True:
        userInput = input(
            "Enter a site code to show the air quality information for. If you would like to exit, input 'Q'").upper()

        #If the user requests to quit return "Q"
        if userInput == "Q":
            return "Q"
                
        # Check that the site code input by the user is valid
        listOfMonitoringStations = outputAllMonitoringStations(False) # Returns a list of all monitoring stations and their site codes
        for item in listOfMonitoringStations:
            if item[1] == userInput:
                return userInput
            
        print("Invalid input.")
        
    
                    
def monitoring_menu():
    """Allows the user to select the required functions from the monitoring module then return to the main menu when desired by inputting 'Q'"""

    exitModule = False
    while exitModule == False:
        outputMonitoringMenuOptions() #Print the options for this module to the terminal

        # Get the user to input the desired sub-division of the monitoring module
        userInput = input(
            "Enter a sub-division of the monitoring module (e.g. 'SSI') or 'Q' to quit:").lower()
        print("")

        # Access the show species information function of the module
        if userInput == "ssi":
            pollutant = inputPollutant()

            # Quit this menu if desired
            if pollutant == "q":
                break

            showSpeciesInfo(pollutant)
            
            

        # Show the information for all pollutant species
        elif userInput == "sasi":
            showAllSpeciesInfo()



        # Display the names and site codes of all London-based monitoring stations inside the terminal
        elif userInput == 'oams':
            outputAllMonitoringStations()



        # Output the air quality information alongside health advice
        elif userInput == "oaqi":
            while True:

                monitoringStation = inputMonitoringStation()
                if monitoringStation != 'Q': #Run only if the user would not like to quit the menu
                    outputAirQualityIndexDataForSpecificSite(monitoringStation)
                else: 
                    break # Exit the loop if the user would like to quit

        elif userInput == "dppc":
            
            global pieChartDrawn
            if pieChartDrawn == False:
                approved = input("This function can only be run once per run. Would you like to resume? (yes/no)")
                if approved.lower() == "yes":
                    pieChartDrawn = drawPollutantPieChart()
            else:
                print("Pie chart has already been drawn.\nThis function can only be called once.\nTo call this function again, kill the terminal and re-run.")
                import time
                time.sleep(1)
                        
        #Output Pollutant Graph
        elif userInput == "opg":
            #Get the number of days of data the user would like to request
            numberOfDays = 0
            while numberOfDays <= 0:
                numberOfDays = int(input("Enter the number of days you would like to calculate the average pollutant level with: "))
                
                if numberOfDays <= 0:
                    print("Invalid input.")
            
            #Get the site code using the pre-existing function                
            siteCode = inputSiteCode()
            
            #Run the function only if the user hasn't requested to quit the module
            if siteCode != 'Q':
                outputPollutantGraph(siteCode,numberOfDays)
            
        # Quit this menu
        elif userInput == "q":  # Quit the menu
            break

        else:
            print("Invalid input")


def intelligence_menu():
    """Allows the user to choose the necessary options for the intelligence module of the program then return back to the main menu when required"""

    while True:
        print("\n\n\nFRP - Find all of the red pixels in a given image\n"
              "FCP - Find all of the cyan pixels in a given image\n"
              "DCC - Detect the number of connected components ina given binary image\n"
              "DCCS - Detect Connected Components Sorted, sort the connected component region sizes based on the number of pixels and output the top two largest connected components\n"
              "Q - Quit to main menu")
        userInput = input("\nInput an option from above: ")

        if userInput.lower() == 'frp':
            find_red_pixels(
                input("enter the map file name (stored in the /data folder)"))
        if userInput.lower() == 'fcp':
            find_cyan_pixels(input("enter the map file name (stored in the /data folder)"))
        if userInput.lower() == 'dcc':
            detect_connected_components(
                input("enter the map file name (stored in the /data folder)"))
        if userInput.lower() == 'dccs':
            detect_connected_components_sorted(detect_connected_components(
                input("enter the map file name (stored in the /data folder)")))
        if userInput.lower() == 'q':
            break


def about():
    """Outputs the course code and candidate number as two separate strings"""
    print("ECM1400", "243352")


def quit():
    """kills the python interpreter"""
    exit()


def reporting_menu():
    """
        Reads data from all known CSV files and places the data into a dictionary.
        Outputs a menu containing all options for the reporting segment of this program
        Allows the user to recieve all types of data from the reporting section of the project
    """
    # Read all CSV files
    pollutionDictionary = dict()
    pollutionDictionary['harlington'] = readCSV(
        "data/Pollution-London Harlington.csv")
    pollutionDictionary['marylebone road'] = readCSV(
        "data/Pollution-London Marylebone Road.csv")
    pollutionDictionary['n kensington'] = readCSV(
        "data/Pollution-London N Kensington.csv")

    while True:
        print("\n\n\nDA - Calculate the daily average\n"
              "DM - Calculate the daily median\n"
              "HA - calculate the hourly average\n"
              "MA - Calculate the monthly average\n"
              "PHD - find the peak pollution hour and pollution level for a specific date\n"
              "CMD - count the number of times missing data appears for a specific pollutant and monitoring station\n"
              "FMD - Replace missing data with another value\n"
              "Q - Quit to main menu")
        userInput = input("\nenter an option from above: ")

        if userInput.lower() == 'da':
            daily_average(pollutionDictionary, input("enter a pollution station (harlington,marylebone road,n kensington): "), input(
                "enter a pollution type (no,pm10,pm25): "))
        elif userInput.lower() == 'dm':
            daily_median(pollutionDictionary, input("enter a pollution station (harlington,marylebone road,n kensington): "), input(
                "enter a pollution type (no,pm10,pm25): "))
        elif userInput.lower() == 'ha':
            hourly_average(pollutionDictionary, input("enter a pollution station (harlington,marylebone road,n kensington): "), input(
                "enter a pollution type (no,pm10,pm25): "))
        elif userInput.lower() == 'ma':
            monthly_average(pollutionDictionary, input("enter a pollution station (harlington,marylebone road,n kensington): "), input(
                "enter a pollution type (no,pm10,pm25): "))
        elif userInput.lower() == 'phd':
            peak_hour_date(pollutionDictionary, input("enter a date you would like to see data for in the format (YYYY-MM-DD): "), input(
                "enter a pollution station (harlington,marylebone road,n kensington): "), input("enter a pollution type (no,pm10,pm25): "))
        elif userInput.lower() == 'cmd':
            count_missing_data(pollutionDictionary, input(
                "enter a pollution station (harlington,marylebone road,n kensington): "), input("enter a pollution type (no,pm10,pm25): "))
        elif userInput.lower() == 'fmd':
            fill_missing_data(pollutionDictionary, input("enter a new value to fill missing data with (type: int/float): "), input(
                "enter a pollution station (harlington,marylebone road,n kensington): ", input("enter a pollution type (no,pm10,pm25): ")))
        elif userInput.lower() == 'q':
            break


if __name__ == '__main__':
    global pieChartDrawn
    pieChartDrawn = False
            
    while True:
        main_menu()

        # Ask the user to input a menu option
        userInput = input(
            "Enter one of the above options to navigate to another menu: ")

        if userInput.lower() == 'r':
            reporting_menu()
        elif userInput.lower() == 'i':
            intelligence_menu()
        elif userInput.lower() == 'm':
            monitoring_menu()
        elif userInput.lower() == 'a':
            about()
        elif userInput.lower() == 'q':
            quit()
