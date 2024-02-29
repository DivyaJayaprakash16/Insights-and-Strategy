# -*- coding: utf-8 -*-
"""
Project:  Airline Data Challenge
Module: Data cleaning
File: Tickets.csv
Author: Capital One - Data Analysis Team
Date: 02/13/2024
Version: 1.0
"""

import pandas as pd
import numpy as np
import Airport_Codes as ac

#Import data
tickets = pd.read_csv("C://Users//...//Capital One Analytics//data3//Tickets.csv")
print(tickets.head(10))
print(len(tickets))
round_trip_tickets = tickets[tickets["ROUNDTRIP"] == 1]
print('len(round_trip_tickets):' , len(round_trip_tickets))


round_trip_tickets.insert(4,"LEN_ORIGIN",round_trip_tickets["ORIGIN"].str.len(),True)
print(round_trip_tickets["LEN_ORIGIN"])
print(round_trip_tickets[round_trip_tickets["ORIGIN"] == np.nan])
print(round_trip_tickets[round_trip_tickets["LEN_ORIGIN"] !=3])

round_trip_tickets.insert(13,"LEN_DESTINATION",round_trip_tickets["DESTINATION"].str.len(),True)
print(round_trip_tickets["LEN_DESTINATION"])
print(round_trip_tickets[round_trip_tickets["DESTINATION"] == np.nan])
print(round_trip_tickets[round_trip_tickets["LEN_DESTINATION"] !=3])

# Remove Duplicates
round_trip_tickets.insert(1,"DUPLICATE_ID",round_trip_tickets.duplicated(subset=['ITIN_ID']),True)
print(round_trip_tickets[round_trip_tickets["DUPLICATE_ID"] == True])
round_trip_tickets = round_trip_tickets[round_trip_tickets.DUPLICATE_ID == False]

#Origin IATA code validation
airport_codes = ac.airport_codes
IATA = pd.DataFrame()
IATA.loc[:, 'ORIGIN'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_ORI_IATA_VALID_CODE'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_ORI_IATA_US'] = airport_codes.loc[:, 'ISO_COUNTRY']
IATA.loc[:, 'CHK_ORI_IATA_TYPE'] = airport_codes.loc[:, 'TYPE']
IATA.loc[:, 'CHK_ORI_NAME'] = airport_codes.loc[:, 'NAME']
options = ['medium_airport', 'large_airport']

#JOIN: Tickets & airport codes 
join_round_trip_tickets_airport_codes = pd.merge(round_trip_tickets,IATA, on ='ORIGIN',  how ='left')
join_round_trip_tickets_airport_codes['CHK_ORI_IATA_VALID_CODE'] = join_round_trip_tickets_airport_codes['CHK_ORI_IATA_VALID_CODE'].replace(np.nan, "???").astype(str)
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_ORI_IATA_VALID_CODE == "???"])
join_round_trip_tickets_airport_codes = join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_ORI_IATA_VALID_CODE != "???"]

join_round_trip_tickets_airport_codes['CHK_ORI_IATA_US'] = join_round_trip_tickets_airport_codes['CHK_ORI_IATA_US'].replace(np.nan, "???").astype(str)
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_ORI_IATA_US == "???"])
join_round_trip_tickets_airport_codes = join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_ORI_IATA_US == "US"]

join_round_trip_tickets_airport_codes['CHK_ORI_IATA_TYPE'] = join_round_trip_tickets_airport_codes['CHK_ORI_IATA_TYPE'].replace(np.nan, "???").astype(str)
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_ORI_IATA_TYPE == "???"])
join_round_trip_tickets_airport_codes = join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_ORI_IATA_TYPE.isin(options)]

#Destination IATA code validation
IATA = pd.DataFrame()
IATA.loc[:, 'DESTINATION'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_DEST_IATA_VALID_CODE'] = airport_codes.loc[:, 'IATA_CODE']
IATA.loc[:, 'CHK_DEST_IATA_US'] = airport_codes.loc[:, 'ISO_COUNTRY']
IATA.loc[:, 'CHK_DEST_IATA_TYPE'] = airport_codes.loc[:, 'TYPE']
IATA.loc[:, 'CHK_DEST_NAME'] = airport_codes.loc[:, 'NAME']
join_round_trip_tickets_airport_codes = pd.merge(join_round_trip_tickets_airport_codes,IATA, on ='DESTINATION',  how ='left')
join_round_trip_tickets_airport_codes['CHK_DEST_IATA_VALID_CODE'] = join_round_trip_tickets_airport_codes['CHK_DEST_IATA_VALID_CODE'].replace(np.nan, "???").astype(str)
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_DEST_IATA_VALID_CODE == "???"])
join_round_trip_tickets_airport_codes = join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_DEST_IATA_VALID_CODE != "???"]

join_round_trip_tickets_airport_codes['CHK_DEST_IATA_US'] = join_round_trip_tickets_airport_codes['CHK_DEST_IATA_US'].replace(np.nan, "???").astype(str)
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_DEST_IATA_US == "???"])
join_round_trip_tickets_airport_codes = join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_DEST_IATA_US == "US"]

