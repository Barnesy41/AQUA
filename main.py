from reporting import readCSV, daily_average, daily_median, hourly_average, monthly_average, peak_hour_date, count_missing_data, fill_missing_data
from intelligence import find_red_pixels, find_cyan_pixels, detect_connected_components, detect_connected_components_sorted
from monitoring import showSpeciesInfo

def main_menu():
    """shows the main menu of the program"""
    print("R - Access the PR module\n"
          "I - Access the MI module\n"
          "M - Access the RM module\n"
          "A - Print the About text.\n"
          "Q - Quit the application")


def monitoring_menu():
    """Your documentation goes here"""
    
    exitModule = False #A flag used to exit this module when set to True
    while exitModule == False:
        
        #Get the user to input the desired sub-division of the monitoring module
        userInput = input("Enter a sub-division of the monitoring module (SSI, Q):").lower()
             
        #Access the show species information function of the module
        if userInput == "ssi":
            whitelistOfPollutants = ['NO2', 'CO', 'O3', 'PM10', 'SO2', 'PM25'] #Stores a list of the whitelisted pollutants ('Q' is used to quit the module therefore cannot be whitelisted)
            
            #Asks the user to select the desired pollutant to get information about
            pollutant = input("Enter a species code to show ('NO2', 'CO', 'O3', 'PM10', 'SO2', 'PM25') or 'Q' to quit: ").upper()
            
            # re-input if an unknown pollutant is entered
            while pollutant not in whitelistOfPollutants:
                #Break the loop if the pollutant == 'Q'
                if pollutant == "Q":
                    break
                
                #Request a new input
                print("Invalid input.")
                pollutant = input("Enter a species code to show ('NO2', 'CO', '03', 'PM10', 'SO2', 'PM25') or 'Q' to quit: ").upper()
            
            #Quit this menu if desired
            if pollutant == "Q":
                break
            
            #Show the species information
            showSpeciesInfo(pollutant)
        
        #Quit this menu
        elif userInput == "q": #Quit the menu
            break
        
        else:
            print("Invalid input")
    
    #Output information about each pollutant when selected
    


def intelligence_menu():
    """Allows the user to choose the necessary options for the intelligence module of the program then return back to the main menu when required"""

    while True:
        print("\n\n\nFRP - Find all of the red pixels in a given image\n"
              "FCP - Find all of the cyan pixels in a given image\n"
              "DCC - Detect the number of connected components ina given binary image\n"
              "DCCS - Detect Connected Components Sorted, sort the connected component region sizes based on the number of pixels and output the top two largest connected components\n"
              "Q - Quit to main menu")
        userInput = input("\nEnter an option from above: ")

        if userInput.lower() == 'frp':
            find_red_pixels(
                input("enter the map file name (stored in data folder)"))
        if userInput.lower() == 'fcp':
            find_cyan_pixels(input("enter the map file name"))
        if userInput.lower() == 'dcc':
            detect_connected_components(
                input("enter the map file name (stored in the data folder)"))
        if userInput.lower() == 'dccs':
            detect_connected_components_sorted(detect_connected_components(
                input("enter the map file name (stored in the data folder)")))
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
