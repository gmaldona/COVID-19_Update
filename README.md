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

This function requests the `URL` and finds the HTML div with the label of `inputClass` and returns data collected from the website
```Python3
def ScrapeNumbers(URL, inputClass):
```