join_round_trip_tickets_airport_codes['CHK_DEST_IATA_TYPE'] = join_round_trip_tickets_airport_codes['CHK_DEST_IATA_TYPE'].replace(np.nan, "???").astype(str)
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_DEST_IATA_TYPE == "???"])
join_round_trip_tickets_airport_codes = join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes.CHK_DEST_IATA_TYPE.isin(options)]
print(join_round_trip_tickets_airport_codes)

#Incorrect values found	Replaced ‘0’ with MEAN_PASSENGERS for the route
#Blank values found	Replaced with MEAN_PASSENGERS for the route
print(join_round_trip_tickets_airport_codes.dtypes)
join_round_trip_tickets_airport_codes.insert(4,"ROUTE",((join_round_trip_tickets_airport_codes['ORIGIN']+'-'+join_round_trip_tickets_airport_codes['DESTINATION']).where(join_round_trip_tickets_airport_codes['ORIGIN'] < join_round_trip_tickets_airport_codes['DESTINATION'], other=(join_round_trip_tickets_airport_codes['DESTINATION']+'-'+join_round_trip_tickets_airport_codes['ORIGIN']))),True)                                             
mean_passengers = join_round_trip_tickets_airport_codes.groupby('ROUTE')['PASSENGERS'].mean()
print(mean_passengers)
join_round_trip_tickets_airport_codes = pd.merge(join_round_trip_tickets_airport_codes,mean_passengers, on ='ROUTE',  how ='left')
mapping = {"PASSENGERS_x" : "PASSENGERS", "PASSENGERS_y" : "MEAN_PASSENGERS"}
join_round_trip_tickets_airport_codes.rename(columns = mapping, inplace = True)
print(join_round_trip_tickets_airport_codes["MEAN_PASSENGERS"])
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes["PASSENGERS"] == np.nan])
join_round_trip_tickets_airport_codes['PASSENGERS'] = join_round_trip_tickets_airport_codes['PASSENGERS'].replace(np.nan, 0).astype(int)
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes["PASSENGERS"] == 0])
join_round_trip_tickets_airport_codes['MEAN_PASSENGERS'] = join_round_trip_tickets_airport_codes['MEAN_PASSENGERS'].round()
print(join_round_trip_tickets_airport_codes.PASSENGERS[join_round_trip_tickets_airport_codes["PASSENGERS"] == 0])
join_round_trip_tickets_airport_codes.PASSENGERS[join_round_trip_tickets_airport_codes.PASSENGERS == 0] = join_round_trip_tickets_airport_codes.MEAN_PASSENGERS
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes["PASSENGERS"] == 0])

#Blank values found	Replaced with MEAN_ ITIN_FARE for the route. Removed rows where MEAN_ITIN_FARE for the route is 0
#Incorrect values found	Replaced  a)	'$ 100.00' with 100 b)	'820$$$' with 820 c)	'200 $' with 200

join_round_trip_tickets_airport_codes['ITIN_FARE'] = join_round_trip_tickets_airport_codes['ITIN_FARE'].replace('$ 100.00', (100)).astype(str)
join_round_trip_tickets_airport_codes['ITIN_FARE'] = join_round_trip_tickets_airport_codes['ITIN_FARE'].replace('820$$$', (820)).astype(str)
join_round_trip_tickets_airport_codes['ITIN_FARE'] = join_round_trip_tickets_airport_codes['ITIN_FARE'].replace(np.nan, (0)).astype(str)
join_round_trip_tickets_airport_codes['ITIN_FARE'] = join_round_trip_tickets_airport_codes['ITIN_FARE'].replace('200 $', (200)).astype(str)
join_round_trip_tickets_airport_codes['ITIN_FARE'] = join_round_trip_tickets_airport_codes['ITIN_FARE'].astype(float)
mean_ITIN_fare = join_round_trip_tickets_airport_codes.groupby('ROUTE')['ITIN_FARE'].mean()
join_round_trip_tickets_airport_codes = pd.merge(join_round_trip_tickets_airport_codes,mean_ITIN_fare, on ='ROUTE',  how ='left')
mapping = {"ITIN_FARE_x" : "ITIN_FARE", "ITIN_FARE_y" : "MEAN_ITIN_FARE"}
join_round_trip_tickets_airport_codes.rename(columns = mapping, inplace = True)
join_round_trip_tickets_airport_codes['MEAN_ITIN_FARE'] = join_round_trip_tickets_airport_codes['MEAN_ITIN_FARE'].round()
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes["ITIN_FARE"] == 0])
join_round_trip_tickets_airport_codes.ITIN_FARE[join_round_trip_tickets_airport_codes.ITIN_FARE == 0] = join_round_trip_tickets_airport_codes.MEAN_ITIN_FARE
print(join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes["ITIN_FARE"] == 0])
print(join_round_trip_tickets_airport_codes)
join_round_trip_tickets_airport_codes = join_round_trip_tickets_airport_codes[join_round_trip_tickets_airport_codes["ITIN_FARE"] != 0]
print(join_round_trip_tickets_airport_codes)

tickets_inscope = join_round_trip_tickets_airport_codes




