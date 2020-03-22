from bs4 import BeautifulSoup
import requests
from csv import writer
import datetime 

### Function that gets the number of cases from the URL
def scrapeNumbers(URL, inputClass):

    ### Variables for web scraping
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    ##Variable to hold the numbers in String form
    numbersStr = []
    ##Variabke to hold the numbers in int form
    numbers = []

    ## Finds all of the divs that have the class label of maincounter-number in the html page
    for div in soup.find_all('div', class_=inputClass):
        ## Stores the div in array of strings
        strArray = list(div.text) 
        ## Variable to reconstruct the number later
        reconstructedNumber = ''
        
        counter = 0 
        ## loops through the characters in the string array from the html page
        for char in strArray:

            if inputClass == 'col-md-8 country-pop-description':
                if counter == 8:
                    break
            ##trys to cast each char in the array to an int
            try:
                ## If the char can cast then the char is added to the reconstructedNumber variable to concatenate all of the numbers together
                int(char)
                reconstructedNumber = reconstructedNumber + char
            ## If not carry on
            except:
                continue

            counter = counter + 1

        ## Each reconstructed number is appended onto the numberStr array to hold each number in String form
        numbersStr.append(reconstructedNumber)

    ## Each numberString is iterrated through
    for numsStr in numbersStr:
        ##Each number is casted into an int type
        numbers.append(int(numsStr))
        
    ## returns the array of numbers that were scraped
    return numbers

## Function that collects the data from the txt file
def getSavedData():
    ##Dictionary variable that holds the date as the key and count as the value
    savedData = {}

    ##Opens the text file
    with open('savedData.txt', 'r') as dataFile:
        ##Reads each line of data
        for line in dataFile: 
            ##Tokenizes the data points 
            dataPoint = line.split(':')
            ##Variable that holds the date
            date = dataPoint[0]
            ##Tokenizes the count
            numberStr = dataPoint[1].split('\n')
            ##Variable that holds the data counts
            dataString = numberStr[0].split(' ')
            ##Array that holds the count in int form
            array = []
            ## goes through each data in the data array String
            for data in dataString:
                ##Casts each data point
                 array.append(int(data))
            
            ##sets the date to that set of data
            savedData[date] = array

    ## returns the dictionary of data points
    return savedData
        
## Add date to a dictionary with the data
def addTo(data):

    ## Data inputted
    worldPopulation = data[0]
    confirmedCases = data[1]
    deaths = data[2]
    recovered = data[3]

    ##String can holds all of the data collected
    dataString = '{} {} {} {}'.format(worldPopulation, confirmedCases, deaths, recovered)

    ## Gets todays date
    date = datetime.datetime.today()
    ## Variable to check if the date for today was already added to the file
    dateSaved = False
    ##Variable to check if the user wants to override data for today
    userInput = ''
    
    ##gets the saved data in the file
    savedData = getSavedData()
    ## Checks to see if todays date in already saved in the file
    if date.strftime('%d-%m-%Y') in savedData:
        ##If the data is saved then it checks to see if the user wants to override the data
        dateSaved = True
        rInput = input('Date is already saved, override data? (y/n): ')
        userInput = rInput

    ## If the date was not already added or the user wants to override the data
    if dateSaved == False:
        ## Opens the data file
        with open('savedData.txt', 'a') as dataFile:
            ##Appends to the data file with the data and count for that date
            dataFile.write(date.strftime('%d-%m-%Y') + ':' + dataString + '\n')
        
    ## If the user wants to override the data then the text file gets overridden
    if userInput == 'y':
        ##The dictionary with todays date gets overridden with the new data
        savedData[date.strftime('%d-%m-%Y')] = data
        ##Open the data file
        with open('savedData.txt', 'w') as DataFile:
            ##for each data point in saved data
            for data in savedData:
                ##A new line in the data file is written too
                DataFile.write(data + ':' + dataString + '\n')





dataSet = scrapeNumbers('https://www.worldometers.info/coronavirus/country/us/', 'maincounter-number')
US_population = scrapeNumbers('https://www.worldometers.info/world-population/us-population/', 'col-md-8 country-pop-description')

##  data[0] = US Population
##  data[1] = Confirmed Corona Cases
##  data[2] = Deaths
##  data[3] = Recovered

dataSet.insert(0, US_population[0])

addTo(dataSet)
print(getSavedData())

