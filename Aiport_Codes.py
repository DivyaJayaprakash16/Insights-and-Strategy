# -*- coding: utf-8 -*-
"""
Project: Airline Data Challenge
Module: Data cleaning
File: Airport_Codes.csv
Author: Capital One - Data Analysis Team
Date: 02/13/2024
Version: 1.0
"""

import pandas as pd
import numpy as np

#Data ingestion
airport_codes = pd.read_csv("C://Users//...//Capital One Analytics//data4//Airport_Codes.csv")
print(airport_codes.head(10))
print(len(airport_codes))

#Identify the available distinct airport types
airport_type = airport_codes[['IATA_CODE','TYPE']]
airport_type.insert(0,"DUPLICATE_ID",airport_type.duplicated(subset=['TYPE']),True)
airport_type = airport_type[airport_type.DUPLICATE_ID == False]
print(airport_type)

#Filter for US large/medium airports
options = ['medium_airport', 'large_airport']
airport_codes = airport_codes[airport_codes['TYPE'].isin(options)]
options = ['US']
airport_codes = airport_codes[airport_codes['ISO_COUNTRY'].isin(options)]
print(len(airport_codes))
print(airport_codes)

#The non-IATA codes are sufficient for the analysis of the Flights and Tickets datasets. Hence, the rows with blank IATA codes were removed
airport_codes['IATA_CODE'] = airport_codes['IATA_CODE'].replace(np.nan, "???").astype(str)
print(airport_codes[airport_codes.IATA_CODE == "???"])
airport_codes['IATA_CODE'] = airport_codes['IATA_CODE'].replace(np.nan, "???").astype(str)
airport_codes = airport_codes[airport_codes['IATA_CODE'] != "???"]
print(airport_codes)

#Remove duplicates
airport_codes.insert(1,"DUPLICATE_ID",airport_codes.duplicated(subset=['IATA_CODE']),True)
airport_codes = airport_codes[airport_codes.DUPLICATE_ID == False]