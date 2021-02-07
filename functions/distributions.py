#Imports
import numpy as np
import pandas as pd
from functions.statistical_functions import*
from functions.coefficient_table import*

#Dates and Array Function which creates the Dates Array for iterating through a number of dates and computing the statistical vlaues for the distributions
def Generate_Dates(
    num_iterations: int,
    num_counter: int,
    start_year: int,
    end_year: int,
    start_month: int,
    end_month: int

):
    Dates = []

    for i in range(num_iterations):
       
       #The Incremented Month numbers
        s_value = start_month+(i*num_counter)
        e_value = end_month+(i*num_counter)
        
        #Adjusting such that the month values are between 1 and 12
        if s_value%12 == 0:
            s_month = 12
        else:
            s_month = s_value%12
        
        if e_value%12 == 0:
            e_month = 12
        else:
            e_month = e_value%12

        #Finding the minimum number of times 12 divides wholly into the number of months
        #This becomes the number of years to increment by
        s_year = (s_value - s_value%12)/12
        s_year = start_year+ s_year

        e_year = (e_value - e_value%12)/12
        e_year = end_year+ e_year 

        #Appending the date to the 2D Array of all dates
        date = [s_year, e_year, s_month, e_month]
        Dates.append(date)
    
    Dates = pd.DataFrame(Dates)
        
    return(Dates)

#Distribution Construction Function
def Distribution_Construction(
    Dates: np.ndarray,
    Return_Table: np.ndarray,
    PERMNO: np.ndarray,
    Function
):

    Function_Distribution = []
    num_iterations = Dates[0:][1]
    
    for i in range(len(num_iterations)):
        start_year = Dates[0][i]
        end_year = Dates[1][i]
        start_month = Dates[2][i]
        end_month = Dates[3][i]

        #Calculating the Coefficient Table for each Date in the Dates Array
        Coefficient_Table = coefficient_table_func(Return_Table, PERMNO, start_year, end_year, start_month, end_month)

        #Calculting the Values of Each Statistical Function
        if Coefficient_Table.size > 1:
            Function_Value = Function(Coefficient_Table)
            Function_Distribution.append(Function_Value)
        
    return Function_Distribution

        