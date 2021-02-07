import numpy as np
import pandas as pd
import datetime

#Adding Year. Month, and Day Columns to the Dataframe
def add_bank_dates(dataset):
    #Initializing the arrays that will store the Year, Month, and Day of all the rows in the BankData DataFrame
    Year = []
    Month = []
    Day = []

    for i in dataset["Date"]:    
        #Getting the Year, Month, and Day for each row in BankData DataFrame
        Year.append((datetime.datetime.strptime(str(i), "%Y%m%d")).year)
        Month.append((datetime.datetime.strptime(str(i), "%Y%m%d")).month)
        Day.append((datetime.datetime.strptime(str(i), "%Y%m%d")).day)
        
    #Adding the Year, Month, and Day arrays as columns to the BankData DataFrame
    dataset["Year"] = Year
    dataset["Month"] = Month
    dataset["Day"] = Day
    return dataset


def add_RF_dates(dataset):
    #Initializing the arrays that will store the Year, Month, and Day of all the rows in the BankData DataFrame
    Year = []
    Month = []
    Day = []

    for i in dataset["Date"]:    
        #Getting the Year, Month, and Day for each row in BankData DataFrame
        Year.append((datetime.datetime.strptime(str(i), "%Y-%m-%d")).year)
        Month.append((datetime.datetime.strptime(str(i), "%Y-%m-%d")).month)
        Day.append((datetime.datetime.strptime(str(i), "%Y-%m-%d")).day)
        
    #Adding the Year, Month, and Day arrays as columns to the BankData DataFrame
    dataset["Year"] = Year
    dataset["Month"] = Month
    dataset["Day"] = Day
    return dataset


def format_bank_data(dataset):
    #Adding Year, Month, and Day columns
    dataset = add_bank_dates(dataset)

    #Dropping Rows with Null Return Values
    dataset = dataset.dropna(axis=0, subset=['RET'])
    #Dropping Rows with values B and C
    dataset.drop(dataset[dataset.RET == 'B'].index, inplace=True)
    dataset.drop(dataset[dataset.RET == 'C'].index, inplace=True)
    #Converting the Return Column to type Float
    dataset["RET"].astype(str).astype(float)

    return dataset


def format_RF_data(dataset):
    #Converting the CREDIT and DHOUSE columns to percent changes (returns)
    dataset["CREDIT"] = dataset["CREDIT"].pct_change()
    dataset["DHOUSE"] = dataset["DHOUSE"].pct_change()

    #Adding Year, Month, and Day columns
    dataset = add_RF_dates(dataset)

    return dataset


def return_table(Bank_Data, RF_Data):
    #Initializing the Return_Table that will consist of all the Bank Returns, and the corresponding Risk Factor Returns
    Return_Table = []
    Return_Table = pd.DataFrame(Return_Table)

    #Adding Columns for the Year, Month, and Day (allows us to easily retrieve the corresponding Risk Factor Returns (by date))
    Return_Table["Year"] = Bank_Data["Year"]
    Return_Table["Month"] = Bank_Data["Month"]
    Return_Table["Day"] = Bank_Data["Day"]

    #Adding a PERMNO column(to be able to identify the firms), and a column consisting of all the Bank Returns
    Return_Table["PERMNO"] = Bank_Data["PERMNO"]
    Return_Table["Return"] = Bank_Data["RET"]

    #----------------------------------------------------------
    #Initializing the Risk Factor columns for the Return Table
    number = np.size(Return_Table.Return)
    zeros = np.zeros(number)
    Return_Table["credit"] = zeros
    Return_Table["sp500"] = zeros
    Return_Table["bond"] = zeros
    Return_Table["dvix"] = zeros
    Return_Table["cmdty"] = zeros
    Return_Table["dhouse"] = zeros

    #Adding all the corresponding Risk Factor Return values for each Bank Return entry (by date)
    #Looping through the Risk Factor DataFrame to apply the returns to each appropriate Bank Return entry
    for index, i in RF_Data.iterrows():
        
        #Determining the year and month of row
        year = RF_Data.loc[index, "Year"]
        month = RF_Data.loc[index, "Month"]
        credit = RF_Data.loc[index, "CREDIT"]
        sp500 = RF_Data.loc[index, "SP500"]
        bond = RF_Data.loc[index, "BOND"]
        cmdty = RF_Data.loc[index, "CMDTY"]
        dvix = RF_Data.loc[index, "DVIX"]
        dhouse = RF_Data.loc[index, "DHOUSE"]
        
        z = Return_Table[(Return_Table.Year == year) & (Return_Table.Month == month)].index
        Return_Table.loc[z, "credit"] = credit
        Return_Table.loc[z, "sp500"] = sp500
        Return_Table.loc[z, "bond"] = bond
        Return_Table.loc[z, "cmdty"] = cmdty
        Return_Table.loc[z, "dvix"] = dvix
        Return_Table.loc[z, "dhouse"] = dhouse

    return Return_Table