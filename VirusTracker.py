from bs4 import BeautifulSoup
import requests
from csv import writer
import datetime 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy
import os
import time
import csv
import sys
import os 

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
    data = []
    #dates = numpy.array()
    ##Opens the text file
    with open('savedDataUS.txt', 'r') as dataFile:
        ##Reads each line of data
        for line in dataFile: 
            ##Tokenizes the data points 
            dataPoint = line.split(':')
            ##Variable that holds the date
            dateToday = dataPoint[0]
            ##Tokenizes the count
            numberStr = dataPoint[1].split('\n')
            ##Variable that holds the data counts
            dataString = numberStr[0].split(' ')
            ##Array that holds the count in int form
            dataArray = []
            ## goes through each data in the data array String
            for d in dataString:
                ##Casts each data point
                dataArray.append(int(d))

            ##sets the date to that set of data
            savedData[dateToday] = dataArray
            data.append(dataArray)
    
    ## Array to hold the dates
    dateArray = []
    ## Loops through all the dates
    for date in savedData:
        ## Adds each date
        dateArray.append(date)

    ## returns the dates and data
    return dateArray, data
        
## Add date to a dictionary with the data
def addTo(date, data):

    ## Data inputted
    confirmedCases = data[0]
    deaths = data[1]
    recovered = data[2]

    ##String can holds all of the data collected
    dataString = '{} {} {}'.format(confirmedCases, deaths, recovered)
    ## Variable to check if the date for today was already added to the file
    dateSaved = False
    ##Variable to check if the user wants to override data for today
    userInput = ''
    
    file_path = 'savedDataUS.txt'

    if os.path.getsize(file_path) == 0:
        with open('savedDataUS.txt', 'w') as dataFile:
            ##Appends to the data file with the data and count for that date
            dataFile.write(date + ':' + dataString + '\n')
    else:
        ##gets the saved data in the file
        (datesSaved, dataSaved) = getSavedData()
        ## Checks to see if todays date in already saved in the file
        if date in datesSaved:
            ##If the data is saved then it checks to see if the user wants to override the data
            dateSaved = True
            # rInput = input('Date is already saved, override data? (y/n): ')
            # userInput = rInput
            print('Data for today was already recorded...')

        ## If the date was not already added or the user wants to override the data
        if dateSaved == False:
            ## Opens the data file
            with open('savedDataUS.txt', 'a') as dataFile:
                ##Appends to the data file with the data and count for that date
                dataFile.write(date + ':' + dataString + '\n')
            
        ## If the user wants to override the data then the text file gets overridden
        if userInput == 'y':
            ##The dictionary with todays date gets overridden with the new data
            ##savedData[date.strftime('%d-%m-%Y')] = data
            index = datesSaved.index(date)
            dataSaved[index] = data
            ##Open the data file
            with open('savedDataUS.txt', 'w') as DataFile:
                ##for each data point in saved data
                for i in datesSaved:
                    DataFile.write(i + ':' + dataString + '\n')

##Function plots a graph
def plot():

    ## Collects the dates and data from the text file
    (dates, data) = getSavedData()

    ## Creates separate arrays for each data set
    cases = []
    deaths = []
    recovered = []

    ## Creates the dates into a numpy array
    numpyDates = numpy.array(dates)

    ##Iterates through each of the data sets and appends them
    for i in range(0, len(data)):
        cases.append(data[i][0])
        deaths.append(data[i][1])
        recovered.append(data[i][2])

    ## Plots and labels
    plt.plot(numpyDates, numpy.array(cases), label = 'Total Confirmed')
    plt.plot(numpyDates, numpy.array(deaths), label = 'Deaths')
    plt.plot(numpyDates, numpy.array(recovered), label = 'Recovered')

    ## Plot style
    plt.ylabel('Cases')
    plt.title('COVID-19 Cases in the United States')
    plt.legend()

    ## X-axis
    plt.xticks("")

## Function that gets the daily Update of the graph
def dailyUpdate():
    dataSet = scrapeNumbers('https://www.worldometers.info/coronavirus/country/us/', 'maincounter-number')
    US_population = scrapeNumbers('https://www.worldometers.info/world-population/us-population/', 'col-md-8 country-pop-description')
    #dataSet.insert(0, US_population[0])

    ## Gets todays date
    date = datetime.datetime.today().strftime('%d-%m-%Y')
    addTo(date, dataSet)    

## Function that gets the Past Data from CSV Files
def getPastData():
    ## Variables to hold the data
    dates = []
    cases = []
    deaths = []
    recovered = []

    ## Opens the csv Files
    with open('total_cases.csv') as csvfile:
        ##tokenizes each value after a comma 
        readCSV = csv.reader(csvfile, delimiter = ',')
        ## Checks each row in the file
        for row in readCSV:
            ## Trys to cast string into an int
            try:
                cases.append(int(row[len(row) - 8]))
                recovered.append(0)
            ## If fails then continue to the next index
            except:
                continue
            ##Reconstructs the date into the desired format
            date = row[0].split('-')
            year = date[0]
            month = date[1]
            day = date[2]
            reconstructedDate = '{}-{}-{}'.format(day, month, year)
            ## Appends the date to the date array
            dates.append(reconstructedDate)

    ## Opens the csv file
    with open('total_deaths.csv') as csvfile:
        ##Tokenizes each element after comma
        readCSV = csv.reader(csvfile, delimiter = ',')
        ## Checks each row in the file
        for row in readCSV:
            ## Trys to cast string into an int
            try: 
                deaths.append(int(row[len(row) - 8])) 
            ## If fail, then continue to next index 
            except:
                continue  
    
    ## Loops through each index
    for i in range(0, len(dates)):
        ## Adds each data set into the file
       addTo(dates[i], [cases[i], deaths[i], recovered[i]])
        

#getPastData()
#dailyUpdate()
plot()
plt.show()

