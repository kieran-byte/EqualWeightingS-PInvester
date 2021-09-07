# EqualWeightingS&PInvester
Takes in a portfolio size and creates an excel file showing showing many shares should be invested in each company to form an equal weight portfolio


# Secrets
The API token in this secrets file is a demo token. 


# How It Works
The application requires one input, the value of your portfolio. It is required to input it as a number. There is no support for alternative inputs.  
The program then reads in stocks from a csv file that doesn't change and determines their price and market cap using an API in batch calls. Then it determines how many shares of
each company is required to make an equal weight portfolio and stores the company symbols, stock price, market cap and number of shares to purchase in an .xlsx file format to the directory the program was run from. 


# Potential Changes
The csv file can be easy changed to become only stocks of interest to you instead of a generic S&P 500 list. For instance, if you only have an interest in tech stocks you could change the symbols to all tech companies and run the applciation to generate an equal weight portfolio of tech companies. 

