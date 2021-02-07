#Imports
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statistical_functions import*
from coefficient_table import*

def stat_relationship(Data, Return_Table, PERMNO, function):
    number = np.size(Data.index)
    zeros = np.zeros(number)
    Data["Stat_Values"] = zeros
    for index, i in Data.iterrows():
        
        end_month = Data.loc[index, "Month"]
        start_month = (end_month + 9)%12
        end_year = Data.loc[index, "Year"]
        if start_month < end_month:
            start_year = end_year
        else:
            start_year = end_year-1
        
        Coefficient_Table = coefficient_table_func(Return_Table, PERMNO, start_year, end_year, start_month, end_month)
        
        #Calculting the Values of Each Statistical Function
        if Coefficient_Table.size > 1:
            Stat_Value = function(Coefficient_Table)
            Data.loc[index, "Stat_Values"] = Stat_Value
        else:
            Data.loc[index, "Stat_Values"] = 1
    
        
    return Data

