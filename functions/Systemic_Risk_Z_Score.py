#Imports
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def Get_Market_Returns(
    market_name: str,
    RF_Data: np.ndarray,
    Dates
):
    #Initializing the array which will containg the returns of the Market
    Returns = []
    
    #Looping through all of the dates, and getting the appropriate Return
    for i in range(8):
        year = Dates[1][i]
        month = Dates[3][i]

        Return = RF_Data.loc[(RF_Data['Year'] == year) & (RF_Data['Month'] == month)]
        Returns.append(Return[market_name])

    return Returns



#Defining the Function which Produces the Z-Score type Model
#This function produces a Beta Regression model for the Predicted Loss of the Financial System via the Values of the Statistical Tests
def Z_Score_Function(
    Statistical_Values: np.ndarray,
    Market_Returns: np.ndarray
):
    #Initializing the X and Y Variables
    x = Statistical_Values
    y = Market_Returns

    #Running the Linear Regression
    Coefficients = []
    reg = LinearRegression().fit(x,y)
    Coefficients.append(reg.coef_)
    Coefficients.append(reg.intercept_)

    return Coefficients

