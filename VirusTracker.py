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

## Add date to a dictionary with the data
def addTo():
    date = datetime.datetime.today()


dataSet = scrapeNumbers('https://www.worldometers.info/coronavirus/country/us/', 'maincounter-number')
US_population = scrapeNumbers('https://www.worldometers.info/world-population/us-population/', 'col-md-8 country-pop-description')

##  data[0] = US Population
##  data[1] = Confirmed Corona Cases
##  data[2] = Deaths
##  data[3] = Recovered

dataSet.insert(0, US_population[0])

