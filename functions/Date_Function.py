#Imports
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def DateFunction(Return_Table, PERMNO, start_year, end_year, start_month, end_month):
    
    Coefficient_Table = []
    
    #Iterate over all firms
    for i in PERMNO:

        #Initializing the Coefficient_Table Array
        #Create a Return table for each firm - consisting of only the dates that have been specified
        Single_Firm = Return_Table.loc[Return_Table['PERMNO'] == i]
        
        #Modifying the DataFrame to only include returns from the specified dates
        Single_Firm = Single_Firm.loc[(Single_Firm.Year >= start_year) & (Single_Firm.Year <= end_year)]
        #Only including the dates that are after the start month of the start year
        Single_Firm = Single_Firm.loc[(Single_Firm.Month >= start_month) | (Single_Firm.Year > start_year)]
        #Only including the dates that are before the end month of the end year
        Single_Firm = Single_Firm.loc[(Single_Firm.Month <= end_month) | (Single_Firm.Year < end_year)]

        #Setting the X Variables to be regressed on (Risk Factors), and setting the Y Variable that will be regressed (Bank Returns)
        y = Single_Firm['Return']
        x = Single_Firm[['BOND', 'CREDIT', 'SP500', 'CMDTY', 'DVIX', 'DHOUSE']]

        #Conducting the Linear Regression
        if len(x['BOND']) > 1:
            
            reg = LinearRegression()
            reg = LinearRegression().fit(x, y)

            Coefficients = (reg.coef_)
            Coefficient_Table.append(Coefficients)
    
    #Formatting the Coefficient Table as a DataFrame
    Coefficient_Table = pd.DataFrame(Coefficient_Table, columns = ["BOND", "CREDIT", "SP500", "CMDTY", "DVIX", "DHOUSE"])
    return Coefficient_Table