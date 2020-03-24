# COVID-19 Automated Update
Web scraper and data analysis for COVID-19 

## Modules Used:

Library:      | Purpose:
------------- | -------------
Beautiful Soup  | Web Scraping
Requests  | URL Requests
MatPlotLib | Visualizing Data
NumPy | Data Structure
CSV | Data Reading

## This Script Consists of 6 Main Functions:
```Python3
def scrapeNumbers(URL, inputClass):
```
This function requests the `URL` and finds the HTML div with the label of `inputClass` and returns data collected from the website
```Python3
def getSavedData():
 ```
 This function return two arrays: `dateArray` and `data`
 The arrays are pulled from a .txt file that contains dates and their respective set of data
